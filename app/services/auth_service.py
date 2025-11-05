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

        # 2. Create JWT pair
        access_token, refresh_token, jti, expires_in_minutes = jwt_handler.create_tokens(user_id=user.user_id)

        # 3. Cache session for revocation tracking
        key = f"user_session:{user.user_id}:{jti}"
        ttl_seconds = expires_in_minutes * 60
        await redis_manager.setex(key, ttl_seconds, "active")

        # 4. Return token DTO
        return TokenData(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in_minutes=expires_in_minutes,
        )

    # @classmethod
    # async def logout(self, jti: str, exp: int):
    #     """Adds a token's JTI to the deny-list until it expires."""
    #     now_ts = int(datetime.now(UTC).timestamp())
    #     # Calculate how many seconds the token has left to live
    #     # Add a small buffer (e.g., 5s) to account for clock skew
    #     remaining_time = exp - now_ts + 5
    #
    #     if remaining_time > 0:
    #         await redis_manager.client.set(
    #             f"deny_list:jti:{jti}", "revoked", ex=remaining_time
    #         )
