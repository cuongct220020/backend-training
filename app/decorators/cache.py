# app/decorators/cache.py
from functools import wraps
from typing import Callable, Any, Type

from pydantic import BaseModel

from app.databases.redis_manager import redis_manager
from app.utils.logger_utils import get_logger

logger = get_logger(__name__)


def _generate_cache_key(
        prefix: str,
        func: Callable,
        *args: Any,
        **kwargs: Any
    ) -> str:
    """
    Generates a cache key based on a prefix, function name, args, and kwargs.
    """
    sorted_kwargs = sorted(kwargs.items())
    key_parts = [prefix, func.__module__, func.__name__]
    key_parts.extend(map(str, args))
    key_parts.extend(f"{k}={v}" for k, v in sorted_kwargs)
    return ":".join(key_parts)


def cache(
        schema: Type[BaseModel],
        ttl: int,
        prefix: str = "cache"
    ):
    """
    A Pydantic-aware decorator for caching the results of an async function.
    The decorated function is expected to return an object that can be validated
    by the provided Pydantic schema.

    :param schema: The Pydantic model to use for parsing the cached data.
    :param ttl: Time-to-live in seconds for the cache entry.
    :param prefix: A prefix for the cache key.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def decorated_function(*args: Any, **kwargs: Any):
            cache_key = _generate_cache_key(prefix, func, *args, **kwargs)
            redis_client = redis_manager.client

            try:
                # 1. Try to get from cache
                cached_result = await redis_client.get(cache_key)
                if cached_result:
                    logger.debug(f"Cache HIT for key: {cache_key}")
                    # Use the provided schema to parse the JSON back into a Pydantic model
                    return schema.model_validate_json(cached_result)
            except Exception as e:
                logger.error(f"Redis GET failed for key {cache_key}: {e}")

            logger.debug(f"Cache MISS for key: {cache_key}")
            # 2. Cache miss: call the original function
            result = await func(*args, **kwargs)

            if result is None:
                return None

            try:
                # 3. Store the result in cache, using Pydantic's JSON export
                validated_result = schema.model_validate(result)
                await redis_client.set(cache_key, validated_result.model_dump_json(), ex=ttl)
            except Exception as e:
                logger.error(f"Redis SET failed for key {cache_key}: {e}")

            return result

        return decorated_function
    return decorator
