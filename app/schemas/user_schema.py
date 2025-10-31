# app/schemas/user_schema.py
import re
from pydantic import Field, SecretStr, field_validator

from app.constants.user_role_constants import UserRole
from app.hooks import exceptions
from app.schemas.base_schema import BaseSchema


# --- Profile Schemas (for reading nested user data) ---

class StudentRead(BaseSchema):
    """Schema for reading student-specific profile data."""
    student_id: str
    major: str
    class_name: str


class LecturerRead(BaseSchema):
    """Schema for reading lecturer-specific profile data."""
    lecturer_id: str
    title: str | None
    department: str | None


class AdminRead(BaseSchema):
    """Schema for reading admin-specific profile data."""
    user_id: int


# --- Core User Schemas (Base, Create, Update, Read) ---

class UserBase(BaseSchema):
    """Base schema with common user fields."""
    username: str = Field(..., min_length=3, max_length=50)
    user_role: UserRole


class UserCreate(UserBase):
    """Schema for creating a new user (replaces RegisterSchema)."""
    password: SecretStr = Field(..., min_length=8)

    # noinspection PyTypeChecker
    @field_validator('password')
    @classmethod
    def validate_password_complexity(cls, value: SecretStr) -> SecretStr:
        """Validate that the password contains at least one uppercase, one lowercase, and one digit."""
        plain_password = value.get_secret_value()
        if not re.search(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', plain_password):
            raise exceptions.BadRequest(
                'Password must contain at least one uppercase letter, '
                'one lowercase letter, and one digit.'
            )
        return value


class UserUpdate(BaseSchema):
    """Schema for updating a user. All fields are optional."""
    username: str | None = Field(None, min_length=3, max_length=50)
    password: SecretStr | None = None
    is_active: bool | None = None


class UserRead(UserBase):
    """Schema for reading a user, including nested profile information."""
    user_id: int
    is_active: bool
    student_profile: StudentRead | None = None
    lecturer_profile: LecturerRead | None = None
    admin_profile: AdminRead | None = None
