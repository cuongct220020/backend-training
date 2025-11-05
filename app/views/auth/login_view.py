# app/views/auth/login_view.py
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from app.decorators.validate_request import validate_request
from app.decorators.rate_limit import limit_per_user
from app.repositories.user_repository import UserRepository
from app.schemas.auth.login_schema import LoginRequest
from app.services.auth_service import AuthService
from app.schemas.response_schema import GenericResponse


class LoginView(HTTPMethodView):

    # Decorators are applied from bottom up.
    # 1. @validate_request runs first to validate and attach data.
    # 2. @limit_per_user runs second, using the validated data.
    @limit_per_user(limit=5, period=300)  # 5 attempts per 5 minutes
    @validate_request(LoginRequest)
    async def post(self, request: Request):
        """Handle user login."""
        login_data = request.ctx.validated_data
        user_repo = UserRepository(session=request.ctx.db_session)

        # The view's responsibility is to call the service and format the response.
        # Exception handling is delegated to the global error handler.
        token_dto = await AuthService.login(user_repo, login_data)

        response = GenericResponse(
            status="success",
            message="Login successful",
            data=token_dto
        )

        # Use by_alias=True to respect camelCase aliases in the response
        return json(response.model_dump(by_alias=True), status=200)