"""
Health endpoints.
"""

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(prefix="/health")


@router.get(
    "",
    summary="Basic Health Check",
    description="Returns application health status.",
)
async def health() -> dict:
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT.value,
    }


@router.get(
    "/details",
    summary="Detailed Health Check",
    description="Returns detailed service health information.",
)
async def health_details() -> dict:
    return {
        "status": "healthy",
        "services": {
            "postgres": "pending",
            "redis": "pending",
            "neo4j": "pending",
            "qdrant": "pending",
        },
    }