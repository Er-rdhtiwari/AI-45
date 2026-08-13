# Day 13 POC Story: Explainable, Fairness-Aware Abnormal Expense Review

## Executive summary

This project is an interview-ready classical machine-learning system that prioritizes employee expense claims for human review. It predicts the probability that a later completed audit will confirm an abnormal expense, then applies a business-cost and review-capacity policy to decide whether the claim should be reviewed, treated as uncertain, or recommended for clearing.

The project demonstrates more than model training. It includes a target definition, data contract, deterministic structured dataset, lineage, quality gates, leakage-safe time splitting, baseline-first experimentation, two tree models, an unsupervised anomaly model, tuning, probability calibration, cost-sensitive threshold selection, subgroup evaluation, uncertainty and abstention, three forms of explanation, a versioned FastAPI service, tests, security controls, observability, model/data cards, latency evidence, and timed demo scripts.

The selected model is balanced logistic regression. It was selected because it produced the best validation average precision after all default models were compared and the winning family was tuned. On the newest untouched test period, it achieved:

- ROC AUC: **0.8740**
- Average precision: **0.3785**, versus 6.67% test prevalence
- 95% bootstrap interval for average precision: **0.2997–0.4716**
- Review rate: **10.94%**, below the 12% capacity
- Review yield/precision: **38.58%**
- Abnormal-claim recall: **63.33%**
- Calibrated Brier score: **0.0484**
- Expected calibration error: **0.0134**
- Local in-process API P95 latency: **29.92 ms**
- Verification: **10 tests passed**

All performance and business numbers in this document come from generated project artifacts. The data is synthetic, so these results demonstrate engineering quality and workflow state—not production effectiveness or realized financial savings.

---

## 1. Problem statement

Finance teams receive more employee expense claims than they can manually inspect. Reviewing every claim is expensive and slow, but reviewing too few can miss duplicate, unsupported, policy-breaking, or otherwise abnormal expenses.

The ML problem is:

> Given information available when an expense is submitted, estimate the probability that a later completed audit will confirm the claim as abnormal, and use that probability to prioritize a capacity-constrained human-review queue.

### Target definition

The binary target is `is_abnormal`:

- `1`: a post-submission audit confirms a material policy violation, duplicate, fabricated evidence, or another abnormal condition.
- `0`: the completed audit does not confirm an abnormal condition.

This definition matters because “high model risk” is not the same as fraud. The system only predicts a later audit outcome and never establishes employee intent or guilt.

### Users

- **Finance reviewers:** receive a prioritized review queue and reason codes.
- **Compliance analysts:** inspect policy performance, fairness slices, auditability, and limitations.
- **ML engineers:** train, evaluate, calibrate, version, and monitor the system.
- **Platform engineers:** operate the API, authentication, telemetry, deployment, and rollback.

### Business value

The system concentrates reviewers on claims with higher predicted abnormality while keeping workload below a declared capacity. It supports:

- Higher abnormal-claim capture per reviewer hour.
- More consistent review prioritization.
- Explicit cost and capacity tradeoffs.
- Traceable model, data, schema, and policy versions.
- Human-readable evidence for each recommendation.

### Scope

- Structured expense data available at submission time.
- Offline chronological training and evaluation.
- Probability calibration and cost-sensitive thresholding.
- Human-review recommendation through a synchronous API.
- Descriptive fairness checks and model-behavior explanations.

### Non-goals

- Automatic reimbursement rejection.
- Fraud adjudication, accusation, or disciplinary action.
- Receipt-image or identity verification.
- Employment decisions.
- Causal conclusions about why an expense is abnormal.
- A production-readiness claim based on synthetic data.

---

## 2. Why abnormal-expense detection was chosen

The preparation brief allowed duplicate/abnormal expenses, invoice approval risk, payment-delay risk, or budget-overrun classification. Abnormal expense review was selected because it naturally supports every required ML-system capability:

1. It is a supervised classification problem when audit labels exist.
2. It supports an unsupervised anomaly benchmark when labels are limited.
3. Errors have asymmetric business costs: missing an abnormal claim is more expensive than reviewing a normal one.
4. Finance review capacity creates a concrete threshold-selection constraint.
5. Individual recommendations require local explanations and audit fields.
6. Employee-related data makes subgroup analysis and governance essential.
7. Human review provides a safe abstention path.

This creates a stronger interview story than treating the task as a standalone Kaggle-style accuracy exercise.

---

## 3. Solution in one sentence

A deterministic, leakage-controlled training pipeline compares classical supervised and unsupervised models, calibrates the selected probability model, chooses a review cutoff from explicit costs and capacity, audits subgroup behavior, generates explanations, and serves versioned human-review recommendations through FastAPI.

---

## 4. Requirements

### Functional requirements

1. Generate or ingest realistic structured expense data.
2. Enforce a versioned data contract and quality rules.
3. Record dataset lineage, version, time range, target rate, and hash.
4. Prevent target, post-outcome, ID, and protected-field leakage.
5. Split data chronologically into train, calibration, validation, and test.
6. Establish a dummy and logistic baseline before tuning.
7. Compare logistic regression, random forest, histogram gradient boosting, and Isolation Forest.
8. Log every baseline, default candidate, and tuning experiment.
9. Calibrate the selected model on an independent calibration window.
10. Select a threshold using false-negative cost, false-positive review cost, and reviewer capacity.
11. Measure ranking, probability, operational, subgroup, uncertainty, and latency outcomes.
12. Produce global, local, and counterfactual explanations.
13. Serve predictions with reason codes and audit metadata.
14. Test data, artifact, model-policy, security, abstention, and API behavior.

### Non-functional requirements

- Reproducible CPU-only execution with a fixed seed.
- Immutable hashes for the dataset and model artifact.
- Strict request validation and deterministic derived features.
- P95 local API latency target below 100 ms after warm-up.
- No raw input fields in application logs.
- No gender in training or inference.
- Generic server failures without internal exception leakage.
- Human review for high-risk, borderline, and sufficiently OOD cases.

---

## 5. End-to-end architecture

```text
                         TRAINING AND GOVERNANCE PATH

 Synthetic generator / future expense warehouse
                        |
                        v
       expense CSV + SHA-256 dataset manifest
                        |
                        v
         data contract and quality gates
       schema | type | range | key | time | leakage
                        |
                        v
       chronological, non-overlapping windows
  +-------------+-------------+-------------+-------------+
  | train 60%   | calibrate 15%| validate 10%| test 15%    |
  | 7,200 rows  | 1,800 rows  | 1,200 rows  | 1,800 rows  |
  +------+------+------+------+------+------+------+------+
         |             |             |             |
         v             v             v             v
 baseline/defaults  isotonic      tune winner   one final
 and anomaly fit    calibrator     + threshold    evaluation
         |             |             |             |
         +-------------+-------------+-------------+
                               |
                               v
       model bundle + artifact hash + reports/cards


                           ONLINE INFERENCE PATH

 Client request
       |
       v
 Pydantic schema validation ---- invalid ----> 422 response
       |
       v
 derive amount/policy ratio + OOD checks
       |
       v
 preprocessing -> logistic score -> isotonic probability
       |
       +----------------------+----------------------+
       |                      |                      |
       v                      v                      v
 auto-clear          borderline/high-risk       OOD abstention
 recommendation          human review             human review
       |                      |                      |
       +----------------------+----------------------+
                              |
                              v
 reason codes + warnings + versions + UUID + UTC time + feature hash
```

### Component ownership

| Component | Responsibility |
|---|---|
| Generator | Creates deterministic realistic structured claims without real personal data |
| Data contract | Defines exact fields, types, ranges, allowed values, target, and exclusions |
| Quality gates | Reject malformed, incomplete, duplicated, temporally invalid, or leakage-prone data |
| Experiment pipeline | Establishes baselines, compares candidates, tunes winner, and logs every run |
| Calibrator | Converts raw model scores into operationally meaningful probabilities |
| Policy layer | Converts probability into review, abstention, or clear recommendation |
| Explanation layer | Produces global, local, and counterfactual model-behavior evidence |
| FastAPI | Validates requests and returns predictions plus audit state |
| Reports/cards | Preserve model, data, fairness, calibration, and evaluation evidence |

---

## 6. Thought process and key design decisions

### 6.1 Human decision support instead of automated rejection

Expense risk is a high-impact employee context. A false positive can inconvenience or unfairly implicate someone. Therefore, the model only recommends review. High risk, borderline uncertainty, and distribution warnings all terminate in a human decision.

### 6.2 A precise post-audit target instead of a vague “fraud” label

“Fraud” is legally and operationally ambiguous. The target is defined as an audit-confirmed abnormal expense. This produces a label that a finance organization could operationalize and avoids claiming the model detects intent.

### 6.3 Synthetic data with explicit limitations

No production expense warehouse or audit system was available. The core capability therefore uses a deterministic synthetic generator rather than mocks or fabricated report numbers. The generator creates plausible interactions—policy exceedance, missing receipt, recent duplicates, risky merchants, cross-border activity, late submission, and claim velocity—while retaining stochastic label noise.

Synthetic performance proves that the repository works end to end. It does not prove that the model will perform on real employee claims.

### 6.4 Chronological splitting instead of random splitting

A random split can let near-contemporaneous behavioral patterns appear in both training and test data, producing optimistic results. The production question is “Can a model trained on history rank future claims?” The project therefore uses four chronological windows:

| Split | Rows | Period | Target rate | Purpose |
|---|---:|---|---:|---|
| Train | 7,200 | 2024-01-01 to 2025-03-15 | 6.50% | Fit models |
| Calibration | 1,800 | 2025-03-15 to 2025-07-03 | 6.44% | Fit isotonic calibrator |
| Validation | 1,200 | 2025-07-03 to 2025-09-15 | 7.08% | Model selection, tuning, threshold |
| Test | 1,800 | 2025-09-15 to 2025-12-30 | 6.67% | Final untouched evaluation |

The four-way split prevents the same validation window from simultaneously training the model, fitting calibration, selecting a threshold, and claiming final performance.

### 6.5 Baseline before tuning

