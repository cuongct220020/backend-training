# app/hooks/error_handler.py
from sanic.response import json
from pydantic import ValidationError

from app.schemas.response_schema import GenericResponse
from app.exceptions import AppException, TooManyRequests
from app.utils.logger_utils import get_logger

logger = get_logger(__name__)

def register_error_handlers(app):
    """Registers custom error handlers for the Sanic application."""

    @app.exception(AppException)
    async def handle_app_exception(request, exc: AppException):
        """Handles known, intentional application exceptions (e.g., 4xx errors)."""
        headers = {}
        # If the exception is TooManyRequests, extract the retry_after value
        if isinstance(exc, TooManyRequests) and exc.retry_after:
            headers["Retry-After"] = str(exc.retry_after)

        response = GenericResponse(
            status="fail",
            message=str(exc)
        )
        return json(response.model_dump(exclude_none=True), status=exc.status_code, headers=headers)

    @app.exception(ValidationError)
    async def handle_validation_error(request, exc: ValidationError):
        """Handles Pydantic validation errors as a fallback."""
        response = GenericResponse(
            status="fail",
            message="Validation error",
            data=exc.errors()
        )
        return json(response.model_dump(exclude_none=True), status=422)

    @app.exception(Exception)
    async def handle_generic_exception(request, exc: Exception):
        """
        Handles all other unexpected exceptions (5xx errors).
        Logs the full error for debugging but returns a generic message to the client.
        """
        logger.error(f"Unexpected error on request {request.path}: {exc}", exc_info=exc)

        response = GenericResponse(
            status="error",
            message="An internal server error occurred."
        )
        return json(response.model_dump(exclude_none=True), status=500)