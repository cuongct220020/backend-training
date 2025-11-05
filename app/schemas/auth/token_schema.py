# app/schemas/auth/token_schema.py
from app.schemas import BaseSchema

class TokenData(BaseSchema):
    """Consolidated token data."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in_minutes: int
