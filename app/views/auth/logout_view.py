# app/views/auth/logout_view.py
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from app.services.auth_service import AuthService
from app.schemas.response_schema import GenericResponse


class LogoutView(HTTPMethodView):
    # This endpoint is protected by the global auth middleware,
    # which ensures request.ctx.user_id, .jti and .exp exist on a valid token.
    async def post(self, request: Request):
        """Handle user logout by revoking the current access token and session."""

        user_id = request.ctx.user_id
        jti = request.ctx.jti
        exp = request.ctx.exp

        await AuthService.logout(user_id=user_id, jti=jti, exp=exp)

        response = GenericResponse(message="Logout successful")
        return json(response.model_dump(exclude_none=True), status=200)
