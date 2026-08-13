from __future__ import annotations

import json
from datetime import UTC, datetime

import joblib
import matplotlib
import numpy as np
import pandas as pd
from sklearn.isotonic import IsotonicRegression

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .config import load_contract, load_project_config
from .data import generate_and_write, sha256_file
from .evaluation import (
    bootstrap_average_precision_interval,
    calibrated_predict,
    calibration_table,
    dump_json,
    fairness_slices,
    policy_metrics,
    select_review_threshold,
)
from .explain import (
    category_values,
    counterfactual_search,
    global_permutation_importance,
    local_contributions,
    numeric_reference_ranges,
    reference_values,
)
from .modeling import (
    build_isolation_forest,
    build_supervised_pipeline,
    chronological_split,
    log_experiment,
    probability_metrics,
    ranking_metrics,
    tuning_candidates,
    xy,
)
from .paths import ARTIFACT_DIR, MANIFEST_PATH, MODEL_PATH, RAW_DATA_PATH, REPORT_DIR
from .quality import read_expenses, validate_or_raise, write_quality_report


def _json_load(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _plot_calibration(raw_table: pd.DataFrame, calibrated_table: pd.DataFrame) -> None:
    fig, axis = plt.subplots(figsize=(7, 6))
    axis.plot([0, 1], [0, 1], linestyle="--", color="gray", label="perfect calibration")
    for table, label, marker in [(raw_table, "raw", "o"), (calibrated_table, "isotonic calibrated", "s")]:
        nonempty = table[table["count"] > 0]
        axis.plot(nonempty["mean_predicted_probability"], nonempty["observed_abnormal_rate"], marker=marker, label=label)
    axis.set(xlabel="Mean predicted probability", ylabel="Observed abnormal rate", title="Test-set calibration")
    axis.legend()
    axis.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(REPORT_DIR / "calibration_plot.png", dpi=150)
    plt.close(fig)


def _split_manifest(splits: dict[str, pd.DataFrame]) -> dict:
    return {
        name: {
            "rows": int(len(frame)),
            "start": frame["submitted_at"].min().isoformat(),
            "end": frame["submitted_at"].max().isoformat(),
            "target_rate": float(frame["is_abnormal"].mean()),
        }
        for name, frame in splits.items()
    }


def run_training() -> dict:
    config = load_project_config()
    contract = load_contract()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    if not RAW_DATA_PATH.exists() or not MANIFEST_PATH.exists():
        generate_and_write()
    manifest = _json_load(MANIFEST_PATH)
    actual_hash = sha256_file(RAW_DATA_PATH)
    if actual_hash != manifest["sha256"]:
        raise ValueError("Dataset hash differs from its manifest")
    data = read_expenses(RAW_DATA_PATH)
    quality = validate_or_raise(data)
    quality["checks"]["manifest_sha256_matches"] = True
    write_quality_report(quality, REPORT_DIR / "data_quality_report.json")

    splits = chronological_split(data)
    dump_json(REPORT_DIR / "split_manifest.json", _split_manifest(splits))
    train_x, train_y = xy(splits["train"])
    calibration_x, calibration_y = xy(splits["calibration"])
    validation_x, validation_y = xy(splits["validation"])
    test_x, test_y = xy(splits["test"])

    experiment_summary: list[dict] = []
    dummy = build_supervised_pipeline("dummy_prior")
    dummy.fit(train_x, train_y)
    dummy_scores = dummy.predict_proba(validation_x)[:, 1]
    dummy_metrics = probability_metrics(validation_y, dummy_scores)
    experiment_summary.append(log_experiment("dummy_prior", "baseline", {}, dummy_metrics))

    default_models: dict[str, object] = {}
    default_metrics: dict[str, dict] = {}
    for model_name in ["logistic_regression", "random_forest", "hist_gradient_boosting"]:
        pipeline = build_supervised_pipeline(model_name)
        pipeline.fit(train_x, train_y)
        scores = pipeline.predict_proba(validation_x)[:, 1]
        metrics = probability_metrics(validation_y, scores)
        default_models[model_name] = pipeline
        default_metrics[model_name] = metrics
        experiment_summary.append(log_experiment(model_name, "untuned_candidate", {}, metrics))

    isolation = build_isolation_forest()
    isolation.fit(train_x)
    anomaly_scores = -isolation.decision_function(validation_x)
    isolation_metrics = ranking_metrics(validation_y, anomaly_scores)
    experiment_summary.append(log_experiment("isolation_forest", "unsupervised_candidate", {"labels_used_for_fit": False}, isolation_metrics))

    selected_family = max(default_metrics, key=lambda name: default_metrics[name]["average_precision"])
    selected_pipeline = default_models[selected_family]
    selected_params: dict = {}
    selected_validation_ap = default_metrics[selected_family]["average_precision"]
    tuning_results: list[dict] = []
    for params in tuning_candidates(selected_family):
        candidate = build_supervised_pipeline(selected_family, params)
        candidate.fit(train_x, train_y)
        scores = candidate.predict_proba(validation_x)[:, 1]
        metrics = probability_metrics(validation_y, scores)
        tuning_results.append({"params": params, "metrics": metrics})
        experiment_summary.append(log_experiment(selected_family, "tuned_candidate", params, metrics))
        if metrics["average_precision"] > selected_validation_ap:
            selected_pipeline = candidate
            selected_params = params
            selected_validation_ap = metrics["average_precision"]

    calibration_raw = selected_pipeline.predict_proba(calibration_x)[:, 1]
    calibrator = IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)
    calibrator.fit(calibration_raw, calibration_y)
    provisional_bundle = {"pipeline": selected_pipeline, "calibrator": calibrator}
    validation_calibrated = calibrated_predict(provisional_bundle, validation_x)
    costs = config["policy"]
    threshold = select_review_threshold(
        validation_y,
        validation_calibrated,
        costs["false_negative_cost_usd"],
        costs["false_positive_review_cost_usd"],
        costs["max_review_rate"] - costs["threshold_selection_capacity_buffer"],
    )
    policy = costs | threshold
    bundle = {
        "pipeline": selected_pipeline,
        "calibrator": calibrator,
        "features": contract["model_features"],
        "reference_values": reference_values(train_x),
        "numeric_ranges": numeric_reference_ranges(train_x),
        "known_categories": category_values(train_x),
        "model_version": config["model_version"],
        "dataset_version": config["dataset_version"],
        "schema_version": config["schema_version"],
        "policy_version": "cost-capacity-policy-v1",
        "policy": policy,
        "selected_family": selected_family,
        "selected_params": selected_params,
        "trained_at_utc": datetime.now(UTC).isoformat(),
        "split_version": "chronological-60-15-10-15-v1",
        "explanation_caveat": "Perturbation explanations describe model behavior, not causality, intent, or guilt.",
    }
    joblib.dump(bundle, MODEL_PATH)
    artifact_manifest = {
        "artifact": MODEL_PATH.name,
        "sha256": sha256_file(MODEL_PATH),
        "model_version": config["model_version"],
        "dataset_version": config["dataset_version"],
        "schema_version": config["schema_version"],
        "selected_family": selected_family,
        "selected_params": selected_params,
        "created_at_utc": bundle["trained_at_utc"],
    }
    dump_json(ARTIFACT_DIR / "artifact_manifest.json", artifact_manifest)

    test_raw = selected_pipeline.predict_proba(test_x)[:, 1]
    test_probabilities = calibrated_predict(bundle, test_x)
    test_quality = probability_metrics(test_y, test_probabilities, policy["review_threshold"])
    test_raw_quality = probability_metrics(test_y, test_raw, policy["review_threshold"])
    operations = policy_metrics(
        test_y,
        test_probabilities,
        policy["review_threshold"],
        costs["false_negative_cost_usd"],
        costs["false_positive_review_cost_usd"],
    )
    uncertainty_interval = bootstrap_average_precision_interval(test_y, test_probabilities, seed=config["random_seed"])

    raw_calibration, raw_ece = calibration_table(test_y, test_raw)
    calibrated_table, calibrated_ece = calibration_table(test_y, test_probabilities)
    raw_calibration.to_csv(REPORT_DIR / "calibration_raw.csv", index=False)
    calibrated_table.to_csv(REPORT_DIR / "calibration_calibrated.csv", index=False)
    _plot_calibration(raw_calibration, calibrated_table)

    fairness, disparities = fairness_slices(splits["test"], test_probabilities, policy["review_threshold"])
    fairness.to_csv(REPORT_DIR / "fairness_slices.csv", index=False)
    dump_json(REPORT_DIR / "fairness_disparities.json", disparities)

    importance = global_permutation_importance(
        selected_pipeline, test_x, test_y, seed=config["random_seed"]
    )
    importance.to_csv(REPORT_DIR / "global_permutation_importance.csv", index=False)
    ranked_indices = np.argsort(-test_probabilities)[:5]
    local_records = []
    counterfactual_records = []
    for index in ranked_indices:
        row = test_x.iloc[[index]]
        local_records.append(
            {
                "expense_id": splits["test"].iloc[index]["expense_id"],
                "probability": float(test_probabilities[index]),
                "contributions": local_contributions(bundle, row),
                "caveat": bundle["explanation_caveat"],
            }
        )
        counterfactual_records.append(
            {
                "expense_id": splits["test"].iloc[index]["expense_id"],
                **counterfactual_search(bundle, row),
            }
        )
    dump_json(REPORT_DIR / "local_explanations.json", local_records)
    dump_json(REPORT_DIR / "counterfactual_explanations.json", counterfactual_records)

    evaluation = {
        "status": "measured_on_untouched_chronological_test_set",
        "model": {
            "selected_family": selected_family,
            "selected_params": selected_params,
            "selected_validation_average_precision": selected_validation_ap,
            "default_candidate_validation_metrics": default_metrics,
            "isolation_forest_validation_ranking_metrics": isolation_metrics,
        },
        "test_rows": int(len(test_y)),
        "test_prevalence": float(test_y.mean()),
        "test_quality_metrics_calibrated": test_quality,
        "test_quality_metrics_raw": test_raw_quality,
        "test_average_precision_95pct_interval": uncertainty_interval,
        "calibration": {
            "raw_expected_calibration_error": raw_ece,
            "calibrated_expected_calibration_error": calibrated_ece,
            "raw_brier_score": test_raw_quality["brier_score"],
            "calibrated_brier_score": test_quality["brier_score"],
        },
        "threshold_policy": policy,
        "test_business_and_operational_metrics": operations,
        "fairness_disparities": disparities,
        "experiment_count_this_run": len(experiment_summary),
        "experiment_ledger": "experiments/experiments.jsonl",
        "latency": {"status": "pending_api_benchmark", "report": "reports/latency_report.json"},
        "performance_target": {
            "minimum_test_average_precision": config["performance_targets"]["minimum_test_average_precision"],
            "passed": bool(test_quality["average_precision"] >= config["performance_targets"]["minimum_test_average_precision"]),
        },
    }
    dump_json(REPORT_DIR / "evaluation.json", evaluation)
    _write_markdown_reports(evaluation, manifest, quality, importance, fairness, artifact_manifest)
    return evaluation


