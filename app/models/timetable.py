# app/models/timetable.py
from datetime import time
from sqlalchemy import String, Integer, Time, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.extensions import Base

if TYPE_CHECKING:
    from .course import Course
    from .classroom import Classroom

class Timetable(Base):
    __tablename__ = "timetables"

    timetable_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    day_of_week: Mapped[str] = mapped_column(String(15), nullable=False) # "Monday", "Tuesday"
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)

    # --- Foreign Keys ---
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey('courses.course_id'), nullable=False)
    classroom_id: Mapped[int] = mapped_column(Integer, ForeignKey('classrooms.classroom_id'), nullable=True)

    # --- Relationships ---
    course: Mapped["Course"] = relationship(back_populates="timetables")
    classroom: Mapped["Classroom"] = relationship(back_populates="timetables")

    def __repr__(self) -> str:
        return f"<Timetable id={self.timetable_id}, course_id={self.course_id}, day={self.day_of_week}, classroom_id={self.classroom_id}>"