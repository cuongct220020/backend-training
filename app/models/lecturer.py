# app/models/lecturer.py
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .address import Address
    from .course import Course
    from .curriculum import Curriculum

class Lecturer(Base):
    __tablename__ = "lecturers"

    lecturer_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=True) # "Tiến sĩ", "Thạc sĩ"
    department: Mapped[str] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)

    # --- Foreign Keys ---
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), unique=True, nullable=False)
    address_id: Mapped[int] = mapped_column(Integer, ForeignKey('addresses.address_id'), nullable=True)

    # --- Relationships ---
    user: Mapped["User"] = relationship(back_populates="lecturer_profile")
    address: Mapped["Address"] = relationship(back_populates="lecturers")
    courses_taught: Mapped[list["Course"]] = relationship(back_populates="lecturer")

    # Một Lecturer (với role 'headmaster') có thể quản lý nhiều curriculum
    curriculums: Mapped[list["Curriculum"]] = relationship(back_populates="lecturer")

    def __repr__(self) -> str:
        return f"<Lecturer lecturer_id={self.lecturer_id}>"