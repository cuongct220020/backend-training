# app/repositories/session_repository.py
from datetime import datetime, UTC
from typing import Optional, Any, List

from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth_session import AuthSession  # Assuming model path
from app.repositories import BaseRepository, PaginationResult


class SessionRepository(BaseRepository[AuthSession]):
    """
    Repository for AuthSession model-specific database operations.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(AuthSession, session)

    async def get_session_by_jti(self, jti: str) -> Optional[AuthSession]:
        """Fetches a session by its JTI."""
        results = await self.get_many(filters={"jti": jti}, limit=1)
        return results[0] if results else None

    async def list_sessions_for_user(
        self,
        user_id: Any,
        page: int = 1,
        page_size: int = 10,
        include_revoked: bool = False
    ) -> PaginationResult[AuthSession]:
        """Lists all sessions for a user, with pagination."""
        filters = {"user_id": user_id}
        if not include_revoked and hasattr(self.model, "revoked"):
            filters["revoked"] = False
        
        return await self.get_paginated(
            page=page,
            page_size=page_size,
            filters=filters,
            sort_by=["created_at_desc"]
        )

    async def revoke_session(self, session_id: Any) -> bool:
        """Efficiently revokes a session by its ID using a bulk UPDATE."""
        if not hasattr(self.model, "revoked"):
            return await self.delete(session_id)

        pk_col = getattr(self.model, self.pk_name)
        stmt = (
            update(self.model)
            .where(pk_col == session_id)
            .where(self.model.revoked == False)
            .values(revoked=True)
        )
        result = await self.session.execute(stmt)
        if result.rowcount > 0:
            await self.session.flush()
            return True
        return False

    async def revoke_all_sessions_for_user(self, user_id: Any, except_jti: Optional[str] = None) -> int:
        """Efficiently revokes all active sessions for a user, with an optional exclusion."""
        if not hasattr(self.model, "revoked"):
            return 0

        stmt = (
            update(self.model)
            .where(self.model.user_id == user_id)
            .where(self.model.revoked == False)
            .values(revoked=True)
        )
        if except_jti:
            stmt = stmt.where(self.model.jti != except_jti)

        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount

    async def prune_expired_sessions(self) -> int:
        """Efficiently revokes all expired sessions using a bulk UPDATE."""
        if not hasattr(self.model, "revoked"):
            return 0
            
        now = datetime.now(UTC)
        stmt = (
            update(self.model)
            .where(self.model.expires_at < now)
            .where(self.model.revoked == False)
            .values(revoked=True)
        )
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount