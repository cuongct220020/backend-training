# app/repositories/refresh_token_repository.py
from datetime import datetime, UTC
from typing import Optional, Any

from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken  # Assuming model path
from app.repositories import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    """
    Repository for RefreshToken model-specific database operations.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(RefreshToken, session)

    async def get_by_jti(self, jti: str) -> Optional[RefreshToken]:
        """Fetches a refresh token by its JTI."""
        # Reusing the powerful get_many method from the base class
        results = await self.get_many(filters={"jti": jti}, limit=1)
        return results[0] if results else None

    async def is_revoked(self, jti: str) -> bool:
        """Checks if a specific token JTI has been revoked."""
        token = await self.get_by_jti(jti)
        # If the token doesn't exist or has no 'revoked' attribute, it's not considered revoked.
        if not token or not hasattr(token, "revoked"):
            return False
        return token.revoked

    async def revoke_by_jti(self, jti: str) -> bool:
        """Efficiently revokes a token by its JTI using a bulk UPDATE."""
        if not hasattr(self.model, "revoked"):
            # If model doesn't support revocation, fallback to hard delete
            token = await self.get_by_jti(jti)
            if token:
                return await self.delete(getattr(token, self.pk_name))
            return False

        stmt = (
            update(self.model)
            .where(self.model.jti == jti)
            .where(self.model.revoked == False)
            .values(revoked=True)
        )
        result = await self.session.execute(stmt)
        if result.rowcount > 0:
            await self.session.flush()
            return True
        return False

    async def revoke_all_for_user(self, user_id: Any) -> int:
        """Efficiently revokes all active tokens for a user using a bulk UPDATE."""
        if not hasattr(self.model, "revoked"):
            return 0  # Cannot revoke if the model doesn't support it

        stmt = (
            update(self.model)
            .where(self.model.user_id == user_id)
            .where(self.model.revoked == False)
            .values(revoked=True)
        )
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount

    async def prune_expired_tokens(self) -> int:
        """Efficiently deletes all expired refresh tokens using a bulk DELETE."""
        now = datetime.now(UTC)
        stmt = delete(self.model).where(self.model.expires_at < now)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount