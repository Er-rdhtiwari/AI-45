# Demo Script

## 3–5 minutes: business value

**0:00–0:40 — Frame the decision.** “Finance cannot inspect every claim. This system does not decide fraud or reject reimbursement; it prioritizes human review of claims likely to be audit-confirmed abnormal.” Show the problem/non-goals at the top of `README.md`.

**0:40–1:30 — Show measured value.** Open `reports/evaluation_report.md`. On 1,800 newest claims: 10.94% reviewed under 12% capacity, 63.33% abnormal recall, 38.58% yield. Explain the $500 missed-case and $15 false-review scenario. The $36,185 avoided-cost calculation is synthetic and not realized savings.

**1:30–2:30 — Run the workflow.** Execute:

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe scripts\demo.py
```

Point out the calibrated probability, human-review decision, recent-duplicate/receipt/policy reason codes, no OOD warnings, model/data/schema/policy versions, request UUID, UTC timestamp, and feature hash. Do not imply that a reason proves wrongdoing.

**2:30–3:30 — Trust and controls.** Open `reports/calibration_plot.png` and `reports/fairness_slices.csv`. State that gender is excluded from prediction, rare-group metrics are marked low-support, and fairness results on synthetic data are directional only. Explain borderline and OOD abstention.

**3:30–4:00 — Close.** “The POC proves a reproducible and auditable workflow; production value still requires real label validation, cost measurement, time backtests, shadow deployment, and human governance.”

## 5–10 minutes: technical depth

**0:00–1:00 — Contract and lineage.** Show `configs/data_contract.json`, the dataset manifest/hash, and quality report. Explain why target, audit time, IDs, and gender are excluded.

**1:00–2:00 — Leakage-safe design.** Show `reports/split_manifest.json`: oldest 60% train, then 15% calibration, 10% validation, newest 15% untouched test. Explain why calibration and threshold selection need separate windows.

**2:00–3:30 — Baseline and experiments.** Show `experiments/experiments.jsonl`. Dummy comes first; defaults compare logistic, RF, HGB, and Isolation Forest; only the default validation winner is tuned. Balanced logistic improves validation AP from 0.3840 to 0.3961 and remains explainable/fast.

**3:30–5:00 — Evaluation and policy.** Contrast ranking, probability, and operational metrics. Raw AP is 0.4245, calibrated AP 0.3785 because isotonic ties; Brier improves 0.1414 to 0.0484 and ECE 0.2574 to 0.0134. Threshold search minimizes `500*FN + 15*FP` under buffered 12% capacity.

**5:00–6:15 — Explainability/fairness.** Open global importance, one local JSON record, and one counterfactual. Discuss correlation, non-causality, truthful facts, small group support, and the 5.95-point region recall spread.

**6:15–7:30 — Serving and auditability.** Walk through `/health`, `/v1/predict`, `/metrics`, strict request fields, derived ratio, OOD warnings, abstention, reason-code perturbation, versions, and hashed audit payload. Mention optional API key and production security gaps.

**7:30–8:30 — Verification.** Run `pytest`; show 10 passing tests. Open the latency report: 29.92 ms P95, 37.07 sequential req/s, zero failures across 150 in-process requests, with its explicit benchmark caveat.

**8:30–10:00 — Production path and Q&A.** Discuss real target semantics, delayed labels, repeated backtests, top-k queue enforcement, drift/fairness/calibration/override monitoring, shadow deployment, rollback, and cost validation.
