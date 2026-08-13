import json

from expense_ml.data import sha256_file
from expense_ml.paths import ARTIFACT_DIR, MODEL_PATH, REPORT_DIR


def test_measured_policy_respects_capacity_and_quality_target():
    evaluation = json.loads((REPORT_DIR / "evaluation.json").read_text(encoding="utf-8"))
    operations = evaluation["test_business_and_operational_metrics"]
    assert operations["review_rate"] <= evaluation["threshold_policy"]["max_review_rate"]
    assert evaluation["performance_target"]["passed"]
    assert evaluation["test_quality_metrics_calibrated"]["average_precision"] >= 0.20


def test_artifact_hash_and_version():
    manifest = json.loads((ARTIFACT_DIR / "artifact_manifest.json").read_text(encoding="utf-8"))
    assert sha256_file(MODEL_PATH) == manifest["sha256"]
    assert manifest["model_version"] == "expense-risk-v1"
