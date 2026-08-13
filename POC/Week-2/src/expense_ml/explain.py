from __future__ import annotations

import itertools
from typing import Any

import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance

from .evaluation import calibrated_predict


REASON_CODES = {
    "amount_usd": "AMOUNT_SIGNAL",
    "policy_limit_usd": "POLICY_LIMIT_CONTEXT",
    "amount_to_policy_ratio": "POLICY_EXCEEDANCE_SIGNAL",
    "days_since_expense": "LATE_SUBMISSION_SIGNAL",
    "prior_30d_claim_count": "CLAIM_VELOCITY_SIGNAL",
    "prior_30d_total_usd": "RECENT_SPEND_SIGNAL",
    "employee_tenure_months": "TENURE_PATTERN_SIGNAL",
    "duplicate_7d_count": "RECENT_DUPLICATE_SIGNAL",
    "receipt_attached": "RECEIPT_SIGNAL",
    "weekend_submission": "WEEKEND_SIGNAL",
    "outside_business_hours": "SUBMISSION_TIME_SIGNAL",
    "cross_border": "CROSS_BORDER_SIGNAL",
    "region": "REGION_PATTERN_SIGNAL",
    "department": "DEPARTMENT_PATTERN_SIGNAL",
    "employee_level": "LEVEL_PATTERN_SIGNAL",
    "expense_category": "CATEGORY_PATTERN_SIGNAL",
    "merchant_risk_tier": "MERCHANT_RISK_SIGNAL",
    "country_risk_tier": "COUNTRY_RISK_SIGNAL",
    "payment_method": "PAYMENT_METHOD_SIGNAL",
}


def reference_values(train_features: pd.DataFrame) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for column in train_features.columns:
        series = train_features[column]
        if pd.api.types.is_bool_dtype(series) or not pd.api.types.is_numeric_dtype(series):
            values[column] = series.mode(dropna=True).iloc[0].item() if hasattr(series.mode(dropna=True).iloc[0], "item") else series.mode(dropna=True).iloc[0]
        else:
            values[column] = float(series.median())
    return values


def numeric_reference_ranges(train_features: pd.DataFrame) -> dict[str, dict[str, float]]:
    result: dict[str, dict[str, float]] = {}
    for column in train_features.select_dtypes(include=["number"]).columns:
        result[column] = {
            "p01": float(train_features[column].quantile(0.01)),
            "p99": float(train_features[column].quantile(0.99)),
            "min": float(train_features[column].min()),
            "max": float(train_features[column].max()),
        }
    return result


def category_values(train_features: pd.DataFrame) -> dict[str, list[str]]:
    return {
        column: sorted(train_features[column].astype(str).unique().tolist())
        for column in train_features.columns
        if not pd.api.types.is_numeric_dtype(train_features[column]) and not pd.api.types.is_bool_dtype(train_features[column])
    }


def local_contributions(bundle: dict[str, Any], row: pd.DataFrame, top_n: int = 5) -> list[dict[str, Any]]:
    if len(row) != 1:
        raise ValueError("local_contributions expects exactly one row")
    features = bundle["features"]
    base_raw_probability = float(bundle["pipeline"].predict_proba(row[features])[:, 1][0])
    base_probability = float(calibrated_predict(bundle, row[features])[0])
    perturbations = pd.concat([row[features]] * len(features), ignore_index=True)
    for index, feature in enumerate(features):
        perturbations.loc[index, feature] = bundle["reference_values"][feature]
    raw_reference_probabilities = bundle["pipeline"].predict_proba(perturbations)[:, 1]
    reference_probabilities = calibrated_predict(bundle, perturbations)
    contributions = []
    for feature, raw_reference_probability, reference_probability in zip(
        features, raw_reference_probabilities, reference_probabilities
    ):
        raw_delta = base_raw_probability - float(raw_reference_probability)
        calibrated_delta = base_probability - float(reference_probability)
        contributions.append(
            {
                "feature": feature,
                "reason_code": REASON_CODES[feature],
                "observed_value": _json_value(row.iloc[0][feature]),
                "reference_value": _json_value(bundle["reference_values"][feature]),
                "raw_probability_delta_vs_reference": raw_delta,
                "calibrated_probability_delta_vs_reference": calibrated_delta,
                "direction": "raises_risk" if raw_delta > 0 else "lowers_risk" if raw_delta < 0 else "neutral",
            }
        )
    contributions.sort(key=lambda item: abs(item["raw_probability_delta_vs_reference"]), reverse=True)
    return contributions[:top_n]


def _json_value(value: Any) -> Any:
    if hasattr(value, "item"):
        return value.item()
    return value


def global_permutation_importance(
    pipeline: Any,
    features: pd.DataFrame,
    target: pd.Series,
    seed: int,
    repeats: int = 8,
) -> pd.DataFrame:
    result = permutation_importance(
        pipeline,
        features,
        target,
        scoring="average_precision",
        n_repeats=repeats,
        random_state=seed,
        n_jobs=-1,
    )
    return pd.DataFrame(
        {
            "feature": features.columns,
            "importance_mean_ap_decrease": result.importances_mean,
            "importance_std": result.importances_std,
        }
    ).sort_values("importance_mean_ap_decrease", ascending=False)


def counterfactual_search(bundle: dict[str, Any], row: pd.DataFrame, max_changes: int = 3) -> dict[str, Any]:
    threshold = bundle["policy"]["review_threshold"]
    original_probability = float(calibrated_predict(bundle, row[bundle["features"]])[0])
    current = row.iloc[0]
    candidates: list[tuple[str, Any, str]] = []
    if not bool(current["receipt_attached"]):
        candidates.append(("receipt_attached", True, "attach valid receipt evidence"))
    if int(current["duplicate_7d_count"]) > 0:
        candidates.append(("duplicate_7d_count", 0, "resolve a genuinely erroneous duplicate link"))
    if current["payment_method"] != "corporate_card":
        candidates.append(("payment_method", "corporate_card", "use corporate card for a future comparable claim"))
    if int(current["days_since_expense"]) > 7:
        candidates.append(("days_since_expense", 7, "submit a future comparable claim within seven days"))
    if current["merchant_risk_tier"] != "low":
        candidates.append(("merchant_risk_tier", "low", "use a verified low-risk merchant for a future comparable claim"))

    best: dict[str, Any] | None = None
    for size in range(1, min(max_changes, len(candidates)) + 1):
        for combination in itertools.combinations(candidates, size):
            changed = row[bundle["features"]].copy()
            for feature, value, _ in combination:
                changed.loc[changed.index[0], feature] = value
            probability = float(calibrated_predict(bundle, changed)[0])
            proposal = {
                "changes": [
                    {"feature": feature, "from": _json_value(current[feature]), "to": value, "scenario": text}
                    for feature, value, text in combination
                ],
                "resulting_probability": probability,
                "crosses_below_review_threshold": probability < threshold,
            }
            if best is None or probability < best["resulting_probability"]:
                best = proposal
            if probability < threshold:
                best = proposal
                break
        if best and best["crosses_below_review_threshold"]:
            break
    return {
        "original_probability": original_probability,
        "review_threshold": threshold,
        "proposal": best,
        "caveat": "Model-behavior scenario, not causal advice. Never alter truthful historical facts; future-process scenarios require policy review.",
    }
