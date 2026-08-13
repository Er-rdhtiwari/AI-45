from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, IsolationForest, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .config import load_contract, load_project_config
from .paths import EXPERIMENT_PATH


NUMERIC_FEATURES = [
    "amount_usd",
    "policy_limit_usd",
    "amount_to_policy_ratio",
    "days_since_expense",
    "prior_30d_claim_count",
    "prior_30d_total_usd",
    "employee_tenure_months",
    "duplicate_7d_count",
]
BOOLEAN_FEATURES = [
    "receipt_attached",
    "weekend_submission",
    "outside_business_hours",
    "cross_border",
]
CATEGORICAL_FEATURES = [
    "region",
    "department",
    "employee_level",
    "expense_category",
    "merchant_risk_tier",
    "country_risk_tier",
    "payment_method",
]


def chronological_split(data: pd.DataFrame) -> dict[str, pd.DataFrame]:
    fractions = load_project_config()["splits"]
    ordered = data.sort_values("submitted_at").reset_index(drop=True)
    n_rows = len(ordered)
    train_end = int(n_rows * fractions["train"])
    calibration_end = train_end + int(n_rows * fractions["calibration"])
    validation_end = calibration_end + int(n_rows * fractions["validation"])
    splits = {
        "train": ordered.iloc[:train_end].copy(),
        "calibration": ordered.iloc[train_end:calibration_end].copy(),
        "validation": ordered.iloc[calibration_end:validation_end].copy(),
        "test": ordered.iloc[validation_end:].copy(),
    }
    for earlier, later in [("train", "calibration"), ("calibration", "validation"), ("validation", "test")]:
        assert splits[earlier]["submitted_at"].max() <= splits[later]["submitted_at"].min()
    return splits


def xy(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    features = load_contract()["model_features"]
    return frame[features].copy(), frame["is_abnormal"].astype(int).copy()


def build_preprocessor(scale_numeric: bool = True) -> ColumnTransformer:
    numeric_steps: list[tuple[str, Any]] = [("impute", SimpleImputer(strategy="median"))]
    if scale_numeric:
        numeric_steps.append(("scale", StandardScaler()))
    numeric = Pipeline(numeric_steps)
    categorical = Pipeline(
        [
            ("impute", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    return ColumnTransformer(
        [
            ("numeric", numeric, NUMERIC_FEATURES + BOOLEAN_FEATURES),
            ("categorical", categorical, CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )


def build_supervised_pipeline(model_name: str, params: dict[str, Any] | None = None) -> Pipeline:
    params = params or {}
    seed = load_project_config()["random_seed"]
    if model_name == "dummy_prior":
        estimator = DummyClassifier(strategy="prior")
    elif model_name == "logistic_regression":
        defaults = {"max_iter": 1000, "random_state": seed}
        estimator = LogisticRegression(**(defaults | params))
    elif model_name == "random_forest":
        defaults = {
            "n_estimators": 220,
            "min_samples_leaf": 3,
            "class_weight": "balanced_subsample",
            "n_jobs": -1,
            "random_state": seed,
        }
        estimator = RandomForestClassifier(**(defaults | params))
    elif model_name == "hist_gradient_boosting":
        defaults = {"max_iter": 160, "learning_rate": 0.08, "random_state": seed}
        estimator = HistGradientBoostingClassifier(**(defaults | params))
    else:
        raise ValueError(f"Unknown model_name={model_name}")
    return Pipeline([("preprocess", build_preprocessor()), ("model", estimator)])


def build_isolation_forest() -> Pipeline:
    seed = load_project_config()["random_seed"]
    return Pipeline(
        [
            ("preprocess", build_preprocessor()),
            (
                "model",
                IsolationForest(
                    n_estimators=220,
                    contamination="auto",
                    random_state=seed,
                    n_jobs=-1,
                ),
            ),
        ]
    )


def probability_metrics(y_true: pd.Series | np.ndarray, scores: np.ndarray, threshold: float = 0.5) -> dict[str, float]:
    y_array = np.asarray(y_true, dtype=int)
    score_array = np.clip(np.asarray(scores, dtype=float), 1e-7, 1 - 1e-7)
    predicted = (score_array >= threshold).astype(int)
    return {
        "roc_auc": float(roc_auc_score(y_array, score_array)),
        "average_precision": float(average_precision_score(y_array, score_array)),
        "brier_score": float(brier_score_loss(y_array, score_array)),
        "log_loss": float(log_loss(y_array, score_array, labels=[0, 1])),
        "precision_at_threshold": float(precision_score(y_array, predicted, zero_division=0)),
        "recall_at_threshold": float(recall_score(y_array, predicted, zero_division=0)),
        "f1_at_threshold": float(f1_score(y_array, predicted, zero_division=0)),
        "positive_rate_at_threshold": float(predicted.mean()),
    }


def ranking_metrics(y_true: pd.Series | np.ndarray, scores: np.ndarray) -> dict[str, float]:
    y_array = np.asarray(y_true, dtype=int)
    score_array = np.asarray(scores, dtype=float)
    return {
        "roc_auc": float(roc_auc_score(y_array, score_array)),
        "average_precision": float(average_precision_score(y_array, score_array)),
    }


def log_experiment(
    model_name: str,
    stage: str,
    params: dict[str, Any],
    validation_metrics: dict[str, float],
    split_version: str = "chronological-60-15-10-15-v1",
) -> dict[str, Any]:
    EXPERIMENT_PATH.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "run_id": f"run-{datetime.now(UTC).strftime('%Y%m%dT%H%M%S%fZ')}",
        "recorded_at_utc": datetime.now(UTC).isoformat(),
        "model_name": model_name,
        "stage": stage,
        "parameters": params,
        "validation_metrics": validation_metrics,
        "split_version": split_version,
        "dataset_version": load_project_config()["dataset_version"],
        "random_seed": load_project_config()["random_seed"],
    }
    with EXPERIMENT_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    return record


def tuning_candidates(model_name: str) -> list[dict[str, Any]]:
    if model_name == "logistic_regression":
        return [
            {"C": 0.3, "class_weight": None},
            {"C": 1.0, "class_weight": None},
            {"C": 1.0, "class_weight": "balanced"},
            {"C": 3.0, "class_weight": None},
        ]
    if model_name == "random_forest":
        return [
            {"max_depth": 8, "min_samples_leaf": 3, "max_features": "sqrt"},
            {"max_depth": 12, "min_samples_leaf": 3, "max_features": "sqrt"},
            {"max_depth": None, "min_samples_leaf": 8, "max_features": 0.7},
            {"max_depth": None, "min_samples_leaf": 3, "max_features": "sqrt"},
        ]
    if model_name == "hist_gradient_boosting":
        return [
            {"learning_rate": 0.05, "max_leaf_nodes": 15, "l2_regularization": 0.1},
            {"learning_rate": 0.08, "max_leaf_nodes": 15, "l2_regularization": 1.0},
            {"learning_rate": 0.05, "max_leaf_nodes": 31, "l2_regularization": 1.0},
            {"learning_rate": 0.10, "max_leaf_nodes": 31, "l2_regularization": 2.0},
        ]
    raise ValueError(f"No tuning grid for {model_name}")
