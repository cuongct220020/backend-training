# app/views/auth/refresh_view.py
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from app.decorators.validate_request import validate_request
from app.schemas.auth.refresh_schema import RefreshRequest
from app.services.auth_service import AuthService
from app.schemas.response_schema import GenericResponse
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository


class RefreshView(HTTPMethodView):

    @validate_request(RefreshRequest)
    async def post(self, request: Request):
        """
        Handles token refresh using a valid refresh token.
        Implements token rotation for enhanced security.
        """
        validated_data = request.ctx.validated_data

        # Instantiate required repositories with the request's DB session
        user_repo = UserRepository(session=request.ctx.db_session)
        refresh_token_repo = RefreshTokenRepository(session=request.ctx.db_session)

        new_token_dto = await AuthService.refresh_tokens(
            old_refresh_token=validated_data.refresh_token,
            refresh_token_repo=refresh_token_repo,
            user_repo=user_repo
        )

        response = GenericResponse(
            status="success",
            message="Tokens refreshed successfully",
            data=new_token_dto
        )
        return json(response.model_dump(by_alias=True), status=200)