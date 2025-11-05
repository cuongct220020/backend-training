# app/decorators/rate_limit_per_user.py
from functools import wraps
from sanic.request import Request
from sanic.response import json

from app.databases.redis_manager import redis_manager
from app.schemas.response_schema import GenericResponse
from app.exceptions import TooManyRequests  # Import the custom exception


def rate_limit_per_user(limit: int, period: int):
    """
    A decorator to rate-limit requests based on username and IP address.
    Only increments the counter on failed login attempts (401/403 status codes).
    Resets the counter on successful login (200 status code).

    Args:
        limit (int): The number of allowed attempts.
        period (int): The time window in seconds.
    """
    def decorator(func):
        @wraps(func)
        async def decorated_function(view, request: Request, *args, **kwargs):
            # This decorator must run after @validate_request to access validated_data
            if not hasattr(request.ctx, 'validated_data') or not hasattr(request.ctx.validated_data, 'username'):
                # Fallback or raise error if the decorator order is wrong
                error_response = GenericResponse(
                    status="error",
                    message="Internal server error: Rate limiter is missing request context.",
                    data=None
                )
                return json(error_response.model_dump(exclude_none=True), status=500)

            # Key composed of username and IP for more targeted rate limiting
            username = request.ctx.validated_data.username
            ip_address = request.ip

            # Construct a unique key for the user and IP
            key = f"rate_limit:login_fail:{username}:{ip_address}"

            # Check the current attempt count and TTL in one pipeline
            redis_pipe = redis_manager.client.pipeline()
            redis_pipe.get(key)
            redis_pipe.ttl(key)
            current_attempts, ttl = await redis_pipe.execute()

            if current_attempts and int(current_attempts) >= limit:
                retry_after = ttl if ttl is not None and ttl > 0 else period
                # Raise an exception instead of returning a direct response
                raise TooManyRequests(
                    message=f"Too many failed login attempts. Please try again in {retry_after} seconds.",
                    retry_after=retry_after
                )

            # Proceed to call the actual view function (e.g., login)
            response = await func(view, request, *args, **kwargs)

            # Post-request logic based on the outcome of the login attempt
            if 200 <= response.status < 300:
                # On successful login, reset the counter
                await redis_manager.client.delete(key)
            elif response.status in [401, 403]:
                # On failed login, increment the counter and set/update the expiry
                pipe = redis_manager.client.pipeline()
                pipe.incr(key)
                # Set expiry only on the first attempt in a new window
                if not current_attempts:
                    pipe.expire(key, period)
                await pipe.execute()

            return response
        return decorated_function
    return decorator
