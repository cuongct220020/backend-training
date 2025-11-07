# app/views/auth/change_password_view.py
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from app.decorators.validate_request import validate_request
from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository
from app.schemas.auth.change_password_schema import ChangePasswordRequest
from app.schemas.response_schema import GenericResponse
from app.services.user_service import UserService


class ChangePasswordView(HTTPMethodView):
    decorators = [validate_request(ChangePasswordRequest)]

    async def post(self, request: Request):
        """Handles changing the password for the authenticated user."""
        user_id = request.ctx.user_id
        validated_data = request.ctx.validated_data

        user_repo = UserRepository(session=request.ctx.db_session)
        session_repo = UserSessionRepository(session=request.ctx.db_session)

        await UserService.change_password(
            user_id=user_id,
            data=validated_data,
            user_repo=user_repo,
            session_repo=session_repo
        )

        response = GenericResponse(
            status="success",
            message="Password changed successfully. All sessions have been logged out."
        )
        return json(response.model_dump(), status=200)