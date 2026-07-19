from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.core.middleware import (
    RequestContextMiddleware,
    SecurityHeadersMiddleware,
)
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.lifespan import lifespan
from app.core.exceptions import register_exception_handlers
configure_logging()
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)
register_exception_handlers(app)

app.add_middleware(RequestContextMiddleware)

app.add_middleware(SecurityHeadersMiddleware)

app.add_middleware(
    GZipMiddleware,
    minimum_size=1024,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],  # tighten in production
)

app.include_router(
    api_router,
    prefix=settings.API_PREFIX,
)