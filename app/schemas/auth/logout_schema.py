# app/schemas/logout_schema.py
from app.schemas import BaseSchema
from app.schemas.custom_types import JwtStr

class LogoutRequest(BaseSchema):
    refresh_token: JwtStr