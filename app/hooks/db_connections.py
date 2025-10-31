from sanic import Sanic, Request

from app.databases.postgresql import postgres_db
from app.hooks import exceptions


async def setup_db(app: Sanic):
    """
    This hook initializes the database connection and creates tables.
    It runs once before the server starts.
    """
    db_uri = app.config.get("DATABASE_URI")
    debug = app.config.get("DEBUG", False)
    await postgres_db.setup(database_uri=db_uri, debug=debug)


async def close_db(_app: Sanic):
    """
    This hook closes the database connection pool when the server stops.
    """
    await postgres_db.dispose()


async def acquire_db_connection(request: Request):
    """
    This hook acquires a database connection from the pool for each request.
    The connection is attached to the request context `request.ctx`.
    """
    try:
        request.ctx.db_connection = await postgres_db.acquire()
    except Exception:
        # It's crucial to handle cases where the pool might be exhausted
        # or the database is down.
        raise exceptions.ServiceUnavailable("Could not acquire a database connection.")


async def release_db_connection(request: Request, response):
    """
    This hook releases the database connection back to the pool after the request is processed.
    This ensures that the connection is returned even if an error occurs.
    """
    if hasattr(request.ctx, "db_connection"):
        await postgres_db.release(request.ctx.db_connection)