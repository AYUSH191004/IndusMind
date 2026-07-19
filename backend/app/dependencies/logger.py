"""
Logger dependency providers.

Provides dependency injection for the application's structured logger.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from structlog.stdlib import BoundLogger

from app.core.logging import get_logger


def provide_logger() -> BoundLogger:
    """
    Return the application's structured logger.

    Returns:
        Configured structlog BoundLogger.
    """
    return get_logger()


LoggerDependency = Annotated[
    BoundLogger,
    Depends(provide_logger),
]