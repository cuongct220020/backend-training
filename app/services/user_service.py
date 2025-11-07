# app/services/user_service.py
from typing import Any
from pydantic import SecretStr

from app.decorators.cache import cache
from app.exceptions import NotFound, Conflict, Unauthorized
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository
from app.schemas.auth.change_password_schema import ChangePasswordRequest
from app.schemas.users.user_schema import UserRead, UserCreate, UserUpdate, ProfileUpdateSchema
from app.schemas.admin.user_admin_schema import AdminUserCreateSchema, AdminUserUpdateSchema
from app.utils.password_utils import hash_password, verify_password
from app.services.auth_service import AuthService


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

    @classmethod
    async def change_password(
            cls,
            user_id: Any,
            data: ChangePasswordRequest,
            user_repo: UserRepository,
            session_repo: UserSessionRepository
    ):
        """Changes a user's password, revokes all DB sessions, and invalidates all access tokens."""
        user = await user_repo.get_by_id(user_id)
        if not user:
            raise NotFound("Authenticated user not found.")

        if verify_password(data.old_password.get_secret_value(), user.password):
            raise Unauthorized("Invalid old password.")

        hashed_new_password = hash_password(data.new_password.get_secret_value())
        update_schema = UserUpdate(password=SecretStr(hashed_new_password))
        await user_repo.update(user.user_id, update_schema)

        await session_repo.revoke_all_for_user(user.user_id)
        await AuthService.revoke_all_access_tokens_for_user(user.user_id)

    async def update_user_profile(self, user_id: Any, profile_data: ProfileUpdateSchema) -> User:
        """Updates a user's profile information."""
        updated_user = await self.user_repo.update_user_profile(user_id, profile_data)
        if not updated_user:
            raise NotFound(f"User with id {user_id} not found.")
        return updated_user

    # --- Admin Management Methods ---

    async def list_all_users(self, page: int, page_size: int):
        """Lists all users with pagination for admin purposes."""
        return await self.user_repo.get_paginated(page=page, page_size=page_size)

    async def create_user_by_admin(self, user_data: AdminUserCreateSchema) -> User:
        """Creates a new user by an admin."""
        existing_user = await self.user_repo.get_by_username(user_data.username)
        if existing_user:
            raise Conflict(f"User with username {user_data.username} already exists.")

        hashed_password = hash_password(user_data.password.get_secret_value())
        
        user_create_for_repo = UserCreate(
            username=user_data.username,
            password=SecretStr(hashed_password),
            user_role=user_data.user_role,
            is_active=user_data.is_active,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        new_user = await self.user_repo.create(user_create_for_repo)
        return new_user

    async def get_user_details_by_admin(self, user_id: int) -> User:
        """Fetches detailed user information for admin."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFound(f"User with id {user_id} not found.")
        return user

    async def update_user_by_admin(self, user_id: int, update_data: AdminUserUpdateSchema) -> User:
        """Updates a user's information by an admin."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFound(f"User with id {user_id} not found.")
        
        user_update_for_repo = UserUpdate(**update_data.model_dump(exclude_unset=True))
        
        updated_user = await self.user_repo.update(user_id, user_update_for_repo)
        return updated_user

    async def delete_user_by_admin(self, user_id: int, session_repo: UserSessionRepository) -> None:
        """
        Deletes a user (soft delete by setting is_active=False) and revokes all their sessions.
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFound(f"User with id {user_id} not found.")
        
        await self.user_repo.update(user_id, UserUpdate(is_active=False))
        
        await session_repo.revoke_all_for_user(user_id)
        await AuthService.revoke_all_access_tokens_for_user(user_id)
