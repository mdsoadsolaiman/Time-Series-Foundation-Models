# South Australian Electricity Demand Case Study

## 1. Research Objective

This case study evaluates whether zero-shot time-series foundation models provide accurate and trustworthy electricity-demand forecasts under both short-horizon and operational day-ahead protocols. Accuracy is considered alongside robustness, temporal generalisation, uncertainty, explainability, and statistical significance.

## 2. Dataset

The source is `data/electricity/australian_electricity_demand_dataset.tsf`. The selected series is T4, identified by the dataset metadata as South Australia (SA). It contains half-hourly demand from 2002-01-01 00:00 through 2015-03-01 23:30: 230,784 observations at 48 observations per day.

## 3. Data Quality

The Phase 1 audit found no missing values, missing timestamps, duplicated timestamps, zero demand values, or negative demand values. The reconstructed index is contiguous at 30-minute frequency. These checks support percentage metrics and exact timestamp joins but do not establish representativeness beyond South Australia.

## 4. Temporal Structure

Electricity demand contains strong persistence, daily and weekly seasonality, recurring demand cycles, and changing demand regimes. These structures motivate lag-1, lag-48, lag-336, moving-average, harmonic-regression, and learned-model comparisons.

## 5. Train / Validation / Test Design

All partitions are chronological and aligned to complete days.

| Partition | Start | End | Observations | Days |
|---|---|---|---:|---:|
| Development train | 2002-01-01 00:00 | 2011-06-23 23:30 | 166,128 | 3,461 |
| Internal validation | 2011-06-24 00:00 | 2012-07-12 23:30 | 18,480 | 385 |
| Frozen final test | 2012-07-13 00:00 | 2015-03-01 23:30 | 46,176 | 962 |

Selection and early stopping use development/validation evidence. The final test is reserved for frozen evaluation. MASE-48 uses a daily-seasonal denominator computed from eligible pre-test observations, consistently across models.

## 6. Forecasting Protocol A

Protocol A is rolling one-step prediction at a 30-minute horizon. Every model predicts timestamp `t` using only observations strictly earlier than `t`; the actual at `t` becomes available only after the prediction is recorded. The artifact contains 46,176 aligned forecasts per model.

## 7. Forecasting Protocol B

Protocol B is true 48-step, 24-hour day-ahead forecasting. There are 962 non-overlapping midnight origins. Each model produces all 48 values without seeing any actual inside that forecast day. Forecast keys are Origin, Horizon, and Timestamp. Protocol B is not constructed by stitching rolling one-step forecasts.

## 8. Baseline Models

The deterministic baselines are Naive persistence (lag 1), Daily Seasonal Naive (lag 48), Weekly Seasonal Naive (lag 336), and a trailing Moving Average. Their strength changes with horizon: lag-1 persistence is useful one-step, while the daily seasonal baseline is competitive day-ahead.

## 9. DHR-ARIMA

Dynamic Harmonic Regression combines preselected daily and weekly Fourier terms with low-order non-seasonal ARIMA errors. It is an excellent Protocol A benchmark but deteriorates under recursive day-ahead forecasting. The saved forecast vectors, rather than a refitted model, are used downstream.

## 10. LSTM

The deterministic LSTM uses chronological training, validation-only selection and early stopping, fixed seeds, past-only scaling, and protocol-specific generation. It is evaluated separately for one-step and day-ahead tasks. It is competitive but does not lead either ranking.

## 11. Chronos-Bolt-Tiny

`amazon/chronos-bolt-tiny` is evaluated zero-shot with a frozen context of 336 observations. It ranks third in Protocol A and second in Protocol B. Its native 80% intervals are substantially better calibrated than TimesFM's intervals, although they are not perfect in either protocol.

## 12. TimesFM

`google/timesfm-2.5-200m-pytorch` is evaluated zero-shot with the same frozen context policy. It ranks first under both protocols and decisively improves on the strongest protocol-specific baselines. Its point-forecast strength does not translate into well-calibrated 80% intervals.

## 13. Validation Audit

Notebook 14 validates shape, keys, alignment, timestamps, finiteness, protocol semantics, and artifact provenance. Protocol A contains 46,176 unique sorted target timestamps. Protocol B contains 962 origins × 48 horizons with no within-window updates. Downstream analyses load these validated artifacts and do not regenerate forecasts.

## 14. Accuracy Results

### Protocol A — rolling one-step, ranked by MASE-48

| Rank | Model | MASE-48 |
|---:|---|---:|
| 1 | TimesFM | 0.1400 |
| 2 | DHR-ARIMA | 0.2276 |
| 3 | Chronos-Bolt-Tiny | 0.2762 |
| 4 | Naive | 0.3611 |
| 5 | LSTM | 0.4017 |
| 6 | Daily Seasonal Naive | 1.1056 |
| 7 | Weekly Seasonal Naive | 1.3088 |
| 8 | Moving Average | 1.5302 |

### Protocol B — true 48-step day-ahead, ranked by MASE-48

