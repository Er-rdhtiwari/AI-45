# Lineage and Operations Notes

## Dataset lineage

1. `expense_ml.data.generate_expenses` deterministically samples synthetic employee profiles and expense events with seed 45.
2. It computes submission-time derived context and samples a later audit-confirmed target from a hidden probabilistic function.
3. `scripts/generate_data.py` writes the chronologically sorted CSV and a manifest with version, generator, row/time/prevalence state, lineage, and SHA-256.
4. Training re-hashes the CSV before reading it, enforces the JSON contract, and writes the quality and split manifests.
5. The model bundle records dataset, schema, model, split, and policy versions; its own SHA-256 is stored beside it.

No external service or mock is used in the core capability. The only source is deterministic synthetic generation because no production warehouse or audit system was supplied.

## Training and deployment lineage

Experiment records are append-only JSON lines with UTC run ID, dataset/split version, seed, stage, family, parameters, and measured validation metrics. Test metrics are written only after selection, calibration, and validation thresholding. The deployed joblib contains preprocessing, selected estimator, isotonic calibrator, training references/ranges/categories, policy, and versions.

## Operational ownership

- Finance owns target/cost semantics, reviewer capacity, adjudication, and override reasons.
- Compliance/legal owns permitted features, protected-group review, retention, and adverse-action boundaries.
- ML owns data/model quality, calibration, drift, subgroup monitoring, retraining, and rollback criteria.
- Platform/security owns authentication, TLS, secrets, authorization, rate limits, durable logs, availability, and incident response.
