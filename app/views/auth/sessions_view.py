# app/views/auth/sessions_view.py
from sanic.request import Request
from sanic.response import json, text
from sanic.views import HTTPMethodView
from sanic_ext import openapi
from sanic_ext.extensions.openapi.types import Schema

from app.decorators.auth import protected
from app.exceptions import Forbidden, NotFound
from app.repositories.user_session_repository import UserSessionRepository
from app.schemas.auth.sessions_schema import SessionResponse
from app.schemas.response_schema import GenericResponse, PaginationResponse


class SessionsView(HTTPMethodView):
    decorators = [protected]

    @openapi.definition(
        summary="List all active sessions for the current user.",
        description="Retrieves a paginated list of all devices and locations the user is currently logged into.",
        response=Schema(PaginationResponse[SessionResponse]),
        tag="Auth"
    )
    async def get(self, request: Request):
        """Lists all current sessions for the authenticated user."""
        user_id = request.ctx.user_id
        session_repo = UserSessionRepository(request.ctx.db_session)

        # You can get pagination params from request.args
        try:
            page = int(request.args.get("page", 1))
            page_size = int(request.args.get("page_size", 10))
        except (ValueError, TypeError):
            page = 1
            page_size = 10

        paginated_result = await session_repo.list_sessions_for_user(
            user_id=user_id,
            page=page,
            page_size=page_size
        )

        response = PaginationResponse(
            status="success",
            message="Successfully retrieved sessions.",
            data=paginated_result
        )
        return json(response.model_dump(by_alias=True), status=200)

    @openapi.definition(
        summary="Revoke a specific session.",
        description="Logs the user out of a specific device or session by its ID.",
        response=Schema(GenericResponse),
        tag="Auth"
    )
    async def delete(self, request: Request, session_id: int):
        """Revokes a specific session by its ID."""
        user_id = request.ctx.user_id
        session_repo = UserSessionRepository(request.ctx.db_session)

        # The repository method includes a user_id check for security
        success = await session_repo.revoke_session_by_id(session_id=session_id, user_id=user_id)

        if not success:
            raise NotFound("Session not found or you do not have permission to revoke it.")

        response = GenericResponse(status="success", message="Session successfully revoked.")
        return json(response.model_dump(), status=200)


class RevokeAllSessionsView(HTTPMethodView):
    decorators = [protected]

    @openapi.definition(
        summary="Revoke all active sessions.",
        description='Logs the user out from all devices. The current session can be optionally preserved by providing its refresh token JTI.',
        response=Schema(GenericResponse),
        tag="Auth"
    )
    async def post(self, request: Request):
        """Revokes all of the user's sessions, effectively logging them out everywhere."""
        user_id = request.ctx.user_id
        session_repo = UserSessionRepository(request.ctx.db_session)

        # Optional: allow excluding the current session from revocation
        # For this, the client would need to send the JTI of its refresh token.
        body = request.json or {}
        except_jti = body.get("except_current_jti")

        revoked_count = await session_repo.revoke_all_for_user(user_id=user_id, except_jti=except_jti)

        response = GenericResponse(
            status="success",
            message=f"{revoked_count} session(s) have been revoked."
        )
        return json(response.model_dump(), status=200)
