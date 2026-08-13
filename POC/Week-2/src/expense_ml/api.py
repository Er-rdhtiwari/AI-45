from __future__ import annotations

import hmac
import json
import logging
import os
import time
from threading import Lock
from typing import Literal

import joblib
from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from .inference import score_record
from .paths import MODEL_PATH


logger = logging.getLogger("expense_ml.api")
logging.basicConfig(level=logging.INFO, format="%(message)s")
app = FastAPI(
    title="Abnormal Expense Review API",
    version="1.0.0",
    description="Decision support only; high-risk and uncertain claims require human review.",
)
_bundle = None
_metrics = {"request_count": 0, "error_count": 0, "latency_ms": []}
_metrics_lock = Lock()


class ExpenseRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    amount_usd: float = Field(ge=1.0, le=25000.0)
    policy_limit_usd: float = Field(ge=20.0, le=10000.0)
    days_since_expense: int = Field(ge=0, le=180)
    prior_30d_claim_count: int = Field(ge=0, le=60)
    prior_30d_total_usd: float = Field(ge=0.0, le=100000.0)
    employee_tenure_months: int = Field(ge=0, le=600)
    duplicate_7d_count: int = Field(ge=0, le=10)
    receipt_attached: bool
    weekend_submission: bool
    outside_business_hours: bool
    cross_border: bool
    region: Literal["APAC", "EMEA", "LATAM", "North America"]
    department: Literal["Engineering", "Finance", "Operations", "Sales", "Support"]
    employee_level: Literal["IC1-2", "IC3-4", "Manager", "Director+"]
    expense_category: Literal["Airfare", "Lodging", "Meals", "Mileage", "Office", "Taxi"]
    merchant_risk_tier: Literal["low", "medium", "high"]
    country_risk_tier: Literal["low", "medium", "high"]
    payment_method: Literal["corporate_card", "personal_card", "cash"]


def get_bundle():
    global _bundle
    if _bundle is None:
        if not MODEL_PATH.exists():
            raise HTTPException(status_code=503, detail="Model artifact is not available; run training first")
        try:
            _bundle = joblib.load(MODEL_PATH)
        except Exception as exc:  # pragma: no cover - defensive production boundary
            logger.exception("model_load_failed")
            raise HTTPException(status_code=503, detail="Model artifact could not be loaded") from exc
    return _bundle


def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    expected = os.getenv("EXPENSE_API_KEY")
    if expected and (x_api_key is None or not hmac.compare_digest(expected, x_api_key)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")


@app.get("/health")
def health() -> dict:
    bundle = get_bundle()
    return {
        "status": "ready",
        "model_version": bundle["model_version"],
        "data_version": bundle["dataset_version"],
        "schema_version": bundle["schema_version"],
    }


@app.get("/metrics", dependencies=[Depends(verify_api_key)])
def metrics() -> dict:
    with _metrics_lock:
        latencies = sorted(_metrics["latency_ms"])
        p95 = latencies[min(len(latencies) - 1, int(0.95 * len(latencies)))] if latencies else None
        return {
            "request_count": _metrics["request_count"],
            "error_count": _metrics["error_count"],
            "observed_p95_latency_ms": p95,
            "note": "Process-local demo metrics; use durable telemetry in production.",
        }


@app.post("/v1/predict", dependencies=[Depends(verify_api_key)])
def predict(request: ExpenseRequest) -> dict:
    started = time.perf_counter()
    try:
        result = score_record(get_bundle(), request.model_dump())
        logger.info(
            json.dumps(
                {
                    "event": "prediction_completed",
                    "request_id": result["request_id"],
                    "decision": result["decision"],
                    "model_version": result["model_version"],
                    "feature_hash_sha256": result["feature_hash_sha256"],
                }
            )
        )
        return result
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive production boundary
        with _metrics_lock:
            _metrics["error_count"] += 1
        logger.exception("prediction_failed")
        raise HTTPException(status_code=500, detail="Prediction failed") from exc
    finally:
        elapsed = (time.perf_counter() - started) * 1000
        with _metrics_lock:
            _metrics["request_count"] += 1
            _metrics["latency_ms"].append(elapsed)
            if len(_metrics["latency_ms"]) > 10000:
                _metrics["latency_ms"] = _metrics["latency_ms"][-10000:]
