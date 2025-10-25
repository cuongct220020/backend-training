from sanic.exceptions import SanicException
from sanic.request import Request
from sanic.response import text


async def sanic_exception_handler(request: Request, e: SanicException):
    return text(None, e.status_code)


async def broad_exception_handler(request: Request, e: Exception):
    return text(None, 500)
