# app/utils/password_utils.py
import bcrypt
import asyncio
from app.schemas.custom_types import PasswordStr

def _blocking_verify_password(
        login_password_str: str,
        hashed_password_str: str
    ) -> bool:
    """
    Hàm đồng bộ (blocking) thực hiện việc so sánh bcrypt.
    Mật khẩu hash đã được lưu trong DB là str, cần encode về bytes cho bcrypt.checkpw.
    """
    # So sánh mật khẩu trần (đã encode) với mật khẩu hash (đã encode)
    return bcrypt.checkpw(
        login_password_str.encode('utf-8'),
        hashed_password_str.encode('utf-8')
    )

async def verify_password(login_password: PasswordStr, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a hashed version in a separate thread.
    """
    # 1. Lấy chuỗi trần của mật khẩu đăng nhập từ SecretStr
    plain_password_str = login_password.get_secret_value()

    # 2. Sử dụng asyncio.to_thread để chạy tác vụ CPU-bound trong ThreadPoolExecutor
    is_valid = await asyncio.to_thread(
        _blocking_verify_password,
        plain_password_str,
        hashed_password
    )

    return is_valid

def hash_password(plain: str) -> str:
    """Hashes a plain text password using bcrypt."""
    hashed = bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')