# Day 6 — Finance Analytics Service PoC

An interview-grade, locally executable FastAPI service for **budget-versus-actual analysis** and **expense exception triage**. The production profile uses PostgreSQL and Redis; the no-Docker profile uses SQLite and an in-process TTL cache with the same versioned-key contract.

## 1. Problem statement

Finance teams commonly receive budget data at a cost-centre/month grain and expense transactions from an ERP. Analysts then spend time reconciling totals, finding overspend, reviewing large or unapproved expenses, and preparing drill-down evidence for department owners.

### Users

- FP&A analyst: compares budget and actuals, identifies overspend, and explains trends.
- Finance controller: reviews high-risk or unapproved expense exceptions.
- Department owner: drills into the transactions driving a variance.
- Platform engineer: operates ingestion, API, database, cache, logs, and health checks.

### Business value

- Reduces manual spreadsheet reconciliation.
- Gives a consistent definition of variance and exception priority.
- Supports faster review through stable pagination and drill-down.
- Makes ingestion retry-safe through idempotency.
- Demonstrates measurable latency improvement from caching.

### Scope

- Deterministic synthetic finance data for 2025.
- Departments, cost centres, budgets, vendors, expenses, approval status, and ingestion batches.
- JSON ingestion with validation and idempotency.
- Variance, trend, exception, drill-down, and statistical-analysis APIs.
- PostgreSQL reference DDL and analytical SQL.
- Redis-backed versioned caching with an in-memory development fallback.
- Structured logs, correlation IDs, health checks, metrics, tests, and benchmark scripts.

### Non-goals

- General ledger accounting, accruals, FX conversion, tax logic, or multi-entity consolidation.
- Fraud detection or claims that an exception is waste, abuse, or policy violation.
- Production IAM, row-level security, secrets management, distributed tracing backend, or rate limiting.
- Streaming ingestion, CDC, data warehouse orchestration, or a user interface.
- A causal conclusion from the included hypothesis test.

## 2. Requirements

### Functional requirements

1. Load reference data, budgets, and expense transactions.
2. Reject invalid amounts, statuses, dates, unknown references, missing budgets, and duplicate records inside one payload.
3. Make a retried ingestion request safe with `Idempotency-Key` plus a payload hash.
4. Return budget, actual, variance, and variance percentage by department and month.
5. Return monthly trend data with a rolling three-month actual total.
6. Rank expense exceptions by a documented composite score.
7. Provide stable cursor pagination for exception and drill-down results.
8. Compare approved and non-approved expense amounts with a Welch t-test and 95% confidence interval.
9. Expose liveness, readiness, and lightweight operational metrics.
10. Measure analytical-query latency with and without caching.

### Non-functional requirements

- Correctness: aggregate results must reconcile to source totals.
- Reliability: ingestion is transactional and idempotent.
- Performance: common aggregate views are cached with bounded TTL.
- Consistency: deterministic sort order under pagination.
- Observability: JSON logs, correlation IDs, response timing, cache counters, and health checks.
- Security baseline: optional API key, input limits, no request-body logging, parameterized SQL, and generic 500 responses.
- Testability: local SQLite profile and deterministic seed data.
- Portability: Docker Compose for PostgreSQL, Redis, and API.

## 3. End-to-end architecture

```text
                         +---------------------------+
                         | Finance analyst / client  |
                         +-------------+-------------+
                                       |
                           HTTP + X-Correlation-ID
                                       |
                                       v
+------------------+      +------------+-------------+      +------------------+
| ERP / batch file | ---> | FastAPI finance service | ---> | PostgreSQL       |
| expense records  | POST | validation + idempotency| SQL  | reference data   |
+------------------+      | analytics + error model |      | budgets/expenses |
                          +------+-------------+-----+      +---------+--------+
                                 |             |                      |
                                 |             |                      |
                          versioned GET/SET    | structured JSON logs|
                                 v             v                      v
                          +------+-----+  +----+----------------+  +--+----------+
                          | Redis cache|  | Health / metrics    |  | SQL queries |
                          | TTL + ver. |  | correlation/timing |  | CTE/window  |
                          +------------+  +---------------------+  +-------------+
```

