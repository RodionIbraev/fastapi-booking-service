import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.config import Settings, get_settings
from app.core.resources import AppResources
from app.routers import health
from app.routers.router import api_router


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    cors_allow_origins = [
        origin.strip() for origin in settings.cors_allow_origins.split(",") if origin.strip()
    ]

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        resources = AppResources.create(settings)
        app.state.resources = resources
        try:
            yield
        finally:
            await resources.close()

    logging.basicConfig(level=logging.DEBUG if settings.debug else logging.INFO)

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        docs_url="/docs",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )
    app.include_router(health.router)
    app.include_router(api_router, prefix=settings.api_prefix)
    if cors_allow_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_allow_origins,
            allow_credentials=False,
            allow_methods=["GET", "POST"],
            allow_headers=["Authorization", "Content-Type", "Idempotency-Key"],
            expose_headers=["Idempotent-Replayed"],
        )
    return app


app = create_app()
