# Model Card: expense-risk-v1

## Intended use

Prioritize expense claims for a trained finance reviewer. Never auto-reject, accuse, discipline, or make employment decisions.

## Model and versions

- Family: `logistic_regression`
- Parameters selected after baseline: `{'C': 1.0, 'class_weight': 'balanced'}`
- Dataset: `expenses-synthetic-v1`
- Schema: `1.0.0`
- Artifact SHA-256: `017b44b438d06c5db9111cff9135b210c9ec3ec3b048573869634a49e62cb88f`

## Measured performance

See `evaluation_report.md` and `evaluation.json`. Average precision is 0.3785; review rate is 10.94%. Latency is filled only by the separate API benchmark.

## Fairness, calibration, and explainability

Gender is excluded from features. Slice metrics and disparities are in `fairness_slices.csv` and `fairness_disparities.json`. Isotonic calibration uses a dedicated chronological calibration window. Explanations use permutation and reference perturbation; correlated inputs can misattribute importance and counterfactuals are non-causal scenarios.

## Risks and controls

Human review is mandatory for flagged or abstained cases. Inputs are range-checked, multiple OOD warnings trigger abstention, identifiers are not logged, and each response includes versions plus a feature hash. Monitor drift, subgroup recall/FPR, calibration, review yield, capacity, and overrides before production use.
