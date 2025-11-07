# app/views/auth/logout_view.py
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from app.decorators.auth import protected
from app.repositories.user_session_repository import UserSessionRepository
from app.services.auth_service import AuthService
from app.schemas.response_schema import GenericResponse
# Không cần LogoutRequest hay validate_request nữa

class LogoutView(HTTPMethodView):
    decorators = [protected]  # Chỉ cần xác thực access token

    async def post(self, request: Request):
        """Handles user logout by revoking access token and clearing refresh token cookie."""
        # 1. Lấy thông tin access token (đã được middleware @protected xác thực)
        access_jti = request.ctx.jti
        access_exp = request.ctx.exp

        # 2. Lấy refresh token từ cookie
        refresh_token = request.cookies.get("refresh_token")

        session_repo = UserSessionRepository(request.ctx.db_session)

        # 3. Gọi AuthService.logout
        # Service sẽ vô hiệu hóa access_jti
        # và vô hiệu hóa refresh_token (nếu nó tồn tại)
        await AuthService.logout(
            session_repo=session_repo,
            access_jti=access_jti,
            access_exp=access_exp,
            refresh_token=refresh_token  # Truyền token từ cookie
        )

        response_data = GenericResponse(status="success", message="Logout successful.")
        response = json(response_data.model_dump(), status=200)

        # 4. Xóa HttpOnly cookie khỏi trình duyệt
        response.delete_cookie("refresh_token")

        return response