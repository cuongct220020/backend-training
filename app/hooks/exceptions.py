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


class TooManyRequests(AppException):
    """Status: 429 Too Many Requests"""
    status_code = 429
    quiet = True


# 5xx Server Errors
class ServerError(AppException):
    """Status: 500 Internal Server Error"""
    status_code = 500


class ServiceUnavailable(AppException):
    """Status: 503 Service Unavailable"""
    status_code = 503
