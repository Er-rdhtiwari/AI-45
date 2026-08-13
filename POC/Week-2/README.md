# Abnormal Expense Review ML System

## Problem statement, users, business value, scope, and non-goals

**Problem.** Finance teams cannot inspect every employee expense. This system estimates the probability that a later completed audit would confirm a material policy violation, duplicate, fabricated evidence, or otherwise abnormal claim, then routes claims within a fixed human-review capacity.

**Users.** Finance reviewers use the ranked queue and reason codes; compliance analysts inspect subgroup and audit evidence; ML/platform engineers train, deploy, and monitor the service.

**Business value.** On the newest untouched synthetic test window, the selected policy reviewed 10.94% of claims, found 63.33% of abnormal claims, and achieved 38.58% review yield. Under the declared scenario costs, it avoided an estimated $36,185 versus reviewing none across 1,800 test claims. This is a modeled comparison on synthetic data—not realized savings.

**Scope.** Deterministic structured-data generation, version manifest and lineage, contract checks, chronological training, calibration, cost/capacity thresholding, fairness slices, uncertainty/abstention, explanations, a versioned FastAPI service, tests, and measured quality/latency/operations reports.

**Non-goals.** The system does not prove fraud, reject reimbursement, accuse or discipline an employee, automate identity/receipt verification, use protected gender in prediction, or claim production readiness from synthetic performance. Every flagged or uncertain claim requires a human decision.

## Functional requirements

- Version and validate data; fail on schema, range, missingness, key, time-order, prevalence, or leakage violations.
- Compare a prior dummy, logistic regression, random forest, histogram gradient boosting, and label-free Isolation Forest before tuning.
- Tune only after baselines, recording each run in an append-only JSONL ledger.
- Fit calibration on a dedicated time window and select a validation threshold with explicit costs and capacity.
- Evaluate once on the newest test window, including subgroup slices and bootstrap uncertainty.
- Return probability, routing decision, uncertainty state, reason codes, versions, feature hash, request ID, and timestamp.
- Produce global permutation, local perturbation, and constrained counterfactual explanations.

## Non-functional requirements

- Reproducible seed, chronological split, SHA-256 dataset/model hashes, and versioned schema/data/model/policy.
- CPU-only operation and P95 local API latency target below 100 ms after warm-up.
- Strict Pydantic input constraints; identifiers and gender absent from inference; no raw feature logging.
- Optional API-key enforcement, generic server errors, health/readiness, and process-local telemetry.
- Human abstention for borderline scores and for inputs with at least two distribution warnings.

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

1. Freeze target semantics, schema, exclusions, business costs, and review capacity.
2. Generate and hash deterministic realistic data; document lineage.
3. Run quality/leakage gates and create non-overlapping chronological splits.
4. Establish dummy and logistic baselines; compare two trees and Isolation Forest.
5. Tune only the validation winner and record every candidate.
6. Calibrate on the calibration split; choose policy only on validation.
7. Evaluate once on test; create fairness, uncertainty, and explanation artifacts.
8. Package the model, serve it, benchmark it, test failure modes, and document evidence.

## Pseudocode before code

```text
generate(seed, 12_000):
  sample employee profile, claim, merchant, timing, policy, and history fields
  sample post-submission audit target from hidden probabilistic interactions
  write sorted CSV; hash it; write manifest and lineage

validate(data):
  enforce exact columns/types/ranges/enums/null/key/time/target-rate rules
  assert target, audit timestamp, IDs, and evaluation-only gender are not features

train(data):
  chronological split = 60% train / 15% calibration / 10% validation / 15% test
  fit and log dummy -> default logistic -> default RF -> default HGB -> Isolation Forest
  select default supervised family by validation average precision
  fit and log declared hyperparameter candidates for that family only
  fit isotonic calibrator on calibration only
  choose validation cutoff minimizing 500*FN + 15*FP under buffered 12% capacity
  open test once; compute quality, calibration, business, subgroup, and bootstrap metrics
  serialize pipeline + calibrator + references + ranges + versions + policy

predict(payload):
  reject invalid/extra fields; derive amount_to_policy_ratio
  warn on numeric p01/p99 excursions or unseen categories
  calibrate model score
  route to high-risk review, borderline abstention, OOD abstention, or clear
  perturb fields in one vectorized batch for local reasons
  return decision, reasons, warnings, versions, UUID, timestamp, and input hash
```

The fuller pre-code design is in [docs/01_problem_and_design.md](docs/01_problem_and_design.md).

## Measured results

All values are stored in [reports/evaluation.json](reports/evaluation.json) and were measured—not invented—on the frozen dataset hash in [data/manifests/expenses_v1.manifest.json](data/manifests/expenses_v1.manifest.json).

### Validation comparison before tuning

