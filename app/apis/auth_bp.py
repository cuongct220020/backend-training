from sanic import Blueprint
from app.views.auth.auth_view import RegisterView, LoginView

auth_bp = Blueprint("auth", url_prefix="/auth")

# Route to the class-based views
auth_bp.add_route(RegisterView.as_view(), "/register")
auth_bp.add_route(LoginView.as_view(), "/login")