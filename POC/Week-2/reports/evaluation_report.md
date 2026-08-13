# Evaluation Report

All numbers below were measured on the newest untouched chronological test split; none are placeholders.

## Selection and data

- Selected model: `logistic_regression` with `{'C': 1.0, 'class_weight': 'balanced'}`
- Test rows: 1800
- Test prevalence: 0.0667
- Review threshold: 0.174603
- Capacity constraint: 12.00%

## Quality and calibration

- ROC AUC: 0.8740
- Average precision: 0.3785
- 95% bootstrap AP interval: [0.2997, 0.4716]
- Brier score: 0.0484
- Expected calibration error, raw -> calibrated: 0.2574 -> 0.0134

## Business and operations

- Review rate: 10.94%
- Review precision/yield: 38.58%
- Abnormal recall: 63.33%
- Expected policy cost per 1,000 claims: $13,230.56
- Estimated cost avoided vs reviewing none on this test sample: $36,185.00

Costs are scenario assumptions ($500 per missed abnormal claim, $15 per normal claim reviewed), not realized financial savings. The policy is descriptive decision support and requires human review.

## Explainability and fairness

Global permutation importance is in `global_permutation_importance.csv`; local and counterfactual examples are separate JSON files. These describe model associations, not causes or employee intent. Fairness slices are descriptive; low support is marked and this synthetic dataset cannot establish legal or real-world fairness.
