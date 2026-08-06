from __future__ import annotations

import base64
import json
from datetime import date
from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.exceptions import NotFoundError


def _decode_cursor(cursor: str | None) -> dict[str, Any] | None:
    if not cursor:
        return None
    try:
        padding = "=" * (-len(cursor) % 4)
        payload = base64.urlsafe_b64decode(cursor + padding).decode("utf-8")
        return json.loads(payload)
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid pagination cursor") from exc


def encode_cursor(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def variance_summary(
    session: Session,
    *,
    period_from: date,
    period_to: date,
    department_code: str | None,
) -> list[dict[str, Any]]:
    query = text(
        """
        WITH budgeted AS (
            SELECT d.code AS department_code,
                   d.name AS department_name,
                   b.period AS period,
                   SUM(b.amount) AS budget
            FROM budgets b
            JOIN cost_centres cc ON cc.id = b.cost_centre_id
            JOIN departments d ON d.id = cc.department_id
            WHERE b.period BETWEEN :period_from AND :period_to
              AND (:department_code IS NULL OR d.code = :department_code)
            GROUP BY d.code, d.name, b.period
        ),
        actuals AS (
            SELECT d.code AS department_code,
                   e.period AS period,
                   SUM(e.amount) AS actual
            FROM expenses e
            JOIN cost_centres cc ON cc.id = e.cost_centre_id
            JOIN departments d ON d.id = cc.department_id
            WHERE e.period BETWEEN :period_from AND :period_to
              AND (:department_code IS NULL OR d.code = :department_code)
            GROUP BY d.code, e.period
        )
        SELECT b.department_code,
               b.department_name,
               b.period,
               ROUND(b.budget, 2) AS budget,
               ROUND(COALESCE(a.actual, 0), 2) AS actual,
               ROUND(COALESCE(a.actual, 0) - b.budget, 2) AS variance,
               CASE WHEN b.budget = 0 THEN NULL
                    ELSE ROUND((COALESCE(a.actual, 0) - b.budget) * 100.0 / b.budget, 2)
               END AS variance_pct
        FROM budgeted b
        LEFT JOIN actuals a
          ON a.department_code = b.department_code AND a.period = b.period
        ORDER BY b.period, b.department_code
        """
    )
    rows = session.execute(
        query,
        {
            "period_from": period_from,
            "period_to": period_to,
            "department_code": department_code,
        },
    ).mappings()
    return [dict(row) for row in rows]


def trend_view(
    session: Session,
    *,
    period_from: date,
    period_to: date,
    department_code: str | None,
) -> list[dict[str, Any]]:
    query = text(
        """
        WITH monthly_budget AS (
            SELECT b.period, SUM(b.amount) AS budget
            FROM budgets b
            JOIN cost_centres cc ON cc.id = b.cost_centre_id
            JOIN departments d ON d.id = cc.department_id
            WHERE b.period BETWEEN :period_from AND :period_to
              AND (:department_code IS NULL OR d.code = :department_code)
            GROUP BY b.period
        ),
        monthly_actual AS (
            SELECT e.period, SUM(e.amount) AS actual
            FROM expenses e
            JOIN cost_centres cc ON cc.id = e.cost_centre_id
            JOIN departments d ON d.id = cc.department_id
            WHERE e.period BETWEEN :period_from AND :period_to
              AND (:department_code IS NULL OR d.code = :department_code)
            GROUP BY e.period
        ),
        combined AS (
            SELECT b.period,
                   b.budget,
                   COALESCE(a.actual, 0) AS actual
            FROM monthly_budget b
            LEFT JOIN monthly_actual a ON a.period = b.period
        )
        SELECT period,
               ROUND(budget, 2) AS budget,
               ROUND(actual, 2) AS actual,
               ROUND(actual - budget, 2) AS variance,
               ROUND(
                   SUM(actual) OVER (
                       ORDER BY period ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                   ),
                   2
               ) AS rolling_3m_actual
        FROM combined
        ORDER BY period
        """
    )
    rows = session.execute(
        query,
        {
            "period_from": period_from,
            "period_to": period_to,
            "department_code": department_code,
        },
    ).mappings()
    return [dict(row) for row in rows]


def top_exceptions(
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
    decoded = _decode_cursor(cursor)
    cursor_score = float(decoded["score"]) if decoded else None
    cursor_id = decoded["id"] if decoded else None
    query = text(
        """
        WITH scored AS (
            SELECT e.id AS expense_id,
                   e.period,
                   e.transaction_date,
                   d.code AS department_code,
                   cc.code AS cost_centre_code,
                   v.vendor_code,
                   v.name AS vendor_name,
                   v.risk_tier AS vendor_risk_tier,
                   e.invoice_number,
                   e.amount,
                   e.approval_status,
                   b.amount AS monthly_budget,
                   ROUND(e.amount * 100.0 / NULLIF(b.amount, 0), 2) AS budget_share_pct,
                   ROUND(
                       (e.amount * 100.0 / NULLIF(b.amount, 0))
                       + CASE e.approval_status
                           WHEN 'REJECTED' THEN 50
                           WHEN 'PENDING' THEN 30
                           ELSE 0
                         END
                       + CASE v.risk_tier
                           WHEN 'HIGH' THEN 25
                           WHEN 'MEDIUM' THEN 10
                           ELSE 0
                         END,
                       2
                   ) AS exception_score
            FROM expenses e
            JOIN cost_centres cc ON cc.id = e.cost_centre_id
            JOIN departments d ON d.id = cc.department_id
            JOIN vendors v ON v.id = e.vendor_id
            JOIN budgets b ON b.cost_centre_id = e.cost_centre_id AND b.period = e.period
            WHERE e.period BETWEEN :period_from AND :period_to
              AND (:department_code IS NULL OR d.code = :department_code)
              AND e.amount >= :min_amount
        )
        SELECT *
        FROM scored
        WHERE exception_score >= :min_score
          AND (
              :cursor_score IS NULL
              OR exception_score < :cursor_score
              OR (exception_score = :cursor_score AND expense_id > :cursor_id)
          )
        ORDER BY exception_score DESC, expense_id ASC
        LIMIT :fetch_limit
        """
    )
    result = [
        dict(row)
        for row in session.execute(
            query,
            {
                "period_from": period_from,
                "period_to": period_to,
                "department_code": department_code,
                "min_amount": float(min_amount),
                "min_score": float(min_score),
                "cursor_score": cursor_score,
                "cursor_id": cursor_id,
                "fetch_limit": limit + 1,
            },
        ).mappings()
    ]
    next_cursor = None
    if len(result) > limit:
        result = result[:limit]
        last = result[-1]
        next_cursor = encode_cursor(
            {"score": str(last["exception_score"]), "id": last["expense_id"]}
        )
    return result, next_cursor


def drilldown(
    session: Session,
    *,
    cost_centre_code: str,
    period: date,
    limit: int,
    cursor: str | None,
) -> tuple[list[dict[str, Any]], str | None]:
    decoded = _decode_cursor(cursor)
    cursor_date = date.fromisoformat(decoded["date"]) if decoded else None
    cursor_id = decoded["id"] if decoded else None
    exists = session.execute(
        text("SELECT 1 FROM cost_centres WHERE code = :code"), {"code": cost_centre_code}
    ).first()
    if not exists:
        raise NotFoundError(f"cost centre {cost_centre_code} not found")
    query = text(
        """
        SELECT e.id AS expense_id,
               e.transaction_date,
               v.vendor_code,
               v.name AS vendor_name,
               e.invoice_number,
               e.amount,
               e.approval_status,
               e.description
        FROM expenses e
        JOIN cost_centres cc ON cc.id = e.cost_centre_id
        JOIN vendors v ON v.id = e.vendor_id
        WHERE cc.code = :cost_centre_code
          AND e.period = :period
          AND (
              :cursor_date IS NULL
              OR e.transaction_date < :cursor_date
              OR (e.transaction_date = :cursor_date AND e.id > :cursor_id)
          )
        ORDER BY e.transaction_date DESC, e.id ASC
        LIMIT :fetch_limit
        """
    )
    rows = [
        dict(row)
        for row in session.execute(
            query,
            {
                "cost_centre_code": cost_centre_code,
                "period": period,
                "cursor_date": cursor_date,
                "cursor_id": cursor_id,
                "fetch_limit": limit + 1,
            },
        ).mappings()
    ]
    next_cursor = None
    if len(rows) > limit:
        rows = rows[:limit]
        last = rows[-1]
        next_cursor = encode_cursor(
            {"date": str(last["transaction_date"]), "id": last["expense_id"]}
        )
    return rows, next_cursor


def amounts_by_approval(session: Session) -> tuple[list[float], list[float]]:
    rows = session.execute(
        text("SELECT amount, approval_status FROM expenses ORDER BY id")
    ).mappings()
    approved: list[float] = []
    non_approved: list[float] = []
    for row in rows:
        target = approved if row["approval_status"] == "APPROVED" else non_approved
        target.append(float(row["amount"]))
    return approved, non_approved


def reconciliation_totals(session: Session) -> dict[str, Decimal]:
    row = session.execute(
        text(
            """
            SELECT
              (SELECT COALESCE(SUM(amount), 0) FROM budgets) AS budget_total,
              (SELECT COALESCE(SUM(amount), 0) FROM expenses) AS actual_total
            """
        )
    ).mappings().one()
    return {"budget_total": Decimal(row["budget_total"]), "actual_total": Decimal(row["actual_total"])}
