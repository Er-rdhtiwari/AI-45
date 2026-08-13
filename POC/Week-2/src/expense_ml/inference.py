from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

import numpy as np
import pandas as pd

from .evaluation import calibrated_predict
from .explain import local_contributions


def feature_hash(features: dict[str, Any]) -> str:
    canonical = json.dumps(features, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def detect_ood(bundle: dict[str, Any], row: pd.DataFrame) -> list[str]:
    warnings: list[str] = []
    for feature, bounds in bundle["numeric_ranges"].items():
        value = float(row.iloc[0][feature])
        if value < bounds["p01"] or value > bounds["p99"]:
            warnings.append(f"{feature}_outside_training_p01_p99")
    for feature, known in bundle["known_categories"].items():
        if str(row.iloc[0][feature]) not in known:
            warnings.append(f"{feature}_unseen_category")
    return warnings


def score_record(bundle: dict[str, Any], features: dict[str, Any]) -> dict[str, Any]:
    model_features = dict(features)
    model_features["amount_to_policy_ratio"] = features["amount_usd"] / features["policy_limit_usd"]
    row = pd.DataFrame([model_features], columns=bundle["features"])
    probability = float(calibrated_predict(bundle, row)[0])
    warnings = detect_ood(bundle, row)
    threshold = float(bundle["policy"]["review_threshold"])
    band = float(bundle["policy"]["borderline_probability_width"])
    max_warnings = int(bundle["policy"]["max_ood_warnings_before_abstain"])
    if len(warnings) >= max_warnings:
        decision = "manual_review_ood_abstention"
        uncertainty = "out_of_distribution"
    elif probability >= min(1.0, threshold + band):
        decision = "review_high_risk"
        uncertainty = "in_distribution"
    elif probability >= threshold:
        decision = "manual_review_borderline_abstention"
        uncertainty = "borderline_probability"
    else:
        decision = "auto_clear_recommendation"
        uncertainty = "in_distribution"
    explanation = local_contributions(bundle, row, top_n=5)
    positive_reasons = [item for item in explanation if item["raw_probability_delta_vs_reference"] > 0]
    selected_reasons = (positive_reasons or explanation)[:3]
    return {
        "request_id": str(uuid4()),
        "scored_at_utc": datetime.now(UTC).isoformat(),
        "abnormal_probability": probability,
        "review_threshold": threshold,
        "decision": decision,
        "uncertainty_status": uncertainty,
        "reason_codes": [item["reason_code"] for item in selected_reasons],
        "explanation": selected_reasons,
        "warnings": warnings,
        "model_version": bundle["model_version"],
        "data_version": bundle["dataset_version"],
        "schema_version": bundle["schema_version"],
        "policy_version": bundle["policy_version"],
        "feature_hash_sha256": feature_hash(features),
    }
