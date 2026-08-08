# Bitcoin Case Study

Status: **Frozen as Domain 1 - Financial Time Series**

This document records the completed Bitcoin experiment before expanding to additional domains. It summarises the dataset, preprocessing, forecasting protocol, validated model results, trustworthiness analysis, known failure cases, and remaining limitations.

## Research Objective

The experiment tests whether zero-shot time-series foundation models improve on strong statistical, neural, and persistence benchmarks for non-stationary daily Bitcoin prices, and whether point accuracy agrees with regime robustness, temporal stability, uncertainty calibration, auditability, statistical significance, and practical effect size.

## Dataset

- Dataset: BTC/USD minute-level OHLCV data.
- Physical file: `data/bitcoin/btcusd_1-min_data.csv`.
- Raw columns: `Timestamp`, `Open`, `High`, `Low`, `Close`, `Volume`.
- Raw timestamp format: Unix seconds converted to UTC datetime.
- Raw date range observed in the repository: 2012-01-01 00:01 UTC to 2026-07-07 01:57 UTC.
- Raw rows observed in the repository audit: 7,633,557.
- Forecast target: daily Bitcoin `Close`.

The Energy case study is now complete using South Australian electricity demand. Weather and Transport remain planned domains; their results are not represented in this Bitcoin artifact.

## Preprocessing

The reusable pipeline is implemented in `src/`:

- `src.data_loader.load_bitcoin_data(path)` loads the raw CSV, converts `Timestamp` to UTC datetime, sorts the data, and resets the index.
- `src.preprocessing.prepare_daily_bitcoin_data(df)` resamples minute-level OHLCV data to daily OHLCV.
- `src.metrics` implements MAE, RMSE, MAPE, sMAPE, and training-scaled MASE.
- `src.plots.plot_time_series` provides a simple daily time-series plot.

The daily forecasting series is the resampled daily `Close` column.

## Chronological Split

The Bitcoin workflow uses an 80/20 chronological split:

- Train end: 2023-08-11.
- Test start: 2023-08-12.
- Test end: 2026-07-07.
- Test length: 1,061 daily observations.

The authoritative artifact `results/validated_forecasts.csv` uses this exact test period.

## Forecasting Protocol

The completed primary comparison uses a rolling one-step-ahead protocol:

- Forecast each test date using only observations strictly before that date.
- After each forecast, the observed actual value may be appended to history for the next forecast.
- The current target value is not used before forecasting.
- Future test observations are not used.

This protocol is used for the authoritative saved vectors:

- Naive
- Persistence-Enhanced LSTM
- Chronos-Bolt-Tiny
- TimesFM
- ARIMA Rolling One-Step
- Prophet 30-Day Periodic Refit

The 7-Day Moving Average is a deterministic rolling one-step benchmark recreated from the historical actual series.

ARIMA now has an exact rolling one-step saved vector using per-observation state updates. Prophet uses a clearly labelled 30-day periodic-refit protocol with a strict 128-day past-only context. SARIMA is omitted: lag-7 return ACF was -0.0234 inside the ±0.0269 bound and weekly STL strength was 0.070, so a seven-day seasonal term was not supported; a zero-seasonal SARIMA would duplicate ARIMA.

## Authoritative Forecast Artifact

The frozen Bitcoin forecast artifact is:

```text
results/validated_forecasts.csv
```

Expected columns:

- `Timestamp`
- `Actual`
- `Naive`
- `Persistence_Enhanced_LSTM`
- `Chronos_Bolt_Tiny`
- `TimesFM`
- `ARIMA_Rolling`
- `Prophet_Periodic_Refit`

Repository audit verification:

- Shape: 1,061 rows x 8 columns.
- Date range: 2023-08-12 to 2026-07-07.
- Timestamps are unique and sorted.
- No missing values were found.
- Forecast metrics reproduce from the saved CSV.

Do not overwrite this file unless intentionally regenerating the frozen Bitcoin experiment.

## Models

Authoritative rolling one-step models:

- Naive persistence baseline.
- Persistence-Enhanced LSTM.
- Chronos-Bolt-Tiny.
- TimesFM.
- ARIMA Rolling One-Step.
- Prophet 30-Day Periodic Refit.

Additional deterministic benchmark:

- 7-Day Moving Average.

Exploratory, failed, or non-authoritative models:

- Original raw-price LSTM.
- Improved experimental LSTM.
- Collapsed Transformer.
- Corrected but over-smoothed Transformer.

