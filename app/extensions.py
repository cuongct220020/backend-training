# app/extensions.py
from sqlalchemy.orm import declarative_base
from redis.asyncio import Redis, ConnectionPool

# Base for all models to inherit from
Base = declarative_base()

# Redis manager
class RedisManager:
    """A manager for the Redis connection pool."""
    def __init__(self):
        self.pool: ConnectionPool | None = None

    def setup(self, host: str, port: int, db: int):
        """Creates the connection pool."""
        self.pool = ConnectionPool(host=host, port=port, db=db, decode_responses=True)
        
    async def close(self):
        """Closes the connection pool."""
        if self.pool:
            await self.pool.disconnect()

    @property
    def client(self) -> Redis:
        """Provides a Redis client from the pool."""
        if not self.pool:
            raise RuntimeError("Redis connection pool not initialized. Call setup() first.")
        return Redis(connection_pool=self.pool)

# A single, shared instance for the entire application
redis_manager = RedisManager()