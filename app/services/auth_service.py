# app/services/auth_service.py
from datetime import datetime, UTC, timedelta
from typing import Any
import jwt
from pydantic import BaseModel as PydanticBase, SecretStr, EmailStr

from app.databases.redis_manager import redis_manager
from app.exceptions import Unauthorized, Forbidden, Conflict, NotFound
from app.models.user_session import UserSession
from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository
from app.schemas.auth.login_schema import LoginRequest
from app.schemas.auth.otp_schema import OTPRequest, OtpAction, OTPVerifyRequest
from app.schemas.auth.register_schema import RegisterRequest
from app.schemas.auth.reset_password_schema import ResetPasswordRequest
from app.schemas.auth.token_schema import TokenData
from app.schemas.users.user_schema import UserUpdate
from app.utils.password_utils import verify_password, hash_password
from app.utils.jwt_utils import jwt_handler
from app.services.email_service import email_service
from app.services.otp_service import otp_service


# A private schema for creating user records
class _UserCreateSchema(PydanticBase):
    username: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool = False  # Users are inactive until email is verified


class AuthService:

    @classmethod
    async def register_user(
            cls,
            reg_data: RegisterRequest,
            user_repo: UserRepository
    ):
        """Handles the first step of registration: creating an inactive user and sending a verification OTP."""
        existing_user = await user_repo.get_by_username(reg_data.email)
        if existing_user and existing_user.is_active:
            raise Conflict("An account with this email already exists.")

        if not existing_user:
            hashed_password = hash_password(reg_data.password.get_secret_value())
            user_create_data = _UserCreateSchema(
                username=reg_data.email,
                password=hashed_password,
                first_name=reg_data.first_name,
                last_name=reg_data.last_name,
                is_active=False
            )
            await user_repo.create(user_create_data)

        # Proceed to send OTP for the new or existing inactive user
        otp_request_data = OTPRequest(email=reg_data.email, action=OtpAction.REGISTER)
        await cls.request_otp(otp_request_data, user_repo)

    @classmethod
    async def login(
            cls,
            login_data: LoginRequest,
            user_repo: UserRepository,
            session_repo: UserSessionRepository,
            ip_address: str | None,
            user_agent: str | None
    ) -> TokenData:
        """Handles user login, creates tokens, and records the user session in the database."""
        user = await user_repo.get_by_username(login_data.username)
        if not user or not verify_password(login_data.password.get_secret_value(), user.password):
            raise Unauthorized("Invalid username or password")

        if not user.is_active:
            raise Forbidden("Account is not active. Please verify your email.")

        if hasattr(user, 'failed_login_attempts') and user.failed_login_attempts > 0:
            await user_repo.reset_failed_attempts(user.user_id)

        await user_repo.update_last_login(user.user_id)

        access_token, refresh_token, access_jti, refresh_jti, expires_in = jwt_handler.create_tokens(
            user_id=user.user_id, user_role=user.user_role.value)

        refresh_payload = jwt.decode(refresh_token, options={"verify_signature": False})
        refresh_expires_at = datetime.fromtimestamp(refresh_payload.get('exp'), tz=UTC)

        session = UserSession(
            user_id=user.user_id,
            jti=refresh_jti,
            expires_at=refresh_expires_at,
            ip_address=ip_address,
            user_agent=user_agent
        )
        await session_repo.create(session)

        return TokenData(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in_minutes=expires_in,
        )

    @classmethod
    async def logout(cls, session_repo: UserSessionRepository, access_jti: str, access_exp: int,
                     refresh_token: str | None):
        """
        Logs out a user by revoking the access token (in Redis) 
        and, if provided, the refresh token (in DB).
        """
        # 1. Vô hiệu hóa access token trong Redis (bắt buộc)
        exp_datetime = datetime.fromtimestamp(access_exp, tz=UTC)
        await jwt_handler.revoke(jti=access_jti, exp=exp_datetime)

        # 2. Vô hiệu hóa refresh token trong DB (nếu nó được cung cấp)
        if not refresh_token:
            return  # Không có cookie, không cần làm gì thêm

        try:
            # Xác minh token (không kiểm tra blacklist) để lấy jti
            payload = await jwt_handler.verify(token=refresh_token, token_type="refresh", check_revocation=False)
            refresh_jti = payload.get("jti")
            user_id = payload.get("sub")

            session = await session_repo.get_by_jti(refresh_jti)
            if session and session.user_id == user_id:
                session.revoked = True
                await session_repo.session.commit()
        except (jwt.PyJWTError, Unauthorized, NotFound):
            # Nếu token không hợp lệ, hết hạn, hoặc không tìm thấy,
            # chúng ta không cần làm gì cả. Mục tiêu là logout,
            # và token này đã không thể sử dụng được nữa.
            pass

    @classmethod
    async def refresh_tokens(
            cls,
            old_refresh_token: str,
            session_repo: UserSessionRepository,
            user_repo: UserRepository,
            ip_address: str | None,
            user_agent: str | None
    ) -> TokenData:
        """Handles token refresh and rotation for enhanced security."""
        try:
            payload = await jwt_handler.verify(token=old_refresh_token, token_type="refresh")
        except (jwt.PyJWTError, Unauthorized) as e:
            raise Unauthorized("Invalid or expired refresh token") from e

        user_id = payload.get("sub")
        old_jti = payload.get("jti")

        session = await session_repo.get_by_jti(old_jti)

        if not session or session.revoked:
            await session_repo.revoke_all_for_user(user_id)
            await cls.revoke_all_access_tokens_for_user(user_id)
            raise Forbidden("Compromised refresh token detected. All sessions have been logged out.")

        user = await user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise Unauthorized("User account is inactive or not found.")

        access_token, new_refresh_token, access_jti, new_refresh_jti, expires_in = jwt_handler.create_tokens(
            user_id=user.user_id, user_role=user.user_role.value)

        new_refresh_payload = jwt.decode(new_refresh_token, options={"verify_signature": False})
        new_expires_at = datetime.fromtimestamp(new_refresh_payload.get('exp'), tz=UTC)

        session.jti = new_refresh_jti
        session.expires_at = new_expires_at
        session.last_active = datetime.now(UTC)
        session.ip_address = ip_address
        session.user_agent = user_agent
        await session_repo.session.commit()

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
            user_repo: UserRepository
    ):
        """Handles the business logic for requesting an OTP using Redis."""
        if otp_data.action == OtpAction.RESET_PASSWORD:
            user = await user_repo.get_by_username(otp_data.email)
            if not user:
                raise NotFound("No account found with this email address.")

        otp_code = await otp_service.generate_and_store_otp(otp_data.email, otp_data.action.value)
        await email_service.send_otp(email=otp_data.email, otp_code=otp_code, action=otp_data.action)

    @classmethod
    async def reset_password_with_otp(
            cls,
            data: ResetPasswordRequest,
            user_repo: UserRepository,
            session_repo: UserSessionRepository
    ):
        """Verifies OTP from Redis, resets password, and revokes all sessions."""
        is_valid = await otp_service.verify_otp(
            email=data.email,
            action=OtpAction.RESET_PASSWORD.value,
            submitted_code=data.otp_code.get_secret_value()
        )

        if not is_valid:
            raise Unauthorized("Invalid or expired OTP code.")

        user = await user_repo.get_by_username(data.email)
        if not user:  # Should not happen if request_otp check passed, but good practice
            raise NotFound("User account not found.")

        hashed_new_password = hash_password(data.new_password.get_secret_value())
        update_schema = UserUpdate(password=SecretStr(hashed_new_password))
        await user_repo.update(user.user_id, update_schema)

        await session_repo.revoke_all_for_user(user.user_id)
        await cls.revoke_all_access_tokens_for_user(user.user_id)

    @classmethod
    async def verify_registration_otp(cls, data: OTPVerifyRequest, user_repo: UserRepository):
        """Verifies an OTP from Redis for registration and activates the user account."""
        is_valid = await otp_service.verify_otp(
            email=data.email,
            action=OtpAction.REGISTER.value,
            submitted_code=data.otp_code.get_secret_value()
        )

        if not is_valid:
            raise Unauthorized("Invalid or expired OTP code.")

        user = await user_repo.get_by_username(data.email, include_deleted=True)
        if not user:
            raise NotFound("User account not found.")

        if not user.is_active:
            await user_repo.activate_user(user.user_id)

    @classmethod
    async def revoke_all_access_tokens_for_user(cls, user_id: Any):
        """Instantly invalidates all access tokens for a user by setting a revocation timestamp in Redis."""
        key = f"user_revoke_all_timestamp:{user_id}"
        await redis_manager.client.set(key, int(datetime.now(UTC).timestamp()), ex=timedelta(days=31))