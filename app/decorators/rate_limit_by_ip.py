# app/decorators/rate_limit_by_ip.py
from functools import wraps
from sanic.request import Request

from app.databases.redis_manager import redis_manager
from app.exceptions import TooManyRequests

def rate_limit_by_ip(limit: int, period: int):
    """
    A decorator to rate-limit requests based on the client's IP address.
    This is useful for public, unauthenticated endpoints like registration
    to prevent abuse.
    """
    def decorator(func):
        @wraps(func)
        async def decorated_function(view, request: Request, *args, **kwargs):
            key = f"rate_limit:ip:{request.ip}"

            # Check the current attempt count
            current_attempts = await redis_manager.client.get(key)

            if current_attempts and int(current_attempts) >= limit:
                ttl = await redis_manager.client.ttl(key)
                retry_after = ttl if ttl > 0 else period
                raise TooManyRequests(
                    message=f"Too many requests from this IP. Please try again in {retry_after} seconds.",
                    retry_after=retry_after
                )

            # On successful request (2xx), increment the counter
            # We increment before calling the function to be more strict
            pipe = redis_manager.client.pipeline()
            pipe.incr(key)
            if not current_attempts:
                pipe.expire(key, period)
            await pipe.execute()

            return await func(view, request, *args, **kwargs)
        return decorated_function
    return decorator