| Rank | Model | MASE-48 |
|---:|---|---:|
| 1 | TimesFM | 0.6892 |
| 2 | Chronos-Bolt-Tiny | 1.0774 |
| 3 | Daily Seasonal Naive | 1.1056 |
| 4 | LSTM | 1.3064 |
| 5 | Weekly Seasonal Naive | 1.3088 |
| 6 | Moving Average | 1.7359 |
| 7 | Naive | 2.0831 |
| 8 | DHR-ARIMA | 2.4557 |

The rankings must not be merged: the information sets and forecast horizons differ.

## 15. Robustness Results

Robustness evidence is saved separately for each protocol and includes pre-registered demand and volatility regimes. Relative scores are comparison-set scores, not absolute guarantees. TimesFM has the highest relative robustness score in Protocol A (100.0) and Protocol B (100.0). Chronos scores 33.53 and 73.00 respectively, illustrating pronounced horizon dependence.

## 16. Generalisation Results

The test is divided chronologically into Earlier, Middle, and Later contiguous segments; Protocol B keeps complete daily origins intact. TimesFM has the highest relative generalisation score under Protocol A and B (100.0 in both). Chronos scores 52.02 in Protocol A and 63.11 in Protocol B. Exact segment metrics remain in the saved generalisation CSVs.

## 17. Uncertainty Results

Only native intervals supported by the installed foundation-model APIs are reported. Missing uncertainty evidence for deterministic models remains unavailable rather than being fabricated.

| Protocol | Model | Nominal coverage | Empirical coverage | Average width (demand units) |
|---|---|---:|---:|---:|
| A | Chronos-Bolt-Tiny | 80% | 91.1231% | 137.419281 |
| A | TimesFM | 80% | 33.6495% | 17.108297 |
| B | Chronos-Bolt-Tiny | 80% | 67.6239% | 283.997589 |
| B | TimesFM | 80% | 24.5604% | 75.642609 |

TimesFM's narrower intervals severely undercover. Narrowness alone is therefore not evidence of uncertainty quality.

## 18. Explainability

Explainability is assessed through declared model-class properties and evidence availability. The saved framework assigns higher scores to transparent deterministic rules than to complex neural and foundation models. These researcher-defined scores are components of a comparative framework, not a user study or causal explanation.

## 19. Trustworthiness Rankings

Weights are Accuracy 35%, Robustness 20%, Generalisation 20%, Uncertainty 15%, and Explainability 10%. Two scores are reported: a penalised score treats missing evidence as zero for evidence completeness; an evidence-available score renormalises over observed components.

| Protocol | Leading model | Penalised Trust Score | Evidence-Available Trust Score |
|---|---|---:|---:|
| A | TimesFM | 92.0332 | 92.0332 |
| B | TimesFM | 91.0788 | 91.0788 |

Chronos scores 51.0431 in Protocol A and 66.3115 in Protocol B under both formulations because all components are available. A high aggregate score does not erase TimesFM's poor calibration; component evidence must be inspected.

## 20. Statistical Significance

Protocol A tests timestamp-level squared-error loss differentials with HAC variance. Protocol B uses daily mean squared error over each 48-step origin as the sampling unit, with HAC adjustment. Benjamini–Hochberg adjustment controls the reported pairwise family.

TimesFM significantly beats DHR-ARIMA and Chronos in Protocol A. It also significantly beats Daily Seasonal Naive and Chronos in Protocol B. Chronos has significantly lower daily squared loss than Daily Seasonal Naive in Protocol B, while the accompanying absolute-loss sensitivity does not support an unconditional claim across all loss definitions.

## 21. Key Findings

- TimesFM is the strongest point forecaster under both electricity protocols.
- DHR-ARIMA is a strong short-horizon benchmark but weak day-ahead.
- Daily Seasonal Naive becomes a strong day-ahead benchmark.
- Chronos is second day-ahead and is much better calibrated than TimesFM.
- Forecast horizon materially changes model rankings.
- Trustworthiness requires component-level interpretation, not only an aggregate score.

## 22. Limitations

The evidence covers one region and one historical demand series. Trust weights and explainability scores are researcher-defined. Only supported 80% foundation-model intervals are available. Moirai, PatchTST, and iTransformer are unavailable; no foundation model is fine-tuned. Results should not be assumed to transfer to other grids, climates, or operational settings.

## 23. Reproducibility

The authoritative vectors are `results/electricity/protocol_a_validated_forecasts.csv` and `protocol_b_validated_forecasts.csv`. Evidence tables, Trust Scores, and DM outputs reside beside them. Hashes are frozen in [`authoritative_artifact_hashes.md`](authoritative_artifact_hashes.md). Notebook 14 audits forecasts; notebooks 15–17 perform artifact-only downstream analysis. See [`environment.md`](environment.md) for dependencies and [`electricity_forecasting_protocol.md`](electricity_forecasting_protocol.md) for the pre-registered protocol.
