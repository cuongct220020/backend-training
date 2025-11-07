# app/apis/user_bp.py
from sanic import Blueprint

from app.views.users.change_password_view import ChangePasswordView
from app.views.users.me_view import MeView

user_bp = Blueprint('user_blueprint', url_prefix='/users')

user_bp.add_route(ChangePasswordView.as_view(), '/change-password')
user_bp.add_route(MeView.as_view(), '/me')