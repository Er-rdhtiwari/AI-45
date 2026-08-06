from __future__ import annotations

import uuid
from datetime import UTC, date, datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    cost_centres: Mapped[list["CostCentre"]] = relationship(back_populates="department")


class CostCentre(Base):
    __tablename__ = "cost_centres"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    department: Mapped[Department] = relationship(back_populates="cost_centres")


class Vendor(Base):
    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vendor_code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    risk_tier: Mapped[str] = mapped_column(String(10), nullable=False, default="LOW")
    __table_args__ = (
        CheckConstraint("risk_tier IN ('LOW','MEDIUM','HIGH')", name="ck_vendor_risk"),
    )


class Budget(Base):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cost_centre_id: Mapped[int] = mapped_column(ForeignKey("cost_centres.id"), nullable=False)
    period: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    __table_args__ = (
        UniqueConstraint("cost_centre_id", "period", name="uq_budget_cc_period"),
        CheckConstraint("amount >= 0", name="ck_budget_non_negative"),
        Index("ix_budgets_period_cc", "period", "cost_centre_id"),
    )


class IngestionBatch(Base):
    __tablename__ = "ingestion_batches"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    idempotency_key: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)
    payload_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="COMPLETED")
    received_rows: Mapped[int] = mapped_column(nullable=False)
    inserted_rows: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    source_system: Mapped[str] = mapped_column(String(40), nullable=False)
    source_record_id: Mapped[str] = mapped_column(String(100), nullable=False)
    cost_centre_id: Mapped[int] = mapped_column(ForeignKey("cost_centres.id"), nullable=False)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("vendors.id"), nullable=False)
    period: Mapped[date] = mapped_column(Date, nullable=False)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False)
    invoice_number: Mapped[str] = mapped_column(String(80), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    approval_status: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(String(240), nullable=False)
    ingestion_batch_id: Mapped[str] = mapped_column(
        ForeignKey("ingestion_batches.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "source_system", "source_record_id", name="uq_expense_source_record"
        ),
        CheckConstraint("amount > 0", name="ck_expense_positive"),
        CheckConstraint(
            "approval_status IN ('APPROVED','PENDING','REJECTED')",
            name="ck_expense_approval_status",
        ),
        Index("ix_expenses_period_cc", "period", "cost_centre_id"),
        Index("ix_expenses_vendor_period", "vendor_id", "period"),
        Index("ix_expenses_status_period", "approval_status", "period"),
    )