| Model | Stage | ROC AUC | Average precision |
|---|---|---:|---:|
| Prior dummy | Baseline | 0.5000 | 0.0708 |
| Logistic regression | Untuned | 0.8396 | 0.3840 |
| Random forest | Untuned | 0.8315 | 0.3738 |
| Histogram gradient boosting | Untuned | 0.8368 | 0.3649 |
| Isolation Forest | Unsupervised; labels not used in fit | 0.6744 | 0.1589 |
| Logistic, `C=1`, balanced | Tuned winner | 0.8439 | 0.3961 |

Every run and parameter set is in [experiments/experiments.jsonl](experiments/experiments.jsonl). Isolation Forest is a benchmark, not the deployed model, because its validation ranking was materially weaker.

### Untouched test quality, calibration, operations, and latency

| Dimension | Measured result |
|---|---:|
| Test rows / prevalence | 1,800 / 6.67% |
| Calibrated ROC AUC | 0.8740 |
| Calibrated average precision | 0.3785 |
| AP 95% nonparametric bootstrap interval | 0.2997–0.4716 |
| Brier score, raw → calibrated | 0.1414 → 0.0484 |
| Expected calibration error, raw → calibrated | 0.2574 → 0.0134 |
| Review threshold | 0.174603 |
| Review rate / capacity | 10.94% / 12.00% |
| Review precision (yield) | 38.58% |
| Abnormal recall | 63.33% |
| Expected policy cost per 1,000 claims | $13,230.56 |
| Estimated cost avoided vs no review on test | $36,185 |
| Local TestClient P95 / target | 29.92 ms / 100 ms |
| Sequential local throughput / failures | 37.07 req/s / 0 of 150 |

The cost calculation is `500 × false negatives + 15 × reviewed normal claims`; those are configurable scenario assumptions. The latency result is an in-process Windows benchmark and excludes network, gateway, concurrency, and production telemetry overhead. Raw ranking AP is 0.4245; calibrated AP is lower because isotonic calibration creates ties, while calibration error and Brier score improve substantially.

### Fairness and uncertainty

Gender is never a model input. On supported gender slices, recall was 66.67% for Female and 60.34% for Male. The Nonbinary slice has only 29 rows and two positives, so its metrics are explicitly marked low-support. Across regions, the maximum-minus-minimum recall gap was 5.95 percentage points. These are descriptive synthetic-data checks, not proof of individual, legal, or real-world fairness. See [reports/fairness_slices.csv](reports/fairness_slices.csv) and [reports/fairness_disparities.json](reports/fairness_disparities.json).

Test AP uncertainty uses 300 bootstrap resamples. At inference, scores from the review threshold through the next 0.04 probability are routed as borderline abstentions; at least two p01/p99 or unseen-category warnings cause OOD abstention regardless of score.

## Data and schema design

The dataset contains 12,000 synthetic claims from 2024-01-01 through 2025-12-30 and no real personal data. The target `is_abnormal` becomes available only after `audit_completed_at`. The model uses submission-time amount/policy, timeliness, prior velocity/spend, duplicate, receipt, timing, cross-border, region, department/level, expense/merchant/country categories, and payment method fields. `amount_to_policy_ratio` is deterministic and derived by the API.

The exact contract is [configs/data_contract.json](configs/data_contract.json). Employee/expense IDs, audit time, target, and `employee_gender` are excluded. Lineage and limitations are in [reports/data_card.md](reports/data_card.md), with quality state in [reports/data_quality_report.json](reports/data_quality_report.json) and split boundaries in [reports/split_manifest.json](reports/split_manifest.json).

## Interfaces

### Batch interfaces

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe scripts\generate_data.py
.\.venv\Scripts\python.exe scripts\train.py
.\.venv\Scripts\python.exe scripts\benchmark_api.py
.\.venv\Scripts\python.exe -m pytest
```

`scripts/run_all.ps1` runs the same sequence. Dataset/model hashes and all measured outputs are regenerated; experiment runs append to the JSONL ledger.

### API

```powershell
$env:PYTHONPATH = "src"
$env:EXPENSE_API_KEY = "replace-in-production"
.\.venv\Scripts\python.exe -m uvicorn expense_ml.api:app --host 127.0.0.1 --port 8000
```

- `GET /health`: readiness plus model/data/schema versions.
- `POST /v1/predict`: validated single-claim scoring; send `X-API-Key` when configured.
- `GET /metrics`: process-local request count, error count, and observed P95.
- Interactive contract: `http://127.0.0.1:8000/docs`.

The prediction response includes calibrated probability, threshold, one of four decisions, uncertainty state, up to three reason codes with raw/calibrated perturbation deltas, OOD warnings, request UUID, UTC timestamp, schema/data/model/policy versions, and a canonical-input SHA-256 hash.

## Explainability

