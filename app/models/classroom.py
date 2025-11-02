# app/models/classroom.py
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .timetable import Timetable

class Classroom(Base):
    __tablename__ = "classrooms"

    classroom_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    room_number: Mapped[str] = mapped_column(String(20), nullable=False)
    building_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # --- Relationships ---
    timetables: Mapped[list["Timetable"]] = relationship(back_populates="classroom")

    def __repr__(self) -> str:
        return f"<Classroom id={self.classroom_id}, room={self.room_number}, building={self.building_name}>"