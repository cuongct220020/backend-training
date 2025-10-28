# app/models/course.py
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.extensions import Base

if TYPE_CHECKING:
    from .subject import Subject
    from .lecturer import Lecturer
    from .course_registration import CourseRegistration
    from .timetable import Timetable


class Course(Base):
    __tablename__ = "courses"

    course_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)  # "Tin học đại cương - Lớp 01"
    semester: Mapped[str] = mapped_column(String(50), nullable=False)  # "HK1-2025"
    max_students: Mapped[int] = mapped_column(Integer, default=50)

    # --- Foreign Keys ---
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    lecturer_id: Mapped[str] = mapped_column(String(20), ForeignKey('lecturers.lecturer_id'), nullable=True)

    # --- Relationships ---
    subject: Mapped["Subject"] = relationship(back_populates="courses")
    lecturer: Mapped["Lecturer"] = relationship(back_populates="courses_taught")
    registrations: Mapped[list["CourseRegistration"]] = relationship(back_populates="course")
    timetables: Mapped[list["Timetable"]] = relationship(back_populates="course")

    def __repr__(self) -> str:
        return f"<Course id={self.course_id}, name={self.name}>"