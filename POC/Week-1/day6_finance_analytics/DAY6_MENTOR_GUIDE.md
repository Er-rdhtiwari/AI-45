# Day 6 Mentor Guide — Finance Analytics Integration PoC

## Beginner-friendly summary

This project combines the first five days into one system:

- **Python/backend:** a FastAPI application with validation, errors, logs, tests, and configuration.
- **API contracts:** typed request/response models, status codes, idempotency, correlation IDs, and stable pagination.
- **SQL/data:** a relational finance schema, constraints, indexes, CTEs, joins, aggregation, and window functions.
- **Concurrency/resilience awareness:** bounded request inputs, transactional writes, cache failure boundaries, and health checks.
- **Statistics:** a confidence interval, Welch hypothesis test, effect size, and limitations.

The important interview lesson is not “I built four endpoints.” It is: **I defined a financial grain, protected correctness at multiple layers, made retries safe, exposed explainable analytics, measured the system, and stated what the PoC cannot prove.**

---

## 1. Problem statement, users, business value, scope, and non-goals

### Problem statement

A finance organization has monthly budget allocations at department and cost-centre level and expense transactions arriving from an ERP. Analysts need to answer:

1. Where are actual expenses above or below budget?
2. Is the variance a one-month spike or a sustained trend?
3. Which individual expenses deserve review first?
4. Can the analyst drill from an aggregate to source transactions?
5. Can a retried ingestion request avoid duplicates?
6. Can the service return consistent results quickly enough for repeated dashboard use?

### Users

- **FP&A analyst:** monitors variance and prepares commentary.
- **Controller:** reviews unapproved, rejected, unusually large, or risky-vendor expenses.
- **Department owner:** sees the transactions behind a cost-centre variance.
- **Data/platform engineer:** operates ingestion, storage, cache, API, logs, and tests.

### Business value

- Consistent and reproducible variance definitions.
- Lower manual reconciliation effort.
- Faster exception review through ranking and drill-down.
- Reduced duplicate-record risk from idempotent ingestion.
- Faster repeated reads through cache-aside serving.
- Better auditability through correlation IDs and source-record lineage.

### Scope

- One legal entity and one currency.
- Monthly budgets and transaction-level expenses.
- Deterministic synthetic data for January–December 2025.
- Finance analytics APIs and one statistical comparison.
- PostgreSQL and Redis production profile.
- SQLite and in-memory cache local profile.

### Non-goals

- General ledger posting, double-entry accounting, accruals, FX, tax, or consolidation.
- Forecasting or ML-based anomaly detection.
- Fraud determination.
- Production-grade identity, fine-grained authorization, data retention, or UI.
- Causal inference from approval status.

---

## 2. Functional and non-functional requirements

### Functional requirements

| ID | Requirement | Acceptance condition |
|---|---|---|
| F1 | Seed realistic finance data | CSVs contain all required entities and deterministic values |
| F2 | Validate ingestion | Bad amount, status, date, reference, duplicate payload row, or missing budget is rejected |
| F3 | Idempotent write | Same key/same payload replays; same key/different payload conflicts |
| F4 | Variance summary | Returns budget, actual, variance, and variance percent by department/month |
| F5 | Exception ranking | Returns documented score and explainable reasons |
| F6 | Trend view | Returns monthly values and rolling three-month actual |
| F7 | Drill-down | Returns source transactions for cost centre/month |
| F8 | Stable pagination | No overlap between consecutive pages under unchanged data |
| F9 | Statistical result | Returns CI, test statistic, p-value, effect size, and limitations |
| F10 | Operability | Liveness, readiness, logs, correlation IDs, and lightweight metrics are present |

### Non-functional requirements

| Attribute | Design response |
|---|---|
| Correctness | database constraints, transactional writes, reconciliation metric, tests |
| Reliability | idempotency key, payload hash, source-record uniqueness |
| Performance | indexed filters, aggregated SQL, cache-aside, measured cold/warm latency |
| Scalability | cursor pagination and a documented aggregate/partitioning path |
| Security | optional API key, parameterized SQL, bounded payloads, generic 500 responses |
| Observability | JSON logs, timing headers, correlation IDs, health checks, counters |
| Maintainability | app factory, repository/service/API layers, deterministic fixtures |
| Explainability | transparent exception score and explicit statistical limitations |

---

## 3. End-to-end architecture