Models not included in the completed Bitcoin scope:

- Moirai / Uni2TS.
- PatchTST.
- iTransformer.

PatchTST and iTransformer remain blocked/planned. Moirai/Uni2TS is likewise deferred to an isolated compatible environment.

## Authoritative Metrics

Metrics reproduced directly from `results/validated_forecasts.csv`:

| Model | MAE | RMSE | MAPE | sMAPE |
|---|---:|---:|---:|---:|
| Naive | 1290.353242 | 1853.624774 | 1.742747 | 1.744142 |
| ARIMA Rolling One-Step | 1299.874638 | 1866.302859 | 1.754004 | 1.754209 |
| Persistence-Enhanced LSTM | 1321.365311 | 1881.091190 | 1.783956 | 1.791645 |
| TimesFM | 1349.946786 | 1924.199337 | 1.823179 | 1.823895 |
| Chronos-Bolt-Tiny | 1424.025828 | 1994.007926 | 1.934509 | 1.928782 |
| Prophet 30-Day Periodic Refit | 8195.262862 | 10781.162873 | 11.199767 | 11.287185 |

The Naive baseline has the strongest point accuracy among the frozen saved-vector models.

## Regime-Conditional Robustness Results

The trustworthiness workflow evaluates performance by market regime using rolling return behavior:

- Low-volatility periods.
- High-volatility periods.
- Major upward movements.
- Major downward movements.

Foundation-model regime results recorded from the validated workflow:

| Model | Regime | MAE | RMSE |
|---|---|---:|---:|
| Chronos-Bolt-Tiny | Low volatility | 1248.161988 | 1706.361802 |
| Chronos-Bolt-Tiny | High volatility | 1871.323135 | 2539.070134 |
| Chronos-Bolt-Tiny | Major upward movement | 2741.499929 | 3136.445465 |
| Chronos-Bolt-Tiny | Major downward movement | 3334.871796 | 3755.413182 |
| TimesFM | Low volatility | 1004.046175 | 1395.964951 |
| TimesFM | High volatility | 1725.906316 | 2431.334540 |
| TimesFM | Major upward movement | 2467.687670 | 2877.414558 |
| TimesFM | Major downward movement | 2454.908958 | 2875.542493 |

TimesFM is stronger than Chronos on the reported point-forecast regime metrics. These are predefined conditional-performance slices, not comprehensive adversarial robustness; perturbations, data corruption, missing-data attacks, and controlled distribution shifts were not tested.

## Temporal Stability

The frozen test period is divided into Earlier, Middle, and Later contiguous segments and evaluated from the same saved forecast vectors. This is a temporal-stability diagnostic (historically labelled `Generalisation` in artifacts), not evidence of geographic, cross-dataset, out-of-distribution, or structural-break generalisation. Missing evidence is retained as missing rather than inferred.

## Uncertainty Results

Chronos-Bolt-Tiny:

- Native 80% interval coverage: 0.845429; average width: 5151.959881.
- Training-only conformalized coverage: 0.815269; average width: 4878.131756.
- 95% interval unavailable because the required 0.025 and 0.975 quantiles are outside the verified Chronos-Bolt trained quantile range.

TimesFM:

- Native 80% interval coverage: 0.330820; average width: 1436.627452.
- Training-only conformalized coverage: 0.556079; average width: 2518.760264.
- 95% interval unavailable.
- Verified quantile range: 0.1 through 0.9.

Interpretation:

- Chronos has lower absolute error from nominal 80% marginal coverage in this task.
- Training-only calibration brought Chronos close to the nominal target. TimesFM coverage improved materially but remained well below 80%, so no test-residual tuning was used to force nominal coverage.
- Coverage alone is insufficient: interval width and sharpness matter, wider intervals may improve coverage, and no universal calibration superiority is claimed from one nominal level.
- Accuracy alone is insufficient for trustworthiness.

## Diebold-Mariano Tests

Notebook 09 implements Diebold-Mariano testing from first principles using squared-error loss and saved forecast vectors.

Executed results:

