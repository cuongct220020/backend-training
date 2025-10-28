# app/models/subject.py
from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from typing import TYPE_CHECKING
from app.extensions import Base

if TYPE_CHECKING:
    from .course import Course
    from .curriculum import Curriculum
    from .curriculum_subject import CurriculumSubject

class Subject(Base):
    __tablename__ = "subjects"

    subject_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subject_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False) # "IT1110"
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    credits: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # Thêm: Gán môn học cho một khoa để phân quyền
    department: Mapped[str] = mapped_column(String(255), nullable=True)

    # --- Relationships ---
    courses: Mapped[list["Course"]] = relationship(back_populates="subject")

    # --- Mối quan hệ M-M với Curriculum ---
    # Liên kết tới Bảng liên kết (Association Table)
    curriculum_links: Mapped[list["CurriculumSubject"]] = relationship(
        back_populates="subject", cascade="all, delete-orphan"
    )

    # Liên kết "ảo" (proxy) để truy cập trực tiếp các Curriculum
    curriculums: Mapped[list["Curriculum"]] = association_proxy("curriculum_links", "curriculum")

    def __repr__(self) -> str:
        return f"<Subject code={self.subject_code}, name={self.name}>"