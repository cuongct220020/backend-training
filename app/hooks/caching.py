# app/hooks/caching.py
from sanic import Sanic, Request
from sanic.exceptions import SanicException

from app.databases.redis_manager import redis_manager
from app.utils.logger_utils import get_logger

logger = get_logger(__name__)


async def setup_redis(app: Sanic):
    """Hook to initialize the Redis connection pool."""
    logger.info("Initializing Redis connection pool...")

    # Redis Configuration
    redis_host = app.config.get("REDIS_HOST")
    redis_port = app.config.get("REDIS_PORT")
    redis_db = app.config.get("REDIS_DB")

    # Redis setup
    redis_manager.setup(
        host=redis_host,
        port=redis_port,
        db=redis_db
    )

    # Ping to check connection
    await redis_manager.client.ping()
    logger.info(f"Redis connection pool successfully created at {redis_host}:{redis_port}.")


async def close_redis(_app: Sanic):
    """Hook to close the Redis connection pool."""
    logger.info("Closing Redis connection pool...")
    await redis_manager.close()
    logger.info("Redis connection pool closed.")


async def inject_redis_client(request: Request):
    """
    Injects the shared Redis client into the request context.
    The connection pool handles the actual connection management.
    """
    request.ctx.redis_client = redis_manager.client