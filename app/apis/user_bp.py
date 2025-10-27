from sanic import Blueprint, response

# Blueprint for user-related APIs
user_bp = Blueprint("users", url_prefix="/users")
