# app/apis/auth_bp.py
from sanic import Blueprint
from app.views.auth_view import RegisterView, LoginView, LogoutView

auth_bp = Blueprint('auth_blueprint', url_prefix='/auth')

auth_bp.add_route(RegisterView.as_view(), '/register')
auth_bp.add_route(LoginView.as_view(), '/login')
auth_bp.add_route(LogoutView.as_view(), '/logout')