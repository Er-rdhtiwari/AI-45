# Likely Interviewer Questions and Answer Anchors

## Why PostgreSQL rather than a document database?

The domain has stable relationships, strict grains, transactional ingestion, uniqueness constraints, and join-heavy analytics. PostgreSQL supports those directly. A document store might fit raw source payload retention, but it would not replace the relational analytical model here.

## Why synchronous endpoints?

The PoC prioritizes clear transaction boundaries and interview readability. FastAPI can execute synchronous route functions without blocking the event loop directly. For a measured high-concurrency workload, I would compare a larger sync connection pool against SQLAlchemy async with an async driver rather than assuming async is automatically faster.

## How is ingestion truly idempotent?

The idempotency key identifies the logical request, and the canonical payload hash detects accidental key reuse with different content. A unique constraint handles concurrent races. Source-system/source-record uniqueness also prevents duplicate business records across separate ingestion batches.

## Why not delete all Redis keys after ingestion?

Wildcard deletion is slow and risky. Versioned keys make invalidation an O(1) increment. Old entries become unreachable and expire by TTL. The trade-off is temporary unused memory.

## Can cache and database become inconsistent?

Yes. The database commit occurs before cache-version increment, so a process failure in that small gap could leave old keys addressable until TTL. Production options include an outbox/event, a very short TTL, or a transactionally coordinated invalidation mechanism depending on consistency requirements.

## Is cursor pagination stable when new data arrives?

It is more stable than offset pagination because it resumes from the last sort tuple. New higher-ranked records can appear before the current position without duplicating previously seen rows. Updates to a previously returned item’s score can still move it; snapshot semantics would require a read timestamp or snapshot/version boundary.

## Why is expense ID part of the cursor?

Scores are not unique. A deterministic unique tie-breaker prevents skipping or repeating rows with equal score.

## What does zero reconciliation error prove?

It proves the tested aggregate query matches source totals for the seeded dataset. It does not prove all business definitions are correct, all filters are tested, or production ingestion is complete.

## Is the p-value enough to act on?

No. I would examine effect size, confidence interval, data-generating process, independence, distribution shape, multiple tests, and business cost. This dataset is synthetic and intentionally creates an association.

## How would you evaluate exception quality?

Collect reviewer outcomes, define the positive class and review cost, measure precision at K, recall, false-positive burden, calibration if a probability model is introduced, review-time reduction, and financial value recovered. Segment metrics by department, vendor, amount band, and period.

## What breaks at 100 million expenses?

Full scans and on-demand aggregation become expensive. I would inspect query plans, partition by period, maintain monthly aggregate facts, use incremental refresh or streaming aggregates, add covering indexes where justified, and separate operational ingestion from analytical serving if workload isolation is needed.

## How would you secure department-specific data?

Use authenticated identities, authorization claims, service-to-service credentials, PostgreSQL row-level security or enforced repository filters, audit access, and test for horizontal privilege escalation. The optional API key in the PoC is only a baseline.

## How would you make the cache resilient?

Set connection and command timeouts, fail open for reads when acceptable, add circuit breaking, protect against stampedes with request coalescing or locks, monitor hit ratio and evictions, and cap payload size.

## Why use a transparent rule score instead of ML?

There is no labeled outcome dataset in this PoC. A transparent rule is testable and explainable. ML would be justified only after defining labels, costs, drift controls, governance, and a baseline comparison.

## What would you change first for production?

Alembic migrations, OAuth/OIDC and authorization, external metrics/traces, Redis/PostgreSQL integration tests, timeouts and pool settings, real workload benchmarks, and a reviewer-feedback data model.
