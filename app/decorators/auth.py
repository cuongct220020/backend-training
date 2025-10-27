from functools import wraps

from sanic import Unauthorized, Forbidden

from app.services.auth_service import decode_jwt


def check_token(secret_key, token):
    if not token:
        raise Unauthorized('Require JWT')

    info = decode_jwt(token, secret_key)
    if not info or not info.get('address'):
        raise Unauthorized('Invalid JWT')

    return info


def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            info = check_token(
                secret_key=request.app.config.SECRET,
                token=request.headers.get('Authorization')
            )

            address = info['address']
            role = info.get('role', 'user')

            request.headers['address'] = address

            resource_owner = kwargs.get('address')
            if resource_owner and (role != 'admin') and (resource_owner.lower() != address):
                raise Forbidden('Permission denied')

            response = await f(request, *args, **kwargs)
            return response

        return decorated_function

    return decorator(wrapped)