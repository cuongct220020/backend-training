# app/schemas/auth/register_schema.py
from pydantic import EmailStr, Field

from app.schemas import BaseSchema
from app.schemas.custom_types import PasswordStr


class RegisterRequest(BaseSchema):
    """Schema for a new user registration request."""
    email: EmailStr = Field(..., description="The user's email address, which will also be their username.")
    password: PasswordStr
    first_name: str | None = Field(None, min_length=1, max_length=50)
    last_name: str | None = Field(None, min_length=1, max_length=50)
