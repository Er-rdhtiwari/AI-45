from __future__ import annotations

import argparse
import statistics
import time

import httpx


def percentile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    index = (len(ordered) - 1) * p
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = index - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("--iterations", type=int, default=300)
    args = parser.parse_args()
    url = f"{args.base_url.rstrip('/')}/v1/analytics/variance"

    with httpx.Client(timeout=10.0) as client:
        first = client.get(url)
        first.raise_for_status()
        print(f"Priming response X-Cache={first.headers.get('X-Cache')}")
        values: list[float] = []
        cache_headers: dict[str, int] = {}
        for _ in range(args.iterations):
            started = time.perf_counter_ns()
            response = client.get(url)
            elapsed = (time.perf_counter_ns() - started) / 1_000_000
            response.raise_for_status()
            values.append(elapsed)
            cache_header = response.headers.get("X-Cache", "UNKNOWN")
            cache_headers[cache_header] = cache_headers.get(cache_header, 0) + 1

    print(
        {
            "iterations": args.iterations,
            "mean_ms": round(statistics.fmean(values), 4),
            "p50_ms": round(percentile(values, 0.50), 4),
            "p95_ms": round(percentile(values, 0.95), 4),
            "cache_headers": cache_headers,
        }
    )


if __name__ == "__main__":
    main()
