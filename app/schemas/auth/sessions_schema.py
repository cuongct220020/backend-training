from datetime import datetime
from pydantic import Field

from app.schemas import BaseSchema

class SessionInfo(BaseSchema):
    session_id: str = Field(alias='sessionId')
    device: str
    ip_address: str = Field(alias='ipAddress')
    user_agent: str = Field(alias='userAgent')
    created_at: datetime = Field(alias='createdAt')
    last_active: datetime = Field(alias='lastActive')
