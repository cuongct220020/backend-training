from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView
from pydantic import ValidationError

from app.services.auth_service import register_user, login_user
from app.schemas.auth_schema import LoginSchema, RegisterSchema


class RegisterView(HTTPMethodView):
    async def post(self, request: Request):
        """Handle user registration."""
        try:
            auth_data = RegisterSchema.model_validate(request.json)
        except ValidationError as e:
            return json({"error": e.errors()}, status=400)

        # Get session from request context and inject it into the service
        result = await register_user(
            db_session=request.ctx.db_session,
            username=auth_data.username,
            password=auth_data.password.get_secret_value(),
            role=auth_data.user_role.value
        )

        if "error" in result:
            return json(result, status=409)

        return json(result, status=201)


class LoginView(HTTPMethodView):
    async def post(self, request: Request):
        """Handle user login."""
        try:
            auth_data = LoginSchema.model_validate(request.json)
        except ValidationError as e:
            return json({"error": e.errors()}, status=400)

        # Get session from request context and inject it into the service
        result = await login_user(
            db_session=request.ctx.db_session,
            username=auth_data.username,
            password=auth_data.password.get_secret_value()
        )

        if "error" in result:
            return json(result, status=401)

        return json(result, status=200)
