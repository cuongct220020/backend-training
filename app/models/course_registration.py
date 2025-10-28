# app/models/course_registration.py
from datetime import datetime, UTC
from enum import Enum
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Enum as SQLEnum
from typing import TYPE_CHECKING
from app.extensions import Base

if TYPE_CHECKING:
    from .student import Student
    from .course import Course


class RegistrationStatus(Enum):
    REGISTERED = "registered"
    FULLED = "fulled"
    CANCELLED = "cancelled"


class CourseRegistration(Base):
    __tablename__ = "course_registrations"

    registration_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    registration_time: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    status: Mapped[RegistrationStatus] = mapped_column(
        SQLEnum(RegistrationStatus), default=RegistrationStatus.REGISTERED
    )

    # --- Foreign Keys ---
    student_id: Mapped[str] = mapped_column(String(20), ForeignKey('students.student_id'), nullable=False)
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey('courses.course_id'), nullable=False)

    # --- Relationships ---
    student: Mapped["Student"] = relationship(back_populates="registrations")
    course: Mapped["Course"] = relationship(back_populates="registrations")

    def __repr__(self) -> str:
        return f"<CourseRegistration student={self.student_id}, course={self.course_id}, status={self.status.value}>"