# app/views/auth/register_view.py
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from app.decorators.validate_request import validate_request
from app.decorators.rate_limit_by_ip import rate_limit_by_ip
from app.repositories.user_repository import UserRepository
from app.repositories.otp_repository import OTPRepository
from app.schemas.auth.register_schema import RegisterRequest
from app.services.auth_service import AuthService
from app.schemas.response_schema import GenericResponse


class RegisterView(HTTPMethodView):
    """View to handle new user registration."""

    # Protect this public endpoint from abuse.
    @rate_limit_by_ip(limit=10, period=3600)  # 10 registration attempts per hour from one IP
    @validate_request(RegisterRequest)
    async def post(self, request: Request):
        """Handles the first step of registration: creating an inactive user and sending a verification OTP."""
        reg_data = request.ctx.validated_data

        # Instantiate required repositories
        user_repo = UserRepository(session=request.ctx.db_session)
        otp_repo = OTPRepository(session=request.ctx.db_session)

        # Delegate all logic to the service layer
        await AuthService.register_user(
            reg_data=reg_data,
            user_repo=user_repo,
            otp_repo=otp_repo
        )

        # For security, always return a generic success message
        response = GenericResponse(message="Registration successful. Please check your email to verify your account.")
        return json(response.model_dump(exclude_none=True), status=201) # 201 Created
