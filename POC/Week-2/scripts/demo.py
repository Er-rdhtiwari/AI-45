import json

from fastapi.testclient import TestClient

from expense_ml.api import app
from expense_ml.paths import REPORT_DIR


EXAMPLE = {
    "amount_usd": 430.0,
    "policy_limit_usd": 300.0,
    "days_since_expense": 10,
    "prior_30d_claim_count": 7,
    "prior_30d_total_usd": 1200.0,
    "employee_tenure_months": 24,
    "duplicate_7d_count": 1,
    "receipt_attached": False,
    "weekend_submission": True,
    "outside_business_hours": True,
    "cross_border": False,
    "region": "APAC",
    "department": "Sales",
    "employee_level": "IC3-4",
    "expense_category": "Lodging",
    "merchant_risk_tier": "high",
    "country_risk_tier": "medium",
    "payment_method": "personal_card",
}


if __name__ == "__main__":
    evaluation = json.loads((REPORT_DIR / "evaluation.json").read_text(encoding="utf-8"))
    operations = evaluation["test_business_and_operational_metrics"]
    print("MEASURED BUSINESS SUMMARY")
    print(json.dumps({
        "test_claims": evaluation["test_rows"],
        "review_rate": operations["review_rate"],
        "review_yield": operations["review_precision"],
        "abnormal_recall": operations["abnormal_recall"],
        "estimated_cost_avoided_vs_no_review_usd": operations["estimated_cost_avoided_vs_no_review_usd"],
    }, indent=2))
    response = TestClient(app).post("/v1/predict", json=EXAMPLE)
    print("\nLIVE API RESPONSE")
    print(json.dumps(response.json(), indent=2))
