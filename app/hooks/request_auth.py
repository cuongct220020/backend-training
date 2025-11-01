# app/hooks/request_auth.py
from sanic import Request

from app.hooks import exceptions
from app.utils.security_utils import verify_jwt
from config import Config


async def check_token(token: str):
    """Helper function to verify a token and check its claims."""
    if not token:
        raise exceptions.Unauthorized('Require JWT')

    # The verify_jwt function now handles all validation, including deny-list
    info = await verify_jwt(
        token=token,
        jwt_secret=Config.JWT_SECRET,
        jwt_algorithm=Config.JWT_ALGORITHM
    )

    # A valid token must contain the subject claim
    if not info or 'sub' not in info:
        raise exceptions.Unauthorized('Invalid JWT')

    return info


async def auth(request: Request):
    """Middleware to authenticate requests and attach user info to the context."""
    if not check_required_authenticate(request=request):
        return

    # Extract token from "Bearer <token>"
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        raise exceptions.Unauthorized("Invalid or missing Authorization header")
    
    token = auth_header.split(" ")[1]
    
    payload = await check_token(token=token)

    # Attach user information to the request context for easy access in views
    request.ctx.user_id = payload.get('sub')
    request.ctx.role = payload.get('role')
    request.ctx.jti = payload.get('jti') # Also store jti for logout
    request.ctx.exp = payload.get('exp') # And exp


def check_required_authenticate(request: Request):
    ignore_methods = ['OPTIONS']
    ignore_paths = ['/', '/docs', '/api/v1/auth/login', '/api/v1/auth/register', '/favicon.ico']
    ignore_paths_prefix = ['/docs/']

    if request.method in ignore_methods:
        return False

    for ignore_path_prefix in ignore_paths_prefix:
        if request.path.startswith(ignore_path_prefix):
            return False

    if request.path in ignore_paths:
        return False

    return True
