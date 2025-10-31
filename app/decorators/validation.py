# app/decorators/validation.py
from functools import wraps
from typing import Type

from pydantic import BaseModel, ValidationError
from sanic.request import Request
from sanic.response import json


def validate_request(schema: Type[BaseModel]):
    """
    A decorator that automatically validates the request body against a Pydantic schema.

    On success, it attaches the validated data to `request.ctx.validated_data`.
    On failure, it returns a 400 Bad Request with validation error details.
    """
    def decorator(f):
        @wraps(f)
        async def decorated_function(view, request: Request, *args, **kwargs):
            try:
                validated_data = schema.model_validate(request.json)
                request.ctx.validated_data = validated_data
            except ValidationError as e:
                return json({"error": e.errors()}, status=400)

            return await f(view, request, *args, **kwargs)
        return decorated_function
    return decorator
