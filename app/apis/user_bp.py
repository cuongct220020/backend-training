# app/apis/user_bp.py
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json

from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

user_bp = Blueprint('user_blueprint', url_prefix='/users')


@user_bp.get("/me")
async def get_current_user_profile(request: Request):
    """
    Endpoint to get the profile of the currently authenticated user.
    This endpoint is protected by the global auth middleware.
    """
    # The auth middleware has already placed user_id and role in the context
    current_user_id = request.ctx.user_id

    # Initialize repository and service
    user_repo = UserRepository(session=request.ctx.db_session)
    user_service = UserService(user_repo=user_repo)

    # Call the service function (this will be cached)
    user_profile = await user_service.get_user_by_id(user_id=current_user_id)

    if not user_profile:
        return json({"error": "User not found"}, status=404)

    # The service returns a Pydantic model, so we can dump it directly
    return json(user_profile.model_dump())