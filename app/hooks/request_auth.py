# app/hooks/request_auth.py

from sanic import Request
from app.utils.jwt_utils import jwt_handler
from app.exceptions import Unauthorized


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
        raise Unauthorized("Missing or invalid Authorization header")

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
    Ensures the token is an 'access' token.
    """
    if not token:
        raise Unauthorized("JWT token required")

    # Explicitly verify that this is an access token
    payload = await jwt_handler.verify(token=token, token_type="access")

    if not payload or "sub" not in payload:
        raise Unauthorized("Invalid JWT payload")

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