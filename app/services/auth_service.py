from datetime import datetime, UTC, timedelta
from typing import Any
import random
import jwt
from pydantic import BaseModel as PydanticBase, SecretStr

from app.databases.redis_manager import redis_manager
from app.exceptions import Unauthorized, Forbidden, Conflict, NotFound
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.otp_repository import OTPRepository
from app.schemas.auth.login_schema import LoginRequest
from app.schemas.auth.otp_schema import OTPRequest, OtpAction
from app.schemas.auth.reset_password_schema import ResetPasswordRequest
from app.schemas.auth.token_schema import TokenData
from app.schemas.users.user_schema import UserUpdate  # Import UserUpdate schema
from app.utils.password_utils import verify_password, hash_password
from app.utils.jwt_utils import jwt_handler
from app.services.email_service import email_service

# A private schema for creating refresh token records, as required by BaseRepository.create
class _RefreshTokenCreateSchema(PydanticBase):
    jti: str
    user_id: Any
    expires_at: datetime
    revoked: bool = False

# A private schema for creating OTP records
class _OTPCreateSchema(PydanticBase):
    email: str
    code: str
    action: str
    expires_at: datetime


class AuthService:

    @classmethod
    async def login(
        cls,
        user_repo: UserRepository,
        login_data: LoginRequest
    ) -> TokenData:
        """Business logic for user login."""
        user = await user_repo.get_by_username(login_data.username)
        if not user or not verify_password(login_data.password, user.password):
            raise Unauthorized("Invalid username or password")

        if hasattr(user, 'failed_login_attempts') and user.failed_login_attempts > 0:
            await user_repo.reset_failed_attempts(user.user_id)
        
        await user_repo.update_last_login(user.user_id)

        access_token, refresh_token, jti, expires_in_minutes = jwt_handler.create_tokens(user_id=user.user_id)

        key = f"user_session:{user.user_id}:{jti}"
        ttl_seconds = expires_in_minutes * 60
        await redis_manager.client.setex(key, ttl_seconds, "active")

        return TokenData(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in_minutes=expires_in_minutes,
        )

    @classmethod
    async def logout(cls, user_id: str, jti: str, exp: int):
        """Logs out a user by revoking their token and cleaning up the session record."""
        if not all([user_id, jti, exp]):
            return

        exp_datetime = datetime.fromtimestamp(exp, tz=UTC)
        await jwt_handler.revoke(jti=jti, exp=exp_datetime)

        session_key = f"user_session:{user_id}:{jti}"
        await redis_manager.client.delete(session_key)

    @classmethod
    async def refresh_tokens(
        cls,
        old_refresh_token: str,
        refresh_token_repo: RefreshTokenRepository,
        user_repo: UserRepository
    ) -> TokenData:
        """Handles the token refresh and rotation logic for enhanced security."""
        payload = await jwt_handler.verify(token=old_refresh_token, token_type="refresh")
        user_id = payload.get("sub")
        old_jti = payload.get("jti")

        if await refresh_token_repo.is_revoked(old_jti):
            await refresh_token_repo.revoke_all_for_user(user_id)
            raise Forbidden("Compromised refresh token detected. All sessions have been logged out.")

        await refresh_token_repo.revoke_by_jti(old_jti)

        user = await user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise Unauthorized("User account is inactive or not found.")

        access_token, new_refresh_token, new_access_jti, expires_in = jwt_handler.create_tokens(user_id=user.user_id)

        new_refresh_payload = jwt.decode(new_refresh_token, options={"verify_signature": False})
        token_create_data = _RefreshTokenCreateSchema(
            jti=new_refresh_payload.get('jti'),
            user_id=user_id,
            expires_at=datetime.fromtimestamp(new_refresh_payload.get('exp'), tz=UTC)
        )
        await refresh_token_repo.create(token_create_data)

        session_key = f"user_session:{user.user_id}:{new_access_jti}"
        ttl_seconds = expires_in * 60
        await redis_manager.client.setex(session_key, ttl_seconds, "active")

        return TokenData(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in_minutes=expires_in
        )

    @classmethod
    async def request_otp(
        cls,
        otp_data: OTPRequest,
        user_repo: UserRepository,
        otp_repo: OTPRepository
    ):
        """Handles the business logic for requesting an OTP."""
        # 1. Business logic validation based on action
        user = await user_repo.get_by_username(otp_data.email) # Assuming email is used as username
        if otp_data.action == OtpAction.REGISTER and user:
            raise Conflict("An account with this email already exists.")
        if otp_data.action == OtpAction.RESET_PASSWORD and not user:
            raise NotFound("No account found with this email address.")

        # 2. Invalidate any old, active OTPs for this email and action
        await otp_repo.invalidate_otps_for_email(otp_data.email, otp_data.action)

        # 3. Generate a new OTP
        otp_code = str(random.randint(100000, 999999))
        expires_at = datetime.now(UTC) + timedelta(minutes=5) # OTP is valid for 5 minutes

        # 4. Store the new OTP in the database
        otp_create_data = _OTPCreateSchema(
            email=otp_data.email,
            code=hash_password(otp_code), # Always store a hash of the OTP
            action=otp_data.action,
            expires_at=expires_at
        )
        await otp_repo.create(otp_create_data)

        # 5. Send the OTP to the user via the email service
        await email_service.send_otp(email=otp_data.email, otp_code=otp_code, action=otp_data.action)

        # The service layer does not return data for this action, only performs it.
        return

    @classmethod
    async def reset_password_with_otp(
        cls,
        data: ResetPasswordRequest,
        user_repo: UserRepository,
        otp_repo: OTPRepository,
        refresh_token_repo: RefreshTokenRepository
    ):
        """Verifies an OTP and resets the user's password."""
        # 1. Find a matching, active OTP.
        # We don't know the OTP hash, so we find the latest active one for the email/action.
        active_otp = await otp_repo.get_active_otp(email=data.email, action=OtpAction.RESET_PASSWORD)

        # 2. Verify the provided code against the hashed code in the DB
        if not active_otp or not verify_password(data.otp_code.get_secret_value(), active_otp.code):
            raise Unauthorized("Invalid or expired OTP code.")

        # 3. Mark the OTP as used immediately
        await otp_repo.mark_otp_used(active_otp.id)

        # 4. Find the user to update their password
        user = await user_repo.get_by_username(data.email)
        if not user:
            # This should not happen if request_otp logic is correct, but as a safeguard:
            raise NotFound("User account not found.")

        # 5. Hash the new password and update the user
        hashed_new_password = hash_password(data.new_password.get_secret_value())
        update_schema = UserUpdate(password=SecretStr(hashed_new_password))
        await user_repo.update(user.user_id, update_schema)

        # 6. Security Best Practice: Log the user out of all other devices
        await refresh_token_repo.revoke_all_for_user(user.user_id)

        return

