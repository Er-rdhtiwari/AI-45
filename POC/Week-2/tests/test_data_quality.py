import json

from expense_ml.data import sha256_file
from expense_ml.modeling import chronological_split
from expense_ml.paths import MANIFEST_PATH, RAW_DATA_PATH
from expense_ml.quality import read_expenses, validate_dataframe


def test_dataset_matches_manifest_and_contract():
    data = read_expenses(RAW_DATA_PATH)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    result = validate_dataframe(data)
    assert result["passed"], result["failures"]
    assert sha256_file(RAW_DATA_PATH) == manifest["sha256"]
    assert len(data) == manifest["row_count"]


def test_chronological_split_has_no_time_overlap():
    splits = chronological_split(read_expenses(RAW_DATA_PATH))
    assert splits["train"]["submitted_at"].max() <= splits["calibration"]["submitted_at"].min()
    assert splits["calibration"]["submitted_at"].max() <= splits["validation"]["submitted_at"].min()
    assert splits["validation"]["submitted_at"].max() <= splits["test"]["submitted_at"].min()
    assert sum(len(frame) for frame in splits.values()) == 12000


def test_protected_and_post_outcome_fields_are_not_features(model_bundle):
    forbidden = {"employee_gender", "employee_id", "expense_id", "audit_completed_at", "is_abnormal"}
    assert forbidden.isdisjoint(model_bundle["features"])
