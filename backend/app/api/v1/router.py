"""
API v1 Router

Central router that aggregates all version 1 API endpoints.
"""

from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router

api_router = APIRouter()

# ---------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------

api_router.include_router(
    health_router,
    tags=["Health"],
)

# ---------------------------------------------------------------------
# Future Modules
# ---------------------------------------------------------------------
#
# api_router.include_router(
#     auth_router,
#     prefix="/auth",
#     tags=["Authentication"],
# )
#
# api_router.include_router(
#     users_router,
#     prefix="/users",
#     tags=["Users"],
# )
#
# api_router.include_router(
#     knowledge_router,
#     prefix="/knowledge",
#     tags=["Knowledge"],
# )
#
# api_router.include_router(
#     ingestion_router,
#     prefix="/ingestion",
#     tags=["Ingestion"],
# )
#
# api_router.include_router(
#     search_router,
#     prefix="/search",
#     tags=["Search"],
# )
#
# api_router.include_router(
#     graph_router,
#     prefix="/graph",
#     tags=["Knowledge Graph"],
# )
#
# api_router.include_router(
#     vector_router,
#     prefix="/vector",
#     tags=["Vector Search"],
# )
#
# api_router.include_router(
#     admin_router,
#     prefix="/admin",
#     tags=["Administration"],
# )