import re
from pydantic import BaseModel, Field, validator

class LoginSchema(BaseModel):
    """Schema for login requests."""
    username: str = Field(..., min_length=3, max_length=50)
    password: str

class RegisterSchema(BaseModel):
    """Schema for registration requests with password complexity validation."""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

    @validator('password')
    def validate_password_complexity(cls, value):
        """Validate that the password contains at least one uppercase, one lowercase, and one digit."""
        if not re.search(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', value):
            raise ValueError('Password must contain at least one uppercase letter, one lowercase letter, and one digit.')
        return value