The experiment order is deliberate:

1. Prior-probability dummy baseline.
2. Untuned logistic regression.
3. Untuned random forest.
4. Untuned histogram gradient boosting.
5. Label-free Isolation Forest.
6. Hyperparameter candidates for only the best default supervised family.

This prevents premature optimization and makes the incremental value of modeling measurable.

### 6.6 Choose the simplest winner, not the most complex model

Both tree models were competitive, but untuned logistic regression had the strongest validation average precision. Balanced logistic regression then improved it further. Selecting it provides:

- Strongest measured validation ranking.
- Lower inference cost.
- Easier operational explanation.
- More stable behavior on a medium-sized structured dataset.
- A useful interview lesson: complexity is not a selection criterion; evidence is.

### 6.7 Average precision as the main selection metric

Only about 6–7% of claims are abnormal. Accuracy would be misleading because predicting every claim as normal would already be highly accurate. Average precision focuses on positive-class ranking and precision-recall tradeoffs in an imbalanced setting. ROC AUC remains useful but is not sufficient by itself.

### 6.8 Calibrate after selection

The raw balanced-logistic score ranks well but is not a reliable operational probability. Isotonic regression is fitted only on the calibration split. Calibration dramatically improves Brier score and expected calibration error, which makes cost-based thresholding more defensible.

The tradeoff is that isotonic regression creates stepwise probabilities and ties. This slightly lowers average precision and can make a one-feature calibrated probability delta equal zero even when the underlying raw model score moves. The API therefore exposes both raw-score and calibrated-probability explanation deltas.

### 6.9 Business threshold instead of 0.5

A default threshold of 0.5 ignores class imbalance, reviewer capacity, and error cost. The project scans validation probabilities and minimizes:

```text
total policy cost = 500 USD × false negatives
                  + 15 USD × reviewed normal claims
```

The cutoff must also satisfy a buffered capacity. Maximum review capacity is 12%, while threshold selection uses a one-percentage-point buffer to reduce the chance of exceeding capacity under modest time drift.

### 6.10 Abstention as a first-class outcome

The model can decline to make a normal automated recommendation:

- Probabilities between the review cutoff and cutoff + 0.04 are marked borderline and sent to human review.
- At least two input distribution warnings trigger OOD abstention regardless of score.
- High-risk in-distribution scores go to standard high-risk review.
- Only sufficiently low-risk, in-distribution claims receive an auto-clear recommendation.

This is safer than pretending every probability is equally reliable.

### 6.11 Model-agnostic explanations

The explanation framework works even if the selected model family changes:

- Permutation importance for global behavior.
- Reference perturbation for a single claim.
- Constrained scenario search for counterfactuals.

SHAP was not required for the core capability. The chosen approach keeps dependencies smaller and makes the mechanics easy to explain, while documenting that perturbation methods are not causal and can be distorted by correlated inputs.

---

## 7. Data design, contract, lineage, and quality

### Dataset state

| Field | Value |
|---|---|
| Dataset version | `expenses-synthetic-v1` |
| Schema version | `1.0.0` |
| Rows | 12,000 |
| Columns | 25 |
| Event range | 2024-01-01 through 2025-12-30 |
| Overall target rate | 6.575% |
| Generator seed | 45 |
| Dataset SHA-256 | `2e41e50a9cec73f84e1ee5d224826bd245ae7fb579b0bcf3205e0a81c5bceb42` |

### Feature groups

| Group | Important fields |
|---|---|
| Claim amount and policy | `amount_usd`, `policy_limit_usd`, derived `amount_to_policy_ratio` |
| Submission timing | `days_since_expense`, weekend, outside-business-hours |
| Employee history | prior 30-day claim count and total, tenure |
| Evidence and duplication | receipt attached, duplicate count in seven days |
| Operational context | cross-border, region, department, employee level |
| Claim categorization | expense category, merchant risk, country risk, payment method |

### Excluded fields

- `is_abnormal`: target leakage.
- `audit_completed_at`: post-outcome timestamp.
- `employee_id` and `expense_id`: identifiers rather than generalizable behavior.
- `employee_gender`: evaluation-only protected field.
- `submitted_at`: used for temporal splitting, not direct prediction.

### Why derive amount-to-policy ratio

An amount of $500 has different meaning under a $100 meal limit and a $1,400 airfare limit. The ratio expresses policy exceedance consistently. It is stored in training data and deterministically derived by the API so callers cannot provide an inconsistent amount/ratio pair.

### Data-quality results

All configured gates passed:

- 12,000 rows found.
- Zero missing required fields.
- Zero duplicated primary keys.
- No missing or unexpected columns.
- Event timestamps are monotonically ordered.
- Every audit completion is after its submission.
- Target rate is within the allowed range.
- No excluded columns appear in model features.
- Dataset bytes match the manifest SHA-256.

### Lineage

```text
project_config seed
        |
        v
deterministic generator
        |
        v
chronologically sorted CSV
        |
        +--> SHA-256/version/row/time/prevalence manifest
        |
        v
contract checks -> split manifest -> experiments -> model/report artifacts
```

No real personal data or external service was used.

