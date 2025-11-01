# app/apis/__init__.py
from sanic import Blueprint

from .auth_bp import auth_bp
from .user_bp import user_bp

# Group all blueprints under a single API object
api = Blueprint.group(auth_bp, user_bp)