from __future__ import annotations

from collections.abc import Generator

from fastapi import Header, HTTPException, Request
from sqlalchemy.orm import Session

from app.cache import Cache
from app.config import Settings


def get_session(request: Request) -> Generator[Session, None, None]:
    session = request.app.state.database.session_factory()
    try:
        yield session
    finally:
        session.close()


def get_cache(request: Request) -> Cache:
    return request.app.state.cache


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def require_api_key(
    request: Request,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> None:
    configured = request.app.state.settings.api_key
    if configured and x_api_key != configured:
        raise HTTPException(status_code=401, detail="invalid API key")