### Request flow

1. Middleware accepts or creates a correlation ID and starts a timer.
2. FastAPI validates query, header, and body fields.
3. Ingestion checks the idempotency key and canonical payload hash.
4. The service validates foreign references and budget coverage.
5. One database transaction writes the ingestion batch and new expenses.
6. Successful ingestion increments the cache namespace version.
7. Analytics reads a versioned cache key; a miss executes parameterized analytical SQL and stores JSON with TTL.
8. Middleware returns correlation and response-time headers and writes a structured log.

## 4. Implementation milestones

| Milestone | Deliverable | Verification |
|---|---|---|
| 1. Domain and data | Problem boundaries, deterministic dataset, validation rules | CSV counts and validation tests |
| 2. Persistence | PostgreSQL schema, constraints, indexes, SQLAlchemy models | Seed script and readiness check |
| 3. Ingestion | Transactional write, idempotency key, payload hash, duplicate protection | Replay and conflict tests |
| 4. Analytics | Variance, exceptions, trends, drill-down | Reconciliation and API tests |
| 5. Cache | Redis/in-memory implementation, TTL, version invalidation | HIT/MISS and invalidation tests |
| 6. Statistics | Welch test, 95% CI, effect size, limitations | Statistical endpoint test |
| 7. Production baseline | Logs, correlation IDs, error envelope, health, metrics, optional API key | Health/security tests |
| 8. Evaluation | Quality, latency, operational/business metrics | `METRICS.md` |
| 9. Interview readiness | Demo scripts, design narrative, likely questions | `docs/demo_script.md` |

## 5. Pseudocode before code

### Idempotent ingestion

```text
function ingest(idempotency_key, payload):
    validate payload shape, dates, status, amount, and batch uniqueness
    payload_hash = sha256(canonical_sorted_payload)

    existing_batch = find batch by idempotency_key
    if existing_batch exists:
        if existing_batch.payload_hash differs:
            return 409 conflict
        return original result with replayed=true

    resolve cost-centre and vendor IDs
    reject unknown references or missing monthly budgets
    find source records already stored

    begin transaction
        insert ingestion batch
        insert only unseen source records
    commit

    increment analytics cache version
    return inserted count and batch ID
```

### Cached variance query

```text
function variance(filters):
    version = cache.get("analytics-version")
    key = stable_json(version + filters)

    if cache contains key:
        increment cache-hit metric
        return cached data and HIT

    increment cache-miss metric
    rows = execute budget CTE + actual CTE + left join
    cache rows with TTL
    return rows and MISS
```

### Stable cursor pagination

```text
sort by exception_score descending, expense_id ascending
cursor contains last_score and last_expense_id
next query keeps rows where:
    score < last_score
    OR score = last_score AND expense_id > last_expense_id
fetch limit + 1 to decide whether another page exists
```

## 6. Data and schema design

### Dataset

The generated dataset is deterministic:

- 8 departments
- 24 cost centres
- 30 vendors
- 288 monthly budgets
- 2,330 expense transactions
- Periods: January–December 2025

Files are under `data/`; regenerate them with:

```bash
python scripts/generate_seed.py
```

### Core entities

| Entity | Grain | Important constraints |
|---|---|---|
| Department | one department | unique code |
| Cost centre | one cost centre | unique code, department FK |
| Vendor | one vendor | unique code, risk tier check |
| Budget | cost centre + month | unique grain, non-negative amount |
| Expense | source system + source record | positive amount, valid status, reference FKs |
| Ingestion batch | idempotency key | unique key, payload hash, row counts |

### Index choices

- `budgets(period, cost_centre_id)` supports period filtering and budget joins.
- `expenses(period, cost_centre_id)` supports variance, trend, and drill-down.
- `expenses(vendor_id, period)` supports vendor analysis.
- `expenses(approval_status, period)` supports approval review.

