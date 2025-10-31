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
    await postgres_db.create_tables()


async def close_db(_app: Sanic):
    """
    This hook closes the database connection pool when the server stops.
    """
    await postgres_db.dispose()


async def acquire_db_session(request: Request):
    """
    Acquires a DB session from the session_maker and attaches it to the request context.
    This runs before the request handler.
    """
    if not postgres_db.session_maker:
        raise exceptions.ServerError("Database not initialized. Call setup() first.")
    request.ctx.db_session = postgres_db.session_maker()


async def release_db_session(request: Request, response):
    """
    Commits on success, rolls back on failure, and closes the session.
    This runs after the request handler.
    """
    if hasattr(request.ctx, "db_session"):
        session = request.ctx.db_session
        try:
            if response and response.status < 400:
                await session.commit()
            else:
                await session.rollback()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()