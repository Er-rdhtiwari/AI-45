from expense_ml.inference import score_record
from expense_ml.modeling import chronological_split, xy
from expense_ml.paths import RAW_DATA_PATH
from expense_ml.quality import read_expenses


def _payload():
    splits = chronological_split(read_expenses(RAW_DATA_PATH))
    features, _ = xy(splits["test"])
    result = features.iloc[0].to_dict()
    result.pop("amount_to_policy_ratio")
    return result


def test_prediction_contains_versions_reasons_and_audit_fields(model_bundle):
    result = score_record(model_bundle, _payload())
    assert 0.0 <= result["abnormal_probability"] <= 1.0
    assert result["model_version"] == "expense-risk-v1"
    assert result["data_version"] == "expenses-synthetic-v1"
    assert len(result["feature_hash_sha256"]) == 64
    assert result["request_id"]
    assert 1 <= len(result["reason_codes"]) <= 3
    assert result["decision"] in {
        "manual_review_ood_abstention",
        "review_high_risk",
        "manual_review_borderline_abstention",
        "auto_clear_recommendation",
    }


def test_multiple_distribution_warnings_trigger_abstention(model_bundle):
    payload = _payload()
    payload.update({"amount_usd": 24999.0, "prior_30d_total_usd": 99999.0, "prior_30d_claim_count": 60})
    result = score_record(model_bundle, payload)
    assert len(result["warnings"]) >= 2
    assert result["decision"] == "manual_review_ood_abstention"
