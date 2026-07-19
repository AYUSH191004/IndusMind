"""
Redis infrastructure.

Provides:

- Async Redis client
- Connection management
- Health check
- Dependency provider
- Graceful shutdown
"""

from __future__ import annotations

from app.core.config import settings
from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool

# ---------------------------------------------------------------------
# Connection Pool
# ---------------------------------------------------------------------

_pool = ConnectionPool.from_url(
    settings.redis_url,
    max_connections=50,
    decode_responses=True,
)

# ---------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------

redis_client = Redis(
    connection_pool=_pool,
)

# ---------------------------------------------------------------------
# Dependency Provider
# ---------------------------------------------------------------------


async def get_redis() -> Redis:
    """
    Return the shared Redis client.
    """
    return redis_client


# ---------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------


async def check_redis_health() -> bool:
    """
    Verify Redis connectivity.

    Returns:
        True if Redis is reachable.
    """
    try:
        await redis_client.ping()
        return True

    except Exception:
        return False


# ---------------------------------------------------------------------
# Shutdown
# ---------------------------------------------------------------------


async def close_redis() -> None:
    """
    Close Redis client and connection pool.
    """
    await redis_client.aclose()
