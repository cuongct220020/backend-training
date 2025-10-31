from functools import wraps

from app.hooks import exceptions
from app.utils.security_utils import verify_jwt


def check_token(jwt_secret, token):
    if not token:
        raise exceptions.Unauthorized('Require JWT')

    info = verify_jwt(jwt_secret, token)
    if not info or not info.get('address'):
        raise exceptions.Unauthorized('Invalid JWT')

    return info


def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            info = check_token(
                jwt_secret=request.app.config.JWT_SECRET,
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