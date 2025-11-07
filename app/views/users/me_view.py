# app/views/users/me_view.py
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView
from sqlalchemy.ext.asyncio import AsyncSession

from app.decorators.auth import Auth
from app.decorators.validate_request import validate_request
from app.hooks.database import db_session
from app.repositories.user_repository import UserRepository
from app.schemas.users.user_schema import UserRead, ProfileUpdateSchema
from app.services.user_service import UserService


class MeView(HTTPMethodView):
    @Auth.login_required
    @db_session
    async def get(self, request: Request, user_id: int, session: AsyncSession):
        user_repo = UserRepository(session)
        user_service = UserService(user_repo)
        user = await user_service.get_user_by_id(user_id)
        return json(UserRead.model_validate(user).model_dump())

    @Auth.login_required
    @db_session
    @validate_request(ProfileUpdateSchema)
    async def put(self, request: Request, user_id: int, session: AsyncSession, payload: ProfileUpdateSchema):
        user_repo = UserRepository(session)
        user_service = UserService(user_repo)
        updated_user = await user_service.update_user_profile(user_id, payload)
        return json(UserRead.model_validate(updated_user).model_dump())