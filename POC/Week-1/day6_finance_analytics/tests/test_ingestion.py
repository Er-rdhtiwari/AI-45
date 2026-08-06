from __future__ import annotations


def valid_payload(record_id: str = "MANUAL-0001", amount: str = "1250.50") -> dict:
    return {
        "rows": [
            {
                "source_system": "MANUAL",
                "source_record_id": record_id,
                "cost_centre_code": "FIN-01",
                "vendor_code": "V001",
                "period": "2025-01-01",
                "transaction_date": "2025-01-15",
                "invoice_number": f"INV-{record_id}",
                "amount": amount,
                "approval_status": "APPROVED",
                "description": "Manual adjustment for test",
            }
        ]
    }


def test_ingestion_is_idempotent(client):
    headers = {"Idempotency-Key": "test-idempotency-key"}
    first = client.post("/v1/ingestion/expenses", headers=headers, json=valid_payload())
    assert first.status_code == 201
    assert first.json()["inserted_rows"] == 1
    assert first.json()["replayed"] is False

    replay = client.post("/v1/ingestion/expenses", headers=headers, json=valid_payload())
    assert replay.status_code == 200
    assert replay.json()["batch_id"] == first.json()["batch_id"]
    assert replay.json()["replayed"] is True


def test_idempotency_key_reuse_with_different_payload_conflicts(client):
    headers = {"Idempotency-Key": "same-key-different-payload"}
    assert client.post(
        "/v1/ingestion/expenses", headers=headers, json=valid_payload("MANUAL-0002")
    ).status_code == 201
    conflict = client.post(
        "/v1/ingestion/expenses",
        headers=headers,
        json=valid_payload("MANUAL-0002", amount="9999.00"),
    )
    assert conflict.status_code == 409
    assert conflict.json()["error"]["code"] == "conflict"


def test_ingestion_validation_rejects_cross_period_date(client):
    payload = valid_payload("MANUAL-0003")
    payload["rows"][0]["transaction_date"] = "2025-02-01"
    response = client.post(
        "/v1/ingestion/expenses",
        headers={"Idempotency-Key": "invalid-date"},
        json=payload,
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


def test_ingestion_invalidates_analytics_cache(client):
    assert client.get("/v1/analytics/variance").headers["X-Cache"] == "MISS"
    assert client.get("/v1/analytics/variance").headers["X-Cache"] == "HIT"
    response = client.post(
        "/v1/ingestion/expenses",
        headers={"Idempotency-Key": "cache-invalidation"},
        json=valid_payload("MANUAL-0004"),
    )
    assert response.status_code == 201
    assert client.get("/v1/analytics/variance").headers["X-Cache"] == "MISS"
