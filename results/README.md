# Result Artifacts

## Authoritative forecasts

- `validated_forecasts.csv`: aligned Bitcoin final-test vectors for Naive, Persistence-Enhanced LSTM, Chronos-Bolt-Tiny, and TimesFM.
- `electricity/protocol_a_validated_forecasts.csv`: aligned rolling one-step electricity vectors.
- `electricity/protocol_b_validated_forecasts.csv`: aligned true 48-step day-ahead electricity vectors.
- `electricity/protocol_b_validated_horizon_metrics.csv`: audited horizon-specific Protocol B metrics.

These files must not be overwritten by exploratory runs. Their hashes are recorded in [`../docs/authoritative_artifact_hashes.md`](../docs/authoritative_artifact_hashes.md).

## Supporting evidence

Bitcoin model-specific CSVs preserve source vectors used to assemble the validated artifact. Electricity forecast files preserve baseline, DHR-ARIMA, LSTM, Chronos, and TimesFM evidence for each protocol. Robustness, generalisation, uncertainty, Trust Score, effect-size, and DM tables are authoritative downstream evidence.

## Protocol separation

Electricity Protocol A is rolling one-step at 30-minute resolution. Protocol B is a true non-overlapping 48-step day-ahead task. Their forecasts, metrics, Trust Scores, and significance tests remain separate and must not be merged into a single electricity ranking.

## Cross-domain outputs

- `cross_domain_model_comparison.csv`
- `cross_domain_foundation_model_comparison.csv`
- `cross_domain_uncertainty_comparison.csv`
- `cross_domain_significance_summary.csv`

These compare within-domain ranks, scale-independent metrics, baseline-relative performance, uncertainty, and significance summaries. They do not compare raw Bitcoin and electricity MAE/RMSE values.

## Exploratory or superseded material

Diagnostic images live under `figures/`. Earlier component metrics, including `electricity/protocol_b_horizon_metrics.csv`, are retained for provenance when a validated counterpart exists; use the explicitly validated artifact for final reporting. An artifact is authoritative because it passes the documented validation and freeze process, not merely because it is stored in this directory.
