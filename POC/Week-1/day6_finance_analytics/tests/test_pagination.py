from __future__ import annotations


def test_exception_cursor_is_stable_without_overlap(client):
    first = client.get("/v1/analytics/exceptions?limit=7")
    assert first.status_code == 200
    first_body = first.json()
    assert len(first_body["items"]) == 7
    assert first_body["next_cursor"]

    second = client.get(
        "/v1/analytics/exceptions",
        params={"limit": 7, "cursor": first_body["next_cursor"]},
    )
    assert second.status_code == 200
    second_body = second.json()
    first_ids = {row["expense_id"] for row in first_body["items"]}
    second_ids = {row["expense_id"] for row in second_body["items"]}
    assert first_ids.isdisjoint(second_ids)

    first_scores = [float(row["exception_score"]) for row in first_body["items"]]
    second_scores = [float(row["exception_score"]) for row in second_body["items"]]
    assert first_scores == sorted(first_scores, reverse=True)
    assert min(first_scores) >= max(second_scores)


def test_invalid_cursor_is_rejected(client):
    response = client.get("/v1/analytics/exceptions?cursor=not-valid")
    assert response.status_code == 400
    assert response.json()["error"]["message"] == "invalid pagination cursor"


def test_drilldown_paginates(client):
    first = client.get(
        "/v1/analytics/drilldown",
        params={"cost_centre_code": "ENG-01", "period": "2025-01-01", "limit": 3},
    )
    assert first.status_code == 200
    body = first.json()
    assert 1 <= len(body["items"]) <= 3
    if body["next_cursor"]:
        second = client.get(
            "/v1/analytics/drilldown",
            params={
                "cost_centre_code": "ENG-01",
                "period": "2025-01-01",
                "limit": 3,
                "cursor": body["next_cursor"],
            },
        )
        assert second.status_code == 200
        assert {item["expense_id"] for item in body["items"]}.isdisjoint(
            {item["expense_id"] for item in second.json()["items"]}
        )
