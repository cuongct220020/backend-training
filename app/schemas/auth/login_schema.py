# app/schemas/login_schema.py
from app.schemas import BaseSchema
from app.schemas.custom_types import UsernameStr, PasswordStr

class LoginRequest(BaseSchema):
    """Schema for login requests (Input)."""
    username: UsernameStr
    password: PasswordStr
    captcha_token: str | None = None