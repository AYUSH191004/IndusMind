"""
Application logging configuration.

Provides a centralized logging configuration using structlog.

Features:
    - Structured logging
    - Console renderer for development
    - JSON renderer for production
    - Request ID support (middleware integration)
    - Timestamped logs
    - Stdlib logging compatibility
"""

from __future__ import annotations

import logging
import sys

import structlog

from app.core.config import settings


def configure_logging() -> None:
    """
    Configure application logging.

    This function should be called exactly once during application startup.
    """

    processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
    ]

    if settings.is_development:
        processors.append(
            structlog.dev.ConsoleRenderer()
        )
    else:
        processors.append(
            structlog.processors.JSONRenderer()
        )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper()),
    )

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """
    Return a configured structured logger.

    Args:
        name:
            Optional logger name.

    Returns:
        Configured structlog logger.
    """
    return structlog.get_logger(name)