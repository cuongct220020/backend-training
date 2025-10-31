from sanic import Request

from app.hooks import exceptions
from app.utils.security_utils import verify_jwt

async def auth(request: Request):
    """Middleware to authenticate requests and attach user info to the context."""
    if not check_required_authenticate(request=request):
        return

    token = request.headers.get('Authorization')
    payload = check_token(token=token)

    # Attach user information to the request context for easy access in views
    request.ctx.user_id = payload.get('sub')
    request.ctx.role = payload.get('role')

def check_token(token: str):
    if not token:
        raise exceptions.Unauthorized('Require JWT')

    info = verify_jwt(token)
    # A valid token must contain the subject claim
    if not info or 'sub' not in info:
        raise exceptions.Unauthorized('Invalid JWT')

    return info

def check_required_authenticate(request: Request):
    ignore_methods = ['OPTIONS']
    ignore_paths = ['/', '/docs', '/register', '/favicon.ico']
    ignore_paths_prefix = ['/docs/']

    if request.method in ignore_methods:
        return False

    for ignore_path_prefix in ignore_paths_prefix:
        if request.path.startswith(ignore_path_prefix):
            return False

    if request.path in ignore_paths:
        return False

    return True