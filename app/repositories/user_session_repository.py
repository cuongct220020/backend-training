# app/repositories/user_session_repository.py
from datetime import datetime, UTC
from typing import Optional, Any

from sqlalchemy import update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_session import UserSession
from app.repositories import BaseRepository, PaginationResult


class UserSessionRepository(BaseRepository[UserSession]):
    """
    Repository for UserSession model-specific database operations.
    This repository is the single source of truth for managing user sessions
    and their corresponding refresh tokens.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(UserSession, session)

    async def get_by_jti(self, jti: str) -> Optional[UserSession]:
        """Fetches a session by its Refresh Token JTI."""
        return await self.get_one_or_none(jti=jti)

    async def list_sessions_for_user(
        self,
        user_id: Any,
        page: int = 1,
        page_size: int = 10,
        include_revoked: bool = False
    ) -> PaginationResult[UserSession]:
        """Lists all sessions for a user, with pagination."""
        filters = {"user_id": user_id}
        if not include_revoked:
            filters["revoked"] = False

        return await self.get_paginated(
            page=page,
            page_size=page_size,
            filters=filters,
            sort_by=["-last_active"]  # Show most recently active first
        )

    async def revoke_session_by_id(self, session_id: Any, user_id: Any) -> bool:
        """
        Revokes a specific session by its primary key ID, ensuring it belongs to the user.
        """
        pk_col = getattr(self.model, self.pk_name)
        stmt = (
            update(self.model)
            .where(pk_col == session_id)
            .where(self.model.user_id == user_id)  # Security check
            .where(self.model.revoked == False)
            .values(revoked=True)
        )
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def revoke_all_for_user(self, user_id: Any, except_jti: Optional[str] = None) -> int:
        """
        Revokes all active sessions for a user, with an optional JTI exclusion.
        This is a critical security function for "log out everywhere" scenarios.
        """
        stmt = (
            update(self.model)
            .where(self.model.user_id == user_id)
            .where(self.model.revoked == False)
        )
        if except_jti:
            stmt = stmt.where(self.model.jti != except_jti)

        result = await self.session.execute(stmt)
        return result.rowcount

    async def prune_expired_sessions(self) -> int:
        """
        Deletes all expired and unrevoked session records from the database.
        This is a maintenance task to keep the user_sessions table clean.
        """
        now = datetime.now(UTC)
        stmt = delete(self.model).where(self.model.expires_at < now)
        result = await self.session.execute(stmt)
        return result.rowcount

    async def is_revoked(self, jti: str) -> bool:
        """Checks if a specific token JTI has been revoked."""
        session = await self.get_by_jti(jti)
        # If the session doesn't exist, it can't be used, so it's "effectively" revoked.
        if not session:
            return True
        return session.revoked
