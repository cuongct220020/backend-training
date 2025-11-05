from enum import Enum
from pydantic import EmailStr, SecretStr, Field

from app.schemas import BaseSchema

class OtpAction(str, Enum):
    REGISTER = "register"
    RESET_PASSWORD = "reset_password"

class OTPRequest(BaseSchema):
    email: EmailStr
    action: OtpAction  # Use Enum for type safety

class OTPVerifyRequest(BaseSchema):
    email: EmailStr
    otp_code: SecretStr = Field(min_length=6, max_length=6)