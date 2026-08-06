# Validation Report

## Executed checks

### Test suite

Command:

```bash
pytest
```

Result:

```text
13 passed in 3.69s
```

Coverage areas include analytics responses, rolling-window logic, stable pagination, idempotent replay, idempotency conflict, validation, cache invalidation, statistics, health, metrics, and optional API-key protection.

### Python compilation

Command:

```bash
python -m compileall -q app scripts tests
```

Result: completed successfully.

### Deterministic seed

Generated and loaded:

- 8 departments
- 24 cost centres
- 30 vendors
- 288 monthly budgets
- 2,330 expense transactions

### Benchmark

Command:

```bash
DATABASE_URL=sqlite:///./finance.db REDIS_URL=memory:// \
python scripts/benchmark.py --iterations 300
```

Measured results are stored in `METRICS.md`.

## Important qualification

Docker was not available in the execution environment used to create this repository. Therefore:

- PostgreSQL and Redis configuration, DDL, Docker Compose, and benchmark commands are included;
- core behavior was executed through SQLite and the real in-process TTL cache implementation;
- no PostgreSQL/Redis latency number is claimed;
- the full-stack benchmark remains an explicitly marked execution step.
