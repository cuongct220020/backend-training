from datetime import datetime
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    user_role: Mapped[str] = mapped_column(String(50), default="member")

    # (Các trường này tạm thời chưa cần trong giai đoạn login/register)
    # email: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    # phone_number: Mapped[str] = mapped_column(String(255), nullable=True)
    # address: Mapped[str] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    last_login: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=True
    )

    def __repr__(self) -> str:
        return f"<User username={self.username}, role={self.user_role}>"
