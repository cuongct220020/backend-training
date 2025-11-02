# app/models/address.py
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .student import Student
    from .lecturer import Lecturer

class Address(Base):
    __tablename__ = "addresses"

    address_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ward: Mapped[str] = mapped_column(String(100), nullable=True)
    district: Mapped[str] = mapped_column(String(100), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    province: Mapped[str] = mapped_column(String(100), nullable=False)

    # --- Relationships ---
    students: Mapped[list["Student"]] = relationship(back_populates="address")
    lecturers: Mapped[list["Lecturer"]] = relationship(back_populates="address")

    def __repr__(self) -> str:
        return f"<Address id={self.address_id}, {self.district}, {self.province_city}>"