"""
Application-wide constants.

This module defines immutable constants shared across the backend.

It intentionally contains no runtime state and should not import any
application modules to avoid circular dependencies.
"""

from __future__ import annotations

# ---------------------------------------------------------------------
# API
# ---------------------------------------------------------------------

API_VERSION = "v1"

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# ---------------------------------------------------------------------
# HTTP Headers
# ---------------------------------------------------------------------

HEADER_REQUEST_ID = "X-Request-ID"
HEADER_CORRELATION_ID = "X-Correlation-ID"

# ---------------------------------------------------------------------
# Timeouts (seconds)
# ---------------------------------------------------------------------

DEFAULT_REQUEST_TIMEOUT = 30
DATABASE_CONNECTION_TIMEOUT = 30
REDIS_CONNECTION_TIMEOUT = 10
NEO4J_CONNECTION_TIMEOUT = 30
QDRANT_CONNECTION_TIMEOUT = 30

# ---------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------

DEFAULT_DB_POOL_SIZE = 10
DEFAULT_DB_MAX_OVERFLOW = 20
DEFAULT_DB_POOL_TIMEOUT = 30
DEFAULT_DB_POOL_RECYCLE = 1800

# ---------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------

DEFAULT_CACHE_TTL = 3600

# ---------------------------------------------------------------------
# Content Types
# ---------------------------------------------------------------------

APPLICATION_JSON = "application/json"

# ---------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------

HEALTHY = "healthy"
UNHEALTHY = "unhealthy"

# ---------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------

REQUEST_ID_LOG_KEY = "request_id"
CORRELATION_ID_LOG_KEY = "correlation_id"

# ---------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------

PASSWORD_MIN_LENGTH = 8

# ---------------------------------------------------------------------
# Limits
# ---------------------------------------------------------------------

MAX_UPLOAD_SIZE_BYTES = 100 * 1024 * 1024  # 100 MB
MAX_REQUEST_BODY_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
