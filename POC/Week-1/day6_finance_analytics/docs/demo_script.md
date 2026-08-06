# Interview Demo Scripts

## Three-minute business demo

### 0:00–0:30 — Problem and user

“Finance teams receive monthly budgets and thousands of ERP expenses. The hard part is not calculating one variance; it is consistently reconciling totals, prioritizing review, and giving department owners a defensible drill-down. This PoC serves FP&A analysts, controllers, and cost-centre owners.”

### 0:30–1:20 — Variance and trend

1. Call `/v1/analytics/variance?department_code=ENG`.
2. Show monthly budget, actual, absolute variance, and percentage variance.
3. Call `/v1/analytics/trends?department_code=ENG`.
4. Point out the rolling three-month actual, which helps distinguish one-month spikes from sustained pressure.

Say: “The aggregate is produced from real seeded transactions and reconciles to source totals with zero absolute error in the measured run.”

### 1:20–2:10 — Exception triage and drill-down

1. Call `/v1/analytics/exceptions?limit=5`.
2. Explain one item’s reasons: pending approval, high-risk vendor, or a large share of monthly budget.
3. Use `/v1/analytics/drilldown` for the item’s cost centre and period.

Say: “The score prioritizes human review. It is intentionally transparent and is not presented as fraud probability.”

### 2:10–2:40 — Reliability and performance

1. Call variance twice.
2. Show `X-Cache: MISS`, then `X-Cache: HIT`.
3. Mention the measured local p50 improvement and qualify the environment.
4. Ingest one new expense twice with the same idempotency key and show the replay result.

### 2:40–3:00 — Statistical reasoning and close

Call `/v1/analytics/statistics/approval-amount-test`.

Say: “The service reports a Welch confidence interval and p-value, but the README explicitly explains that this synthetic association is not causal. The PoC combines data contracts, SQL, statistics, APIs, caching, tests, and operational controls.”

## Two-minute design explanation

### 0:00–0:35 — Data model and correctness

“Budgets are stored at cost-centre/month grain; expenses are source-system/source-record grain. Database uniqueness and check constraints backstop Pydantic validation. Analytical queries aggregate expenses into actuals and left-join them to budget so a month with no expense still appears.”

### 0:35–1:05 — Ingestion and consistency

“Ingestion uses an idempotency key plus a SHA-256 hash of a canonical sorted payload. A same-key same-payload retry returns the original batch; same-key different-payload returns 409. Batch and expense writes commit in one transaction.”

### 1:05–1:30 — Cache and pagination

“Analytics cache keys include a namespace version and normalized filters. Successful ingestion increments the version, so no wildcard key scan is required. Exception pagination sorts by score descending and UUID ascending; the cursor stores both values to avoid offset drift.”

### 1:30–2:00 — Operations and scale path

“Middleware creates a correlation ID, measures latency, and emits structured logs. Readiness checks database and cache. For scale, I would add Alembic, OpenTelemetry, Redis timeouts and stampede control, PostgreSQL plan analysis, partitioning or aggregates, OAuth/RLS, and load tests.”

## Extended 5–10 minute technical walkthrough

### 1. Contracts and validation

- Show `ExpenseIn` and the cross-field transaction-period validator.
- Explain the 5,000-row bound and reference-data validation.
- Explain why database constraints remain necessary after API validation.

### 2. Analytical SQL

- Show the variance CTEs and left join.
- Show the trend window frame: `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`.
- Show the transparent exception score and deterministic tie-breaker.

### 3. Idempotency

- Canonicalize and sort records before hashing so payload order does not create a new semantic request.
- Explain replay versus conflict behavior.
- Explain the residual concurrent-request race and unique constraint fallback.

### 4. Cache strategy

- Read version, normalize filters, build cache key.
- Miss executes SQL and stores JSON with TTL.
- Write increments version.
- Discuss stale-read window, cache-aside behavior, and why versioning avoids expensive key scans.

### 5. Statistical analysis

- State null and alternative hypotheses.
- Explain why Welch’s test is used instead of assuming equal variance.
- Interpret CI, effect size, and p-value separately.
- State non-causality, clustering, heavy-tail, synthetic-data, and multiple-testing limitations.

### 6. Verification

- Run `pytest` and show 13 passing tests.
- Open `METRICS.md` and explain zero reconciliation error.
- Qualify the SQLite/in-memory benchmark and explain how to collect PostgreSQL/Redis numbers.

### 7. Production evolution

- Schema migrations, authentication, authorization, RLS, secret management.
- OpenTelemetry and Prometheus.
- Partitioning/materialized aggregates after observing plans and workload.
- Queue-based ingestion for very large batches.
- Reviewer labels and precision/recall for exception quality.
