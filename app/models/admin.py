# app/models/admin.py
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .user import User


class Admin(Base):
    __tablename__ = "admins"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), primary_key=True)

    # --- Relationships ---
    user: Mapped["User"] = relationship(back_populates="admin_profile")

    def __repr__(self) -> str:
        return f"<Admin user_id={self.user_id}>"