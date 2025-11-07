# app/views/auth/refresh_view.py
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from app.exceptions import Unauthorized
from app.services.auth_service import AuthService
from app.schemas.response_schema import GenericResponse
from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository
from app.schemas.auth.token_schema import TokenData


class RefreshView(HTTPMethodView):
    # Không cần @validate_request vì chúng ta không đọc body
    async def post(self, request: Request):
        """
        Handles token refresh using a valid refresh token from an HttpOnly cookie.
        Implements token rotation for enhanced security.
        """
        # 1. Đọc refresh token từ cookie
        old_refresh_token = request.cookies.get("refresh_token")
        if not old_refresh_token:
            raise Unauthorized("Missing refresh token cookie.")

        config = request.app.config

        # Instantiate required repositories
        user_repo = UserRepository(session=request.ctx.db_session)
        session_repo = UserSessionRepository(session=request.ctx.db_session)

        # Get request metadata
        ip_address = request.ip
        user_agent = request.headers.get("User-Agent")

        # 2. Gọi service với token từ cookie
        new_token_dto: TokenData = await AuthService.refresh_tokens(
            old_refresh_token=old_refresh_token,
            session_repo=session_repo,
            user_repo=user_repo,
            ip_address=ip_address,
            user_agent=user_agent
        )

        # 3. Chuẩn bị response chỉ chứa access token mới
        access_token_data = {
            "access_token": new_token_dto.access_token,
            "token_type": new_token_dto.token_type,
            "expires_in_minutes": new_token_dto.expires_in_minutes
        }
        response_data = GenericResponse(
            status="success",
            message="Tokens refreshed successfully",
            data=access_token_data
        )
        response = json(response_data.model_dump(by_alias=True), status=200)

        # 4. Đặt refresh token MỚI (đã được xoay vòng) vào cookie
        refresh_expires_days = int(config.get("REFRESH_TOKEN_EXPIRE_DAYS", 7))
        max_age = refresh_expires_days * 24 * 60 * 60

        response.set_cookie(
            "refresh_token",
            new_token_dto.refresh_token,
            max_age=max_age,
            httponly=True,
            secure=not config.get("DEBUG", False),
            samesite="Strict"
        )

        return response