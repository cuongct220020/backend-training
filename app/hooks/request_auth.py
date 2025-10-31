from sanic import Request

from app.decorators.auth import check_token
from app.hooks import exceptions


async def auth(request: Request):
    if not check_required_authenticate(request=request):
        return

    info = check_token(
        jwt_secret=request.app.config.JWT_SECRET,
        token=request.headers.get('Authorization')
    )

    address = info['address']
    role = info.get('role', 'user')

    request.headers['address'] = address

    resource_owner = request.match_info.get('address')
    if resource_owner and (role != 'admin') and (resource_owner.lower() != address):
        raise exceptions.Forbidden('Permission denied')


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