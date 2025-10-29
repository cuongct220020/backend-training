from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    """Schema for representing a user in API responses."""
    user_id: int
    username: str
    user_role: str