from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

ApprovalStatus = Literal["APPROVED", "PENDING", "REJECTED"]


class ExpenseIn(BaseModel):
    source_system: str = Field(min_length=1, max_length=40)
    source_record_id: str = Field(min_length=1, max_length=100)
    cost_centre_code: str = Field(min_length=1, max_length=30)
    vendor_code: str = Field(min_length=1, max_length=30)
    period: date
    transaction_date: date
    invoice_number: str = Field(min_length=1, max_length=80)
    amount: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    approval_status: ApprovalStatus
    description: str = Field(min_length=1, max_length=240)

    @field_validator("source_system", "source_record_id", "invoice_number", mode="before")
    @classmethod
    def strip_required(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value

    @field_validator("cost_centre_code", "vendor_code", "approval_status", mode="before")
    @classmethod
    def normalize_codes(cls, value: object) -> object:
        return value.strip().upper() if isinstance(value, str) else value

    @model_validator(mode="after")
    def dates_are_consistent(self) -> "ExpenseIn":
        if self.period.day != 1:
            raise ValueError("period must be the first day of the month")
        if (self.transaction_date.year, self.transaction_date.month) != (
            self.period.year,
            self.period.month,
        ):
            raise ValueError("transaction_date must fall inside period")
        return self


class ExpenseBatchIn(BaseModel):
    rows: list[ExpenseIn] = Field(min_length=1, max_length=5000)

    @model_validator(mode="after")
    def unique_source_records(self) -> "ExpenseBatchIn":
        keys = [(row.source_system, row.source_record_id) for row in self.rows]
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate source_system/source_record_id inside payload")
        return self


class IngestionResult(BaseModel):
    batch_id: str
    received_rows: int
    inserted_rows: int
    replayed: bool


class VarianceItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    department_code: str
    department_name: str
    period: date
    budget: Decimal
    actual: Decimal
    variance: Decimal
    variance_pct: Decimal | None


class TrendItem(BaseModel):
    period: date
    budget: Decimal
    actual: Decimal
    variance: Decimal
    rolling_3m_actual: Decimal


class ExceptionItem(BaseModel):
    expense_id: str
    period: date
    transaction_date: date
    department_code: str
    cost_centre_code: str
    vendor_code: str
    vendor_name: str
    vendor_risk_tier: str
    invoice_number: str
    amount: Decimal
    approval_status: ApprovalStatus
    monthly_budget: Decimal
    budget_share_pct: Decimal
    exception_score: Decimal
    exception_reasons: list[str]


class DrilldownItem(BaseModel):
    expense_id: str
    transaction_date: date
    vendor_code: str
    vendor_name: str
    invoice_number: str
    amount: Decimal
    approval_status: ApprovalStatus
    description: str


class PaginatedExceptions(BaseModel):
    items: list[ExceptionItem]
    next_cursor: str | None


class PaginatedDrilldown(BaseModel):
    items: list[DrilldownItem]
    next_cursor: str | None


class StatisticalTestResult(BaseModel):
    approved_n: int
    non_approved_n: int
    approved_mean: float
    non_approved_mean: float
    mean_difference: float
    ci_95_low: float
    ci_95_high: float
    t_statistic: float
    p_value: float
    cohen_d: float
    interpretation: str
    limitations: list[str]