def _write_markdown_reports(evaluation, manifest, quality, importance, fairness, artifact_manifest) -> None:
    q = evaluation["test_quality_metrics_calibrated"]
    op = evaluation["test_business_and_operational_metrics"]
    cal = evaluation["calibration"]
    report = f"""# Evaluation Report\n\nAll numbers below were measured on the newest untouched chronological test split; none are placeholders.\n\n## Selection and data\n\n- Selected model: `{evaluation['model']['selected_family']}` with `{evaluation['model']['selected_params']}`\n- Test rows: {evaluation['test_rows']}\n- Test prevalence: {evaluation['test_prevalence']:.4f}\n- Review threshold: {evaluation['threshold_policy']['review_threshold']:.6f}\n- Capacity constraint: {evaluation['threshold_policy']['max_review_rate']:.2%}\n\n## Quality and calibration\n\n- ROC AUC: {q['roc_auc']:.4f}\n- Average precision: {q['average_precision']:.4f}\n- 95% bootstrap AP interval: [{evaluation['test_average_precision_95pct_interval']['lower']:.4f}, {evaluation['test_average_precision_95pct_interval']['upper']:.4f}]\n- Brier score: {q['brier_score']:.4f}\n- Expected calibration error, raw -> calibrated: {cal['raw_expected_calibration_error']:.4f} -> {cal['calibrated_expected_calibration_error']:.4f}\n\n## Business and operations\n\n- Review rate: {op['review_rate']:.2%}\n- Review precision/yield: {op['review_precision']:.2%}\n- Abnormal recall: {op['abnormal_recall']:.2%}\n- Expected policy cost per 1,000 claims: ${op['expected_cost_per_1000_usd']:,.2f}\n- Estimated cost avoided vs reviewing none on this test sample: ${op['estimated_cost_avoided_vs_no_review_usd']:,.2f}\n\nCosts are scenario assumptions ($500 per missed abnormal claim, $15 per normal claim reviewed), not realized financial savings. The policy is descriptive decision support and requires human review.\n\n## Explainability and fairness\n\nGlobal permutation importance is in `global_permutation_importance.csv`; local and counterfactual examples are separate JSON files. These describe model associations, not causes or employee intent. Fairness slices are descriptive; low support is marked and this synthetic dataset cannot establish legal or real-world fairness.\n"""
    (REPORT_DIR / "evaluation_report.md").write_text(report, encoding="utf-8")
    data_card = f"""# Data Card: {manifest['dataset_version']}\n\n## Purpose and target\n\nSynthetic employee-expense claims for a portfolio ML system. `is_abnormal` is sampled to represent a later completed audit that confirms an abnormal claim. The label is unavailable at submission time.\n\n## Provenance, version, and lineage\n\n- Rows: {manifest['row_count']}\n- Period: {manifest['event_time_min']} to {manifest['event_time_max']}\n- Target rate: {manifest['target_rate']:.4f}\n- Generator seed: {manifest['generator_seed']}\n- SHA-256: `{manifest['sha256']}`\n- Personal/external data: none\n\nSee `configs/data_contract.json`, `data/manifests/expenses_v1.manifest.json`, and `reports/split_manifest.json`. Quality gates passed: {quality['passed']}.\n\n## Sensitive fields and use\n\n`employee_gender` is synthetic, excluded from training/inference, and used only for evaluation. Employee and expense IDs are excluded. Region is a modeled operational field and separately audited.\n\n## Limitations\n\nSynthetic patterns are simpler than real fraud, labels have no investigator disagreement, distribution shift is limited, and rare subgroup estimates are unstable. Do not use this dataset to make claims about real people or populations.\n"""
    (REPORT_DIR / "data_card.md").write_text(data_card, encoding="utf-8")
    model_card = f"""# Model Card: {artifact_manifest['model_version']}\n\n## Intended use\n\nPrioritize expense claims for a trained finance reviewer. Never auto-reject, accuse, discipline, or make employment decisions.\n\n## Model and versions\n\n- Family: `{artifact_manifest['selected_family']}`\n- Parameters selected after baseline: `{artifact_manifest['selected_params']}`\n- Dataset: `{artifact_manifest['dataset_version']}`\n- Schema: `{artifact_manifest['schema_version']}`\n- Artifact SHA-256: `{artifact_manifest['sha256']}`\n\n## Measured performance\n\nSee `evaluation_report.md` and `evaluation.json`. Average precision is {evaluation['test_quality_metrics_calibrated']['average_precision']:.4f}; review rate is {evaluation['test_business_and_operational_metrics']['review_rate']:.2%}. Latency is filled only by the separate API benchmark.\n\n## Fairness, calibration, and explainability\n\nGender is excluded from features. Slice metrics and disparities are in `fairness_slices.csv` and `fairness_disparities.json`. Isotonic calibration uses a dedicated chronological calibration window. Explanations use permutation and reference perturbation; correlated inputs can misattribute importance and counterfactuals are non-causal scenarios.\n\n## Risks and controls\n\nHuman review is mandatory for flagged or abstained cases. Inputs are range-checked, multiple OOD warnings trigger abstention, identifiers are not logged, and each response includes versions plus a feature hash. Monitor drift, subgroup recall/FPR, calibration, review yield, capacity, and overrides before production use.\n"""
    (REPORT_DIR / "model_card.md").write_text(model_card, encoding="utf-8")


if __name__ == "__main__":
    result = run_training()
    print(json.dumps(result, indent=2))
