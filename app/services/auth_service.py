from datetime import datetime, UTC, timedelta
from typing import Any
import random
import jwt
from pydantic import BaseModel as PydanticBase, SecretStr, EmailStr

from app.databases.redis_manager import redis_manager
from app.exceptions import Unauthorized, Forbidden, Conflict, NotFound
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.otp_repository import OTPRepository
from app.schemas.auth.login_schema import LoginRequest
from app.schemas.auth.otp_schema import OTPRequest, OtpAction, OTPVerifyRequest
from app.schemas.auth.register_schema import RegisterRequest
from app.schemas.auth.reset_password_schema import ResetPasswordRequest
from app.schemas.auth.token_schema import TokenData
from app.schemas.users.user_schema import UserUpdate
from app.utils.password_utils import verify_password, hash_password
from app.utils.jwt_utils import jwt_handler
from app.services.email_service import email_service

# A private schema for creating user records
class _UserCreateSchema(PydanticBase):
    username: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool = False # Users are inactive until email is verified

# A private schema for creating refresh token records
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
    async def register_user(
        cls,
        reg_data: RegisterRequest,
        user_repo: UserRepository,
        otp_repo: OTPRepository
    ):
        """Handles the first step of registration: creating an inactive user and sending a verification OTP."""
        # 1. Check if user already exists
        existing_user = await user_repo.get_by_username(reg_data.email)
        if existing_user:
            raise Conflict("An account with this email already exists.")

        # 2. Create the user record as inactive
        hashed_password = hash_password(reg_data.password.get_secret_value())
        user_create_data = _UserCreateSchema(
            username=reg_data.email,
            password=hashed_password,
            first_name=reg_data.first_name,
            last_name=reg_data.last_name,
            is_active=False
        )
        await user_repo.create(user_create_data)

        # 3. Trigger the OTP verification email by reusing the request_otp service
        otp_request_data = OTPRequest(email=reg_data.email, action=OtpAction.REGISTER)
        # We must call request_otp on the class itself (cls) to ensure it's part of the same transaction
        await cls.request_otp(otp_request_data, user_repo, otp_repo)

        return

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
        # This check is now primarily for the RESET_PASSWORD flow.
        # For REGISTER, the check is done in the register_user service.
        if otp_data.action == OtpAction.RESET_PASSWORD:
            user = await user_repo.get_by_username(otp_data.email)
            if not user:
                raise NotFound("No account found with this email address.")

        await otp_repo.invalidate_otps_for_email(otp_data.email, otp_data.action)

        otp_code = str(random.randint(100000, 999999))
        expires_at = datetime.now(UTC) + timedelta(minutes=5)

        otp_create_data = _OTPCreateSchema(
            email=otp_data.email,
            code=hash_password(otp_code),
            action=otp_data.action,
            expires_at=expires_at
        )
        await otp_repo.create(otp_create_data)

        await email_service.send_otp(email=otp_data.email, otp_code=otp_code, action=otp_data.action)

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
        active_otp = await otp_repo.get_active_otp(email=data.email, action=OtpAction.RESET_PASSWORD)

        if not active_otp or not verify_password(data.otp_code.get_secret_value(), active_otp.code):
            raise Unauthorized("Invalid or expired OTP code.")

        await otp_repo.mark_otp_used(active_otp.id)

        user = await user_repo.get_by_username(data.email)
        if not user:
            raise NotFound("User account not found.")

        hashed_new_password = hash_password(data.new_password.get_secret_value())
        update_schema = UserUpdate(password=SecretStr(hashed_new_password))
        await user_repo.update(user.user_id, update_schema)

        await refresh_token_repo.revoke_all_for_user(user.user_id)

        return

    @classmethod
    async def verify_registration_otp(cls, data: OTPVerifyRequest, user_repo: UserRepository, otp_repo: OTPRepository):
        """Verifies an OTP for the registration action and activates the user account."""
        active_otp = await otp_repo.get_active_otp(email=data.email, action=OtpAction.REGISTER)

        if not active_otp or not verify_password(data.otp_code.get_secret_value(), active_otp.code):
            raise Unauthorized("Invalid or expired OTP code.")

        await otp_repo.mark_otp_used(active_otp.id)

        user = await user_repo.get_by_username(data.email, include_deleted=True)
        if not user:
            raise NotFound("User account not found.")

        if not user.is_active:
            await user_repo.activate_user(user.user_id)

        return
