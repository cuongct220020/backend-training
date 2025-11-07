# app/views/auth/login_view.py
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from app.decorators.validate_request import validate_request
from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository
from app.schemas.access_token_schema import AccessTokenResponse
from app.schemas.auth.login_schema import LoginRequest
from app.services.auth_service import AuthService
from app.schemas.response_schema import GenericResponse
from app.schemas.auth.token_schema import TokenData


class LoginView(HTTPMethodView):
    decorators = [validate_request(LoginRequest)]

    async def post(self, request: Request):
        """Handles user login and token generation."""
        validated_data = request.ctx.validated_data
        config = request.app.config

        # Instantiate required repositories with the request's DB session
        user_repo = UserRepository(session=request.ctx.db_session)
        session_repo = UserSessionRepository(session=request.ctx.db_session)

        # Get request metadata
        ip_address = request.ip
        user_agent = request.headers.get("User-Agent")

        token_dto: TokenData = await AuthService.login(
            login_data=validated_data,
            user_repo=user_repo,
            session_repo=session_repo,
            ip_address=ip_address,
            user_agent=user_agent
        )

        # 1. Chuẩn bị dữ liệu JSON chỉ chứa access token
        access_token_data = AccessTokenResponse(
            access_token=token_dto.access_token,
            token_type=token_dto.token_type,
            expires_in_minutes=token_dto.expires_in_minutes,
        )

        response_data = GenericResponse(
            status="success",
            message="Login successful",
            data=access_token_data
        )
        response = json(response_data.model_dump(by_alias=True), status=200)

        # 2. Đặt refresh token vào một HttpOnly cookie
        refresh_expires_days = int(config.get("REFRESH_TOKEN_EXPIRE_DAYS", 7))
        max_age = refresh_expires_days * 24 * 60 * 60  # Tính bằng giây

        response.set_cookie(
            "refresh_token",
            token_dto.refresh_token,
            max_age=max_age,
            httponly=True,
            secure=not config.get("DEBUG", False),  # Chỉ gửi qua HTTPS khi không ở chế độ DEBUG
            samesite="Strict"  # Ngăn chặn CSRF
        )

        return response