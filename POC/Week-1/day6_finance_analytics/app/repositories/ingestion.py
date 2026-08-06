from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import CostCentre, Expense, IngestionBatch, Vendor


def get_batch_by_idempotency_key(
    session: Session, idempotency_key: str
) -> IngestionBatch | None:
    return session.scalar(
        select(IngestionBatch).where(IngestionBatch.idempotency_key == idempotency_key)
    )


def reference_maps(session: Session) -> tuple[dict[str, int], dict[str, int]]:
    cost_centres = {
        row.code: row.id for row in session.scalars(select(CostCentre)).all()
    }
    vendors = {row.vendor_code: row.id for row in session.scalars(select(Vendor)).all()}
    return cost_centres, vendors


def existing_source_keys(
    session: Session, keys: list[tuple[str, str]]
) -> set[tuple[str, str]]:
    if not keys:
        return set()
    systems = sorted({system for system, _ in keys})
    records = sorted({record for _, record in keys})
    rows = session.execute(
        select(Expense.source_system, Expense.source_record_id).where(
            Expense.source_system.in_(systems), Expense.source_record_id.in_(records)
        )
    ).all()
    return {(row[0], row[1]) for row in rows}
