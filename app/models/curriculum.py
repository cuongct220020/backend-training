# app/models/curriculum.py
from datetime import datetime, UTC
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .lecturer import Lecturer
    from .subject import Subject
    from .curriculum_subject import CurriculumSubject

class Curriculum(Base):
    __tablename__ = "curriculums"

    curriculum_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    curriculum_code: Mapped[str] = mapped_column(String(20), nullable=False)
    curriculum_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[str] = mapped_column(String(100), nullable=False)
    create_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    update_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    # --- Foreign Keys ---
    lecturer_id: Mapped[str] = mapped_column(String(20), ForeignKey('lecturers.lecturer_id'), nullable=True)

    # --- Relationships ---
    lecturer: Mapped["Lecturer"] = relationship(back_populates="curriculums")

    # Liên kết tới Bảng liên kết (Association Table)
    subject_links: Mapped[list["CurriculumSubject"]] = relationship(
        back_populates="curriculum", cascade="all, delete-orphan"
    )
    subjects: Mapped[list["Subject"]] = association_proxy("subject_links", "subject")

    def __repr__(self) -> str:
        return f"<Curriculum curriculum_name={self.curriculum_name!r}, academic_year={self.academic_year!r}>"