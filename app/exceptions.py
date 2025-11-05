# app/exceptions.py
from sanic import SanicException


# Base exception for the application
class AppException(SanicException):
    """
    Base class for application-specific exceptions.
    Allows for catching all custom errors with a single 'except' block.
    """
    pass


# 4xx Client Errors
class BadRequest(AppException):
    """Status: 400 Bad Request"""
    status_code = 400


class Unauthorized(AppException):
    """Status: 401 Unauthorized"""
    status_code = 401


class Forbidden(AppException):
    """Status: 403 Forbidden"""
    status_code = 403


class NotFound(AppException):
    """Status: 404 Not Found"""
    status_code = 404


class Conflict(AppException):
    """Status: 409 Conflict"""
    status_code = 409


class UnprocessableEntity(AppException):
    """Status: 422 Unprocessable Entity"""
    status_code = 422


class TooManyRequests(AppException):
    """Status: 429 Too Many Requests"""
    status_code = 429
    quiet = True

    def __init__(self, message: str | None = None, status_code: int | None = None, retry_after: int | None = None):
        super().__init__(message, status_code)
        self.retry_after = retry_after


# 5xx Server Errors
class ServerError(AppException):
    """Status: 500 Internal Server Error"""
    status_code = 500


class BadGateway(AppException):
    """Status: 502 Bad Gateway"""
    status_code = 502


class ServiceUnavailable(AppException):
    """Status: 503 Service Unavailable"""
    status_code = 503
