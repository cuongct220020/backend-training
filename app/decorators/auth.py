from functools import wraps

from app.hooks import exceptions
from app.utils.security_utils import verify_jwt


def check_token(token: str):
    if not token:
        raise exceptions.Unauthorized('Require JWT')

    info = verify_jwt(token)
    # A valid token must contain the subject claim
    if not info or 'sub' not in info:
        raise exceptions.Unauthorized('Invalid JWT')

    return info


def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            info = check_token(
                token=request.headers.get('Authorization')
            )

            address = info['address']
            role = info.get('role', 'user')

            request.headers['address'] = address

            resource_owner = kwargs.get('address')
            if resource_owner and (role != 'admin') and (resource_owner.lower() != address):
                raise exceptions.Forbidden('Permission denied')

            response = await f(request, *args, **kwargs)
            return response

        return decorated_function

    return decorator(wrapped)