```text
            Expense JSON / seed CSVs
                       |
                       v
           +-----------+------------+
           | FastAPI ingestion API  |
           | Pydantic validation    |
           | idempotency + hash     |
           +-----------+------------+
                       |
                 one transaction
                       v
+--------------+  +----+------------------+  +--------------------+
| API consumer |->| Analytics API/service |->| PostgreSQL         |
| FP&A/control |  | variance/exceptions   |  | dimensions, budget |
+--------------+  | trends/drill-down     |  | expense, batches   |
                  +----+-------------+-----+  +--------------------+
                       |             |
                  cache-aside       structured logs/metrics
                       v             v
                  +----+----+   +----+----------------+
                  | Redis   |   | Correlation/timing  |
                  | version |   | health + counters   |
                  +---------+   +---------------------+
```

### Correctness boundaries

1. **Pydantic** protects the API contract.
2. **Service validation** checks reference and budget existence.
3. **Database constraints** protect stored state even if another writer bypasses the API.
4. **Transaction** makes batch metadata and expense writes atomic.
5. **Reconciliation** checks aggregate output against source totals.
6. **Tests** protect retry, cache, pagination, statistics, and error behavior.

---

## 4. Implementation milestones

### Milestone 1 — Model the financial grain

Before coding endpoints, state the grain:

- Budget: one row per **cost centre + month**.
- Expense: one row per **source system + source record ID**.
- Variance: aggregate expenses to the budget grain before comparison.

A common interview mistake is to begin with API routes without defining grain. That creates duplicate joins, incorrect totals, and ambiguous ownership.

### Milestone 2 — Build deterministic data

Use a fixed random seed. Include normal variation and deliberate review cases:

- quarter-end seasonality;
- occasional cost-centre overspend;
- amount-dependent pending/rejected status;
- vendor risk tiers;
- a few very large transactions.

Determinism matters because test and benchmark results must be repeatable.

### Milestone 3 — Add relational constraints and indexes

Use unique constraints for business grains and source identity. Index the actual filters and joins rather than adding indexes to every field.

### Milestone 4 — Implement idempotent ingestion

Separate two concepts:

- **Request idempotency:** same logical request is safe to retry.
- **Record deduplication:** the same source record is not inserted by another request.

This project uses both.

### Milestone 5 — Implement analytical SQL

- Variance: budget CTE + actual CTE + left join.
- Trend: monthly aggregate + window frame.
- Exceptions: joined context + composite score.
- Drill-down: source detail with deterministic ordering.

### Milestone 6 — Add cache-aside serving

Use normalized filters and a version in every key. On ingestion, increment the version. This avoids a wildcard delete.

### Milestone 7 — Add statistics honestly

Define the comparison, calculate the interval and test, and list reasons not to interpret it causally.

### Milestone 8 — Verify and measure

Run tests, reconciliation, query benchmarks, cache hit ratio, and a business triage metric. Label the environment.

---

## 5. Pseudocode

### Ingestion

```text
INPUT: idempotency key, list of expenses

validate request fields and cross-field dates
canonicalize rows and calculate SHA-256 hash

lookup ingestion batch by idempotency key
if found:
    if stored hash != current hash: return conflict
    return original batch as replay

resolve cost centres and vendors
check every cost-centre/month has a budget
find records already stored by source identity

begin transaction
    insert ingestion batch
    insert unseen expense rows linked to batch
commit

increment cache namespace version
return batch ID, received count, inserted count
```

### Variance

```text
budgeted = group budget by department and month
actuals = group expense amount by department and month
left join actuals onto budgeted
variance = actual - budget
variance_pct = variance / budget * 100, unless budget is zero
```

### Exception pagination

```text
score = budget share + approval penalty + vendor-risk penalty
sort by score DESC, expense_id ASC
cursor = last score + last expense_id
next page filters after that tuple and fetches limit + 1
```

### Welch confidence interval

```text
split amounts into approved and non-approved groups
calculate each mean, variance, and sample size
standard_error = sqrt(var1/n1 + var2/n2)
degrees_of_freedom = Welch-Satterthwaite formula
critical_value = t quantile at 97.5%
CI = mean_difference +/- critical_value * standard_error
run two-sided Welch t-test
calculate pooled-standard-deviation effect size separately
```

---

## 6. Key implementation decisions

### Why actuals are derived from expense rows

A separate actual table could drift from transaction detail. In this PoC, actual is the sum of stored expenses, so drill-down and aggregate share one source of truth. At larger scale, a maintained aggregate fact may be introduced, but it must reconcile back to transactions.

### Why budget is the left side of the variance join

