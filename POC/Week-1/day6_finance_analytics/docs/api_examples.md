# API Examples

## Variance summary

```bash
curl -i \
  -H 'X-Correlation-ID: demo-variance-001' \
  'http://localhost:8000/v1/analytics/variance?period_from=2025-01-01&period_to=2025-12-01&department_code=ENG'
```

Run twice and compare `X-Cache: MISS` with `X-Cache: HIT`.

## Trend view

```bash
curl -s \
  'http://localhost:8000/v1/analytics/trends?period_from=2025-01-01&period_to=2025-12-01&department_code=MKT'
```

## Top exceptions

```bash
curl -s \
  'http://localhost:8000/v1/analytics/exceptions?period_from=2025-01-01&period_to=2025-12-01&min_amount=5000&min_score=35&limit=5'
```

Use the returned `next_cursor` in the next request:

```bash
curl -sG 'http://localhost:8000/v1/analytics/exceptions' \
  --data-urlencode 'limit=5' \
  --data-urlencode 'cursor=<NEXT_CURSOR>'
```

## Cost-centre drill-down

```bash
curl -sG 'http://localhost:8000/v1/analytics/drilldown' \
  --data-urlencode 'cost_centre_code=ENG-01' \
  --data-urlencode 'period=2025-01-01' \
  --data-urlencode 'limit=10'
```

## Statistical test

```bash
curl -s 'http://localhost:8000/v1/analytics/statistics/approval-amount-test'
```

## Idempotent ingestion

```bash
curl -i -X POST 'http://localhost:8000/v1/ingestion/expenses' \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: manual-demo-001' \
  -d '{
    "rows": [
      {
        "source_system": "MANUAL",
        "source_record_id": "MANUAL-DEMO-001",
        "cost_centre_code": "FIN-01",
        "vendor_code": "V001",
        "period": "2025-01-01",
        "transaction_date": "2025-01-20",
        "invoice_number": "INV-MANUAL-DEMO-001",
        "amount": "2500.00",
        "approval_status": "APPROVED",
        "description": "Manual interview demonstration record"
      }
    ]
  }'
```

Repeat the same request and observe `replayed: true`. Change the amount while retaining the same idempotency key and observe HTTP 409.

## Health and metrics

```bash
curl -s http://localhost:8000/health/live
curl -s http://localhost:8000/health/ready
curl -s http://localhost:8000/internal/metrics
```
