from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from .config import load_contract


TYPE_CHECKS = {
    "string": lambda s: pd.api.types.is_object_dtype(s) or pd.api.types.is_string_dtype(s),
    "float": pd.api.types.is_numeric_dtype,
    "integer": pd.api.types.is_integer_dtype,
    "boolean": pd.api.types.is_bool_dtype,
    "datetime": pd.api.types.is_datetime64_any_dtype,
}


def read_expenses(path: Path) -> pd.DataFrame:
    data = pd.read_csv(path, parse_dates=["submitted_at", "audit_completed_at"])
    for column in ["receipt_attached", "weekend_submission", "outside_business_hours", "cross_border"]:
        if not pd.api.types.is_bool_dtype(data[column]):
            data[column] = data[column].map({"True": True, "False": False, True: True, False: False})
    return data


def validate_dataframe(data: pd.DataFrame, contract: dict[str, Any] | None = None) -> dict[str, Any]:
    contract = contract or load_contract()
    failures: list[str] = []
    checks: dict[str, Any] = {}
    expected = set(contract["columns"])
    actual = set(data.columns)
    missing_columns = sorted(expected - actual)
    unexpected_columns = sorted(actual - expected)
    checks["missing_columns"] = missing_columns
    checks["unexpected_columns"] = unexpected_columns
    if missing_columns:
        failures.append(f"missing columns: {missing_columns}")
    if unexpected_columns:
        failures.append(f"unexpected columns: {unexpected_columns}")
    if missing_columns:
        return {"passed": False, "failures": failures, "checks": checks}

    for name, spec in contract["columns"].items():
        series = data[name]
        if not spec["nullable"] and series.isna().any():
            failures.append(f"{name}: contains nulls")
        expected_type = spec["type"]
        if not TYPE_CHECKS[expected_type](series):
            failures.append(f"{name}: expected {expected_type}, got {series.dtype}")
        if "allowed" in spec:
            invalid = sorted(set(series.dropna().unique()) - set(spec["allowed"]), key=str)
            if invalid:
                failures.append(f"{name}: invalid values {invalid[:5]}")
        if "min" in spec and (series.dropna() < spec["min"]).any():
            failures.append(f"{name}: value below {spec['min']}")
        if "max" in spec and (series.dropna() > spec["max"]).any():
            failures.append(f"{name}: value above {spec['max']}")

    rules = contract["quality_rules"]
    duplicate_keys = int(data[contract["primary_key"]].duplicated().sum())
    max_missing_rate = float(data.isna().mean().max())
    target_rate = float(data[contract["label"]].mean())
    checks.update(
        {
            "row_count": int(len(data)),
            "duplicate_primary_keys": duplicate_keys,
            "maximum_observed_missing_rate": max_missing_rate,
            "target_rate": target_rate,
            "event_time_monotonic": bool(data[contract["event_time"]].is_monotonic_increasing),
            "audit_after_submission": bool((data["audit_completed_at"] >= data["submitted_at"]).all()),
        }
    )
    if len(data) < rules["minimum_rows"]:
        failures.append("row count below minimum")
    if duplicate_keys > rules["maximum_duplicate_primary_keys"]:
        failures.append("duplicate primary keys exceed maximum")
    if max_missing_rate > rules["maximum_column_missing_rate"]:
        failures.append("missing rate exceeds maximum")
    if not rules["minimum_target_rate"] <= target_rate <= rules["maximum_target_rate"]:
        failures.append("target rate outside allowed range")
    if not checks["event_time_monotonic"]:
        failures.append("events are not sorted chronologically")
    if not checks["audit_after_submission"]:
        failures.append("audit completion precedes submission")

    leaked = set(contract["model_features"]) & set(contract["excluded_columns"])
    checks["leakage_columns_in_features"] = sorted(leaked)
    if leaked:
        failures.append(f"excluded leakage/evaluation columns used as features: {sorted(leaked)}")
    return {"passed": not failures, "failures": failures, "checks": checks}


def validate_or_raise(data: pd.DataFrame) -> dict[str, Any]:
    result = validate_dataframe(data)
    if not result["passed"]:
        raise ValueError("Data contract failed: " + "; ".join(result["failures"]))
    return result


def write_quality_report(result: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
