"""
PostgreSQL health checks.

Provides health diagnostics for the PostgreSQL database.
"""

from __future__ import annotations

import time
from typing import Any

from sqlalchemy import text

from app.db.postgres.engine import engine


async def check_database_health() -> dict[str, Any]:
    """
    Perform a PostgreSQL health check.

    Returns:
        Dictionary containing health information.
    """
    started = time.perf_counter()

    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))

        latency = round((time.perf_counter() - started) * 1000, 2)

        return {
            "healthy": True,
            "latency_ms": latency,
            "database": "postgresql",
        }

    except Exception as exc:
        latency = round((time.perf_counter() - started) * 1000, 2)

        return {
            "healthy": False,
            "latency_ms": latency,
            "database": "postgresql",
            "error": str(exc),
        }