---

## 8. Preprocessing and modeling

### Preprocessing

- Numeric and Boolean fields: median imputation followed by standard scaling.
- Categorical fields: most-frequent imputation followed by one-hot encoding.
- Unknown categorical values: ignored by the encoder, while the inference layer separately produces an OOD warning.
- Transformations are inside the fitted scikit-learn pipeline so training and serving use identical logic.

Even though generated data currently has no missing values, imputation makes the pipeline structurally robust and documents expected behavior for future sources.

### Model comparison on validation

| Model | Stage | ROC AUC | Average precision |
|---|---|---:|---:|
| Prior dummy | Baseline | 0.5000 | 0.0708 |
| Logistic regression | Untuned candidate | 0.8396 | 0.3840 |
| Random forest | Untuned candidate | 0.8315 | 0.3738 |
| Histogram gradient boosting | Untuned candidate | 0.8368 | 0.3649 |
| Isolation Forest | Unsupervised candidate | 0.6744 | 0.1589 |
| Logistic, `C=0.3`, unbalanced | Tuning candidate | 0.8399 | 0.3835 |
| Logistic, `C=1`, unbalanced | Tuning candidate | 0.8396 | 0.3840 |
| Logistic, `C=1`, balanced | **Selected** | **0.8439** | **0.3961** |
| Logistic, `C=3`, unbalanced | Tuning candidate | 0.8389 | 0.3830 |

Nine experiments were recorded. Isolation Forest did not use labels during fitting; labels were used only afterward to evaluate how well its anomaly score ranked audit-confirmed abnormal claims.

### Selected model artifact

| Field | Value |
|---|---|
| Model version | `expense-risk-v1` |
| Family | Logistic regression |
| Parameters | `C=1.0`, `class_weight=balanced` |
| Dataset version | `expenses-synthetic-v1` |
| Schema version | `1.0.0` |
| Artifact SHA-256 | `017b44b438d06c5db9111cff9135b210c9ec3ec3b048573869634a49e62cb88f` |

The serialized bundle contains preprocessing, estimator, calibrator, feature order, training reference values, numeric ranges, known categories, threshold policy, explanation caveat, and all versions.

---

## 9. Detailed evaluation report

### Test-set classification and ranking

The test set contains 1,800 claims, including 120 abnormal claims.

| Metric | Result |
|---|---:|
| ROC AUC | 0.8740 |
| Calibrated average precision | 0.3785 |
| Raw average precision | 0.4245 |
| AP bootstrap 95% interval | 0.2997–0.4716 |
| Log loss | 0.1740 |
| F1 at operational cutoff | 0.4795 |

The average precision is substantially higher than the 6.67% positive prevalence, showing that the model ranks abnormal claims above random selection.

### Test confusion matrix at the operational cutoff

```text
                         Predicted clear   Predicted review
Actually normal              1,559              121
Actually abnormal               44               76
```

From these measured counts:

```text
reviewed claims = 121 + 76 = 197
review rate     = 197 / 1,800 = 10.94%
review yield    = 76 / 197 = 38.58%
abnormal recall = 76 / 120 = 63.33%
```

### Business-cost calculation

The declared scenario assumes:

- $500 for each missed abnormal claim.
- $15 reviewer cost for each normal claim sent to review.

Measured test calculation:

```text
false-negative cost = 44 × $500 = $22,000
false-positive cost = 121 × $15 =  $1,815
total policy cost                 = $23,815

no-review cost      = 120 × $500 = $60,000
estimated avoided cost           = $60,000 - $23,815
                                 = $36,185
```

The expected policy cost per 1,000 claims is $13,230.56. These are scenario-model outputs, not booked savings. A real deployment must estimate costs from reviewer time, recovery rate, claim value, appeal cost, employee friction, and downstream impact.

### Threshold state

| Policy value | Value |
|---|---:|
| Review threshold | 0.174603 |
| Maximum review rate | 12.00% |
| Selection buffer | 1 percentage point |
| Validation review rate | 9.17% |
| Test review rate | 10.94% |
| Borderline width | 0.04 probability |

The threshold was selected only on validation data. Test capacity was checked afterward, not used to choose the cutoff.

---

## 10. Calibration and uncertainty

### Why calibration matters

A risk-ranking model can order claims correctly while producing unreliable numerical probabilities. Because the policy assigns business costs to probabilities and thresholds, probability quality matters in addition to ranking.

### Measured calibration change

| Metric | Raw model | Isotonic calibrated |
|---|---:|---:|
| Brier score | 0.1414 | 0.0484 |
| Expected calibration error | 0.2574 | 0.0134 |
| ROC AUC | 0.8776 | 0.8740 |
| Average precision | 0.4245 | 0.3785 |

Lower Brier score and lower expected calibration error are better. Ranking metrics fall slightly because isotonic regression maps ranges of raw scores to the same stepwise probability.

### Statistical uncertainty

Average precision uses 300 nonparametric bootstrap resamples. The measured 95% interval is 0.2997–0.4716. The interval communicates that performance is estimated from a finite test sample rather than known exactly.

### Operational uncertainty

