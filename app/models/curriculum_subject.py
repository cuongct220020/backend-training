# app/models/curriculum_subject.py
from sqlalchemy import Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.extensions import Base
from app.constants.subject_type_constants import SubjectType

if TYPE_CHECKING:
    from .curriculum import Curriculum
    from .subject import Subject

class CurriculumSubject(Base):
    __tablename__ = "curriculum_subjects"

    curriculum_subject_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # --- Foreign Keys ---
    curriculum_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('curriculums.curriculum_id'), primary_key=True
    )
    subject_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('subjects.subject_id'), primary_key=True
    )

    type: Mapped[SubjectType] = mapped_column(SQLEnum(SubjectType), default=SubjectType.REQUIRED)

    # --- Relationships ---
    curriculum: Mapped["Curriculum"] = relationship(back_populates="subject_links")
    subject: Mapped["Subject"] = relationship(back_populates="curriculum_links")

    def __repr__(self) -> str:
        return f"<CurriculumSubject curriculum_id={self.curriculum_id}, subject_id={self.subject_id}>"