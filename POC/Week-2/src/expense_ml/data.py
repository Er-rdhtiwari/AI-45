from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd

from .config import load_project_config
from .paths import MANIFEST_PATH, RAW_DATA_PATH


def _sigmoid(value: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-value))


def generate_expenses(row_count: int, seed: int) -> pd.DataFrame:
    """Generate realistic claims; the latent target function is not saved."""
    rng = np.random.default_rng(seed)
    employee_count = max(500, row_count // 12)
    employee_ids = np.array([f"EMP-{idx:05d}" for idx in range(employee_count)])
    profiles = pd.DataFrame(
        {
            "employee_id": employee_ids,
            "employee_gender": rng.choice(
                ["Female", "Male", "Nonbinary"], employee_count, p=[0.47, 0.51, 0.02]
            ),
            "region": rng.choice(
                ["APAC", "EMEA", "LATAM", "North America"],
                employee_count,
                p=[0.29, 0.25, 0.13, 0.33],
            ),
            "department": rng.choice(
                ["Engineering", "Finance", "Operations", "Sales", "Support"],
                employee_count,
                p=[0.25, 0.12, 0.22, 0.27, 0.14],
            ),
            "employee_level": rng.choice(
                ["IC1-2", "IC3-4", "Manager", "Director+"],
                employee_count,
                p=[0.37, 0.36, 0.21, 0.06],
            ),
            "tenure_at_start": rng.integers(0, 180, employee_count),
        }
    ).set_index("employee_id")

    chosen_employees = rng.choice(employee_ids, row_count, replace=True)
    chosen_profiles = profiles.loc[chosen_employees].reset_index()
    minute_offsets = np.sort(rng.integers(0, 730 * 24 * 60, row_count))
    submitted_at = pd.Timestamp("2024-01-01", tz="UTC") + pd.to_timedelta(minute_offsets, unit="m")
    expense_category = rng.choice(
        ["Airfare", "Lodging", "Meals", "Mileage", "Office", "Taxi"],
        row_count,
        p=[0.09, 0.13, 0.29, 0.10, 0.16, 0.23],
    )
    base_limits = {
        "Airfare": 1400.0,
        "Lodging": 350.0,
        "Meals": 100.0,
        "Mileage": 250.0,
        "Office": 500.0,
        "Taxi": 120.0,
    }
    level_factor = {"IC1-2": 0.9, "IC3-4": 1.0, "Manager": 1.15, "Director+": 1.4}
    policy_limit = np.array(
        [base_limits[c] * level_factor[level] for c, level in zip(expense_category, chosen_profiles["employee_level"])]
    )
    amount_ratio = np.clip(rng.lognormal(mean=-0.48, sigma=0.72, size=row_count), 0.02, 8.0)
    amount_usd = np.minimum(np.maximum(policy_limit * amount_ratio, 1.0), 25000.0)
    merchant_risk = rng.choice(["low", "medium", "high"], row_count, p=[0.68, 0.25, 0.07])
    country_risk = rng.choice(["low", "medium", "high"], row_count, p=[0.76, 0.19, 0.05])
    payment_method = rng.choice(
        ["corporate_card", "personal_card", "cash"], row_count, p=[0.61, 0.32, 0.07]
    )
    cross_border = rng.random(row_count) < np.where(expense_category == "Airfare", 0.30, 0.09)
    receipt_probability = np.where(amount_usd > 75.0, 0.91, 0.82)
    receipt_attached = rng.random(row_count) < receipt_probability
    days_since = np.clip(rng.negative_binomial(2, 0.22, row_count), 0, 180)
    prior_count = np.clip(rng.poisson(4.2, row_count), 0, 60)
    prior_total = np.clip(rng.gamma(2.0 + prior_count / 5.0, 260.0), 0, 100000.0)
    duplicate_count = np.clip(rng.poisson(0.055, row_count), 0, 10)
    submit_hour = rng.integers(0, 24, row_count)
    outside_hours = (submit_hour < 7) | (submit_hour > 20)
    weekend = pd.DatetimeIndex(submitted_at).dayofweek >= 5
    months_since_start = ((pd.DatetimeIndex(submitted_at) - pd.Timestamp("2024-01-01", tz="UTC")).days / 30.4).astype(int)
    tenure_months = np.clip(chosen_profiles["tenure_at_start"].to_numpy() + months_since_start, 0, 600)

    latent = (
        -5.25
        + 2.00 * (amount_ratio > 1.0)
        + 1.40 * (amount_ratio > 1.8)
        + 1.50 * (~receipt_attached)
        + 2.50 * (duplicate_count > 0)
        + 1.20 * (merchant_risk == "high")
        + 0.90 * (country_risk == "high")
        + 0.70 * cross_border
        + 0.60 * outside_hours
        + 0.45 * weekend
        + 1.00 * (prior_count >= 8)
        + 0.60 * (payment_method == "cash")
        + 0.80 * (days_since > 30)
        + 1.20 * ((~receipt_attached) & (amount_ratio > 1.2))
        + rng.normal(0.0, 0.24, row_count)
    )
    target = rng.binomial(1, _sigmoid(latent))
    audit_completed_at = submitted_at + pd.to_timedelta(rng.integers(3, 31, row_count), unit="D")

    data = pd.DataFrame(
        {
            "expense_id": [f"EXP-{idx:07d}" for idx in range(row_count)],
            "employee_id": chosen_profiles["employee_id"].to_numpy(),
            "submitted_at": submitted_at,
            "audit_completed_at": audit_completed_at,
            "employee_gender": chosen_profiles["employee_gender"].to_numpy(),
            "region": chosen_profiles["region"].to_numpy(),
            "department": chosen_profiles["department"].to_numpy(),
            "employee_level": chosen_profiles["employee_level"].to_numpy(),
            "expense_category": expense_category,
            "merchant_risk_tier": merchant_risk,
            "country_risk_tier": country_risk,
            "payment_method": payment_method,
            "amount_usd": np.round(amount_usd, 2),
            "policy_limit_usd": np.round(policy_limit, 2),
            "amount_to_policy_ratio": np.round(amount_usd / policy_limit, 4),
            "days_since_expense": days_since.astype(int),
            "prior_30d_claim_count": prior_count.astype(int),
            "prior_30d_total_usd": np.round(prior_total, 2),
            "employee_tenure_months": tenure_months.astype(int),
            "duplicate_7d_count": duplicate_count.astype(int),
            "receipt_attached": receipt_attached.astype(bool),
            "weekend_submission": np.asarray(weekend, dtype=bool),
            "outside_business_hours": outside_hours.astype(bool),
            "cross_border": cross_border.astype(bool),
            "is_abnormal": target.astype(int),
        }
    )
    return data.sort_values("submitted_at").reset_index(drop=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_dataset(data: pd.DataFrame, output_path: Path = RAW_DATA_PATH) -> dict:
    config = load_project_config()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False, date_format="%Y-%m-%dT%H:%M:%SZ")
    manifest = {
        "dataset_version": config["dataset_version"],
        "schema_version": config["schema_version"],
        "created_at_utc": datetime.now(UTC).isoformat(),
        "generator": "expense_ml.data.generate_expenses",
        "generator_seed": config["random_seed"],
        "row_count": int(len(data)),
        "column_count": int(len(data.columns)),
        "event_time_min": data["submitted_at"].min().isoformat(),
        "event_time_max": data["submitted_at"].max().isoformat(),
        "target_rate": float(data["is_abnormal"].mean()),
        "file": str(output_path.relative_to(output_path.parents[2])).replace("\\", "/"),
        "sha256": sha256_file(output_path),
        "lineage": [
            "Deterministic synthetic generator seeded from project_config.json",
            "No external or personal data used",
            "Target sampled from a hidden probabilistic audit-outcome function",
            "Submitted features precede audit_completed_at and target availability"
        ]
    }
    with MANIFEST_PATH.open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
    return manifest


def generate_and_write() -> dict:
    config = load_project_config()
    return write_dataset(generate_expenses(config["row_count"], config["random_seed"]))
