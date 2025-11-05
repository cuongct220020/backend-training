# app/hooks/database.py
from sanic import Sanic, Request

from app.databases.postgresql_manager import postgres_db


async def setup_db(app: Sanic):
    """
    This hook initializes the database connection and creates tables.
    It runs once before the server starts.
    """
    db_uri = app.config.get("DATABASE_URI")
    debug = app.config.get("DEBUG", False)
    await postgres_db.setup(database_uri=db_uri, debug=debug)
    await postgres_db.create_tables()


async def close_db(_app: Sanic):
    """
    This hook closes the database connection pool when the server stops.
    """
    await postgres_db.dispose()


async def manage_db_session(request: Request, handler):
    """
    Creates a new DB session for a request, handles commit/rollback,
    and closes it, using a context manager from the PostgreSQLManager.
    """
    async with postgres_db.get_session() as session:
        request.ctx.db_session = session
        response = await handler(request)
    return response