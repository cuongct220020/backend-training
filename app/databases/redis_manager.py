from redis.asyncio import Redis, ConnectionPool
from app.exceptions import ServerError


class RedisManager:
    """A manager for the Redis connection pool."""

    def __init__(self):
        self.pool: ConnectionPool | None = None
        self._client: Redis | None = None

    def setup(self, host: str, port: int, db: int):
        """Creates the connection pool."""
        self.pool = ConnectionPool(host=host, port=port, db=db, decode_responses=True)

    async def close(self):
        """Closes the connection pool."""
        if self._client:
            await self._client.close()
        if self.pool:
            await self.pool.disconnect()

    @property
    def client(self) -> Redis:
        """
        Provides a cached, reusable Redis client from the connection pool.
        The connection pool handles the underlying connection management.
        """
        if not self.pool:
            raise ServerError("Redis connection pool not initialized. Call setup() first.")
        if not self._client:
            self._client = Redis(connection_pool=self.pool)
        return self._client


# A single, shared instance for the entire application
redis_manager = RedisManager()
