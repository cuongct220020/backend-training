# app/schemas/auth_schema.py
from pydantic import SecretStr

from app.schemas.base_schema import BaseSchema


class LoginSchema(BaseSchema):
    """Schema for login requests (Input)."""
    username: str
    password: SecretStr


class Token(BaseSchema):
    """Schema for the response after a successful login (Output)."""
    access_token: str
    token_type: str = "bearer"
