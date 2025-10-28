# app/models/curriculum_subject.py
from sqlalchemy import Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.extensions import Base

if TYPE_CHECKING:
    from .curriculum import Curriculum
    from .subject import Subject

class CurriculumSubject(Base):
    __tablename__ = "curriculum_subjects"

    # --- Composite Primary Key ---
    curriculum_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("curriculums.curriculum_id"), primary_key=True
    )
    subject_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("subjects.subject_id"), primary_key=True
    )

    # --- Extra Data ---
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=True)
    # Bạn có thể thêm các trường khác như: semester_recommended (học kỳ gợi ý)

    # --- Relationships ---
    curriculum: Mapped["Curriculum"] = relationship(back_populates="subject_links")
    subject: Mapped["Subject"] = relationship(back_populates="curriculum_links")

    def __repr__(self) -> str:
        return f"<CurriculumSubject c_id={self.curriculum_id}, s_id={self.subject_id}>"