For a much larger table, consider monthly range partitioning, covering indexes based on real query plans, and pre-aggregated monthly facts.

## 7. API surface

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/v1/ingestion/expenses` | Validated, idempotent expense ingestion |
| GET | `/v1/analytics/variance` | Department/month budget-versus-actual |
| GET | `/v1/analytics/trends` | Monthly trend and rolling three-month actual |
| GET | `/v1/analytics/exceptions` | Ranked, cursor-paginated exception candidates |
| GET | `/v1/analytics/drilldown` | Transaction detail for cost centre/month |
| GET | `/v1/analytics/statistics/approval-amount-test` | Welch test, CI, and limitations |
| GET | `/health/live` | Process liveness |
| GET | `/health/ready` | Database and cache readiness |
| GET | `/internal/metrics` | In-process request/cache metrics |

OpenAPI documentation is available at `/docs` after startup.

Detailed curl examples are in `docs/api_examples.md`.

## 8. Local setup

### Option A: no Docker

This path uses SQLite and the in-memory TTL cache.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

export DATABASE_URL=sqlite:///./finance.db
export REDIS_URL=memory://
export AUTO_CREATE_SCHEMA=true

python scripts/seed_db.py
uvicorn app.main:app --reload
```

Test:

```bash
curl -i http://localhost:8000/v1/analytics/variance
```

### Option B: PostgreSQL and Redis with Docker Compose

```bash
docker compose up --build -d

docker compose exec api python scripts/seed_db.py
curl -i http://localhost:8000/v1/analytics/variance
```

Stop and remove data:

```bash
docker compose down -v
```

### Run tests

```bash
pytest
```

### Run measured local benchmark

```bash
export DATABASE_URL=sqlite:///./finance.db
export REDIS_URL=memory://
python scripts/benchmark.py --iterations 300
```

### Run full-stack HTTP benchmark

```bash
python scripts/http_benchmark.py --base-url http://localhost:8000 --iterations 300
```

## 9. Exception score

The PoC score is transparent and deterministic:

```text
expense as % of monthly cost-centre budget
+ 50 for REJECTED or 30 for PENDING
+ 25 for HIGH-risk vendor or 10 for MEDIUM-risk vendor
```

This is a **review-priority score**, not a probability and not a fraud label. A production version should be calibrated with historical review outcomes, false-positive cost, policy severity, vendor context, and explainability requirements.

## 10. Statistical calculation

The endpoint compares approved expense amounts with pending/rejected expense amounts using Welch’s two-sample t-test because the group variances and sample sizes may differ. It returns:

- group sample sizes and means;
- non-approved minus approved mean difference;
- 95% confidence interval for the difference;
- t statistic and p-value;
- Cohen’s d effect size;
- explicit limitations.

The result is not causal. The synthetic generator intentionally makes large expenses somewhat more likely to remain pending or be rejected, observations are clustered, and amounts are heavy-tailed.

## 11. Error handling

Errors use a consistent envelope:

```json
{
  "error": {
    "code": "validation_error",
    "message": "request validation failed",
    "details": [],
    "correlation_id": "..."
  }
}
```

- 400: invalid business rule or cursor.
- 401: missing/incorrect API key when configured.
- 404: missing cost centre.
- 409: idempotency-key conflict or concurrent duplicate.
- 422: request schema validation failure.
- 500: generic message; detailed exception stays in logs.

## 12. Security baseline

Included:

- Optional `X-API-Key` protection through `API_KEY`.
- Parameterized SQL.
- Request size bounded to 5,000 rows per ingestion batch.
- Strict status and date validation.
- No raw request-body logging.
- Generic internal-error response.
- Database constraints as a second validation layer.

Production additions:

- OAuth/OIDC service and user authentication.
- Role/department authorization and PostgreSQL row-level security.
- TLS, secret manager, key rotation, network policies, WAF/rate limits.
- Audit log for data access and configuration changes.
- PII classification, retention, deletion, and masking policies.