| Comparison | DM Statistic | p-value | Winner | Significant at alpha = 0.05 |
|---|---:|---:|---|---|
| Naive vs Persistence-Enhanced LSTM | -2.196432 | 0.028277 | Naive | True |
| Naive vs Chronos-Bolt-Tiny | -5.482418 | < 0.000001 | Naive | True |
| Naive vs ARIMA Rolling One-Step | -1.018986 | 0.308442 | Naive by RMSE | False |
| Naive vs Prophet 30-Day Periodic Refit | -20.709702 | < 0.000001 | Naive | True |
| Persistence-Enhanced LSTM vs Chronos-Bolt-Tiny | -3.621925 | 0.000306 | Persistence-Enhanced LSTM | True |
| Naive vs TimesFM | -4.278078 | 0.000021 | Naive | True |
| Persistence-Enhanced LSTM vs TimesFM | -1.909856 | 0.056421 | Persistence-Enhanced LSTM by RMSE | False |
| Chronos-Bolt-Tiny vs TimesFM | 2.760989 | 0.005862 | TimesFM | True |

The complete 15-pair table is frozen in `results/bitcoin_dm_pairwise_results.csv`.

Practical effect sizes were recorded as small relative to the average Bitcoin price.

## Practical Effect Sizes

Statistical significance is interpreted alongside magnitude. The saved effect-size analysis expresses model differences relative to the average Bitcoin price and finds the practical effects small, preventing low p-values over 1,061 observations from being presented as automatically operationally large.

## Transparency and Auditability

The researcher-defined rubric covers model transparency, interpretation, complexity, reproducibility, and failure detectability. It is broader than feature-attribution XAI and does not establish attribution faithfulness, counterfactual quality, representation-level explanation, saliency validity, or user-centred usefulness. Exact saved vectors, deterministic baselines, explicit exclusion rules, failure cases, and the artifact hash ledger provide the audit trail.

## Trustworthiness Findings

Notebook 06 is designed as an artifact-only trustworthiness analysis. It should load saved forecasts from `results/validated_forecasts.csv` and must not train, refit, or load forecasting checkpoints.

Primary trustworthiness evidence:

- Relative Accuracy Score.
- Relative Regime-Conditional Robustness Score.
- Relative Temporal Stability Score (historical artifact label: `Generalisation`).
- Uncertainty Score.
- Transparency/Auditability Score (historical artifact label: `Explainability`).
- Overall Trust Score - Missing Evidence Penalised.
- Evidence-Available Trust Score.

Important interpretation note:

A score of 100 is relative to the best model in the comparison set and does not represent perfect forecast accuracy. A missing uncertainty artifact is not evidence of poor calibration. The two composite scores are exploratory sensitivity summaries: their weights are researcher-defined, components overlap, and normalisation depends on the comparison set. Component evidence remains primary.

ARIMA now uses the same training-residual empirical interval method as the deterministic baselines, based on the final 1,061 training dates. Its test coverage is 0.662582 for the empirical 80% interval and 0.899152 for the 95% interval, producing an Uncertainty Score of 86.615087.

Final ranking for both scoring variants: Naive 97.810622, ARIMA Rolling One-Step 96.552205, Chronos-Bolt-Tiny 91.318843, TimesFM 90.528647, Persistence-Enhanced LSTM 79.607361 penalised / 93.655719 evidence-available, 7-Day Moving Average 70.729402, and Prophet 30-Day Periodic Refit 22.626693 penalised / 26.619639 evidence-available. Naive leads both rankings after ARIMA is evaluated on the uncertainty dimension rather than having that dimension excluded.

## Validation and Audit Procedure

Notebooks 07 and 08 audit forecast shape, timestamps, alignment, finiteness, metric reproduction, and Naive construction. Notebook 09 performs artifact-only significance testing. Frozen downstream analyses load saved vectors and do not train, refit, or load forecasting checkpoints. The repository verifier `src/verify_research_artifacts.py` independently checks protected hashes, schemas, row counts, keys, and reproduced metrics.

## Authoritative Artifacts

The principal vector is `results/validated_forecasts.csv`. Supporting point vectors include `results/baseline_forecasts.csv`, `results/persistence_enhanced_lstm_forecast.csv`, `results/chronos_bolt_tiny_forecast.csv`, `results/timesfm_forecast.csv`, `results/arima_rolling_forecast.csv`, and `results/prophet_rolling_forecast.csv`. Calibration, Trust Score, and full pairwise significance CSVs are also protected by [`../results/authoritative_artifact_hashes.md`](../results/authoritative_artifact_hashes.md). Hash equality establishes byte preservation; methodological validity is established by the protocol and audits.

## Failure Case Studies

Original raw-price LSTM:

