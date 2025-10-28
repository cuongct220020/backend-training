# app/models/user.py
from datetime import datetime, UTC
from sqlalchemy import String, Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Enum as SQLEnum
from typing import TYPE_CHECKING
from app.extensions import Base
from app.constants.user_role_constants import UserRole

if TYPE_CHECKING:
    from .student import Student
    from .lecturer import Lecturer
    from .admin import Admin


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    user_role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.STUDENT)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), nullable=False
    )
    last_login: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), nullable=True
    )

    # --- Relationships ---
    student_profile: Mapped["Student"] = relationship(back_populates="user", cascade="all, delete-orphan")
    lecturer_profile: Mapped["Lecturer"] = relationship(back_populates="user", cascade="all, delete-orphan")
    admin_profile: Mapped["Admin"] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User username={self.username}, role={self.user_role}>"