"""
Application lifespan management.

This module defines the FastAPI lifespan context responsible for
application startup and shutdown events.

All shared infrastructure resources (database engines, Redis clients,
Neo4j drivers, Qdrant clients, background workers, etc.) should be
initialized and cleaned up here.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import get_logger
from app.core.security import validate_secret_key
from app.db.database_manager import database_manager
from fastapi import FastAPI

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Manage the application lifecycle.

    Startup:
        - Log startup information.
        - Initialize shared resources.
        - Perform startup validation.

    Shutdown:
        - Close shared resources.
        - Flush logs if required.
        - Log shutdown completion.

    Args:
        app: FastAPI application instance.

    Yields:
        Control back to FastAPI while the application is running.
    """
    logger.info(
        "Starting %s v%s (%s)",
        settings.APP_NAME,
        settings.APP_VERSION,
        settings.ENVIRONMENT.value,
    )
    validate_secret_key()
    await database_manager.initialize()

    # ------------------------------------------------------------------
    # Future startup initialization
    #
    # Examples:
    #   - PostgreSQL engine
    #   - Redis connection pool
    #   - Neo4j driver
    #   - Qdrant client
    #   - Celery application
    # ------------------------------------------------------------------

    try:
        yield
    finally:
        # --------------------------------------------------------------
        # Future resource cleanup
        #
        # Examples:
        #   - await postgres.dispose()
        #   - await redis.aclose()
        #   - neo4j_driver.close()
        #   - qdrant_client.close()
        # --------------------------------------------------------------

        logger.info(
            "Shutting down %s",
            settings.APP_NAME,
            await database_manager.shutdown(),
        )