The service returns an explicit uncertainty state:

- `in_distribution`
- `borderline_probability`
- `out_of_distribution`

At least two learned-range/category warnings trigger `manual_review_ood_abstention`. Borderline scores trigger `manual_review_borderline_abstention`. Neither case is silently treated as low risk.

---

## 11. Explainability

### Global explanation

Permutation importance measures the decrease in held-out average precision when one input is shuffled. The leading measured features were:

| Feature | Mean AP decrease when permuted |
|---|---:|
| Amount-to-policy ratio | 0.2871 |
| Receipt attached | 0.1117 |
| Duplicate count in seven days | 0.0788 |
| Policy limit | 0.0242 |
| Merchant risk tier | 0.0107 |
| Cross-border indicator | 0.0088 |
| Outside-business-hours indicator | 0.0077 |

Permutation importance is not causality. Correlated fields can share, hide, or transfer importance.

### Local explanation

For one claim, the system replaces each feature with its training median or mode, scores all perturbations in a single vectorized batch, and reports the largest changes.

Each local reason contains:

- Feature and stable reason code.
- Observed value.
- Training reference value.
- Raw model-probability delta.
- Calibrated-probability delta.
- Whether the observed value raises or lowers modeled risk.

Raw and calibrated deltas are both shown because isotonic calibration may produce a zero calibrated delta across a flat step even when the underlying model changes.

### Counterfactual explanation

The counterfactual search considers up to three constrained scenarios, such as:

- Attach valid receipt evidence.
- Resolve a genuinely erroneous duplicate link.
- Use a corporate card for a future comparable claim.
- Submit a future claim promptly.
- Use a verified lower-risk merchant in a future comparable situation.

The output says whether a scenario crosses below the review cutoff. A proposal that does not cross is reported honestly. These scenarios explain model behavior and are not instructions to rewrite truthful historical facts.

### Explanation caveats

- Association is not causation.
- Reasons do not prove wrongdoing.
- One-feature perturbations may create unlikely combinations.
- Correlated features can distort attribution.
- Counterfactual feasibility requires finance and policy review.

---

## 12. Fairness evaluation

### Protected-field strategy

`employee_gender` is included only in the synthetic offline evaluation data. It is excluded from preprocessing, model fitting, artifact features, and the inference request.

### Gender slices

| Group | Rows | Positives | Review rate | Review precision | Recall |
|---|---:|---:|---:|---:|---:|
| Female | 833 | 60 | 12.00% | 40.00% | 66.67% |
| Male | 938 | 58 | 10.23% | 36.46% | 60.34% |
| Nonbinary | 29 | 2 | 3.45% | 100.00% | 50.00% |

The Nonbinary slice is explicitly low-support: 29 records and two positives cannot support a reliable conclusion. The overall gender recall max-minus-min is 16.67 percentage points, but that number is dominated by the low-support group. Even the better-supported group comparison should be treated as descriptive because the data is synthetic.

### Region slices

| Region | Rows | Positives | Review rate | Recall |
|---|---:|---:|---:|---:|
| APAC | 569 | 50 | 13.88% | 64.00% |
| EMEA | 430 | 21 | 10.93% | 61.90% |
| LATAM | 275 | 21 | 10.18% | 66.67% |
| North America | 526 | 28 | 8.17% | 60.71% |

The measured regional recall gap is 5.95 percentage points. Region remains a modeled operational field, so its use needs a real legal, policy, proxy-risk, and necessity review before deployment.

### What this fairness analysis can and cannot say

It can identify differences in selection rate, recall, false-positive rate, prevalence, and support. It cannot establish legal fairness, absence of discrimination, causal fairness, or individual fairness—especially with synthetic and low-support groups.

---

## 13. FastAPI serving design

### Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /health` | Readiness and model/data/schema versions |
| `POST /v1/predict` | Validate and score one expense claim |
| `GET /metrics` | Process-local request, error, and P95 latency state |
| `/docs` | Generated OpenAPI interface |

### Input behavior

- Extra fields are forbidden.
- Numeric ranges and categorical values are validated.
- `employee_gender` is rejected because it is not in the request contract.
- `amount_to_policy_ratio` is computed from amount and policy limit.
- The caller cannot supply target, employee ID, expense ID, or audit timestamp.

### Output and audit fields

Every successful prediction includes:

- Calibrated abnormal probability.
- Operational review threshold.
- Decision and uncertainty status.
- Up to three reason codes and explanations.
- Distribution warnings.
- Request UUID and UTC scoring time.
- Model, dataset, schema, and policy versions.
- SHA-256 of the canonical input payload.

### Decision states

```text
manual_review_ood_abstention
review_high_risk
manual_review_borderline_abstention
auto_clear_recommendation
```

“Auto-clear” remains a recommendation rather than an irreversible reimbursement decision.

### Error handling

- `422`: invalid range, category, missing field, or forbidden extra field.
- `401`: invalid or missing key when `EXPENSE_API_KEY` is configured.
- `503`: model artifact missing or unreadable.
- `500`: unexpected scoring error, returned without internal stack details.

### Security

Implemented POC controls:

- Optional constant-time API-key comparison.
- Strict input schema.
- No protected field in the request.
- No raw feature values in structured prediction logs.
- Input hash for traceability.
- Generic error responses at the scoring boundary.

Production additions still required:

- TLS, gateway authentication, and role authorization.
- Secret manager and key rotation.
- Rate limits and abuse protection.
- Durable, access-controlled audit storage and retention.
- Dependency/container scanning and threat modeling.

### Observability

The POC records request count, error count, recent latency, decision, request ID, version, and feature hash. A production service should also monitor:

- Feature and score drift.
- Calibration drift and delayed-label performance.
- Review rate and queue capacity.
- Review yield and abnormal recall.
- Subgroup recall and false-positive rate.
- Reviewer overrides and disagreement.
- OOD and abstention rates.
- Availability, saturation, and error budgets.

---

## 14. Latency and operational evidence

The latest local benchmark used FastAPI `TestClient`, 10 warm-up calls, and 150 measured sequential requests.

| Metric | Result |
|---|---:|
| Failures | 0 of 150 |
| Mean | 26.97 ms |
| P50 | 26.29 ms |
| P95 | 29.92 ms |
| P99 | 36.43 ms |
| Maximum | 67.20 ms |
| Sequential throughput | 37.07 requests/second |
| P95 target | Below 100 ms — passed |

This is an in-process Windows benchmark. It excludes network, API gateway, concurrent load, serialization across services, production logging, autoscaling, and cold starts. It proves local implementation efficiency, not production capacity.

---

## 15. Testing and verification

Ten tests pass. They cover:

1. Dataset manifest hash and row count.
2. Full data-contract success.
3. Chronological split separation and row preservation.
4. Protected, identifier, target, and post-outcome feature exclusions.
5. Prediction probability range and required audit/version fields.
6. Multiple distribution warnings causing OOD abstention.
7. Health endpoint and successful prediction.
8. Rejection of invalid amount and protected extra field.
9. API-key enforcement when configured.
10. Test capacity, quality target, artifact hash, and model version.

The final integrity check also recompiles source, scripts, and tests; verifies dataset and artifact hashes; and asserts the declared quality and latency targets passed.

---

## 16. Repository structure

```text
Week-2/
|-- README.md
|-- Day-13-poc-story.md
|-- requirements.txt
|-- pyproject.toml
|-- configs/
|   |-- data_contract.json
|   `-- project_config.json
|-- data/
|   |-- raw/expenses_v1.csv
|   `-- manifests/expenses_v1.manifest.json
|-- src/expense_ml/
|   |-- data.py                 # deterministic generator and manifest
|   |-- quality.py              # data-contract gates
|   |-- modeling.py             # preprocessing, models, metrics, experiment log
|   |-- evaluation.py           # thresholds, calibration, fairness, uncertainty
|   |-- explain.py              # global/local/counterfactual explanations
|   |-- inference.py            # OOD, policy, audit response
|   |-- api.py                  # FastAPI endpoints and security boundary
|   `-- train.py                # full training/evaluation orchestration
|-- experiments/
|   `-- experiments.jsonl
|-- artifacts/model/
|   |-- expense_risk_v1.joblib
|   `-- artifact_manifest.json
|-- reports/
|   |-- evaluation.json / evaluation_report.md
|   |-- calibration_plot.png / calibration tables
|   |-- fairness_slices.csv / fairness_disparities.json
|   |-- global_permutation_importance.csv
|   |-- local_explanations.json
|   |-- counterfactual_explanations.json
|   |-- data_card.md / model_card.md
|   |-- data_quality_report.json / split_manifest.json
|   `-- latency_report.json
|-- scripts/
|   |-- run_all.ps1
|   |-- generate_data.py / train.py
|   |-- benchmark_api.py / refresh_explanations.py
|   `-- demo.py
|-- tests/
`-- docs/
```

---

## 17. How to run the complete project

From the project root:

```powershell
cd E:\print-out\AI-45\POC\Week-2
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\scripts\run_all.ps1
```

The full workflow:

1. Regenerates deterministic data and its manifest.
2. Validates the dataset.
3. Trains baselines and candidates.
4. Tunes the selected family.
5. Calibrates and chooses the threshold.
6. Generates evaluation, fairness, calibration, and explanation artifacts.
7. Serializes and hashes the model.
8. Benchmarks the API.
9. Runs the tests.