- Implemented and executed as an exploratory supervised neural model.
- Underperformed the Naive baseline.
- Diagnostics indicated non-stationarity, range issues, lag, and over-smoothing.
- Not included as an authoritative saved-vector model unless an exact validated vector is available.

Improved experimental LSTM:

- Notebook scaffold exists.
- Saved notebook is unexecuted.
- Not part of the frozen authoritative Bitcoin comparison.

Collapsed Transformer:

- The initial Transformer collapsed to constant predictions.
- Failure analysis identified LayerNormalization over a one-dimensional feature axis after projecting back to one feature.
- This is an implementation-failure case study, not a valid model.

Corrected but over-smoothed Transformer:

- A corrected Transformer projected the 1D input into a higher model dimension before attention and normalization.
- It avoided the exact original collapse but still showed severe range compression and poor accuracy.
- Excluded from the authoritative comparison and exploratory composite summary.

ARIMA/SARIMA:

- ARIMA(1,1,1) was executed in the classical notebook as a static multi-step forecast.
- The advanced notebook now provides an exact ARIMA rolling one-step vector using a 128-day context and per-observation state append.
- SARIMA was dropped as a distinct final model because weekly-seasonality diagnostics did not support a seven-day term and the zero-seasonal specification would duplicate ARIMA.

## Foundation Model Status

Chronos-Bolt-Tiny:

- Installed and imported successfully in the main environment.
- Checkpoint `amazon/chronos-bolt-tiny` loaded on CPU.
- Rolling one-step forecasts saved and validated.
- Native 80% uncertainty interval evaluated.

TimesFM:

- Installed and imported successfully in the main environment.
- Model `google/timesfm-2.5-200m-pytorch` evaluated on CPU.
- Rolling one-step forecasts saved and validated.
- Native 80% interval evaluated but under-calibrated.

Moirai / Uni2TS:

- Current Python 3.13 setup attempt failed.
- A separate Python 3.12 environment is the recommended follow-up path.
- No Moirai smoke-test forecast exists.

PatchTST and iTransformer:

- NeuralForecast workflow was investigated.
- Python 3.13 compatibility is blocked by unavailable Ray dependency.
- No validated PatchTST or iTransformer Bitcoin results exist.

Prophet:

- Package availability was investigated.
- A validated 1,061-row periodic-refit forecast is part of the frozen Bitcoin comparison; the model refits every 30 days using only the latest 128 observations available before each refit date.

## Limitations

- The completed case study covers only one domain: Bitcoin finance.
- Bitcoin is highly non-stationary and volatile; conclusions should not be generalized to energy, weather, or transport before those domains are evaluated.
- TimesFM and Chronos are evaluated zero-shot; no fine-tuning comparison is included.
- Some exploratory notebooks are intentionally excluded because they lack validated saved forecast vectors or use non-comparable protocols. PatchTST/iTransformer and Moirai require an isolated Python 3.12 environment.
- Notebook output state may differ from artifact state for exploratory notebooks; the frozen comparison should rely on `results/validated_forecasts.csv`.

## Reproducibility and Environment

The completed workflow was audited on CPU-only Windows 11 build 26100 with Python 3.13.2. Direct dependencies are frozen in [`../requirements-research.txt`](../requirements-research.txt); notebook tooling must be installed explicitly in a clean environment. Chronos-Bolt-Tiny and TimesFM inference completed on CPU. Moirai / Uni2TS and PatchTST/iTransformer require an isolated Python 3.12 environment. Those unavailable models have no authoritative Bitcoin vectors and are excluded from rankings. Reproducing model generation is substantially more expensive than artifact-only verification and must not overwrite frozen results without a new experiment version.

## Final Bitcoin Conclusions

- The Naive persistence baseline remains the strongest point forecaster among the frozen authoritative Bitcoin models.
- Rolling ARIMA is second by RMSE and is not significantly different from Naive at alpha 0.05.
- Persistence-Enhanced LSTM is the strongest supervised neural model with an exact saved forecast vector.
- TimesFM is the strongest zero-shot foundation model for point forecasting.
- Chronos-Bolt-Tiny is weaker than TimesFM on point accuracy but has lower absolute error from nominal 80% marginal coverage.
- TimesFM native intervals are too narrow and severely under-cover; training-only conformalization improves coverage to 0.556079 but does not eliminate the gap to 0.80.
- Advanced model complexity does not guarantee trustworthiness.
- Trustworthiness depends on protocol comparability, diagnostics, uncertainty calibration, and failure detectability, not just headline error metrics.
