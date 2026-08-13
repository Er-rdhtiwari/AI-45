# Abnormal Expense Review System: Problem and Design

## Problem statement, users, business value, scope, and non-goals

Finance teams cannot manually inspect every employee expense. The system ranks newly submitted expenses by the probability that a completed audit would confirm a material policy violation, duplicate, fabricated receipt, or otherwise abnormal claim. Its users are finance reviewers, compliance analysts, and ML/platform engineers. Its value is higher abnormal-expense recall within a fixed review capacity, with calibrated risk, traceable reasons, and consistent audit evidence.

Scope covers synthetic-but-realistic USD-normalized expense records, batch training, offline evaluation, human-review routing, model-agnostic explanations, and synchronous FastAPI inference. The model recommends review; it never rejects, disciplines, or accuses an employee. Non-goals are fraud adjudication, reimbursement automation, identity verification, receipt-image analysis, causal claims, and production authentication/data storage.

Target definition: `is_abnormal = 1` only when a completed audit, available after submission, confirms an abnormal expense. Features are restricted to facts available when the claim is submitted. The synthetic generator hides a probabilistic risk function; that function and the target are never available to the model.

## Functional requirements

1. Version and validate the dataset and record lineage.
2. Split chronologically into train, calibration, validation, and untouched test sets.
3. Establish dummy and logistic baselines before tuning.
4. Compare logistic regression, random forest, histogram gradient boosting, and Isolation Forest.
5. Calibrate the selected supervised model on a dedicated split.
6. Choose a review threshold using explicit costs and a maximum review rate.
7. Report discrimination, calibration, subgroup, latency, and review-operations metrics.
8. Generate global, local, and counterfactual explanations with non-causal caveats.
9. Serve versioned predictions, reason codes, uncertainty, warnings, and audit fields.
10. Test validation, deterministic splitting, inference schema, policy behavior, and API endpoints.

## Non-functional requirements

- Reproducible seeds, hashes, immutable manifests, and an append-only experiment ledger.
- CPU-only training and inference; deterministic single-record predictions.
- P95 local API latency target below 100 ms after warm-up (measured, not assumed).
- Strict input validation and no protected attributes in the model input.
- No raw input logging; hashed feature payload in the audit response.
- Graceful errors for missing artifacts, incompatible schemas, and invalid values.
- Human review for high-risk, borderline, or detected out-of-distribution inputs.

## End-to-end architecture

```text
Synthetic source / future warehouse
             |
             v
  CSV + SHA-256 manifest -----> data contract + quality gates
             |                              |
             +--------------+---------------+
                            v
     chronological train | calibration | validation | test
                |               |              |        |
                v               v              v        v
    baseline + candidates -> calibrator -> cost/capacity -> final evaluation
                |                              threshold          |
                +------------------+------------------------------+
                                   v
                  versioned model bundle + reports/cards
                                   |
                                   v
 Client -> FastAPI validation -> feature/OOD checks -> probability + policy
                                   |                    |
                                   v                    v
                            reason codes          review/abstain/clear
                                   \                    /
                                    +--> audit fields <-+
```

## Implementation milestones

1. Freeze target semantics, schema, constraints, costs, and capacity.
2. Generate deterministic realistic data; write manifest and lineage.
3. Fail fast on contract violations and leakage columns.
4. Establish dummy/logistic baselines, then compare untuned candidates.
5. Tune only the best eligible supervised family and log every run.
6. Fit a separate calibrator; select policy on validation only.
7. Evaluate once on test and create fairness/explanation artifacts.
8. package the model, expose the API, test, benchmark, and document.

## Pseudocode (defined before implementation)

```text
generate(seed, n):
  sample employee, claim, merchant, timing, and policy attributes
  compute hidden risk from plausible interactions plus random noise
  sample audit-confirmed target from hidden risk
  save CSV; hash bytes; save dataset manifest and lineage

validate(data, contract):
  assert exact required columns and types
  assert primary key unique and non-null
  assert ranges, enums, date ordering, target domain, and missingness limits
  assert target and post-outcome columns are excluded from model features

train(data):
  sort by submitted_at
  slice oldest 60% train, next 15% calibration, next 10% validation, newest 15% test
  fit dummy; log measured metrics
  fit default logistic and two tree models; log each
  score Isolation Forest; orient anomaly score; log
  choose best supervised default by validation average precision
  tune only that family using declared grid; log every combination
  keep tuned model only if it improves validation average precision
  fit isotonic calibration on calibration predictions
  scan validation cutoffs satisfying review_rate <= capacity
  minimize FN_cost * FN + FP_review_cost * FP
  evaluate exactly once on test
  serialize pipeline, calibrator, schema, references, policy, and versions

explain(row):
  global = permutation importance on held-out test rows
  local = probability delta after replacing one field with a training reference
  counterfactual = search truthful/actionable scenarios, never overwrite facts
  attach caveat: association and model behavior are not causality or guilt

predict(request):
  validate request schema and constraints
  detect unseen categories and numeric range excursions
  score and calibrate
  route high risk, borderline uncertainty, OOD abstention, or auto-clear
  return reason codes, versions, request id, timestamp, input hash, warnings
```

