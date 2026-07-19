"""
Qdrant database infrastructure.

Provides:

- Shared Qdrant client
- Dependency provider
- Health check
- Graceful shutdown
"""

from __future__ import annotations

from app.core.config import settings
from qdrant_client import AsyncQdrantClient

# ---------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------

qdrant_client = AsyncQdrantClient(
    url=settings.qdrant_url,
)

# ---------------------------------------------------------------------
# Dependency Provider
# ---------------------------------------------------------------------


async def get_qdrant() -> AsyncQdrantClient:
    """
    Return the shared Qdrant client.
    """
    return qdrant_client


# ---------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------


async def check_qdrant_health() -> bool:
    """
    Verify Qdrant connectivity.

    Returns:
        True if the server is reachable.
    """
    try:
        await qdrant_client.get_collections()
        return True

    except Exception:
        return False


# ---------------------------------------------------------------------
# Shutdown
# ---------------------------------------------------------------------


async def close_qdrant() -> None:
    """
    Close the Qdrant client.
    """
    await qdrant_client.close()
