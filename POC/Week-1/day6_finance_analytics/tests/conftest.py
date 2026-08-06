from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.config import Settings  # noqa: E402
from app.main import create_app  # noqa: E402
from scripts.seed_db import seed  # noqa: E402


@pytest.fixture()
def settings(tmp_path: Path) -> Settings:
    return Settings(
        app_env="test",
        database_url=f"sqlite:///{tmp_path / 'test.db'}",
        redis_url="memory://",
        cache_ttl_seconds=600,
        auto_create_schema=True,
        log_level="WARNING",
    )


@pytest.fixture()
def client(settings: Settings):
    seed(settings)
    app = create_app(settings)
    with TestClient(app) as test_client:
        yield test_client
