# app/models/curriculum.py
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from typing import TYPE_CHECKING
from app.extensions import Base

if TYPE_CHECKING:
    # Sửa: Import Lecturer thay vì HeadMaster
    from .lecturer import Lecturer
    from .subject import Subject
    from .curriculum_subject import CurriculumSubject

class Curriculum(Base):
    __tablename__ = "curriculums"

    curriculum_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    department: Mapped[str] = mapped_column(String(255), nullable=False)
    start_year: Mapped[int] = mapped_column(Integer, nullable=False)

    # --- Foreign Keys ---
    lecturer_id: Mapped[str] = mapped_column(String(20), ForeignKey("lecturers.lecturer_id"), nullable=True)

    # --- Relationships ---
    lecturer: Mapped["Lecturer"] = relationship(back_populates="curriculums")

    # Liên kết tới Bảng liên kết (Association Table)
    subject_links: Mapped[list["CurriculumSubject"]] = relationship(
        back_populates="curriculum", cascade="all, delete-orphan"
    )
    subjects: Mapped[list["Subject"]] = association_proxy("subject_links", "subject")

    def __repr__(self) -> str:
        return f"<Curriculum name={self.name}, year={self.start_year}>"