Run the live prepared demo:

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe scripts\demo.py
```

Run the API:

```powershell
$env:PYTHONPATH = "src"
$env:EXPENSE_API_KEY = "replace-in-production"
.\.venv\Scripts\python.exe -m uvicorn expense_ml.api:app --host 127.0.0.1 --port 8000
```

---

## 18. Three-to-five-minute business story

### Opening

“Finance cannot manually inspect every employee expense. I built a human-in-the-loop system that prioritizes claims likely to be confirmed abnormal by a later audit. It never determines fraud or rejects a claim automatically.”

### Business rule

“The policy assumes a missed abnormal claim costs $500 and reviewing a normal claim costs $15, with reviewer capacity capped at 12%. I calibrate probabilities and select the validation threshold that minimizes this cost under capacity.”

### Evidence

“On 1,800 newest claims, the system reviews 10.94%, captures 63.33% of abnormal claims, and produces a 38.58% review yield. Under the scenario costs, that is $36,185 lower than reviewing none. Those are synthetic scenario results, not realized savings.”

### Live prediction

Run `scripts/demo.py`. Point out probability, review decision, recent-duplicate/receipt/policy reason codes, no OOD warnings, and the model/data/schema/policy versions plus request hash.

### Trust and close

“Gender is excluded from prediction, slice performance is reported with low-support warnings, uncertain/OOD claims abstain to humans, and the service has reproducible hashes and tests. Production still requires real target validation, legal review, shadow deployment, drift monitoring, and validated costs.”

---

## 19. Five-to-ten-minute technical story

1. **Contract and target:** audit-confirmed abnormal label, exact JSON schema, post-outcome and protected exclusions.
2. **Lineage:** deterministic seed, CSV hash, schema/data versions, quality report.
3. **Leakage control:** 60/15/10/15 chronological split with calibration and threshold windows separated.
4. **Experiments:** dummy first; logistic, random forest, gradient boosting; label-free Isolation Forest; tune only the default winner.
5. **Selection:** balanced logistic wins validation AP at 0.3961; simpler model retained on evidence.
6. **Calibration:** raw-to-isotonic Brier 0.1414 to 0.0484 and ECE 0.2574 to 0.0134; explain ranking-tie tradeoff.
7. **Policy:** explicit $500/$15 costs and 12% capacity; show confusion-matrix arithmetic.
8. **Uncertainty:** 300-sample AP bootstrap, borderline abstention, multi-warning OOD abstention.
9. **Explainability:** permutation, local raw/calibrated perturbation, constrained counterfactual; all non-causal.
10. **Fairness:** gender excluded, region audited, rare-group support caveat.
11. **Serving:** strict FastAPI contract, derived ratio, optional API key, versions, feature hash, no raw logging.
12. **Evidence:** 10 tests, artifact hashes, 29.92 ms local P95, and explicit production benchmark limitations.

---

## 20. Limitations and risks

1. **Synthetic-data realism:** generated relationships are simpler and cleaner than real finance behavior.
2. **Label quality:** there is no investigator disagreement, appeal, label censoring, or audit-selection bias.
3. **Feedback loops:** prioritized review changes which claims receive labels and can bias future training.
4. **Calibration steps:** isotonic mapping creates ties and flat local calibrated deltas.
5. **Fixed threshold:** prevalence or score drift can push review workload away from the intended capacity.
6. **Fairness evidence:** synthetic and small subgroups cannot establish real-world equity.
7. **Feature proxies:** region, department, and level may correlate with protected or organizational attributes.
8. **Counterfactual realism:** independent perturbations can violate feature relationships.
9. **Latency scope:** the benchmark does not include concurrent production traffic or network overhead.
10. **Security scope:** a demo API key is not production identity, authorization, or secrets management.
11. **Financial assumptions:** $500 and $15 are illustrative and require operational validation.
12. **Human factors:** reviewer consistency, override reasons, employee appeals, and reviewer fatigue are not modeled.

---

## 21. Production next steps

### Data and labels

- Agree on target semantics and audit-completion windows with finance/compliance.
- Measure missingness, audit-selection bias, resubmissions, delayed labels, and investigator disagreement.
- Create point-in-time correct history features from a governed feature pipeline.
- Add repeated temporal backtests across business cycles.

### Modeling and policy

- Validate cost assumptions and recovery amounts.
- Compare Platt, isotonic, and potentially segment-aware calibration over time.
- Add top-k batch queue enforcement alongside the score cutoff.
- Measure reviewer overrides, appeals, and decision consistency.
- Define retraining, promotion, rollback, and challenger gates.

### Fairness and governance

- Obtain legal guidance on protected classes and permitted feature use.
- Add confidence intervals and minimum-support policies for subgroup decisions.
- Evaluate intersections such as region × level, subject to privacy and support.
- Establish documentation, review, and escalation processes for adverse outcomes.

### Platform and monitoring

- Containerize and deploy behind an authenticated TLS gateway.
- Store audit events durably with access controls and retention policies.
- Add concurrent load, soak, failure, and cold-start tests.
- Monitor feature/score drift, calibration, yield, capacity, overrides, OOD, and subgroup performance.
- Shadow deploy before allowing any operational routing.

---

## 22. Likely interviewer questions and concise answers

### Why not use accuracy?

Only 6.67% of test claims are abnormal. A mostly-normal prediction can have high accuracy without helping reviewers. Average precision and review yield better evaluate rare-positive ranking.

### Why chronological instead of random splitting?

The real task predicts future claims from historical data. Chronological windows better expose time drift and prevent optimistic mixing of near-contemporaneous behavior.

### Why four splits?

Train fits model parameters, calibration maps scores to probabilities, validation selects family/hyperparameters/threshold, and test provides one untouched final estimate. Combining these roles would leak selection decisions into reported performance.

### Why did logistic regression beat the trees?

The engineered structured signals, especially policy ratio, are strongly separable with additive effects. Logistic regression had the highest measured validation AP. I chose evidence and operational simplicity rather than assuming trees must win.

### Why include Isolation Forest?

It provides a label-free anomaly benchmark for cold-start or scarce-label conditions. Its AP of 0.1589 was better than the dummy but far below supervised candidates, so it was not deployed.

### Why class weighting?

The positive class is rare. Balanced weighting improved validation average precision from 0.3840 to 0.3961 and therefore won the declared selection rule.

### Why not use 0.5 as the threshold?

Probability 0.5 has no special connection to review capacity or asymmetric costs. The chosen 0.174603 cutoff minimizes validation scenario cost under the capacity constraint.

### Why calibrate, and why did AP fall?

Cost decisions require meaningful probabilities. Isotonic calibration improved Brier and ECE substantially. It is stepwise and introduces ties, so ranking AP can fall even while probability reliability improves.

### How do you prevent leakage?

The contract explicitly excludes target, audit completion time, IDs, and gender. All history fields are defined as prior to submission, splitting is chronological, and preprocessing is fitted within the training pipeline.

### How is uncertainty handled?

Statistical performance gets a bootstrap interval. Operationally, borderline probabilities and multiple distribution warnings abstain to human review.

### Are the explanations causal?

No. Permutation and reference perturbation describe model behavior. Correlation and unrealistic feature combinations can alter attribution. Counterfactuals are constrained scenarios, not proof or advice to modify records.

### Is the model fair?

The project reports descriptive slice metrics and excludes gender from training, but synthetic data and a 29-row Nonbinary slice cannot establish fairness. Real deployment needs legal requirements, representative data, uncertainty intervals, proxy analysis, and ongoing audits.

### What would you monitor?

Inputs, scores, calibration, delayed-label AP/recall, reviewer workload, yield, OOD/abstention, overrides, subgroup recall/FPR, latency, errors, and data/model/schema version consistency.

### What happens if reviewer demand exceeds 12%?

The POC uses a buffered fixed cutoff. Production should additionally use a monitored top-k queue or daily capacity allocator, with escalation rules for OOD and critical policies.

### How would you prove business value?

Validate costs, shadow-score live claims, compare review yield and recovery against current operations or a randomized controlled allocation, include employee/reviewer friction, and measure realized rather than assumed recovery.

---

## 23. What this project demonstrates for a Senior Applied AI/ML Engineer role

### ML judgment

- Starts with target and decision design rather than an algorithm.
- Uses a metric appropriate for imbalance.
- Compares simple, tree-based, and unsupervised methods.
- Tunes only after establishing baselines.
- Selects a simpler model when it wins on evidence.

### Production thinking

- Treats preprocessing and calibration as model artifacts.
- Versions schema, data, model, and policy separately.
- Uses hashes, audit fields, validation, health, telemetry, and tests.
- Measures quality, latency, workload, yield, recall, and scenario cost.

### Responsible AI

- Keeps humans in the decision loop.
- Excludes gender from prediction.
- Reports subgroup support and disparities.
- Implements uncertainty and OOD abstention.
- Documents explanation and counterfactual caveats.

### Communication

- Connects metrics to reviewer workflow and business costs.
- Separates measured results, assumptions, and limitations.
- Provides both a business demo and a technical deep dive.

---

## 24. Evidence map

| Question | Source of truth |
|---|---|
| What is the project and how do I run it? | `README.md` |
| What was designed before implementation? | `docs/01_problem_and_design.md` |
| What is the exact schema and target? | `configs/data_contract.json` |
| What data was used? | `data/manifests/expenses_v1.manifest.json` and `reports/data_card.md` |
| Did data quality pass? | `reports/data_quality_report.json` |
| Are time splits leakage-safe? | `reports/split_manifest.json` |
| What experiments ran? | `experiments/experiments.jsonl` |
| Which artifact is deployed? | `artifacts/model/artifact_manifest.json` |
| What are final measured metrics? | `reports/evaluation.json` and `reports/evaluation_report.md` |
| Is it calibrated? | `reports/calibration_plot.png` and calibration CSV files |
| What are subgroup results? | `reports/fairness_slices.csv` and `reports/fairness_disparities.json` |
| What explains model behavior? | global importance CSV and local/counterfactual JSON reports |
| How fast is the API? | `reports/latency_report.json` |
| What are intended use and limitations? | `reports/model_card.md` |
| How do I present it? | `docs/02_demo_script.md` and `scripts/demo.py` |
| What does testing cover? | `tests/` |

---

## Final takeaway

The strongest part of this Day 13 POC is not that logistic regression achieved a particular score on synthetic data. It is that the project turns a model into a governed decision-support system: target semantics are explicit, leakage is controlled, experiments are traceable, probability is calibrated, thresholds reflect operational constraints, uncertainty can abstain, subgroup behavior is visible, explanations carry caveats, predictions are versioned and auditable, and every major claim has an artifact or test behind it.

That is the core interview story: **build the smallest model that satisfies the measured business objective, then surround it with the data, evaluation, governance, serving, and operational evidence required to use it responsibly.**
