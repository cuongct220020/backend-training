# app/views/auth/change_password_view.py
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from app.decorators.validate_request import validate_request
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.schemas.auth.change_password_schema import ChangePasswordRequest
from app.services.user_service import UserService
from app.schemas.response_schema import GenericResponse


class ChangePasswordView(HTTPMethodView):
    """View for an authenticated user to change their password."""

    # The global `auth` middleware already protects this endpoint.
    @validate_request(ChangePasswordRequest)
    async def post(self, request: Request):
        """Handles the password change logic."""
        user_id = request.ctx.user_id
        validated_data = request.ctx.validated_data

        # Instantiate repositories and services
        user_repo = UserRepository(request.ctx.db_session)
        refresh_token_repo = RefreshTokenRepository(request.ctx.db_session)
        user_service = UserService(user_repo)

        # Delegate logic to the service layer
        await user_service.change_password(
            user_id=user_id,
            old_password=validated_data.old_password.get_secret_value(),
            new_password=validated_data.new_password.get_secret_value(),
            refresh_token_repo=refresh_token_repo
        )

        response = GenericResponse(message="Your password has been changed successfully.")
        return json(response.model_dump(exclude_none=True), status=200)