The finance question is “How did we perform against an allocated budget?” A budget period with zero expenses should still appear. An inner join would silently remove it.

### Why payloads are sorted before hashing

Two JSON arrays with the same logical records in different orders should not become different requests. Sorting by source identity before hashing makes the idempotency definition semantic rather than byte-order dependent.

### Why successful ingestion increments a cache version

Deleting keys by pattern is operationally risky. Versioning makes old entries unreachable immediately after the increment and lets TTL reclaim them later.

### Why the score is not ML

There is no labeled reviewer outcome. A transparent rule is a defensible baseline. An interviewer should hear that ML is not automatically better; it needs labels, an objective, costs, evaluation, drift monitoring, and governance.

### Why Welch’s test

The approved and non-approved groups need not have equal variance or sample size. Welch’s method relaxes the equal-variance assumption. It still relies on independent observations and mean-based inference, which are imperfect here.

---

## 7. Data and schema design

### Dimensions and facts

- `departments`: business ownership.
- `cost_centres`: lower-level budget and accountability unit.
- `vendors`: counterparty and risk tier.
- `budgets`: monthly allocation fact.
- `expenses`: transaction fact and actual source.
- `ingestion_batches`: operational lineage and idempotency record.

### Important constraints

- department, cost-centre, and vendor codes are unique;
- one budget exists per cost-centre/month;
- amount is positive for expenses and non-negative for budgets;
- approval status is from a controlled set;
- source-system/source-record is unique;
- idempotency key is unique;
- every expense points to valid reference data and an ingestion batch.

### Query patterns and indexes

The main access path is period + cost centre, so composite indexes lead with period. Vendor and approval indexes support exception slices. Do not claim an index is optimal until a PostgreSQL query plan is measured.

---

## 8. API behavior

### Variance endpoint

Filters: period range and optional department. Response models filter and validate output. Cache status is visible in `X-Cache`.

### Exception endpoint

Filters: period range, optional department, minimum amount, minimum score, page limit, and cursor. Each result includes reasons derived from its components.

### Trend endpoint

Returns budget, actual, variance, and rolling three-month actual. The first two months naturally contain one- and two-month partial windows.

### Drill-down endpoint

Uses cost-centre code and month. Stable cursor order is transaction date descending and unique expense ID ascending.

### Ingestion endpoint

Requires `Idempotency-Key`. Same request can be replayed safely. Different payload under the same key returns 409.

---

## 9. Tests

The repository executes 13 tests covering:

- first cache miss and later hit;
- aggregate shape and reconciliation behavior;
- rolling-window calculation;
- real statistical output;
- invalid period range error envelope;
- exception pagination without overlap;
- invalid cursor rejection;
- drill-down pagination;
- idempotent replay;
- key reuse conflict;
- cross-period date validation;
- cache invalidation after ingestion;
- liveness, readiness, metrics, and optional API key.

### What is not yet tested

- actual PostgreSQL/Redis integration in this execution environment;
- concurrent same-key requests;
- Redis outage behavior;
- load, soak, and connection-pool saturation;
- migration rollback;
- authorization boundaries.

---

## 10. Error handling

Use a stable machine-readable code, human-readable message, optional details, and correlation ID. Do not expose stack traces or SQL errors to clients.

Important mapping:

- 400 for domain validation and invalid cursor;
- 401 for API-key failure;
- 404 for unknown drill-down resource;
- 409 for idempotency conflict;
- 422 for request contract failure;
- 500 for unexpected failures.

The database transaction rolls back on integrity failure.

---

## 11. Security

### Included baseline

- optional API key;
- parameterized SQL;
- bounded batch size;
- input validation;
- generic internal errors;
- no payload logging;
- database constraints.

### Production controls

- OAuth/OIDC and service identities;
- role and department authorization;
- row-level security or centrally enforced query scope;
- TLS and secret manager;
- audit access logs;
- retention, deletion, encryption, and data classification;
- rate limiting and abuse controls.

---

## 12. Observability

### Logs

Every request gets a correlation ID. Completion logs include method, path, status, and latency. Ingestion logs batch ID and row count. Logs are JSON so a log backend can parse them.

### Health

- Liveness answers whether the process can respond.
- Readiness checks database and cache connectivity.

### Metrics

The PoC tracks request count, status count, 5xx count, average request latency, cache hits, cache misses, and hit ratio. Production should use histogram buckets and external aggregation.

---

## 13. Evaluation

### Quality

