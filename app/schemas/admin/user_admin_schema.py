# app/schemas/admin/user_admin_schema.py
from pydantic import EmailStr, Field
from typing import Optional
from datetime import datetime

from app.constants.user_role_constants import UserRole
from app.schemas import BaseSchema
from app.schemas.custom_types import PasswordStr


# --- Schemas for Admin Actions ---

class AdminUserCreateSchema(BaseSchema):
    """Schema for admin to create a new user."""
    username: EmailStr = Field(..., description="User's email and username.")
    password: PasswordStr = Field(..., description="User's password.")
    user_role: UserRole = Field(default=UserRole.STUDENT, description="Role to assign to the user.")
    is_active: bool = Field(default=True, description="Set user's active status.")
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)


class AdminUserUpdateSchema(BaseSchema):
    """Schema for admin to update a user's information. All fields are optional."""
    user_role: Optional[UserRole] = Field(None, description="Update the user's role.")
    is_active: Optional[bool] = Field(None, description="Update the user's active status.")
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)


# --- Schemas for Admin Responses ---

class AdminUserResponseSchema(BaseSchema):
    """Detailed user information for admin responses. Never includes password."""
    user_id: int
    username: EmailStr
    user_role: UserRole
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]
