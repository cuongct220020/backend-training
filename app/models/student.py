# app/models/student.py
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.extensions import Base

if TYPE_CHECKING:
    from .user import User
    from .address import Address
    from .course_registration import CourseRegistration


class Student(Base):
    __tablename__ = 'students'

    student_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    major: Mapped[str] = mapped_column(String(20), nullable=False)
    class_name: Mapped[str] = mapped_column(String(20), nullable=False)
    enrollment_year: Mapped[int] = mapped_column(Integer, nullable=False)

    # --- Foreign Keys ---
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), unique=True, nullable=False)
    address_id: Mapped[int] = mapped_column(Integer, ForeignKey('addresses.address_id'), nullable=True)

    # --- Relationships ---
    user: Mapped["User"] = relationship(back_populates="student_profile")
    address: Mapped["Address"] = relationship(back_populates="students")
    registrations: Mapped[list["CourseRegistration"]] = relationship(back_populates="student")

    def __repr__(self):
        return f'<Student user_id={self.user_id}>'