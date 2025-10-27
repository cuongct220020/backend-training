from sanic import SanicException

ENTITY_NOT_FOUND = 'Entity not found'

class TooManyRequests(SanicException):
    """
    Status: 429 Too Many Requests
    """

    status_code = 429
    quiet = True