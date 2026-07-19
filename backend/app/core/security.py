"""
Security utilities.

Provides reusable cryptographic helpers for:

- Password hashing
- Password verification
- JWT generation
- JWT decoding

No authentication or authorization logic belongs here.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from app.core.config import settings
from jwt import InvalidTokenError
from pwdlib import PasswordHash

# ---------------------------------------------------------------------
# Password Hasher
# ---------------------------------------------------------------------

password_hasher = PasswordHash.recommended()


# ---------------------------------------------------------------------
# Password Utilities
# ---------------------------------------------------------------------


def hash_password(password: str) -> str:
    """
    Hash a plaintext password.

    Args:
        password: Plaintext password.

    Returns:
        Secure password hash.
    """
    return password_hasher.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plaintext password against its hash.

    Args:
        plain_password: Plaintext password.
        hashed_password: Stored password hash.

    Returns:
        True if valid, otherwise False.
    """
    return password_hasher.verify(
        plain_password,
        hashed_password,
    )


# ---------------------------------------------------------------------
# JWT Utilities
# ---------------------------------------------------------------------


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    """
    Create a signed JWT access token.

    Args:
        subject: User identifier.
        expires_delta: Custom expiration.
        additional_claims: Additional JWT claims.

    Returns:
        Encoded JWT.
    """
    expire = datetime.now(UTC) + (
        expires_delta
        or timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    )

    payload: dict[str, Any] = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.now(UTC),
    }

    if additional_claims:
        payload.update(additional_claims)

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm="HS256",
    )


def decode_token(
    token: str,
) -> dict[str, Any]:
    """
    Decode and validate a JWT.

    Args:
        token: JWT access token.

    Returns:
        Decoded payload.

    Raises:
        InvalidTokenError:
            If the token is invalid or expired.
    """
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=["HS256"],
    )


# ---------------------------------------------------------------------
# Validation Utilities
# ---------------------------------------------------------------------


def validate_secret_key() -> None:
    """
    Validate the configured application secret.

    Raises:
        ValueError:
            If the configured secret is considered insecure.
    """
    if len(settings.SECRET_KEY) < 32:
        raise ValueError("SECRET_KEY must contain at least 32 characters.")


__all__ = [
    "hash_password",
    "verify_password",
    "create_access_token",
    "decode_token",
    "validate_secret_key",
    "InvalidTokenError",
]
