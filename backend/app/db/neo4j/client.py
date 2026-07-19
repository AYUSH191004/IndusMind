"""
Neo4j database infrastructure.

Provides:

- Async Neo4j driver
- Session provider
- Health check
- Driver lifecycle management
"""

from __future__ import annotations

from collections.abc import AsyncGenerator

from neo4j import AsyncDriver, AsyncGraphDatabase

from app.core.config import settings

# ---------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------

driver: AsyncDriver = AsyncGraphDatabase.driver(
    settings.NEO4J_URI,
    auth=(
        settings.NEO4J_USER,
        settings.NEO4J_PASSWORD,
    ),
)

# ---------------------------------------------------------------------
# Session Provider
# ---------------------------------------------------------------------


async def get_graph() -> AsyncGenerator:
    """
    Provide an async Neo4j session.

    Yields:
        Async Neo4j session.
    """
    async with driver.session() as session:
        yield session


# ---------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------


async def check_neo4j_health() -> bool:
    """
    Verify Neo4j connectivity.

    Returns:
        True if reachable.
    """
    try:
        async with driver.session() as session:
            await session.run("RETURN 1")

        return True

    except Exception:
        return False


# ---------------------------------------------------------------------
# Shutdown
# ---------------------------------------------------------------------


async def close_graph() -> None:
    """
    Close the Neo4j driver.
    """
    await driver.close()