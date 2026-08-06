from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.api.routes import analytics, health, ingestion
from app.cache import create_cache
from app.config import Settings
from app.db import Database
from app.exceptions import DomainError
from app.logging import configure_logging, correlation_id_var
from app.metrics import MetricsRegistry
from app.middleware import CorrelationAndTimingMiddleware

logger = logging.getLogger("finance.app")


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved = settings or Settings.from_env()
    configure_logging(resolved.log_level)
    database = Database(resolved.database_url)
    cache = create_cache(resolved.redis_url)
    metrics = MetricsRegistry()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if resolved.auto_create_schema:
            database.create_schema()
        logger.info("application_started")
        yield
        cache.close()
        database.dispose()
        logger.info("application_stopped")

    application = FastAPI(
        title=resolved.app_name,
        version="0.1.0",
        description="Budget-versus-actual and expense exception analytics PoC",
        lifespan=lifespan,
    )
    application.state.settings = resolved
    application.state.database = database
    application.state.cache = cache
    application.state.metrics = metrics
    application.add_middleware(CorrelationAndTimingMiddleware)

    @application.exception_handler(DomainError)
    async def handle_domain_error(request: Request, exc: DomainError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "correlation_id": correlation_id_var.get(),
                }
            },
        )


    @application.exception_handler(HTTPException)
    async def handle_http_error(request: Request, exc: HTTPException) -> JSONResponse:
        message = exc.detail if isinstance(exc.detail, str) else "request failed"
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": "http_error",
                    "message": message,
                    "correlation_id": correlation_id_var.get(),
                }
            },
            headers=exc.headers,
        )

    @application.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "validation_error",
                    "message": "request validation failed",
                    "details": jsonable_encoder(exc.errors()),
                    "correlation_id": correlation_id_var.get(),
                }
            },
        )

    @application.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("unhandled_exception")
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "internal_error",
                    "message": "an unexpected error occurred",
                    "correlation_id": correlation_id_var.get(),
                }
            },
        )

    application.include_router(health.router)
    application.include_router(ingestion.router)
    application.include_router(analytics.router)
    return application


app = create_app()
