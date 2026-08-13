from fastapi.testclient import TestClient

from expense_ml.api import app


VALID_REQUEST = {
    "amount_usd": 430.0,
    "policy_limit_usd": 300.0,
    "days_since_expense": 35,
    "prior_30d_claim_count": 9,
    "prior_30d_total_usd": 3200.0,
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


def test_health_and_prediction():
    client = TestClient(app)
    health = client.get("/health")
    assert health.status_code == 200
    response = client.post("/v1/predict", json=VALID_REQUEST)
    assert response.status_code == 200
    body = response.json()
    assert "abnormal_probability" in body
    assert "reason_codes" in body
    assert body["model_version"] == health.json()["model_version"]


def test_validation_rejects_invalid_and_protected_fields():
    client = TestClient(app)
    invalid = dict(VALID_REQUEST, amount_usd=-1)
    assert client.post("/v1/predict", json=invalid).status_code == 422
    protected = dict(VALID_REQUEST, employee_gender="Female")
    assert client.post("/v1/predict", json=protected).status_code == 422


def test_api_key_when_configured(monkeypatch):
    client = TestClient(app)
    monkeypatch.setenv("EXPENSE_API_KEY", "test-secret")
    assert client.post("/v1/predict", json=VALID_REQUEST).status_code == 401
    assert client.post("/v1/predict", json=VALID_REQUEST, headers={"X-API-Key": "test-secret"}).status_code == 200
