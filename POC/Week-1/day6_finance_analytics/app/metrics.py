from __future__ import annotations

import threading
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class MetricsRegistry:
    _lock: threading.Lock = field(default_factory=threading.Lock)
    requests_total: int = 0
    errors_total: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    request_latency_ms_sum: float = 0.0
    status_counts: dict[int, int] = field(default_factory=lambda: defaultdict(int))

    def observe_request(self, status_code: int, duration_ms: float) -> None:
        with self._lock:
            self.requests_total += 1
            self.request_latency_ms_sum += duration_ms
            self.status_counts[status_code] += 1
            if status_code >= 500:
                self.errors_total += 1

    def observe_cache(self, hit: bool) -> None:
        with self._lock:
            if hit:
                self.cache_hits += 1
            else:
                self.cache_misses += 1

    def snapshot(self) -> dict[str, object]:
        with self._lock:
            total_cache = self.cache_hits + self.cache_misses
            return {
                "requests_total": self.requests_total,
                "errors_total": self.errors_total,
                "average_request_latency_ms": (
                    self.request_latency_ms_sum / self.requests_total
                    if self.requests_total
                    else 0.0
                ),
                "cache_hits": self.cache_hits,
                "cache_misses": self.cache_misses,
                "cache_hit_ratio": self.cache_hits / total_cache if total_cache else 0.0,
                "status_counts": dict(self.status_counts),
            }
