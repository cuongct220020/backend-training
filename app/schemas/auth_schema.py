import re
from pydantic import BaseModel, Field, field_validator, SecretStr, ConfigDict

from app.hooks import exceptions
from app.constants.user_role_constants import UserRole


# 1. Base Schema for common configuration
class BaseSchema(BaseModel):
    """A base schema that forbids extra fields for improved security."""
    model_config = ConfigDict(extra='forbid')


# 2. Schema for shared fields to keep code DRY (Don't Repeat Yourself)
class UserIdentitySchema(BaseSchema):
    """Schema for fields that identify a user."""
    username: str = Field(..., min_length=3, max_length=50)


# --- Final Schemas ---
class LoginSchema(UserIdentitySchema):
    """Schema for login requests."""
    # 3. Use SecretStr for password security
    password: SecretStr


class RegisterSchema(UserIdentitySchema):
    """Schema for registration requests with password complexity validation."""
    password: SecretStr = Field(..., min_length=8)
    user_role: UserRole

    # noinspection PyTypeChecker
    @field_validator('password')
    @classmethod
    def validate_password_complexity(cls, value: SecretStr) -> SecretStr:
        """
        Validate that the password contains at least one uppercase,
        one lowercase, and one digit.
        """
        # Use get_secret_value() to securely access the password content
        plain_password = value.get_secret_value()
        if not re.search(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', plain_password):
            raise exceptions.BadRequest(
                'Password must contain at least one uppercase letter, '
                'one lowercase letter, and one digit.'
            )
        return value