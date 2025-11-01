# app/hooks/request_context.py
from sanic.request import Request
from sanic.response import BaseHTTPResponse


async def after_request(_: Request, response: BaseHTTPResponse) -> None:
    try:
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'deny'
    finally:
        ...