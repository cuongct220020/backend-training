from datetime import datetime, UTC
from sqlalchemy import String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .user import User


class UserSession(Base):
    """
    Model đại diện cho một phiên đăng nhập (Session) dài hạn của người dùng.

    Bảng này đóng vai trò là kho lưu trữ cho các Refresh Token đang hoạt động.
    Mỗi bản ghi tương ứng với một thiết bị đã đăng nhập.
    Việc "thu hồi" (revoke) một session chính là thu hồi Refresh Token tương ứng.
    """
    __tablename__ = "user_sessions"

    session_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Khóa ngoại trỏ đến người dùng sở hữu session này.
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), nullable=False, index=True)

    # JWT ID (jti) của Refresh Token. Đây là định danh duy nhất
    # để chúng ta có thể thu hồi (revoke) một token cụ thể.
    jti: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)

    # Cờ 'kill switch'. Đặt thành True để vô hiệu hóa Refresh Token này.
    revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), nullable=False
    )

    # Thời điểm Refresh Token này hết hạn.
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # --- Siêu dữ liệu (Metadata) cho tính năng "Quản lý thiết bị" ---

    # Cập nhật mỗi khi token được làm mới (refresh).
    last_active: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )
    ip_address: Mapped[str | None] = mapped_column(String(100), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # --- Mối quan hệ ---
    user: Mapped["User"] = relationship(back_populates="sessions")

    def __repr__(self) -> str:
        return f"<UserSession id={self.session_id}, user_id={self.user_id}, jti={self.jti}, revoked={self.revoked}>"