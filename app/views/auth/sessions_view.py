# app/views/auth/sessions_view.py
from sanic.request import Request
from sanic.views import HTTPMethodView

# Quản lý phiên đăng nhập
# Áp dụng khi:

2# - Bạn lưu session trong DB hoặc Redis kèm thông tin thiết bị/IP
class SessionsView(HTTPMethodView):
    # Liệt kê tất cả các phiên hiện tại của user
    # GET /auth/sessions
    async def get(self, request: Request):
        pass

    # Thu hồi một phiên cụ thể
    # DELETE /auth/sessions/:session_id
    async def delete(self, request: Request):
        pass

    # Thu hồi toàn bộ session của user
    # POST /auth/sessions/revoke-all
    async def post(self, request: Request):
        pass
