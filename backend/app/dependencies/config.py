"""
Configuration dependency providers.

Centralized dependency injection for application settings.
"""

from __future__ import annotations

from typing import Annotated

from app.core.config import Settings, get_settings
from fastapi import Depends


def provide_settings() -> Settings:
    """
    Return the cached application settings.
    """
    return get_settings()


SettingsDependency = Annotated[
    Settings,
    Depends(provide_settings),
]
