# app/schemas/custom_types.py
import re
from typing import Annotated
from pydantic import Field, SecretStr, AfterValidator
from app.exceptions import BadRequest

# --- Custom Validators ---

def _validate_password_complexity(value: SecretStr) -> SecretStr:
    """Validate that the password contains at least one uppercase, one lowercase, and one digit."""
    plain_password = value.get_secret_value()
    if not re.search(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', plain_password):
        raise BadRequest(
            'Password must contain at least one uppercase letter, '
            'one lowercase letter, and one digit.'
        )
    return value

# --- Annotated Types for Reusability ---

# Username with strict character set (alphanumeric and underscore/hyphen) and length constraints.
# This is a strong defense against injection attacks (XSS, NoSQLi, etc.) by disallowing special characters.
UsernameStr = Annotated[
    str,
    Field(min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_-]+$')
]

# Password with minimum length and complexity validation.
PasswordStr = Annotated[
    SecretStr,
    Field(min_length=8, max_length=128), # Added max_length to prevent resource exhaustion
    AfterValidator(_validate_password_complexity)
]

# Non-empty string for fields that must not be empty.
NonEmptyStr = Annotated[str, Field(min_length=1)]

# JWT String (basic format check). Prevents malformed tokens.
JwtStr = Annotated[
    str,
    Field(pattern=r'^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$')
]
