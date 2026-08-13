# Data Card: expenses-synthetic-v1

## Purpose and target

Synthetic employee-expense claims for a portfolio ML system. `is_abnormal` is sampled to represent a later completed audit that confirms an abnormal claim. The label is unavailable at submission time.

## Provenance, version, and lineage

- Rows: 12000
- Period: 2024-01-01T01:17:00+00:00 to 2025-12-30T23:51:00+00:00
- Target rate: 0.0658
- Generator seed: 45
- SHA-256: `2e41e50a9cec73f84e1ee5d224826bd245ae7fb579b0bcf3205e0a81c5bceb42`
- Personal/external data: none

See `configs/data_contract.json`, `data/manifests/expenses_v1.manifest.json`, and `reports/split_manifest.json`. Quality gates passed: True.

## Sensitive fields and use

`employee_gender` is synthetic, excluded from training/inference, and used only for evaluation. Employee and expense IDs are excluded. Region is a modeled operational field and separately audited.

## Limitations

Synthetic patterns are simpler than real fraud, labels have no investigator disagreement, distribution shift is limited, and rare subgroup estimates are unstable. Do not use this dataset to make claims about real people or populations.
