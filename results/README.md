# Result Artifacts

## Authoritative forecasts

- `validated_forecasts.csv`: the `bitcoin-v1` aligned Bitcoin freeze with 1,061 rows and 11 columns: `Timestamp`, `Actual`, and nine saved model vectors—`Naive`, `Persistence_Enhanced_LSTM`, `Chronos_Bolt_Tiny`, `TimesFM`, `ARIMA_Rolling`, `Prophet_Periodic_Refit`, `Simple_Exp_Smoothing`, `Holt_Winters`, and `Persistence_Enhanced_Transformer`. The 7-Day Moving Average is reconstructed deterministically downstream from the seven strictly prior prices.
- `electricity/protocol_a_validated_forecasts.csv`: aligned rolling one-step electricity vectors.
- `electricity/protocol_b_validated_forecasts.csv`: aligned true 48-step day-ahead electricity vectors.
- `electricity/protocol_b_validated_horizon_metrics.csv`: audited horizon-specific Protocol B metrics.

These files must not be overwritten by exploratory runs. Their hashes are recorded in [`authoritative_artifact_hashes.md`](authoritative_artifact_hashes.md).

## Supporting evidence

Bitcoin model-specific CSVs preserve source vectors used to assemble the validated artifact. Corrected Bitcoin downstream evidence uses training-defined regimes, Temporal Stability, method-labelled uncertainty, HAC Diebold–Mariano tests, Holm adjustment, and component-first trustworthiness synthesis. The `*_v2.csv`, `*_training_defined.csv`, and `*_hac_holm.csv` files preserve this rebuilt evidence without silently replacing historical artifacts. Electricity forecast files preserve baseline, DHR-ARIMA, LSTM, Chronos, and TimesFM evidence for each protocol.

## Protocol separation

Electricity Protocol A is rolling one-step at 30-minute resolution. Protocol B is a true non-overlapping 48-step day-ahead task. Their forecasts, metrics, exploratory composite summaries, and significance tests remain separate and must not be merged into a single electricity ranking.

## Reproducibility levels

Downstream trustworthiness, significance, and cross-domain analyses operate on saved forecast vectors and do not require model checkpoints. Regenerating forecasts is a separate, substantially more expensive operation and must use a new experiment version rather than overwrite frozen artifacts.

**Artifact-level reproducibility** is available directly from saved vectors: existence, SHA-256 hashes, schemas, keys, row counts, and key metrics can be checked with `python src/verify_research_artifacts.py`. This path uses pandas/NumPy only and does not load a forecasting model.

**End-to-end regeneration** is a different and more demanding claim. It requires external raw datasets, exact model checkpoints, compatible package versions, and substantial CPU time. Frozen artifacts permit verification of reported results even when those dependencies are unavailable.

## Cross-domain outputs

- `cross_domain_model_comparison.csv`
- `cross_domain_foundation_model_comparison.csv`
- `cross_domain_uncertainty_comparison.csv`
- `cross_domain_significance_summary.csv`

These compare within-domain ranks, scale-independent metrics, baseline-relative performance, uncertainty, and significance summaries. They do not compare raw Bitcoin and electricity MAE/RMSE values.

## Exploratory or superseded material

Diagnostic images live under `figures/`. Earlier component metrics, including `electricity/protocol_b_horizon_metrics.csv`, are retained for provenance when a validated counterpart exists; use the explicitly validated artifact for final reporting. An artifact is authoritative because it passes the documented validation and freeze process, not merely because it is stored in this directory.
