from __future__ import annotations

from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, Query, Request, Response
from sqlalchemy.orm import Session

from app.api.deps import get_cache, get_session, require_api_key
from app.cache import Cache
from app.exceptions import DomainError
from app.schemas import (
    PaginatedDrilldown,
    PaginatedExceptions,
    StatisticalTestResult,
    TrendItem,
    VarianceItem,
)
from app.services import analytics as service
from app.services.statistics import approval_amount_welch_test

router = APIRouter(
    prefix="/v1/analytics",
    tags=["analytics"],
    dependencies=[Depends(require_api_key)],
)


def _validate_range(period_from: date, period_to: date) -> None:
    if period_from > period_to:
        raise DomainError("period_from must be before or equal to period_to")
    if period_from.day != 1 or period_to.day != 1:
        raise DomainError("period filters must use the first day of a month")


@router.get("/variance", response_model=list[VarianceItem])
def variance_summary(
    request: Request,
    response: Response,
    period_from: date = Query(default=date(2025, 1, 1)),
    period_to: date = Query(default=date(2025, 12, 1)),
    department_code: str | None = Query(default=None, min_length=2, max_length=20),
    session: Session = Depends(get_session),
    cache: Cache = Depends(get_cache),
) -> list[dict[str, object]]:
    _validate_range(period_from, period_to)
    department_code = department_code.upper() if department_code else None
    rows, cache_hit = service.get_variance_summary(
        session,
        cache,
        request.app.state.metrics,
        period_from=period_from,
        period_to=period_to,
        department_code=department_code,
        ttl_seconds=request.app.state.settings.cache_ttl_seconds,
    )
    response.headers["X-Cache"] = "HIT" if cache_hit else "MISS"
    return rows


@router.get("/trends", response_model=list[TrendItem])
def trend_view(
    request: Request,
    response: Response,
    period_from: date = Query(default=date(2025, 1, 1)),
    period_to: date = Query(default=date(2025, 12, 1)),
    department_code: str | None = Query(default=None, min_length=2, max_length=20),
    session: Session = Depends(get_session),
    cache: Cache = Depends(get_cache),
) -> list[dict[str, object]]:
    _validate_range(period_from, period_to)
    department_code = department_code.upper() if department_code else None
    rows, cache_hit = service.get_trend_view(
        session,
        cache,
        request.app.state.metrics,
        period_from=period_from,
        period_to=period_to,
        department_code=department_code,
        ttl_seconds=request.app.state.settings.cache_ttl_seconds,
    )
    response.headers["X-Cache"] = "HIT" if cache_hit else "MISS"
    return rows


@router.get("/exceptions", response_model=PaginatedExceptions)
def top_exceptions(
    period_from: date = Query(default=date(2025, 1, 1)),
    period_to: date = Query(default=date(2025, 12, 1)),
    department_code: str | None = Query(default=None, min_length=2, max_length=20),
    min_amount: Decimal = Query(default=Decimal("1000"), ge=0),
    min_score: Decimal = Query(default=Decimal("25"), ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    cursor: str | None = Query(default=None, max_length=500),
    session: Session = Depends(get_session),
) -> PaginatedExceptions:
    _validate_range(period_from, period_to)
    department_code = department_code.upper() if department_code else None
    try:
        rows, next_cursor = service.get_top_exceptions(
            session,
            period_from=period_from,
            period_to=period_to,
            department_code=department_code,
            min_amount=min_amount,
            min_score=min_score,
            limit=limit,
            cursor=cursor,
        )
    except ValueError as exc:
        raise DomainError(str(exc)) from exc
    return PaginatedExceptions(items=rows, next_cursor=next_cursor)


@router.get("/drilldown", response_model=PaginatedDrilldown)
def drilldown(
    cost_centre_code: str = Query(min_length=2, max_length=30),
    period: date = Query(),
    limit: int = Query(default=20, ge=1, le=100),
    cursor: str | None = Query(default=None, max_length=500),
    session: Session = Depends(get_session),
) -> PaginatedDrilldown:
    if period.day != 1:
        raise DomainError("period must be the first day of a month")
    try:
        rows, next_cursor = service.get_drilldown(
            session,
            cost_centre_code=cost_centre_code.upper(),
            period=period,
            limit=limit,
            cursor=cursor,
        )
    except ValueError as exc:
        raise DomainError(str(exc)) from exc
    return PaginatedDrilldown(items=rows, next_cursor=next_cursor)


@router.get("/statistics/approval-amount-test", response_model=StatisticalTestResult)
def approval_amount_test(
    session: Session = Depends(get_session),
) -> StatisticalTestResult:
    return approval_amount_welch_test(session)
