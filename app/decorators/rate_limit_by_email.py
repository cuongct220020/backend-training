# app/decorators/rate_limit_by_email.py
from functools import wraps
from sanic.request import Request

from app.databases.redis_manager import redis_manager
from app.exceptions import TooManyRequests

def rate_limit_by_email(limit: int, period: int):
    """
    A decorator to rate-limit requests based on the email in the validated data.
    This is crucial for endpoints like OTP request to prevent spamming.
    """
    def decorator(func):
        @wraps(func)
        async def decorated_function(view, request: Request, *args, **kwargs):
            # This decorator must run after @validate_request
            if not hasattr(request.ctx, 'validated_data') or not hasattr(request.ctx.validated_data, 'email'):
                # This should ideally not happen if decorators are ordered correctly
                raise TooManyRequests("Rate limit context is missing.")

            email = request.ctx.validated_data.email
            key = f"rate_limit:otp_request:{email}"

            # Check the current attempt count
            current_attempts = await redis_manager.client.get(key)

            if current_attempts and int(current_attempts) >= limit:
                ttl = await redis_manager.client.ttl(key)
                retry_after = ttl if ttl > 0 else period
                raise TooManyRequests(
                    message=f"Too many OTP requests. Please try again in {retry_after} seconds.",
                    retry_after=retry_after
                )

            # Proceed to call the actual view function
            response = await func(view, request, *args, **kwargs)

            # On successful request (2xx), increment the counter
            if 200 <= response.status < 300:
                pipe = redis_manager.client.pipeline()
                # Atomically increment the counter
                pipe.incr(key)
                # Set expiry only on the first request in a new window
                if not current_attempts:
                    pipe.expire(key, period)
                await pipe.execute()

            return response
        return decorated_function
    return decorator
