# Bitcoin Case Study

Status: **Frozen as Domain 1 - Financial Time Series**

This document records the completed Bitcoin experiment before expanding to additional domains. It summarises the dataset, preprocessing, forecasting protocol, validated model results, trustworthiness analysis, known failure cases, and remaining limitations.

## Dataset

- Dataset: BTC/USD minute-level OHLCV data.
- Physical file: `data/bitcoin/btcusd_1-min_data.csv`.
- Raw columns: `Timestamp`, `Open`, `High`, `Low`, `Close`, `Volume`.
- Raw timestamp format: Unix seconds converted to UTC datetime.
- Raw date range observed in the repository: 2012-01-01 00:01 UTC to 2026-07-07 01:57 UTC.
- Raw rows observed in the repository audit: 7,633,557.
- Forecast target: daily Bitcoin `Close`.

Planned folders for exchange-rate, weather, traffic, and energy-style experiments exist or are referenced, but no additional domain dataset has been completed yet.

## Preprocessing

The reusable pipeline is implemented in `src/`:

- `src.data_loader.load_bitcoin_data(path)` loads the raw CSV, converts `Timestamp` to UTC datetime, sorts the data, and resets the index.
- `src.preprocessing.prepare_daily_bitcoin_data(df)` resamples minute-level OHLCV data to daily OHLCV.
- `src.metrics` implements MAE, RMSE, MAPE, and sMAPE.
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

The 7-Day Moving Average is a deterministic rolling one-step benchmark recreated from the historical actual series.

ARIMA and SARIMA are retained as protocol-limited statistical references unless exact rolling one-step saved vectors exist. Static multi-step forecasts are not directly equivalent to rolling one-step forecasts.

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

Repository audit verification:

- Shape: 1,061 rows x 6 columns.
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

Additional deterministic benchmark:

- 7-Day Moving Average.

Exploratory, failed, or non-authoritative models:

- Original raw-price LSTM.
- Improved experimental LSTM.
- Collapsed Transformer.
- Corrected but over-smoothed Transformer.

Protocol-limited models:

- ARIMA(1,1,1).
- SARIMA, where available.

Models not included in the completed Bitcoin scope:

- Moirai / Uni2TS.
- PatchTST.
- iTransformer.
- Prophet.

These are not included because they either lack validated saved forecast vectors for the Bitcoin frozen artifact or remain blocked/planned.

## Authoritative Metrics

Metrics reproduced directly from `results/validated_forecasts.csv`:

| Model | MAE | RMSE | MAPE | sMAPE |
|---|---:|---:|---:|---:|
| Naive | 1290.353242 | 1853.624774 | 1.742747 | 1.744142 |
| Persistence-Enhanced LSTM | 1323.040782 | 1886.566387 | 1.787392 | 1.794338 |
| TimesFM | 1349.946786 | 1924.199337 | 1.823179 | 1.823895 |
| Chronos-Bolt-Tiny | 1424.025828 | 1994.007926 | 1.934509 | 1.928782 |

The Naive baseline has the strongest point accuracy among the frozen saved-vector models.

## Regime Results

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

TimesFM is stronger than Chronos on the reported point-forecast regime metrics. Neither result should be interpreted as native causal robustness.

## Uncertainty Results

Chronos-Bolt-Tiny:

- Nominal 80% interval coverage: 0.845429.
- Average 80% interval width: 5151.959961.
- 95% interval unavailable because the required 0.025 and 0.975 quantiles are outside the verified Chronos-Bolt trained quantile range.

TimesFM:

- Nominal 80% interval coverage: 0.330820.
- Average 80% interval width: 1436.627452.
- 95% interval unavailable.
- Verified quantile range: 0.1 through 0.9.

Interpretation:

- Chronos provides better 80% uncertainty calibration.
- TimesFM intervals are too narrow and severely under-cover.
- Accuracy alone is insufficient for trustworthiness.

