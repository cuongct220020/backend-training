# app/apis/auth_bp.py
from sanic import Blueprint
from app.views.auth.login_view import LoginView
from app.views.auth.logout_view import LogoutView
from app.views.auth.refresh_view import RefreshView
from app.views.auth.sessions_view import SessionsView
from app.views.auth.otp_view import OTPView
from app.views.auth.change_password_view import ChangePasswordView
from app.views.auth.unlock_view import UnlockView

auth_bp = Blueprint('auth_blueprint', url_prefix='/auth')

auth_bp.add_route(LoginView.as_view(), '/login')
auth_bp.add_route(LogoutView.as_view(), '/logout')
auth_bp.add_route(RefreshView.as_view(), '/refresh')
# auth_bp.add_route(VerifyToken.as_view(), '/verify')
# auth_bp.add_route(RevokeToken.as_view(), '/token')
auth_bp.add_route(SessionsView.as_view(), '/sessions')
auth_bp.add_route(OTPView.as_view(), '/otp')
auth_bp.add_route(ChangePasswordView.as_view(), '/change-password')
auth_bp.add_route(UnlockView.as_view(), '/unlock')