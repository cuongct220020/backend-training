# app/repositories/user_repository.py
from datetime import datetime, UTC
from typing import Optional, Any

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for User model-specific database operations.
    Inherits all common CRUD, pagination, and soft-delete logic from BaseRepository.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_username(self, username: str, include_deleted: bool = False) -> Optional[User]:
        """
        Fetch a user record by username (case-insensitive), respecting soft-delete.
        Returns None if no user is found.
        """
        if not username:
            return None

        # Build the initial statement with the username filter
        stmt = select(self.model).where(func.lower(self.model.username) == func.lower(username))

        # Use the base class's helper to apply standard filters (like soft-delete)
        stmt = self._apply_filters_and_sort(stmt, include_deleted=include_deleted)

        result = await self.session.execute(stmt.limit(1))
        return result.scalars().first()

    async def activate_user(self, user_id: Any) -> bool:
        """
        Activates a user account by setting is_active to True.
        Returns True if the user was found and activated, False otherwise.
        """
        if not hasattr(self.model, 'is_active'):
            return False

        stmt = (
            update(self.model)
            .where(self.model.user_id == user_id)
            .where(self.model.is_active == False)
            .values(is_active=True)
        )
        result = await self.session.execute(stmt)
        if result.rowcount > 0:
            await self.session.flush()
            return True
        return False

    async def increment_failed_attempts(self, user_id: Any, by: int = 1) -> Optional[int]:
        """
        Increment failed_login_attempts and return new value.
        Use atomic update for safety under concurrency.
        """
        if not (hasattr(self.model, 'failed_login_attempts') and hasattr(self.model, 'updated_at')):
            return None

        q = (
            update(self.model)
            .where(self.model.user_id == user_id)  # Correctly use user_id
            .values(failed_login_attempts=self.model.failed_login_attempts + by,
                    updated_at=func.now())
            .returning(self.model.failed_login_attempts)
        )
        result = await self.session.execute(q)
        row = result.first()
        await self.session.flush()
        return row[0] if row else None

    async def reset_failed_attempts(self, user_id: Any) -> None:
        if not (hasattr(self.model, 'failed_login_attempts') and hasattr(self.model, 'updated_at')):
            return

        q = (
            update(self.model)
            .where(self.model.user_id == user_id)  # Correctly use user_id
            .values(failed_login_attempts=0, updated_at=func.now())
        )
        await self.session.execute(q)
        await self.session.flush()

    async def lock_user(self, user_id: Any, until: Optional[datetime] = None) -> None:
        """Lock user account. Optionally set a lock expiration (if model supports it)."""
        if not (hasattr(self.model, 'is_locked') and hasattr(self.model, 'updated_at')):
            return

        values = {"is_locked": True, "updated_at": func.now()}
        if hasattr(self.model, "locked_until") and until is not None:
            values["locked_until"] = until
        q = update(self.model).where(self.model.user_id == user_id).values(**values)  # Correctly use user_id
        await self.session.execute(q)
        await self.session.flush()

    async def unlock_user(self, user_id: Any) -> None:
        if not (hasattr(self.model, 'is_locked') and hasattr(self.model, 'updated_at')):
            return

        values = {"is_locked": False, "failed_login_attempts": 0, "updated_at": func.now()}
        if hasattr(self.model, "locked_until"):
            values["locked_until"] = None
        q = update(self.model).where(self.model.user_id == user_id).values(**values)  # Correctly use user_id
        await self.session.execute(q)
        await self.session.flush()

    async def update_last_login(self, user_id: Any, when: Optional[datetime] = None) -> None:
        if not hasattr(self.model, 'last_login'):
            return

        when = when or datetime.now(UTC)
        q = update(self.model).where(self.model.user_id == user_id).values(last_login=when, updated_at=func.now()) # Correctly use user_id
        await self.session.execute(q)
        await self.session.flush()