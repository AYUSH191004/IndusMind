"""
Global exception definitions and handlers.

Provides a consistent error model across the application.
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.logging import get_logger

logger = get_logger(__name__)


class ErrorResponse(BaseModel):
    """Standard API error response."""

    success: bool = False
    error: dict[str, Any]


class ApplicationException(Exception):
    """Base exception for all application-specific errors."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = "APPLICATION_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}


class ResourceNotFoundException(ApplicationException):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str) -> None:
        super().__init__(
            message=f"{resource} not found.",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="RESOURCE_NOT_FOUND",
        )


class ValidationException(ApplicationException):
    """Raised for application-level validation failures."""

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="VALIDATION_ERROR",
        )


class UnauthorizedException(ApplicationException):
    """Raised for authentication failures."""

    def __init__(self, message: str = "Authentication required.") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED",
        )


class ForbiddenException(ApplicationException):
    """Raised when access is denied."""

    def __init__(self, message: str = "Access denied.") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="FORBIDDEN",
        )


class DatabaseException(ApplicationException):
    """Raised for database-related failures."""

    def __init__(self, message: str = "Database operation failed.") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="DATABASE_ERROR",
        )


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers.

    Args:
        app: FastAPI application instance.
    """

    @app.exception_handler(ApplicationException)
    async def application_exception_handler(
        request: Request,
        exc: ApplicationException,
    ) -> JSONResponse:
        logger.error(
            "Application exception",
            path=str(request.url),
            error_code=exc.error_code,
            message=exc.message,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error={
                    "code": exc.error_code,
                    "message": exc.message,
                    "details": exc.details,
                }
            ).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        logger.warning(
            "Request validation failed",
            path=str(request.url),
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ErrorResponse(
                error={
                    "code": "REQUEST_VALIDATION_ERROR",
                    "message": "Invalid request payload.",
                    "details": exc.errors(),
                }
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        logger.exception(
            "Unhandled exception",
            path=str(request.url),
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                error={
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred.",
                    "details": {},
                }
            ).model_dump(),
        )