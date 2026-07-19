"""
PostgreSQL dependency providers.

Provides dependency injection for PostgreSQL database sessions.
"""

from __future__ import annotations

from typing import Annotated

from app.db.postgres.session import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


def provide_db_session() -> AsyncSession:
    """
    Provide an async database session.

    This delegates session creation to the PostgreSQL
    infrastructure layer.

    Returns:
        Async SQLAlchemy session.
    """
    return get_db()


DatabaseSession = Annotated[
    AsyncSession,
    Depends(provide_db_session),
]
