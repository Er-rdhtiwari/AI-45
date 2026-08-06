from __future__ import annotations

from decimal import Decimal


def test_variance_reconciles_and_cache_header_changes(client):
    first = client.get(
        "/v1/analytics/variance",
        headers={"X-Correlation-ID": "day6-test-correlation"},
    )
    assert first.status_code == 200
    assert first.headers["X-Cache"] == "MISS"
    assert first.headers["X-Correlation-ID"] == "day6-test-correlation"
    rows = first.json()
    assert len(rows) == 96
    assert sum(Decimal(row["budget"]) for row in rows) > 0
    assert sum(Decimal(row["actual"]) for row in rows) > 0

    second = client.get("/v1/analytics/variance")
    assert second.status_code == 200
    assert second.headers["X-Cache"] == "HIT"
    assert second.json() == rows


def test_trends_have_rolling_window(client):
    response = client.get("/v1/analytics/trends?department_code=ENG")
    assert response.status_code == 200
    rows = response.json()
    assert len(rows) == 12
    assert Decimal(rows[2]["rolling_3m_actual"]) == sum(
        Decimal(row["actual"]) for row in rows[:3]
    )


def test_statistics_endpoint_returns_real_calculation(client):
    response = client.get("/v1/analytics/statistics/approval-amount-test")
    assert response.status_code == 200
    result = response.json()
    assert result["approved_n"] > 100
    assert result["non_approved_n"] > 100
    assert result["ci_95_low"] < result["mean_difference"] < result["ci_95_high"]
    assert 0 <= result["p_value"] <= 1
    assert len(result["limitations"]) >= 4


def test_invalid_period_range_has_consistent_error(client):
    response = client.get(
        "/v1/analytics/variance?period_from=2025-12-01&period_to=2025-01-01"
    )
    assert response.status_code == 400
    body = response.json()
    assert body["error"]["code"] == "domain_error"
    assert body["error"]["correlation_id"]
