# app/views/auth/otp_verify_view.py
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from app.decorators.validate_request import validate_request
from app.repositories.user_repository import UserRepository
from app.schemas.auth.otp_schema import OTPVerifyRequest
from app.services.auth_service import AuthService
from app.schemas.response_schema import GenericResponse


class OTPVerifyView(HTTPMethodView):

    @validate_request(OTPVerifyRequest)
    async def post(self, request: Request):
        """Handles the verification of registration OTPs."""
        validated_data = request.ctx.validated_data

        user_repo = UserRepository(session=request.ctx.db_session)

        await AuthService.verify_registration_otp(
            data=validated_data,
            user_repo=user_repo
        )

        response = GenericResponse(
            status="success",
            message="Account activated successfully."
        )
        return json(response.model_dump(), status=200)
