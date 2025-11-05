from datetime import datetime, UTC

from app.databases.redis_manager import redis_manager
from app.exceptions import Unauthorized
from app.repositories.user_repository import UserRepository
from app.schemas.auth.login_schema import LoginRequest
from app.schemas.auth.token_schema import TokenData
from app.utils.password_utils import verify_password
from app.utils.jwt_utils import jwt_handler


class AuthService:

    @classmethod
    async def login(
        cls,
        user_repo: UserRepository,
        login_data: LoginRequest
    ) -> TokenData:
        """Business logic for user login."""

        # 1. Validate user credentials
        user = await user_repo.get_by_username(login_data.username)
        if not user or not verify_password(login_data.password, user.password):
            raise Unauthorized("Invalid username or password")

        # --- Final Polish: Update user state on successful login ---
        # Reset failed login attempts if any
        if hasattr(user, 'failed_login_attempts') and user.failed_login_attempts > 0:
            await user_repo.reset_failed_attempts(user.user_id)
        
        # Update last login timestamp
        await user_repo.update_last_login(user.user_id)
        # --- End Final Polish ---

        # 2. Create JWT pair
        access_token, refresh_token, jti, expires_in_minutes = jwt_handler.create_tokens(user_id=user.user_id)

        # 3. Cache session for revocation tracking
        key = f"user_session:{user.user_id}:{jti}"
        ttl_seconds = expires_in_minutes * 60
        await redis_manager.client.setex(key, ttl_seconds, "active")

        # 4. Return token DTO
        return TokenData(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in_minutes=expires_in_minutes,
        )

    @classmethod
    async def logout(cls, user_id: str, jti: str, exp: int):
        """
        Logs out a user by revoking their token and cleaning up the session record.
        """
        if not all([user_id, jti, exp]):
            return

        # 1. Add the token's JTI to the denylist to invalidate it for future use
        exp_datetime = datetime.fromtimestamp(exp, tz=UTC)
        await jwt_handler.revoke(jti=jti, exp=exp_datetime)

        # 2. Delete the active session tracking record from Redis
        session_key = f"user_session:{user_id}:{jti}"
        await redis_manager.client.delete(session_key)
