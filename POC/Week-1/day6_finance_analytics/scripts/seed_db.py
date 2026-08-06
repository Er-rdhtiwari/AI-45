from __future__ import annotations

import csv
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sqlalchemy import delete  # noqa: E402

from app.cache import create_cache  # noqa: E402
from app.config import Settings  # noqa: E402
from app.db import Database  # noqa: E402
from app.models import (  # noqa: E402
    Budget,
    CostCentre,
    Department,
    Expense,
    IngestionBatch,
    Vendor,
)
from app.schemas import ExpenseBatchIn  # noqa: E402
from app.services.ingestion import ingest_expenses  # noqa: E402
from scripts.generate_seed import DATA_DIR, generate  # noqa: E402


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA_DIR / name).open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def seed(settings: Settings | None = None) -> dict[str, int]:
    resolved = settings or Settings.from_env()
    generate()
    database = Database(resolved.database_url)
    database.create_schema()
    cache = create_cache(resolved.redis_url)

    with database.session_factory() as session:
        for model in (Expense, IngestionBatch, Budget, Vendor, CostCentre, Department):
            session.execute(delete(model))
        session.commit()

        departments = [Department(code=row["code"], name=row["name"]) for row in read_csv("departments.csv")]
        session.add_all(departments)
        session.flush()
        department_ids = {row.code: row.id for row in departments}

        cost_centres = [
            CostCentre(
                department_id=department_ids[row["department_code"]],
                code=row["code"],
                name=row["name"],
            )
            for row in read_csv("cost_centres.csv")
        ]
        session.add_all(cost_centres)
        session.flush()
        cost_centre_ids = {row.code: row.id for row in cost_centres}

        vendors = [
            Vendor(
                vendor_code=row["vendor_code"],
                name=row["name"],
                risk_tier=row["risk_tier"],
            )
            for row in read_csv("vendors.csv")
        ]
        session.add_all(vendors)
        session.flush()

        budgets = [
            Budget(
                cost_centre_id=cost_centre_ids[row["cost_centre_code"]],
                period=date.fromisoformat(row["period"]),
                amount=Decimal(row["amount"]),
            )
            for row in read_csv("budgets.csv")
        ]
        session.add_all(budgets)
        session.commit()

        payload = ExpenseBatchIn(rows=read_csv("expenses.csv"))
        result = ingest_expenses(
            session,
            cache,
            idempotency_key="deterministic-seed-v1",
            payload=payload,
        )
        counts = {
            "departments": len(departments),
            "cost_centres": len(cost_centres),
            "vendors": len(vendors),
            "budgets": len(budgets),
            "expenses": result.inserted_rows,
        }

    cache.close()
    database.dispose()
    return counts


if __name__ == "__main__":
    result = seed()
    print(f"Seeded: {result}")
