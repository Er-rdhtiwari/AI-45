from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any, Callable

from sqlalchemy.orm import Session

from app.cache import Cache, canonical_cache_key
from app.metrics import MetricsRegistry
from app.repositories import analytics as repository


def _cached(
    cache: Cache,
    metrics: MetricsRegistry,
    *,
    prefix: str,
    params: dict[str, Any],
    ttl_seconds: int,
    loader: Callable[[], list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], bool]:
    key = canonical_cache_key(prefix, cache.get_version(), params)
    cached = cache.get_json(key)
    if cached is not None:
        metrics.observe_cache(True)
        return cached, True
    metrics.observe_cache(False)
    loaded = loader()
    cache.set_json(key, loaded, ttl_seconds)
    return loaded, False


def get_variance_summary(
    session: Session,
    cache: Cache,
    metrics: MetricsRegistry,
    *,
    period_from: date,
    period_to: date,
    department_code: str | None,
    ttl_seconds: int,
) -> tuple[list[dict[str, Any]], bool]:
    return _cached(
        cache,
        metrics,
        prefix="variance",
        params={
            "period_from": period_from,
            "period_to": period_to,
            "department_code": department_code,
        },
        ttl_seconds=ttl_seconds,
        loader=lambda: repository.variance_summary(
            session,
            period_from=period_from,
            period_to=period_to,
            department_code=department_code,
        ),
    )


def get_trend_view(
    session: Session,
    cache: Cache,
    metrics: MetricsRegistry,
    *,
    period_from: date,
    period_to: date,
    department_code: str | None,
    ttl_seconds: int,
) -> tuple[list[dict[str, Any]], bool]:
    return _cached(
        cache,
        metrics,
        prefix="trend",
        params={
            "period_from": period_from,
            "period_to": period_to,
            "department_code": department_code,
        },
        ttl_seconds=ttl_seconds,
        loader=lambda: repository.trend_view(
            session,
            period_from=period_from,
            period_to=period_to,
            department_code=department_code,
        ),
    )


def get_top_exceptions(
    session: Session,
    *,
    period_from: date,
    period_to: date,
    department_code: str | None,
    min_amount: Decimal,
    min_score: Decimal,
    limit: int,
    cursor: str | None,
) -> tuple[list[dict[str, Any]], str | None]:
    rows, next_cursor = repository.top_exceptions(
        session,
        period_from=period_from,
        period_to=period_to,
        department_code=department_code,
        min_amount=min_amount,
        min_score=min_score,
        limit=limit,
        cursor=cursor,
    )
    for row in rows:
        reasons: list[str] = []
        if row["approval_status"] == "PENDING":
            reasons.append("approval_pending")
        elif row["approval_status"] == "REJECTED":
            reasons.append("approval_rejected")
        if row["vendor_risk_tier"] == "HIGH":
            reasons.append("high_risk_vendor")
        elif row["vendor_risk_tier"] == "MEDIUM":
            reasons.append("medium_risk_vendor")
        if Decimal(row["budget_share_pct"]) >= Decimal("20"):
            reasons.append("large_share_of_monthly_budget")
        row["exception_reasons"] = reasons or ["high_composite_score"]
    return rows, next_cursor


def get_drilldown(
    session: Session,
    *,
    cost_centre_code: str,
    period: date,
    limit: int,
    cursor: str | None,
) -> tuple[list[dict[str, Any]], str | None]:
    return repository.drilldown(
        session,
        cost_centre_code=cost_centre_code,
        period=period,
        limit=limit,
        cursor=cursor,
    )