- **Global:** held-out permutation decrease in average precision. The leading fields were amount-to-policy ratio, receipt presence, and recent duplicate count.
- **Local:** one-feature-at-a-time perturbation against training medians/modes, vectorized into one scoring call. Raw-score and calibrated-probability deltas are both returned because isotonic steps can flatten the latter.
- **Counterfactual:** searches up to three truthful/actionable scenarios such as adding valid evidence, resolving an erroneous duplicate link, or a future corporate-card process.

These explain model behavior, not causality, employee intent, or guilt. Correlated inputs can divide or move attribution; counterfactual historical facts must never be falsified. Artifacts are [reports/global_permutation_importance.csv](reports/global_permutation_importance.csv), [reports/local_explanations.json](reports/local_explanations.json), and [reports/counterfactual_explanations.json](reports/counterfactual_explanations.json).

## Tests, error handling, security, and observability

Ten tests cover manifest hashes, data gates, temporal separation, leakage/protected exclusions, version/audit fields, OOD abstention, invalid and extra fields, API-key behavior, capacity, quality target, and artifact integrity. Latest result: **10 passed**.

- Input errors return FastAPI `422`; bad configured keys return `401`; missing/unreadable artifacts return `503`; unexpected scoring failures return a generic `500` and increment errors.
- The demo API-key option is not full production security. Production requires TLS, secret management/rotation, authorization, rate limiting, durable audit retention, and threat testing.
- Logs contain request ID, decision, versions, and feature hash—not raw claim values. `/metrics` is intentionally process-local; production should export latency/error/decision, drift, calibration, subgroup, capacity, override, and review-yield telemetry without sensitive payloads.

## Repository structure and README outline

```text
Week-2/
|-- README.md                       # problem -> design -> evidence -> operation
|-- configs/                        # project policy and exact data contract
|-- data/raw/ + data/manifests/     # versioned CSV and SHA-256 lineage
|-- src/expense_ml/                 # generation, gates, models, eval, explain, API
|-- scripts/                        # reproduce, benchmark, refresh, and demo
|-- experiments/experiments.jsonl   # every model run and parameter set
|-- artifacts/model/                # joblib bundle and artifact manifest
|-- reports/                        # metrics, calibration, fairness, cards, reasons
|-- tests/                          # data, temporal, model, policy, security, API tests
|-- docs/                           # design and timed presentation scripts
|-- requirements.txt
`-- pyproject.toml
```

This README is deliberately ordered as: problem and boundaries → requirements → architecture → milestones/pseudocode → measured evidence → schema/interfaces → explainability/controls → repository/use → demos → limitations/interview preparation.

## Setup and reproducibility

```powershell
cd E:\print-out\AI-45\POC\Week-2
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\scripts\run_all.ps1
```

To run only the prepared live demo:

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe scripts\demo.py
```

## Demo scripts

The exact talk tracks are in [docs/02_demo_script.md](docs/02_demo_script.md).

- **3–5 minute business demo:** problem and non-goal; capacity/cost policy; measured quality/yield/recall; one live reason-coded response; human-review and fairness caveats.
- **5–10 minute technical depth:** contract/hash/lineage; four time splits; baseline-before-tuning experiment ledger; calibration and cost threshold; subgroup/uncertainty/explanation artifacts; API security/audit state; tests and latency evidence.

## Limitations and next steps

- Synthetic labels, features, and subgroup membership make this an engineering POC, not evidence of production effectiveness or fairness.
- Audit labels have no delay censoring, investigator disagreement, or feedback-loop simulation.
- Isotonic calibration is stepwise; it improves calibration but introduces ranking ties and zero calibrated deltas for some local perturbations.
- Fixed thresholds can drift from capacity as prevalence changes; a production batch queue should combine a monitored cutoff with top-k capacity enforcement.
- Single-process metrics and TestClient latency do not represent production concurrency.
- Reference perturbations can be unrealistic under feature correlation and are non-causal.

Next: validate warehouse/label semantics with finance; add delayed-label and drift monitoring; use repeated time backtests; define legal/protected-class review; estimate cost assumptions from operations; add a durable feature/audit store; containerize with TLS/auth/rate limits; load test concurrently; shadow deploy; monitor overrides; and define retraining/rollback gates.

## Likely interviewer questions

1. Why use four chronological splits instead of cross-validation or a random split?
2. Why did logistic regression beat the trees, and why keep the simpler winner?
3. Why does calibration lower AP here while improving Brier score and ECE?
4. How exactly was the threshold chosen, and how would you enforce capacity under drift?
5. What leakage risks exist in audit outcomes, employee histories, duplicates, and resubmissions?
6. Why is gender excluded while region remains, and how would legal/fairness requirements change that?
7. What does abstention cover, and how do OOD warnings affect reviewer load?
8. What can permutation, local perturbation, and counterfactual explanations not tell us?
9. How would you validate the $500/$15 costs and estimated savings?
10. What monitoring, shadow deployment, rollback, and delayed-label strategy would you use in production?
