"""
Qdrant dependency providers.

Provides dependency injection for the shared Qdrant client.
"""

from __future__ import annotations

from typing import Annotated

from app.db.qdrant.client import get_qdrant
from fastapi import Depends
from qdrant_client import AsyncQdrantClient


async def provide_qdrant() -> AsyncQdrantClient:
    """
    Return the shared Qdrant client.

    Returns:
        Configured AsyncQdrantClient.
    """
    return await get_qdrant()


QdrantDependency = Annotated[
    AsyncQdrantClient,
    Depends(provide_qdrant),
]