**Reconciliation absolute error** compares the sum returned by analytical queries with source table totals. The measured deterministic run produced zero error for budget and actual.

### Latency

The local benchmark separately measures direct analytical SQL and warm versioned cache. It reports p50 and p95, not only an average.

### Operational metric

**Cache hit ratio** shows whether the cache is serving repeated analytics effectively.

### Business metric

**Exception spend share** measures how much spend is routed into review by the current threshold. It is not “money saved” and should not be presented as such.

### Statistical metric

The project reports p-value, confidence interval, and effect size. Business action should consider all three plus the limitations.

---

## 14. Measured results

The executed local environment contained 2,330 expenses. Results are in `METRICS.md`.

Key measured outcomes:

- 13 tests passed;
- budget reconciliation absolute error: 0.00;
- actual reconciliation absolute error: 0.00;
- direct SQL p50: 1.5992 ms;
- warm cache p50: 0.0778 ms;
- measured p50 speed-up: 20.55x;
- cache hit ratio: 99.67% after one priming miss;
- exception candidates: 834;
- exception spend share: 56.52%;
- Welch mean-difference 95% CI: 4,836.35 to 8,851.39 in synthetic currency units.

Do not use these numbers as PostgreSQL/Redis or production claims. The benchmark was SQLite plus an in-process cache on the stated machine.

---

## 15. Repository and README outline

The repository separates transport, services, repositories, storage contracts, scripts, SQL, data, tests, and interview documentation. The README follows this order:

1. problem and boundaries;
2. requirements;
3. architecture;
4. milestones and pseudocode;
5. schema and APIs;
6. setup and execution;
7. statistics, errors, security, and observability;
8. measured evaluation;
9. repository structure and trade-offs;
10. limitations, next steps, and demo references.

This ordering is interview-friendly because it explains **why**, then **what**, then **how**, then **evidence**.

---

## 16. Demo preparation

### Three-minute business demo

1. State the finance reconciliation and review problem.
2. Show engineering variance and trend.
3. Show top exception reasons and drill-down.
4. Show miss/hit cache headers.
5. Replay an ingestion request safely.
6. Show the statistical endpoint and state non-causality.

### Two-minute design explanation

1. State budget and expense grains.
2. Explain transactional idempotency and source uniqueness.
3. Explain versioned cache invalidation.
4. Explain stable cursor tuple.
5. Explain logs, health, metrics, and production evolution.

### Five-to-ten-minute technical depth

Open the models, ingestion service, SQL repository, cache interface, statistical service, tests, and measured metrics in that order.

---

## 17. Limitations and next steps

### Limitations

- synthetic data and designed patterns;
- one currency/entity and monthly calendar;
- transparent heuristic rather than calibrated risk;
- process-local metrics;
- no migration tool;
- no full-stack benchmark in this environment;
- cache invalidation has a small post-commit failure window;
- no snapshot isolation across paginated requests;
- no user/department authorization;
- no warehouse-scale strategy implemented.

### Next steps

1. Add Alembic migrations.
2. Execute PostgreSQL and Redis integration tests in CI.
3. Add query-plan capture and index tuning.
4. Add OpenTelemetry and Prometheus.
5. Add cache timeouts, fail-open policy, circuit breaker, and stampede control.
6. Add OAuth/OIDC, department authorization, and audit logs.
7. Add duplicate-invoice and policy-rule analysis.
8. Add reviewer labels and evaluate precision at K, false-positive burden, and review-time reduction.
9. Add partitions or aggregate tables only after workload measurement.
10. Add concurrency and load tests.

---

## 18. Likely interviewer questions

1. Why PostgreSQL rather than NoSQL?
2. Why derive actuals from expense detail?
3. Why is the budget side a left join?
4. How does idempotency differ from deduplication?
5. What happens under two concurrent requests with the same key?
6. Why use a payload hash?
7. Why version cache keys rather than delete by pattern?
8. Where can database/cache inconsistency occur?
9. Why cursor pagination, and what changes can still cause movement?
10. Why is UUID a tie-breaker?
11. How would you evaluate the exception score?
12. Why is the hypothesis test not causal?
13. What assumptions does Welch’s test retain?
14. What would change at 100 million rows?
15. What do zero reconciliation error and passing tests not prove?
16. Which production control would you add first?
17. Would async SQLAlchemy improve this service?
18. How would you protect department-specific financial data?
19. How would you handle Redis failure?
20. How would you explain the measured metrics without overstating them?

Use `docs/interview_questions.md` for answer anchors.
