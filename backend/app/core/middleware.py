"""
Application middleware.

Provides custom middleware for:

- Request ID generation
- Request timing
- Security headers
"""

from __future__ import annotations

import time
import uuid

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.constants import (
    HEADER_REQUEST_ID,
    REQUEST_ID_LOG_KEY,
)
from app.core.logging import get_logger

logger = get_logger(__name__)


class RequestContextMiddleware(BaseHTTPMiddleware):
    """
    Adds a unique request identifier and logs request metadata.
    """

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:
        request_id = str(uuid.uuid4())

        request.state.request_id = request_id

        start = time.perf_counter()

        response = await call_next(request)

        duration = time.perf_counter() - start

        response.headers[HEADER_REQUEST_ID] = request_id

        logger.info(
            "HTTP Request",
            **{
                REQUEST_ID_LOG_KEY: request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration * 1000, 2),
            },
        )

        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Adds common HTTP security headers.
    """

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        return response