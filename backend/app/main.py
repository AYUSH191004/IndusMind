from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from backendapp.core.lifespan import lifespan

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.include_router(api_router)