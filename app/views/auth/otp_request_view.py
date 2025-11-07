# app/views/auth/otp_request_view.py
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from app.decorators.validate_request import validate_request
from app.decorators.rate_limit_by_email import rate_limit_by_email
from app.repositories.user_repository import UserRepository
from app.schemas.auth.otp_schema import OTPRequest
from app.services.auth_service import AuthService
from app.schemas.response_schema import GenericResponse


class OTPRequestView(HTTPMethodView):
    """View to handle the request for a new OTP."""

    # Decorators are applied from bottom up.
    # 1. @validate_request runs first to validate email and action.
    # 2. @rate_limit_by_email runs second to prevent spam.
    @rate_limit_by_email(limit=3, period=300)  # 3 requests per 5 minutes per email
    @validate_request(OTPRequest)
    async def post(self, request: Request):
        """Handles the logic to request and send an OTP."""
        otp_data = request.ctx.validated_data

        # Instantiate required repositories
        user_repo = UserRepository(session=request.ctx.db_session)

        # Delegate all business logic to the service layer
        await AuthService.request_otp(
            otp_data=otp_data,
            user_repo=user_repo
        )

        # For security, always return a generic success message
        # regardless of whether the email exists or not.
        response = GenericResponse(message="If an account with that email exists, an OTP has been sent.")
        return json(response.model_dump(exclude_none=True), status=200)

# Note: The OTPVerifyView would be a separate class to handle the verification part.