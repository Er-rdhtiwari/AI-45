from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str = "Finance Analytics Service"
    app_env: str = "development"
    database_url: str = "sqlite:///./finance.db"
    redis_url: str = "memory://"
    cache_ttl_seconds: int = 60
    auto_create_schema: bool = True
    log_level: str = "INFO"
    api_key: str | None = None

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_env=os.getenv("APP_ENV", "development"),
            database_url=os.getenv("DATABASE_URL", "sqlite:///./finance.db"),
            redis_url=os.getenv("REDIS_URL", "memory://"),
            cache_ttl_seconds=int(os.getenv("CACHE_TTL_SECONDS", "60")),
            auto_create_schema=os.getenv("AUTO_CREATE_SCHEMA", "true").lower()
            in {"1", "true", "yes"},
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            api_key=os.getenv("API_KEY") or None,
        )
