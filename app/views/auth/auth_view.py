from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from app.decorators.validation import validate_request
from app.hooks import exceptions
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import LoginSchema
from app.schemas.user_schema import UserCreate
from app.services.auth_service import register_user, login_user


class RegisterView(HTTPMethodView):
    decorators = [validate_request(UserCreate)]

    async def post(self, request: Request):
        """Handle user registration."""
        user_create_data = request.ctx.validated_data
        user_repo = UserRepository(session=request.ctx.db_session)

        try:
            # Service now returns a UserRead DTO on success
            new_user_dto = await register_user(user_repo, user_create_data)
            return json(new_user_dto.model_dump(), status=201)
        except exceptions.Conflict as e:
            # Catch specific business logic exceptions from the service
            return json({"error": str(e)}, status=e.status_code)


class LoginView(HTTPMethodView):
    decorators = [validate_request(LoginSchema)]

    async def post(self, request: Request):
        """Handle user login."""
        login_data = request.ctx.validated_data
        user_repo = UserRepository(session=request.ctx.db_session)

        try:
            # Service now returns a Token DTO on success
            token_dto = await login_user(user_repo, login_data)
            return json(token_dto.model_dump(), status=200)
        except exceptions.Unauthorized as e:
            # Catch specific business logic exceptions from the service
            return json({"error": str(e)}, status=e.status_code)
