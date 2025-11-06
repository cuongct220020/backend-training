# app/apis/user_bp.py
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json

from app.repositories.user_repository import UserRepository
from app.schemas.auth.change_password_schema import ChangePasswordRequest
from app.services.user_service import UserService


user_bp = Blueprint('user_blueprint', url_prefix='/users')

user_bp.add_route(ChangePasswordRequest.as_view(), '/change-password')
# user_bp.add_route(RegisterView.as_view(), '/register')