"""
Application configuration.

Loads configuration from environment variables and .env file using
Pydantic Settings.

Priority:
1. Environment Variables
2. .env
3. Default Values
"""

from enum import Enum
from functools import lru_cache

from pydantic import computed_field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """Supported deployment environments."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------

    APP_NAME: str = "Industrial Knowledge Intelligence Platform"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    DEBUG: bool = True

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    API_PREFIX: str = "/api/v1"

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    LOG_LEVEL: str = "INFO"

    # ------------------------------------------------------------------
    # PostgreSQL
    # ------------------------------------------------------------------

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "knowledge"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"

    # ------------------------------------------------------------------
    # Redis
    # ------------------------------------------------------------------

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # ------------------------------------------------------------------
    # Neo4j
    # ------------------------------------------------------------------

    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"

    # ------------------------------------------------------------------
    # Qdrant
    # ------------------------------------------------------------------

    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333

    # ------------------------------------------------------------------
    # Security
    # ------------------------------------------------------------------

    SECRET_KEY: str = "CHANGE_ME"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ------------------------------------------------------------------
    # Timeouts
    # ------------------------------------------------------------------

    REQUEST_TIMEOUT_SECONDS: int = 30

    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # ------------------------------------------------------------------
    # Validators
    # ------------------------------------------------------------------

    @model_validator(mode="after")
    def validate_settings(self):
        """Validate critical configuration."""

        if self.PORT <= 0 or self.PORT > 65535:
            raise ValueError("PORT must be between 1 and 65535")

        if self.POSTGRES_PORT <= 0:
            raise ValueError("Invalid PostgreSQL port")

        if self.REDIS_PORT <= 0:
            raise ValueError("Invalid Redis port")

        if self.QDRANT_PORT <= 0:
            raise ValueError("Invalid Qdrant port")

        if self.ACCESS_TOKEN_EXPIRE_MINUTES <= 0:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be positive")

        if not self.SECRET_KEY.strip():
            raise ValueError("SECRET_KEY cannot be empty")

        return self

    # ------------------------------------------------------------------
    # Computed Fields
    # ------------------------------------------------------------------

    @computed_field
    @property
    def postgres_url(self) -> str:
        """Async SQLAlchemy PostgreSQL URL."""

        return (
            "postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    @computed_field
    @property
    def redis_url(self) -> str:
        """Redis URL."""

        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @computed_field
    @property
    def qdrant_url(self) -> str:
        """Qdrant endpoint."""

        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"

    @computed_field
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == Environment.DEVELOPMENT

    @computed_field
    @property
    def is_testing(self) -> bool:
        return self.ENVIRONMENT == Environment.TESTING

    @computed_field
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == Environment.PRODUCTION


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.

    Returns:
        Singleton Settings object.
    """
    return Settings()


settings = get_settings()
