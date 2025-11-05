# app/repositories/otp_repository.py
from datetime import datetime, UTC
from typing import Optional, Any

from sqlalchemy import select, func, update, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.otp import OTP  # Assuming the model is in app/models/otp.py
from app.repositories import BaseRepository


class OTPRepository(BaseRepository[OTP]):
    """
    Repository for OTP model-specific database operations.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(OTP, session)

    async def get_active_otp(self, email: str, action: str, code: Optional[str] = None) -> Optional[OTP]:
        """
        Fetch the active (not used, not expired) OTP for an email+action, optionally filter by code.
        """
        now = datetime.now(UTC)
        stmt = select(self.model).where(
            and_(
                func.lower(self.model.email) == email.lower(),
                self.model.action == action,
                self.model.used.is_(False),
                self.model.expires_at >= now
            )
        )
        if code:
            stmt = stmt.where(self.model.code == code)

        result = await self.session.execute(stmt.limit(1))
        return result.scalars().first()

    async def mark_otp_used(self, otp_id: Any) -> bool:
        """Marks a specific OTP as used using an efficient UPDATE statement."""
        stmt = (
            update(self.model)
            .where(getattr(self.model, self.pk_name) == otp_id)
            .where(self.model.used.is_(False))
            .values(used=True)
        )
        result = await self.session.execute(stmt)
        if result.rowcount > 0:
            await self.session.flush()
            return True
        return False

    async def invalidate_otps_for_email(self, email: str, action: Optional[str] = None) -> int:
        """Efficiently invalidates all active OTPs for a given email using a bulk UPDATE."""
        stmt = (
            update(self.model)
            .where(func.lower(self.model.email) == email.lower())
            .where(self.model.used.is_(False))
            .values(used=True)
        )
        if action:
            stmt = stmt.where(self.model.action == action)

        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount

    async def prune_expired_otps(self) -> int:
        """Efficiently deletes all expired OTPs using a bulk DELETE."""
        now = datetime.now(UTC)
        stmt = delete(self.model).where(self.model.expires_at < now)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount