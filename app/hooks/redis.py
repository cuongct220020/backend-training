# app/hooks/redis.py
from sanic import Sanic

from app.extensions import redis_manager
from config import RedisConfig
from app.utils.logger_utils import get_logger

logger = get_logger(__name__)

async def setup_redis(_app: Sanic):
    """Hook to initialize the Redis connection pool."""
    logger.info("Initializing Redis connection pool...")
    redis_manager.setup(
        host=RedisConfig.HOST,
        port=RedisConfig.PORT,
        db=RedisConfig.DB
    )
    # Ping to check connection
    await redis_manager.client.ping()
    logger.info("Redis connection pool initialized successfully.")


async def close_redis(_app: Sanic):
    """Hook to close the Redis connection pool."""
    logger.info("Closing Redis connection pool...")
    await redis_manager.close()
    logger.info("Redis connection pool closed.")
