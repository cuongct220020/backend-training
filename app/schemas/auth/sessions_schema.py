# app/schemas/auth/sessions_schema.py
from datetime import datetime
from pydantic import Field

from app.schemas import BaseSchema


class SessionResponse(BaseSchema):
    """Schema for representing a user's login session."""
    session_id: int = Field(..., description="The unique identifier for the session.")
    ip_address: str | None = Field(None, description="The IP address where the session originated.")
    user_agent: str | None = Field(None, description="The user agent of the client for the session.")
    last_active: datetime = Field(..., description="The last time the session was actively used.")
    created_at: datetime = Field(..., description="The time the session was created.")