## 13. Observability

- JSON logs include timestamp, level, logger, message, and correlation ID.
- Request completion logs include method, path, status, and duration.
- Responses include `X-Correlation-ID`, `X-Response-Time-Ms`, and analytics cache status.
- Readiness checks database and cache connectivity.
- Metrics track request count, 5xx count, average latency, status counts, cache hits, cache misses, and hit ratio.

Production additions would export OpenTelemetry traces and Prometheus metrics rather than relying on process-local counters.

## 14. Evaluation and measured metrics

See `METRICS.md` for executed results. The included local run reports:

- quality: budget and actual reconciliation absolute error;
- latency: direct analytical SQL versus warm cache p50/p95;
- operational metric: cache hit ratio;
- business triage metric: count and spend share of exception candidates;
- statistical result: p-value and confidence interval.

All local results are labeled with their environment. PostgreSQL/Redis production numbers are deliberately left for an executed full-stack benchmark.

## 15. Repository structure

```text
.
├── app/
│   ├── api/routes/          # HTTP endpoints
│   ├── repositories/       # SQL and persistence access
│   ├── services/           # ingestion, cache use, statistics
│   ├── cache.py             # Redis and in-memory TTL cache
│   ├── config.py            # environment settings
│   ├── db.py                # engine/session lifecycle
│   ├── logging.py           # structured JSON logs
│   ├── metrics.py           # lightweight counters
│   ├── middleware.py        # correlation ID and timing
│   ├── models.py            # SQLAlchemy schema
│   ├── schemas.py           # Pydantic contracts
│   └── main.py              # app factory and handlers
├── data/                    # deterministic CSV seed data
├── docs/                    # API, demos, interview notes
├── scripts/                 # generation, seeding, stats, benchmarks
├── sql/                     # PostgreSQL DDL and analytical SQL
├── tests/                   # API, ingestion, pagination, security tests
├── docker-compose.yml
├── Dockerfile
├── METRICS.md
└── README.md
```

## 16. Trade-offs

| Decision | Benefit | Cost / alternative |
|---|---|---|
| Relational normalized schema | Constraints and explainable joins | Warehouse/star schema may be better for very large analytics |
| Raw analytical SQL behind repository | Clear CTE/window-function reasoning | More dialect-specific than pure ORM |
| Versioned cache keys | Safe invalidation without key scans | Old keys remain until TTL |
| Synchronous SQLAlchemy | Simple interview PoC and predictable transactions | Async may help under high I/O concurrency but adds complexity |
| Cursor pagination | Stable under inserts and large offsets | Cursor is opaque and tied to sort order |
| Transparent rule score | Explainable and easy to validate | Not calibrated to review outcomes |
| SQLite local profile | Runs without Docker | Does not reproduce PostgreSQL optimizer or Redis network latency |

## 17. Known limitations and next steps

1. Replace API key with OAuth/OIDC and fine-grained authorization.
2. Add Alembic migrations rather than automatic table creation.
3. Run PostgreSQL `EXPLAIN (ANALYZE, BUFFERS)` and tune indexes from real plans.
4. Add Redis failure policy, timeouts, circuit breaker, and cache stampede protection.
5. Export metrics/traces to Prometheus and OpenTelemetry backends.
6. Add duplicate-invoice and policy-rule endpoints.
7. Add fiscal calendars, currencies, accruals, forecasts, and organizational hierarchies.
8. Add snapshot or aggregate tables for high-volume workloads.
9. Validate exception rules against labeled reviewer outcomes and measure precision/recall plus review-time reduction.
10. Add concurrency/load tests and PostgreSQL/Redis integration tests in CI.

## 18. Demo and interview material

- `docs/demo_script.md`: three-minute business demo, two-minute design explanation, and extended technical walkthrough.
- `docs/interview_questions.md`: likely interviewer questions and answer anchors.
- `docs/api_examples.md`: runnable API examples.
- `DAY6_MENTOR_GUIDE.md`: interview-focused learning notes and explanation.
