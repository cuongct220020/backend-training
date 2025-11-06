# app/views/auth/otp_verify_view.py
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from app.decorators.validate_request import validate_request
from app.decorators.rate_limit_by_email import rate_limit_by_email
from app.repositories.user_repository import UserRepository
from app.repositories.otp_repository import OTPRepository
from app.schemas.auth.otp_schema import OTPVerifyRequest
from app.services.auth_service import AuthService
from app.schemas.response_schema import GenericResponse


class OTPVerifyView(HTTPMethodView):
    """View to handle the verification of an OTP (e.g., for account activation)."""

    @rate_limit_by_email(limit=5, period=600)  # 5 attempts per 10 minutes per email
    @validate_request(OTPVerifyRequest)
    async def post(self, request: Request):
        """Handles the logic to verify an OTP and activate the user."""
        validated_data = request.ctx.validated_data

        user_repo = UserRepository(session=request.ctx.db_session)
        otp_repo = OTPRepository(session=request.ctx.db_session)

        await AuthService.verify_registration_otp(
            data=validated_data,
            user_repo=user_repo,
            otp_repo=otp_repo
        )

        response = GenericResponse(message="Your account has been successfully verified and activated.")
        return json(response.model_dump(exclude_none=True), status=200)
