# app/services/user_service.py
from typing import Any
from pydantic import SecretStr

from app.decorators.cache import cache
from app.exceptions import NotFound, Conflict, Unauthorized
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.schemas.users.user_schema import UserRead, UserCreate, UserUpdate
from app.utils.password_utils import hash_password, verify_password


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    @cache(schema=UserRead, ttl=300, prefix="user_profile")
    async def get_user_by_id(self, user_id: int) -> User:
        """Fetches a user by their ID. Raises NotFound if the user does not exist."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFound(f"User with id {user_id} not found")
        return user

    async def change_password(
        self,
        user_id: Any,
        old_password: str,
        new_password: str,
        refresh_token_repo: RefreshTokenRepository
    ):
        """Handles the logic for a logged-in user to change their password."""
        # 1. Fetch the current user
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            # This should not happen if the user is authenticated, but it's a good safeguard
            raise NotFound("Authenticated user not found.")

        # 2. Verify the old password
        if not verify_password(old_password, user.password):
            raise Unauthorized("Incorrect old password.")

        # 3. Hash the new password and update the user record
        hashed_new_password = hash_password(new_password)
        update_schema = UserUpdate(password=SecretStr(hashed_new_password))
        await self.user_repo.update(user_id, update_schema)

        # 4. Security Best Practice: Revoke all other refresh tokens
        await refresh_token_repo.revoke_all_for_user(user_id)

        return