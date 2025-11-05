from app.schemas import BaseSchema
from app.schemas.custom_types import JwtStr

class RefreshRequest(BaseSchema):
    refresh_token: JwtStr