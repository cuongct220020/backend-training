from urllib.request import Request

from sanic.views import HTTPMethodView

from app.schemas.users.user_schema import UserCreate
from app.services.user_service import register_user

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

class UserView(HTTPMethodView):
    async def get(self, request: Request):
        pass



