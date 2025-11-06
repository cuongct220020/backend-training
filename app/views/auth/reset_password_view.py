# app/views/auth/reset_password_view.py
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from app.decorators.validate_request import validate_request
from app.decorators.rate_limit_by_email import rate_limit_by_email
from app.repositories.user_repository import UserRepository
from app.repositories.otp_repository import OTPRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.schemas.auth.reset_password_schema import ResetPasswordRequest
from app.services.auth_service import AuthService
from app.schemas.response_schema import GenericResponse


class ResetPasswordView(HTTPMethodView):
    """View to handle the password reset process using a valid OTP."""

    # Protect against OTP brute-force attacks
    @rate_limit_by_email(limit=5, period=300)  # 5 attempts per 5 minutes per email
    @validate_request(ResetPasswordRequest)
    async def post(self, request: Request):
        """Handles the logic to verify an OTP and set a new password."""
        validated_data = request.ctx.validated_data

        # Instantiate required repositories
        user_repo = UserRepository(session=request.ctx.db_session)
        otp_repo = OTPRepository(session=request.ctx.db_session)
        refresh_token_repo = RefreshTokenRepository(session=request.ctx.db_session)

        # Delegate all business logic to the service layer
        await AuthService.reset_password_with_otp(
            data=validated_data,
            user_repo=user_repo,
            otp_repo=otp_repo,
            refresh_token_repo=refresh_token_repo
        )

        response = GenericResponse(message="Your password has been reset successfully.")
        return json(response.model_dump(exclude_none=True), status=200)
