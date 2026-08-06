from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(tags=["health"])


@router.get("/health/live")
def liveness() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/ready")
def readiness(request: Request) -> JSONResponse:
    checks = {"database": False, "cache": False}
    try:
        checks["database"] = request.app.state.database.ping()
    except Exception:
        checks["database"] = False
    try:
        checks["cache"] = request.app.state.cache.ping()
    except Exception:
        checks["cache"] = False
    ready = all(checks.values())
    return JSONResponse(
        status_code=200 if ready else 503,
        content={"status": "ready" if ready else "not_ready", "checks": checks},
    )


@router.get("/internal/metrics")
def metrics(request: Request) -> dict[str, object]:
    return request.app.state.metrics.snapshot()
