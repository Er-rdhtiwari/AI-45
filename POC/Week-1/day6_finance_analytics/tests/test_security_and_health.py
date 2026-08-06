from __future__ import annotations

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from scripts.seed_db import seed


def test_health_and_metrics(client):
    assert client.get("/health/live").json() == {"status": "ok"}
    ready = client.get("/health/ready")
    assert ready.status_code == 200
    assert ready.json()["checks"] == {"database": True, "cache": True}
    metrics = client.get("/internal/metrics").json()
    assert metrics["requests_total"] >= 2


def test_optional_api_key(settings: Settings):
    protected = Settings(
        app_env=settings.app_env,
        database_url=settings.database_url,
        redis_url=settings.redis_url,
        cache_ttl_seconds=settings.cache_ttl_seconds,
        auto_create_schema=True,
        log_level="WARNING",
        api_key="secret-test-key",
    )
    seed(protected)
    with TestClient(create_app(protected)) as client:
        assert client.get("/v1/analytics/variance").status_code == 401
        assert client.get(
            "/v1/analytics/variance", headers={"X-API-Key": "secret-test-key"}
        ).status_code == 200
