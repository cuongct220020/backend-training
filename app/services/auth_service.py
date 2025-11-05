from datetime import datetime, UTC
from typing import Any
import jwt
from pydantic import BaseModel as PydanticBase

from app.databases.redis_manager import redis_manager
from app.exceptions import Unauthorized, Forbidden
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.schemas.auth.login_schema import LoginRequest
from app.schemas.auth.token_schema import TokenData
from app.utils.password_utils import verify_password
from app.utils.jwt_utils import jwt_handler


# A private schema for creating refresh token records, as required by BaseRepository.create
class _RefreshTokenCreateSchema(PydanticBase):
    jti: str
    user_id: Any
    expires_at: datetime
    revoked: bool = False


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
        # 1. Verify the refresh token is valid and of type 'refresh'
        payload = await jwt_handler.verify(token=old_refresh_token, token_type="refresh")
        user_id = payload.get("sub")
        old_jti = payload.get("jti")

        # 2. Check if the token has already been used/revoked in the DB
        if await refresh_token_repo.is_revoked(old_jti):
            await refresh_token_repo.revoke_all_for_user(user_id)
            raise Forbidden("Compromised refresh token detected. All sessions have been logged out.")

        # 3. Revoke the old refresh token in the database immediately
        await refresh_token_repo.revoke_by_jti(old_jti)

        # 4. Check if the user account is still active
        user = await user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise Unauthorized("User account is inactive or not found.")

        # 5. Issue a new pair of tokens
        access_token, new_refresh_token, new_access_jti, expires_in = jwt_handler.create_tokens(user_id=user.user_id)

        # 6. Store the new refresh token's metadata in the database
        new_refresh_payload = jwt.decode(new_refresh_token, options={"verify_signature": False})
        token_create_data = _RefreshTokenCreateSchema(
            jti=new_refresh_payload.get('jti'),
            user_id=user_id,
            expires_at=datetime.fromtimestamp(new_refresh_payload.get('exp'), tz=UTC)
        )
        await refresh_token_repo.create(token_create_data)

        # 7. Create a new active session tracking key for the new access token
        session_key = f"user_session:{user.user_id}:{new_access_jti}"
        ttl_seconds = expires_in * 60
        await redis_manager.client.setex(session_key, ttl_seconds, "active")

        # 8. Return the new token pair to the client
        return TokenData(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in_minutes=expires_in
        )
