from __future__ import annotations

import json
import threading
import time
from abc import ABC, abstractmethod
from collections.abc import Mapping
from datetime import date, datetime
from decimal import Decimal
from typing import Any


class Cache(ABC):
    @abstractmethod
    def get_json(self, key: str) -> Any | None: ...

    @abstractmethod
    def set_json(self, key: str, value: Any, ttl_seconds: int) -> None: ...

    @abstractmethod
    def get_version(self) -> int: ...

    @abstractmethod
    def bump_version(self) -> int: ...

    @abstractmethod
    def ping(self) -> bool: ...

    def close(self) -> None:
        return None


class _Encoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)


class MemoryTTLCache(Cache):
    def __init__(self) -> None:
        self._data: dict[str, tuple[float, str]] = {}
        self._version = 1
        self._lock = threading.Lock()

    def get_json(self, key: str) -> Any | None:
        with self._lock:
            item = self._data.get(key)
            if item is None:
                return None
            expires_at, payload = item
            if expires_at < time.monotonic():
                self._data.pop(key, None)
                return None
            return json.loads(payload)

    def set_json(self, key: str, value: Any, ttl_seconds: int) -> None:
        payload = json.dumps(value, cls=_Encoder, separators=(",", ":"))
        with self._lock:
            self._data[key] = (time.monotonic() + ttl_seconds, payload)

    def get_version(self) -> int:
        with self._lock:
            return self._version

    def bump_version(self) -> int:
        with self._lock:
            self._version += 1
            return self._version

    def ping(self) -> bool:
        return True


class RedisCache(Cache):
    VERSION_KEY = "finance-analytics:cache-version"

    def __init__(self, url: str) -> None:
        try:
            from redis import Redis
        except ImportError as exc:  # pragma: no cover - exercised in Docker profile
            raise RuntimeError("redis package is required for RedisCache") from exc
        self._client = Redis.from_url(url, decode_responses=True)
        self._client.setnx(self.VERSION_KEY, 1)

    def get_json(self, key: str) -> Any | None:
        payload = self._client.get(key)
        return json.loads(payload) if payload is not None else None

    def set_json(self, key: str, value: Any, ttl_seconds: int) -> None:
        self._client.setex(key, ttl_seconds, json.dumps(value, cls=_Encoder))

    def get_version(self) -> int:
        value = self._client.get(self.VERSION_KEY)
        return int(value or 1)

    def bump_version(self) -> int:
        return int(self._client.incr(self.VERSION_KEY))

    def ping(self) -> bool:
        return bool(self._client.ping())

    def close(self) -> None:
        self._client.close()


def create_cache(url: str) -> Cache:
    if url.startswith("memory://"):
        return MemoryTTLCache()
    return RedisCache(url)


def canonical_cache_key(prefix: str, version: int, params: Mapping[str, Any]) -> str:
    normalized = json.dumps(dict(sorted(params.items())), cls=_Encoder, separators=(",", ":"))
    return f"finance-analytics:v{version}:{prefix}:{normalized}"