## Diebold-Mariano Tests

Notebook 09 implements Diebold-Mariano testing from first principles using squared-error loss and saved forecast vectors.

Executed results:

| Comparison | DM Statistic | p-value | Winner | Significant at alpha = 0.05 |
|---|---:|---:|---|---|
| Naive vs Persistence-Enhanced LSTM | -2.345239 | 0.019199 | Naive | True |
| Naive vs Chronos-Bolt-Tiny | -5.482418 | < 0.000001 | Naive | True |
| Persistence-Enhanced LSTM vs Chronos-Bolt-Tiny | -3.350112 | 0.000836 | Persistence-Enhanced LSTM | True |
| Naive vs TimesFM | -4.278078 | 0.000021 | Naive | True |
| Persistence-Enhanced LSTM vs TimesFM | -1.541492 | 0.123495 | Persistence-Enhanced LSTM by RMSE | False |
| Chronos-Bolt-Tiny vs TimesFM | 2.760989 | 0.005862 | TimesFM | True |

Practical effect sizes were recorded as small relative to the average Bitcoin price.

## Trustworthiness Findings

Notebook 06 is designed as an artifact-only trustworthiness analysis. It should load saved forecasts from `results/validated_forecasts.csv` and must not train, refit, or load forecasting checkpoints.

Trustworthiness dimensions:

- Relative Accuracy Score.
- Relative Robustness Score.
- Relative Generalisation Score.
- Uncertainty Score.
- Explainability Score.
- Overall Trust Score - Missing Evidence Penalised.
- Evidence-Available Trust Score.

Important interpretation note:

A score of 100 is relative to the best model in the comparison set and does not represent perfect forecast accuracy. A missing uncertainty artifact is not evidence of poor calibration. The penalised ranking measures deployment readiness, while the evidence-available ranking measures performance on evaluated dimensions.

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
- Excluded from the main Trust Score ranking.

ARIMA/SARIMA:

- ARIMA(1,1,1) was executed in the classical notebook as a static multi-step forecast.
- SARIMA appears in advanced workflow scaffolding.
- These models are not directly comparable to rolling one-step models unless exact rolling one-step saved vectors are produced.

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
- A separate Python 3.11 environment was planned, but Python 3.11 was not available on the audited machine.
- No Moirai smoke-test forecast exists.

PatchTST and iTransformer:

- NeuralForecast workflow was investigated.
- Python 3.13 compatibility is blocked by unavailable Ray dependency.
- No validated PatchTST or iTransformer Bitcoin results exist.

Prophet:

- Package availability was investigated.
- No validated Prophet forecast artifact is part of the frozen Bitcoin comparison.

## Limitations

- The completed case study covers only one domain: Bitcoin finance.
- Bitcoin is highly non-stationary and volatile; conclusions should not be generalized to energy, weather, or transport before those domains are evaluated.
- TimesFM and Chronos are evaluated zero-shot; no fine-tuning comparison is included.
- Some exploratory notebooks are intentionally excluded because they lack validated saved forecast vectors or use non-comparable protocols.
- Notebook output state may differ from artifact state for exploratory notebooks; the frozen comparison should rely on `results/validated_forecasts.csv`.

## Final Bitcoin Conclusions

- The Naive persistence baseline remains the strongest point forecaster among the frozen authoritative Bitcoin models.
- Persistence-Enhanced LSTM is the strongest supervised neural model with an exact saved forecast vector.
- TimesFM is the strongest zero-shot foundation model for point forecasting.
- Chronos-Bolt-Tiny is weaker than TimesFM on point accuracy but stronger for 80% uncertainty calibration.
- TimesFM uncertainty intervals are too narrow and severely under-cover.
- Advanced model complexity does not guarantee trustworthiness.
- Trustworthiness depends on protocol comparability, diagnostics, uncertainty calibration, and failure detectability, not just headline error metrics.
