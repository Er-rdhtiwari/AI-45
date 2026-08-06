-- PostgreSQL reference DDL. The application can also create equivalent tables via SQLAlchemy.

CREATE TABLE IF NOT EXISTS departments (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(120) NOT NULL
);

CREATE TABLE IF NOT EXISTS cost_centres (
    id BIGSERIAL PRIMARY KEY,
    department_id BIGINT NOT NULL REFERENCES departments(id),
    code VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(120) NOT NULL
);

CREATE TABLE IF NOT EXISTS vendors (
    id BIGSERIAL PRIMARY KEY,
    vendor_code VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(160) NOT NULL,
    risk_tier VARCHAR(10) NOT NULL CHECK (risk_tier IN ('LOW', 'MEDIUM', 'HIGH'))
);

CREATE TABLE IF NOT EXISTS budgets (
    id BIGSERIAL PRIMARY KEY,
    cost_centre_id BIGINT NOT NULL REFERENCES cost_centres(id),
    period DATE NOT NULL,
    amount NUMERIC(14, 2) NOT NULL CHECK (amount >= 0),
    CONSTRAINT uq_budget_cc_period UNIQUE (cost_centre_id, period),
    CONSTRAINT ck_budget_period_month_start CHECK (period = date_trunc('month', period)::date)
);

CREATE TABLE IF NOT EXISTS ingestion_batches (
    id VARCHAR(36) PRIMARY KEY,
    idempotency_key VARCHAR(160) NOT NULL UNIQUE,
    payload_hash CHAR(64) NOT NULL,
    status VARCHAR(20) NOT NULL,
    received_rows INTEGER NOT NULL CHECK (received_rows >= 0),
    inserted_rows INTEGER NOT NULL CHECK (inserted_rows >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS expenses (
    id VARCHAR(36) PRIMARY KEY,
    source_system VARCHAR(40) NOT NULL,
    source_record_id VARCHAR(100) NOT NULL,
    cost_centre_id BIGINT NOT NULL REFERENCES cost_centres(id),
    vendor_id BIGINT NOT NULL REFERENCES vendors(id),
    period DATE NOT NULL,
    transaction_date DATE NOT NULL,
    invoice_number VARCHAR(80) NOT NULL,
    amount NUMERIC(14, 2) NOT NULL CHECK (amount > 0),
    approval_status VARCHAR(20) NOT NULL
        CHECK (approval_status IN ('APPROVED', 'PENDING', 'REJECTED')),
    description VARCHAR(240) NOT NULL,
    ingestion_batch_id VARCHAR(36) NOT NULL REFERENCES ingestion_batches(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_expense_source_record UNIQUE (source_system, source_record_id),
    CONSTRAINT ck_expense_period_month_start
        CHECK (period = date_trunc('month', period)::date),
    CONSTRAINT ck_expense_transaction_in_period
        CHECK (date_trunc('month', transaction_date)::date = period)
);

CREATE INDEX IF NOT EXISTS ix_budgets_period_cc
    ON budgets(period, cost_centre_id);
CREATE INDEX IF NOT EXISTS ix_expenses_period_cc
    ON expenses(period, cost_centre_id);
CREATE INDEX IF NOT EXISTS ix_expenses_vendor_period
    ON expenses(vendor_id, period);
CREATE INDEX IF NOT EXISTS ix_expenses_status_period
    ON expenses(approval_status, period);
