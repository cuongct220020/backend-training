# app/decorators/auth.py
from functools import wraps
from typing import Callable, Sequence

from sanic.request import Request

from app.exceptions import Unauthorized, Forbidden


def protected(roles: Sequence[str] | None = None):
    """
    A decorator to protect endpoints, with optional role-based access control.

    Usage:
        @protected() - Requires a valid login.
        @protected(roles=["admin"]) - Requires login and the 'admin' role.
        @protected(roles=["admin", "lecturer"]) - Requires login and either 'admin' or 'lecturer' role.
    """
    def decorator(f: Callable):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            # 1. Check for a valid login (user_id should be attached by middleware)
            is_authenticated = hasattr(request.ctx, "user_id") and request.ctx.user_id is not None
            if not is_authenticated:
                raise Unauthorized("Authentication required.")

            # 2. If roles are specified, check for role permission
            if roles:
                user_role = getattr(request.ctx, "role", None)
                if user_role not in roles:
                    raise Forbidden("You do not have permission to access this resource.")

            # If all checks pass, proceed to the original view function
            response = await f(request, *args, **kwargs)
            return response
        return decorated_function
    return decorator
