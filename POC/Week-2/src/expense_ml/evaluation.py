from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    precision_score,
    recall_score,
    roc_auc_score,
)


def calibrated_predict(bundle: dict[str, Any], features: pd.DataFrame) -> np.ndarray:
    raw = bundle["pipeline"].predict_proba(features)[:, 1]
    return np.clip(bundle["calibrator"].predict(raw), 0.0, 1.0)


def select_review_threshold(
    y_true: pd.Series | np.ndarray,
    probabilities: np.ndarray,
    false_negative_cost: float,
    false_positive_cost: float,
    max_review_rate: float,
) -> dict[str, float]:
    y = np.asarray(y_true, dtype=int)
    probabilities = np.asarray(probabilities, dtype=float)
    candidates = np.unique(np.r_[probabilities, np.nextafter(probabilities.max(), np.inf)])
    feasible: list[dict[str, float]] = []
    for threshold in candidates:
        reviewed = probabilities >= threshold
        review_rate = float(reviewed.mean())
        if review_rate > max_review_rate + 1e-12:
            continue
        false_negatives = int(((~reviewed) & (y == 1)).sum())
        false_positives = int((reviewed & (y == 0)).sum())
        total_cost = false_negatives * false_negative_cost + false_positives * false_positive_cost
        feasible.append(
            {
                "review_threshold": float(threshold),
                "validation_review_rate": review_rate,
                "validation_false_negatives": false_negatives,
                "validation_false_positives": false_positives,
                "validation_total_cost_usd": float(total_cost),
            }
        )
    if not feasible:
        raise ValueError("No threshold satisfies review capacity")
    return min(feasible, key=lambda item: (item["validation_total_cost_usd"], -item["validation_review_rate"]))


def policy_metrics(
    y_true: pd.Series | np.ndarray,
    probabilities: np.ndarray,
    threshold: float,
    false_negative_cost: float,
    false_positive_cost: float,
) -> dict[str, float | int]:
    y = np.asarray(y_true, dtype=int)
    reviewed = np.asarray(probabilities) >= threshold
    tn, fp, fn, tp = confusion_matrix(y, reviewed.astype(int), labels=[0, 1]).ravel()
    total_cost = fn * false_negative_cost + fp * false_positive_cost
    no_review_cost = int(y.sum()) * false_negative_cost
    return {
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
        "review_rate": float(reviewed.mean()),
        "review_precision": float(precision_score(y, reviewed, zero_division=0)),
        "abnormal_recall": float(recall_score(y, reviewed, zero_division=0)),
        "expected_policy_cost_usd": float(total_cost),
        "expected_cost_per_1000_usd": float(total_cost / len(y) * 1000),
        "no_review_cost_usd": float(no_review_cost),
        "estimated_cost_avoided_vs_no_review_usd": float(no_review_cost - total_cost),
    }


def calibration_table(y_true: pd.Series | np.ndarray, probabilities: np.ndarray, bins: int = 10) -> tuple[pd.DataFrame, float]:
    frame = pd.DataFrame({"target": np.asarray(y_true), "probability": np.asarray(probabilities)})
    edges = np.linspace(0.0, 1.0, bins + 1)
    frame["bin"] = pd.cut(frame["probability"], bins=edges, include_lowest=True, duplicates="drop")
    table = (
        frame.groupby("bin", observed=False)
        .agg(count=("target", "size"), mean_predicted_probability=("probability", "mean"), observed_abnormal_rate=("target", "mean"))
        .reset_index()
    )
    table["bin"] = table["bin"].astype(str)
    nonempty = table["count"] > 0
    ece = float(
        (
            table.loc[nonempty, "count"]
            / len(frame)
            * (table.loc[nonempty, "mean_predicted_probability"] - table.loc[nonempty, "observed_abnormal_rate"]).abs()
        ).sum()
    )
    return table, ece


def fairness_slices(
    test_frame: pd.DataFrame,
    probabilities: np.ndarray,
    threshold: float,
    group_columns: tuple[str, ...] = ("employee_gender", "region"),
) -> tuple[pd.DataFrame, dict[str, Any]]:
    records: list[dict[str, Any]] = []
    y_all = test_frame["is_abnormal"].to_numpy()
    for column in group_columns:
        for group in sorted(test_frame[column].unique()):
            mask = test_frame[column].to_numpy() == group
            y = y_all[mask]
            scores = probabilities[mask]
            predicted = scores >= threshold
            tn, fp, fn, tp = confusion_matrix(y, predicted.astype(int), labels=[0, 1]).ravel()
            records.append(
                {
                    "slice_feature": column,
                    "slice_value": group,
                    "n": int(mask.sum()),
                    "positives": int(y.sum()),
                    "prevalence": float(y.mean()),
                    "selection_rate": float(predicted.mean()),
                    "precision": float(precision_score(y, predicted, zero_division=0)),
                    "recall_tpr": float(recall_score(y, predicted, zero_division=0)),
                    "false_positive_rate": float(fp / (fp + tn)) if (fp + tn) else float("nan"),
                    "false_negative_rate": float(fn / (fn + tp)) if (fn + tp) else float("nan"),
                    "average_precision": float(average_precision_score(y, scores)) if len(np.unique(y)) == 2 else float("nan"),
                    "support_note": "low_support" if mask.sum() < 100 or y.sum() < 10 else "adequate_for_directional_audit",
                }
            )
    result = pd.DataFrame(records)
    disparities: dict[str, Any] = {}
    for column in group_columns:
        subset = result[result["slice_feature"] == column]
        disparities[column] = {
            "selection_rate_max_minus_min": float(subset["selection_rate"].max() - subset["selection_rate"].min()),
            "recall_tpr_max_minus_min": float(subset["recall_tpr"].max() - subset["recall_tpr"].min()),
            "false_positive_rate_max_minus_min": float(subset["false_positive_rate"].max() - subset["false_positive_rate"].min()),
            "caveat": "Descriptive, not a legal fairness determination; small groups and synthetic data create uncertainty."
        }
    return result, disparities


def bootstrap_average_precision_interval(
    y_true: pd.Series | np.ndarray,
    probabilities: np.ndarray,
    samples: int = 300,
    seed: int = 45,
) -> dict[str, float | int]:
    rng = np.random.default_rng(seed)
    y = np.asarray(y_true)
    probabilities = np.asarray(probabilities)
    values: list[float] = []
    for _ in range(samples):
        indices = rng.integers(0, len(y), len(y))
        if len(np.unique(y[indices])) < 2:
            continue
        values.append(float(average_precision_score(y[indices], probabilities[indices])))
    return {
        "method": "nonparametric_bootstrap",
        "confidence_level": 0.95,
        "samples_requested": samples,
        "samples_used": len(values),
        "lower": float(np.quantile(values, 0.025)),
        "upper": float(np.quantile(values, 0.975)),
    }


def dump_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, default=str, allow_nan=False)
