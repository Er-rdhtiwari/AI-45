from __future__ import annotations

import json
import logging
import time

import numpy as np
from fastapi.testclient import TestClient

from expense_ml.api import app, logger
from expense_ml.evaluation import dump_json
from expense_ml.paths import REPORT_DIR


PAYLOAD = {
    "amount_usd": 430.0,
    "policy_limit_usd": 300.0,
    "days_since_expense": 10,
    "prior_30d_claim_count": 7,
    "prior_30d_total_usd": 1200.0,
    "employee_tenure_months": 24,
    "duplicate_7d_count": 1,
    "receipt_attached": False,
    "weekend_submission": True,
    "outside_business_hours": True,
    "cross_border": False,
    "region": "APAC",
    "department": "Sales",
    "employee_level": "IC3-4",
    "expense_category": "Lodging",
    "merchant_risk_tier": "high",
    "country_risk_tier": "medium",
    "payment_method": "personal_card",
}


def benchmark(requests: int = 150, warmup: int = 10) -> dict:
    logger.setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    client = TestClient(app)
    for _ in range(warmup):
        assert client.post("/v1/predict", json=PAYLOAD).status_code == 200
    latencies = []
    failures = 0
    wall_started = time.perf_counter()
    for _ in range(requests):
        started = time.perf_counter()
        response = client.post("/v1/predict", json=PAYLOAD)
        latencies.append((time.perf_counter() - started) * 1000)
        failures += int(response.status_code != 200)
    wall_seconds = time.perf_counter() - wall_started
    target_ms = 100.0
    report = {
        "status": "measured_local_in_process_testclient",
        "measured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "requests": requests,
        "warmup_requests": warmup,
        "failures": failures,
        "sequential_throughput_requests_per_second": requests / wall_seconds,
        "latency_ms": {
            "mean": float(np.mean(latencies)),
            "p50": float(np.percentile(latencies, 50)),
            "p95": float(np.percentile(latencies, 95)),
            "p99": float(np.percentile(latencies, 99)),
            "max": float(np.max(latencies)),
        },
        "target_p95_latency_ms": target_ms,
        "target_passed": bool(np.percentile(latencies, 95) < target_ms),
        "caveat": "In-process Windows TestClient benchmark; excludes network, gateway, concurrency, and production logging overhead.",
    }
    dump_json(REPORT_DIR / "latency_report.json", report)
    evaluation_path = REPORT_DIR / "evaluation.json"
    evaluation = json.loads(evaluation_path.read_text(encoding="utf-8"))
    evaluation["latency"] = report
    dump_json(evaluation_path, evaluation)
    return report


if __name__ == "__main__":
    print(json.dumps(benchmark(), indent=2))
