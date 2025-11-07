# app/apis/auth_bp.py
from sanic import Blueprint

# --- Import tất cả các Views cho blueprint này ---
from app.views.auth.register_view import RegisterView
from app.views.auth.login_view import LoginView
from app.views.auth.logout_view import LogoutView
from app.views.auth.refresh_view import RefreshView
from app.views.users.change_password_view import ChangePasswordView
from app.views.auth.reset_password_view import ResetPasswordView
from app.views.auth.otp_request_view import OTPRequestView
from app.views.auth.otp_verify_view import OTPVerifyView
from app.views.auth.sessions_view import SessionsView
# from app.views.auth.unlock_view import UnlockView

# --- Khởi tạo Blueprint ---
# Toàn bộ các đường dẫn này sẽ có tiền tố là /api/v1/auth
auth_bp = Blueprint('auth_blueprint', url_prefix='/auth')

# --- Đăng ký các đường dẫn (Routes) ---

# === 1. Đăng ký & Đăng nhập ===
# POST /api/v1/auth/register
auth_bp.add_route(RegisterView.as_view(), '/register')

# POST /api/v1/auth/login
auth_bp.add_route(LoginView.as_view(), '/login')

# === 2. Quản lý Token & Phiên (Session) ===
# POST /api/v1/auth/logout (Protected: Yêu cầu Access Token)
auth_bp.add_route(LogoutView.as_view(), '/logout')

# POST /api/v1/auth/refresh (Public: Yêu cầu Refresh Token)
auth_bp.add_route(RefreshView.as_view(), '/refresh')

# GET /api/v1/auth/sessions (Protected: Lấy danh sách thiết bị)
# DELETE /api/v1/auth/sessions/<session_id> (Protected: Xóa 1 thiết bị)
auth_bp.add_route(SessionsView.as_view(), '/sessions')
auth_bp.add_route(SessionsView.as_view(), '/sessions/<session_id:int>')


# === 3. Quản lý Mật khẩu ===
# POST /api/v1/auth/password/change (Protected: Đổi mật khẩu khi đã đăng nhập)
auth_bp.add_route(ChangePasswordView.as_view(), '/password/change')

# POST /api/v1/auth/password/reset (Public: Đặt lại mật khẩu khi bị quên)
auth_bp.add_route(ResetPasswordView.as_view(), '/password/reset')


# === 4. Quy trình OTP & Mở khóa Tài khoản ===
# POST /api/v1/auth/otp/request (Public: Gửi yêu cầu OTP cho 'register' hoặc 'reset_password')
auth_bp.add_route(OTPRequestView.as_view(), '/otp/request')

# POST /api/v1/auth/otp/verify (Public: Xác thực OTP cho 'register')
auth_bp.add_route(OTPVerifyView.as_view(), '/otp/verify')

# # POST /api/v1/auth/account/unlock (Public: Mở khóa tài khoản bằng OTP)
# auth_bp.add_route(UnlockView.as_view(), '/account/unlock')