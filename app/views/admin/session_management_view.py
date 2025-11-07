# app/views/admin/session_management_view.py
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_ext import openapi
from sanic_ext.extensions.openapi.types import Schema

from app.decorators.auth import protected
from app.exceptions import NotFound
from app.repositories.user_session_repository import UserSessionRepository
from app.schemas.auth.sessions_schema import SessionResponse
from app.schemas.response_schema import GenericResponse, PaginationResponse


class AdminSessionManagementView(HTTPMethodView):
    # Protect all methods in this view, only allowing users with the 'admin' role.
    decorators = [protected(roles=["admin"])]

    @openapi.definition(
        summary="List all sessions for a specific user.",
        description="Allows an admin to retrieve a paginated list of all login sessions for any user.",
        response=Schema(PaginationResponse[SessionResponse]),
        tag="Admin"
    )
    async def get(self, request: Request, user_id: int):
        """Lists all sessions for a given user ID."""
        session_repo = UserSessionRepository(request.ctx.db_session)

        try:
            page = int(request.args.get("page", 1))
            page_size = int(request.args.get("page_size", 10))
        except (ValueError, TypeError):
            page = 1
            page_size = 10

        paginated_result = await session_repo.list_sessions_for_user(
            user_id=user_id,
            page=page,
            page_size=page_size,
            include_revoked=True  # Admins can see revoked sessions
        )

        response = PaginationResponse(
            status="success",
            message=f"Successfully retrieved sessions for user {user_id}.",
            data=paginated_result
        )
        return json(response.model_dump(by_alias=True), status=200)

    @openapi.definition(
        summary="Revoke a specific user session.",
        description="Allows an admin to revoke a specific login session for any user.",
        response=Schema(GenericResponse),
        tag="Admin"
    )
    async def delete(self, request: Request, user_id: int, session_id: int):
        """Revokes a specific session by its ID for a given user ID."""
        session_repo = UserSessionRepository(request.ctx.db_session)

        # In the admin context, we trust the admin and revoke directly.
        # The user_id from the URL is used for targeting, not for ownership check.
        session = await session_repo.get_by_id(session_id)
        if not session or session.user_id != user_id:
            raise NotFound(f"Session with ID {session_id} not found for user {user_id}.")

        if session.revoked:
            response = GenericResponse(status="success", message="Session was already revoked.")
            return json(response.model_dump(), status=200)

        session.revoked = True
        await session_repo.session.commit()

        response = GenericResponse(status="success", message=f"Session {session_id} for user {user_id} has been revoked.")
        return json(response.model_dump(), status=200)
