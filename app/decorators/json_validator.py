from functools import wraps

from jsonschema import ValidationError, validate
from sanic.request import Request
from sanic.response import text


def validate_with_jsonschema(jsonschema: dict):
    def decorator(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            for arg in args:
                if isinstance(arg, Request):
                    request: Request = arg

                    try:
                        validate(request.json, jsonschema)
                    except ValidationError:
                        return text(None, 400)

            return await fn(*args, **kwargs)
        return wrapper
    return decorator
