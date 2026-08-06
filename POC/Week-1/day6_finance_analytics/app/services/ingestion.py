from __future__ import annotations

import hashlib
import json
import logging
import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.cache import Cache
from app.exceptions import ConflictError, DomainError
from app.models import Budget, Expense, IngestionBatch
from app.repositories import ingestion as repository
from app.schemas import ExpenseBatchIn, IngestionResult

logger = logging.getLogger("finance.ingestion")


def _payload_hash(payload: ExpenseBatchIn) -> str:
    rows = sorted(
        (row.model_dump(mode="json") for row in payload.rows),
        key=lambda row: (row["source_system"], row["source_record_id"]),
    )
    canonical = json.dumps(rows, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def ingest_expenses(
    session: Session,
    cache: Cache,
    *,
    idempotency_key: str,
    payload: ExpenseBatchIn,
) -> IngestionResult:
    if not idempotency_key.strip():
        raise DomainError("Idempotency-Key header is required")

    digest = _payload_hash(payload)
    existing_batch = repository.get_batch_by_idempotency_key(session, idempotency_key)
    if existing_batch:
        if existing_batch.payload_hash != digest:
            raise ConflictError("idempotency key was already used with a different payload")
        return IngestionResult(
            batch_id=existing_batch.id,
            received_rows=existing_batch.received_rows,
            inserted_rows=existing_batch.inserted_rows,
            replayed=True,
        )

    cost_centres, vendors = repository.reference_maps(session)
    missing_cost_centres = sorted(
        {row.cost_centre_code for row in payload.rows if row.cost_centre_code not in cost_centres}
    )
    missing_vendors = sorted(
        {row.vendor_code for row in payload.rows if row.vendor_code not in vendors}
    )
    if missing_cost_centres or missing_vendors:
        details = []
        if missing_cost_centres:
            details.append(f"unknown cost centres: {', '.join(missing_cost_centres)}")
        if missing_vendors:
            details.append(f"unknown vendors: {', '.join(missing_vendors)}")
        raise DomainError("; ".join(details))

    requested_budget_keys = {
        (cost_centres[row.cost_centre_code], row.period) for row in payload.rows
    }
    available_budget_keys = set(
        session.execute(select(Budget.cost_centre_id, Budget.period)).all()
    )
    missing_budgets = requested_budget_keys - available_budget_keys
    if missing_budgets:
        raise DomainError(
            f"missing monthly budgets for {len(missing_budgets)} cost-centre/period combinations"
        )

    source_keys = [(row.source_system, row.source_record_id) for row in payload.rows]
    existing_source_keys = repository.existing_source_keys(session, source_keys)
    batch_id = str(uuid.uuid4())
    rows_to_insert = [
        row
        for row in payload.rows
        if (row.source_system, row.source_record_id) not in existing_source_keys
    ]

    batch = IngestionBatch(
        id=batch_id,
        idempotency_key=idempotency_key,
        payload_hash=digest,
        status="COMPLETED",
        received_rows=len(payload.rows),
        inserted_rows=len(rows_to_insert),
        created_at=datetime.now(UTC),
    )
    session.add(batch)
    for row in rows_to_insert:
        session.add(
            Expense(
                source_system=row.source_system,
                source_record_id=row.source_record_id,
                cost_centre_id=cost_centres[row.cost_centre_code],
                vendor_id=vendors[row.vendor_code],
                period=row.period,
                transaction_date=row.transaction_date,
                invoice_number=row.invoice_number,
                amount=row.amount,
                approval_status=row.approval_status,
                description=row.description,
                ingestion_batch_id=batch_id,
            )
        )

    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise ConflictError("concurrent ingestion conflict; retry with the same idempotency key") from exc

    cache.bump_version()
    logger.info(
        "ingestion_completed",
        extra={"batch_id": batch_id, "row_count": len(rows_to_insert)},
    )
    return IngestionResult(
        batch_id=batch_id,
        received_rows=len(payload.rows),
        inserted_rows=len(rows_to_insert),
        replayed=False,
    )
