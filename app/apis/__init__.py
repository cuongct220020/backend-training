from sanic import Blueprint

from app.apis.auth_bp import auth_bp
# from app.apis.subject_bp import subject_bp
# from app.apis.user_bp import user_bp

api = Blueprint.group(
    auth_bp
    # subject_bp,
    # user_bp,
)