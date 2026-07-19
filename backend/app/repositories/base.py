"""
Base repository.

Provides common functionality shared by all repositories.
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Base class for all repositories.

    Repositories should inherit from this class to gain access
    to the shared database session.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    @property
    def session(self) -> AsyncSession:
        """
        Return the underlying SQLAlchemy session.
        """
        return self._session

    async def flush(self) -> None:
        """
        Flush pending changes.
        """
        await self._session.flush()

    async def refresh(
        self,
        instance: ModelType,
    ) -> None:
        """
        Refresh an ORM instance.
        """
        await self._session.refresh(instance)

    async def commit(self) -> None:
        """
        Commit the current transaction.
        """
        await self._session.commit()

    async def rollback(self) -> None:
        """
        Roll back the current transaction.
        """
        await self._session.rollback()

    async def execute(self, statement: Any):
        """
        Execute a SQLAlchemy statement.
        """
        return await self._session.execute(statement)
