from __future__ import annotations

from fastapi import APIRouter, Depends, Header, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_cache, get_session, require_api_key
from app.cache import Cache
from app.schemas import ExpenseBatchIn, IngestionResult
from app.services.ingestion import ingest_expenses

router = APIRouter(
    prefix="/v1/ingestion",
    tags=["ingestion"],
    dependencies=[Depends(require_api_key)],
)


@router.post(
    "/expenses",
    response_model=IngestionResult,
    status_code=status.HTTP_201_CREATED,
)
def ingest_expense_batch(
    payload: ExpenseBatchIn,
    response: Response,
    idempotency_key: str = Header(alias="Idempotency-Key", min_length=1, max_length=160),
    session: Session = Depends(get_session),
    cache: Cache = Depends(get_cache),
) -> IngestionResult:
    result = ingest_expenses(
        session,
        cache,
        idempotency_key=idempotency_key,
        payload=payload,
    )
    if result.replayed:
        response.status_code = status.HTTP_200_OK
    return result
