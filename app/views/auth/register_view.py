from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from app.decorators.validate_request import validate_request
from app.repositories.user_repository import UserRepository
from app.schemas.auth.register_schema import RegisterRequest
from app.services.auth_service import AuthService
from app.schemas.response_schema import GenericResponse


class RegisterView(HTTPMethodView):

    @validate_request(RegisterRequest)
    async def post(self, request: Request):
        """Handles new user registration."""
        validated_data = request.ctx.validated_data

        user_repo = UserRepository(session=request.ctx.db_session)

        await AuthService.register_user(
            reg_data=validated_data,
            user_repo=user_repo
        )

        response = GenericResponse(
            status="success",
            message="Registration successful. Please check your email for a verification OTP."
        )
        return json(response.model_dump(), status=201)
