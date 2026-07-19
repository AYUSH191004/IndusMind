"""
PostgreSQL database infrastructure.

Provides:

- Async SQLAlchemy engine
- Session factory
- Session dependency
- Health check
- Graceful shutdown
"""

from __future__ import annotations

from app.core.config import settings
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# ---------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------

engine: AsyncEngine = create_async_engine(
    settings.postgres_url,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_recycle=1800,
)

# ---------------------------------------------------------------------
# Session Factory
# ---------------------------------------------------------------------

AsyncSessionFactory = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)

# ---------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------


async def check_database_health() -> bool:
    """
    Verify database connectivity.

    Returns:
        True if database is reachable.
    """
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return True

    except Exception:
        return False


# ---------------------------------------------------------------------
# Shutdown
# ---------------------------------------------------------------------


async def close_database() -> None:
    """
    Dispose of the SQLAlchemy engine.
    """
    await engine.dispose()
