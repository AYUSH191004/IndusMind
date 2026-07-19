"""
Neo4j dependency providers.

Provides dependency injection for Neo4j graph sessions.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Annotated

from app.db.neo4j.client import get_graph
from fastapi import Depends
from neo4j import AsyncSession


async def provide_graph() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a Neo4j session.

    Yields:
        Async Neo4j session.
    """
    async for session in get_graph():
        yield session


Neo4jDependency = Annotated[
    AsyncSession,
    Depends(provide_graph),
]
