"""
Database infrastructure manager.

Centralized lifecycle management for all infrastructure services.

Responsibilities:
    - Startup initialization
    - Graceful shutdown
    - Health aggregation

This module should remain orchestration-only and must not contain
business logic or database queries beyond connectivity checks.
"""

from __future__ import annotations

import asyncio
from typing import Any

from app.core.logging import get_logger
from app.db.neo4j.client import check_neo4j_health, close_graph
from app.db.postgres.engine import close_database
from app.db.postgres.health import check_database_health
from app.db.qdrant.client import check_qdrant_health, close_qdrant
from app.db.redis.client import check_redis_health, close_redis

logger = get_logger(__name__)


class DatabaseManager:
    """
    Coordinates the lifecycle of all database services.
    """

    async def initialize(self) -> None:
        """
        Initialize infrastructure services.

        Individual clients are lazily created, so this currently verifies
        that startup has begun successfully. Future versions may eagerly
        establish connections if desired.
        """
        logger.info("Initializing database infrastructure")

    async def shutdown(self) -> None:
        """
        Gracefully close all infrastructure services.
        """
        logger.info("Shutting down database infrastructure")

        await asyncio.gather(
            close_database(),
            close_redis(),
            close_graph(),
            close_qdrant(),
            return_exceptions=False,
        )

        logger.info("Database infrastructure shutdown complete")

    async def health(self) -> dict[str, Any]:
        """
        Perform health checks for all infrastructure services.

        Returns:
            Dictionary containing individual service health.
        """

        postgres, redis, neo4j, qdrant = await asyncio.gather(
            check_database_health(),
            check_redis_health(),
            check_neo4j_health(),
            check_qdrant_health(),
        )

        overall = all(
            (
                postgres,
                redis,
                neo4j,
                qdrant,
            )
        )

        return {
            "status": "healthy" if overall else "unhealthy",
            "services": {
                "postgres": postgres,
                "redis": redis,
                "neo4j": neo4j,
                "qdrant": qdrant,
            },
        }


database_manager = DatabaseManager()
