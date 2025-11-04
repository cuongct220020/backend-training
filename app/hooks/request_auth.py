# app/middlewares/auth_middleware.py

from sanic import Request
from app.utils.security_utils import verify_jwt
from app.hooks import exceptions
from config import Config


# --- Middleware entry point ---
async def auth(request: Request):
    """
    Middleware to authenticate requests using JWT and attach user info to request.ctx.
    Runs before view handlers.
    """
    if not _is_auth_required(request):
        return  # Skip for public endpoints

    # Extract "Authorization: Bearer <token>"
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise exceptions.Unauthorized("Missing or invalid Authorization header")

    token = auth_header.split(" ")[1]
    payload = await _verify_and_decode_token(token)

    # Attach claims to request context for later access in views
    request.ctx.user_id = payload.get("sub")
    request.ctx.role = payload.get("role")
    request.ctx.jti = payload.get("jti")
    request.ctx.exp = payload.get("exp")


# --- Internal helpers ---

async def _verify_and_decode_token(token: str):
    """
    Verify JWT signature, expiration, and optional denylist checks.
    """
    if not token:
        raise exceptions.Unauthorized("JWT token required")

    payload = await verify_jwt(
        token=token,
        jwt_secret=Config.JWT_SECRET,
        jwt_algorithm=Config.JWT_ALGORITHM
    )

    if not payload or "sub" not in payload:
        raise exceptions.Unauthorized("Invalid JWT payload")

    return payload


def _is_auth_required(request: Request) -> bool:
    """
    Determine if the current request should be authenticated.
    """
    ignore_methods = {"OPTIONS"}
    ignore_paths = {
        "/",
        "/favicon.ico",
        "/api/v1/auth/login",
        "/api/v1/auth/register"
    }
    ignore_prefixes = ["/docs/"]

    # Skip OPTIONS and docs
    if request.method in ignore_methods:
        return False

    for prefix in ignore_prefixes:
        if request.path.startswith(prefix):
            return False

    if request.path in ignore_paths:
        return False

    return True