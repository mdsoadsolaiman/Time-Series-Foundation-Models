# South Australian Electricity-Demand Forecasting Protocol

## Scope and status

This document freezes the Phase 2 experimental design for Domain 2. It defines the information sets, partitions, metrics, fairness rules, and downstream validation requirements before any model is trained or any final-test forecast is generated. Bitcoin artifacts and numerical results remain frozen and outside this protocol.

No baseline, LSTM, Chronos, or TimesFM forecast is produced in Phase 2.

## Dataset and target

- Dataset: Australian Electricity Demand, Monash TSF relation `Aus_Electricity_Demand`.
- Source file: `data/electricity/australian_electricity_demand_dataset.tsf`.
- Target series: South Australia, identified from metadata as `series_name = T4`, `state = SA`.
- Target variable: half-hourly electricity demand in the source dataset's units.
- Frequency: one observation every 30 minutes (`48` observations per day and `336` per week).
- Full T4 range: 2002-01-01 00:00 through 2015-03-01 23:30.
- Full T4 length: 230,784 observations.
- TSF benchmark horizon: not specified in the file. No horizon is inferred from this omission.
- Phase 1 quality audit: no missing values, missing timestamps, duplicated timestamps, zero values, or negative values.

## Frozen data partitions

All boundaries are chronological and aligned to midnight at the start of a complete day. The final test partition is unchanged from Phase 1.

| Partition | Start | End | N | Complete days | Intended use |
|---|---|---|---:|---:|---|
| Development train | 2002-01-01 00:00 | 2011-06-23 23:30 | 166,128 | 3,461 | Parameter fitting and historical context |
| Internal validation | 2011-06-24 00:00 | 2012-07-12 23:30 | 18,480 | 385 | Model selection, early stopping, diagnostics, and eligible residual calibration |
| Frozen final test | 2012-07-13 00:00 | 2015-03-01 23:30 | 46,176 | 962 | Final evaluation only |

The internal validation partition is the nearest complete-day allocation to the final 10% of the original 184,608-observation training partition: 18,480 observations, or 10.0104%. Development train plus validation exactly reproduces the frozen training partition. The intervals are contiguous but do not overlap: development train ends 30 minutes before validation starts, and validation ends 30 minutes before final test starts.

Model selection, preprocessing selection, moving-average window selection, LSTM context selection, early stopping, and uncertainty calibration must not access final-test outcomes. After choices have been frozen using development/validation evidence, a model may be refitted on the full pre-test history (development train plus validation) if this is declared consistently for that model class. Any such refit still cannot use test observations beyond what the applicable rolling protocol makes available.

## Protocol A: rolling one-step ahead

Protocol A is the primary short-horizon evaluation.

- Horizon: one half-hourly step (30 minutes).
- Evaluation timestamps: every timestamp in the frozen final test set.
- At target timestamp `t`, a forecaster may use only information with timestamps strictly earlier than `t`.
- The prediction for `t` is recorded before `actual[t]` is revealed.
- After `actual[t]` becomes observed, it may be appended to history for the forecast at the next timestamp.
- Every ranked model receives the same information availability. Model-specific context-length limits may truncate older history but cannot add newer information.
- Forecasts and actuals must be joined one-to-one by timestamp and preserve all 46,176 sorted, unique test timestamps.

Pre-registered deterministic lag rules are:

```text
Naive[t]                 = actual[t - 1]
Daily Seasonal Naive[t]  = actual[t - 48]
Weekly Seasonal Naive[t] = actual[t - 336]
```

No forecast may inspect `actual[t]` or any later value before predicting `t`. Protocol A results must be labelled **rolling one-step** and must not be combined silently with multi-step results.

## Protocol B: non-overlapping day-ahead forecasting

Protocol B is the primary realistic electricity-demand experiment.

- Horizon: 48 half-hourly steps (24 hours).
- Origin convention: one origin at 00:00 at the beginning of every test calendar day.
- Information cutoff: for an origin `o`, only observations strictly before `o` are available.
- Forecast window: `o` through `o + 47 × 30 minutes`, inclusive.
- All 48 predictions are generated without revealing any actual inside that window.
- History or model state cannot be updated with within-window actuals until the complete 48-step forecast has been produced.
- Primary forecast windows are non-overlapping.
- A 48-step score may not be constructed by stitching together 48 rolling one-step forecasts.

The actual test timestamps establish:

- Complete test days: 962.
- Forecast origins: 962.
- First origin: 2012-07-13 00:00.
- Last origin: 2015-03-01 00:00.
- Last horizon endpoint: 2015-03-01 23:30.
- Partial test days: none.
- Horizons extending beyond the test interval: none.

Protocol B forecasts require keys for `Origin`, `Horizon` (1 through 48), and target `Timestamp`. These keys must be unique and must map to exactly one actual value.

## Optional Protocol C: weekly stress test

Protocol C is documented but not executed in Phase 2.

- Horizon: 336 half-hours (seven days).
- Purpose: secondary long-horizon seasonal stress testing.
- It cannot replace the 48-step Protocol B evaluation.
- Its origin schedule, overlap treatment, and inference feasibility must be frozen before execution.
- The TSF file's unspecified benchmark horizon is not assumed to be 336.

## Pre-registered baselines and seasonal lags

| Baseline | Definition | Selection rule |
|---|---|---|
| Naive Persistence | Lag 1 | Fixed in advance |
| Daily Seasonal Naive | Lag 48 | Fixed in advance |
| Weekly Seasonal Naive | Lag 336 | Fixed in advance |
| Moving Average | Mean of a trailing, past-only window | Window predefined from domain reasoning or selected using internal validation only; final test cannot select it |
| Seasonal statistical model | Suitable seasonal or multi-seasonal model, if computationally practical | Exact choice remains open for baseline analysis; SARIMA is not mandatory for 230k observations |

For Protocol B, any baseline must respect the frozen origin information set. In particular, recursive or direct 48-step logic cannot consume actuals inside the forecast day. A lagged seasonal value is permitted only when its timestamp is strictly before the origin. These requirements distinguish a genuine day-ahead forecast from rolling evaluation.

## LSTM design fairness

- The target is electricity demand, not Bitcoin returns, unless a later transformation is justified solely from training/validation diagnostics.
- Candidate context lengths include 48 (one day), 336 (one week), and 672 (two weeks).
- Context length and all architecture or stopping choices are selected without final-test results.
- Scaling is fitted on eligible training data only and inverse scaling must preserve target alignment.
- Protocol A and Protocol B require separate forecast-generation logic. Protocol B must produce all 48 values without within-horizon actual updates.
- Fixed seeds and deterministic settings will be recorded during the LSTM phase.

## Foundation-model fairness

- Chronos model: `amazon/chronos-bolt-tiny`.
- TimesFM model: `google/timesfm-2.5-200m-pytorch`.
- Both models remain zero-shot; neither is fine-tuned.
- Protocol A uses rolling one-step inference over the full final test.
- Protocol B uses a true 48-step forecast at each daily origin.
- Context supplied to each model must end strictly before the target or forecast window.
- Model API limitations, context truncation, supported quantiles, runtime, and failures must be recorded transparently.
- Stitched one-step forecasts are not admissible as Protocol B results.

## Metrics

Both protocols report MAE, RMSE, MAPE, sMAPE, and MASE-48. Metric definitions must remain identical across model classes within a protocol. Percentage metrics must use explicit zero handling; the audited target has no zeros, but forecast artifacts must still be checked for finite values.

For actuals `y_i`, forecasts `ŷ_i`, and evaluation size `n`:

```text
MAE   = mean(|y_i - ŷ_i|)
RMSE  = sqrt(mean((y_i - ŷ_i)^2))
MAPE  = 100 × mean(|(y_i - ŷ_i) / y_i|)
sMAPE = 100 × mean(2|y_i - ŷ_i| / (|y_i| + |ŷ_i|))
```

### Primary MASE-48 definition

The primary scale-free electricity metric is daily-seasonal MASE with `m = 48`:

```text
MASE-48 denominator = (1 / (T - 48)) × Σ[t=49..T] |y_train[t] - y_train[t-48]|
MASE-48             = MAE_evaluation / MASE-48 denominator
```

The denominator is computed from training observations only, never from final-test actuals. During development comparisons it is computed from the development-train partition. For frozen final evaluation, the denominator policy and eligible pre-test fitting sample must be declared once and applied identically to every model; the default final-evaluation denominator is the full frozen pre-test training partition (development train plus validation), after all selection decisions are frozen. MASE-336 may later be reported as a clearly secondary sensitivity measure.

### Protocol B multi-horizon reporting

Protocol B reports:

1. Overall metrics across all 962 × 48 target forecasts.
2. A horizon table for `h = 1, …, 48` containing Horizon, MAE, RMSE, sMAPE, and MASE-48.
3. Predefined summaries for horizons 1–12 (first six hours), 13–24 (6–12 hours), and 25–48 (12–24 hours).

Each horizon-specific MASE-48 uses the same frozen training-only denominator. Horizon deterioration must remain visible rather than being hidden by the overall mean.

## Pre-registered robustness regimes

Regimes will be fixed before final-model error inspection and evaluated consistently for all authoritative models. Thresholds should be derived from the eligible training partition wherever feasible:

| Regime | Pre-registered definition |
|---|---|
| High Demand | `actual >= training 90th percentile` |
| Low Demand | `actual <= training 10th percentile` |
| High Volatility | Past-observable rolling volatility of half-hour changes exceeds its training 90th percentile; window and `ddof` must be frozen during validation design |
| Peak Demand Event | `actual >= training 99th percentile` |

The actual target may be used to assign a test observation to a demand regime for retrospective stratified evaluation, but thresholds cannot be tuned against test errors. High-volatility features used as forecast inputs must use only past observations; retrospective regime labels must be identified as such. No days or events may be hand-picked. Each regime reports MAE, RMSE, MAPE, sMAPE, MASE-48, and N. If validation evidence justifies a different quantile or rolling window, that change must be documented and frozen before final-test evaluation.

## Temporal Stability

The final test is divided chronologically into Earlier, Middle, and Later contiguous sections of approximately equal size. There is no randomisation. For Protocol A, boundaries are day-aligned. For Protocol B, the 962 complete forecast days are allocated contiguously as 321, 320, and 321 daily blocks, keeping every 48-step origin intact. Exact segment dates will be derived and saved with the evaluation artifact before metrics are inspected.

All models report MAE, RMSE, MAPE, sMAPE, and MASE-48 per segment, with changes over time described explicitly.

## Uncertainty rules

- Chronos and TimesFM use only probabilistic outputs actually supported by their installed APIs and model versions.
- Report the supported nominal interval or quantile levels, empirical coverage, average interval width, and an interval score later if validly implemented.
- Do not invent or interpolate an unsupported 95% interval.
- Deterministic baselines and LSTM receive empirical residual intervals only when a valid, strictly pre-test validation residual sample exists.
- Final-test residuals cannot calibrate test intervals.
- Missing uncertainty evidence is recorded as unavailable, not as evidence of poor calibration.

## Trustworthiness framework

The cross-domain framework is pre-registered unchanged:

| Dimension | Weight |
|---|---:|
| Accuracy | 35% |
| Robustness | 20% |
| Generalisation | 20% |
| Uncertainty | 15% |
| Transparency/Auditability (historical artifact label: Explainability) | 10% |

Later analysis reports both **Overall Trust Score – Missing Evidence Penalised** and **Evidence-Available Trust Score** as exploratory composite summaries. A component score of 100 is relative to the comparison set, not perfect prediction. Weights are researcher-defined, components overlap, and normalisation depends on the comparison set. Dimension-level evidence remains primary. Missing uncertainty evidence is not evidence of poor calibration. No composite is calculated in Phase 2.

## Statistical-significance plan

Pairwise Diebold–Mariano tests will use exact saved forecast vectors and a loss differential defined before testing.

- Protocol A: use the timestamp-level one-step loss differential, with squared-error loss as the primary specification. Serial dependence is handled using a heteroskedasticity-and-autocorrelation-consistent variance estimate rather than assuming independent errors.
- Protocol B: do not treat the 48 within-day errors as independent. For each daily origin and model, calculate daily mean squared error across its 48-step horizon. The DM loss differential is the resulting series of 962 daily losses. Because primary origins are non-overlapping, the day is the sampling unit; remaining serial dependence is handled with a documented HAC lag rule.
- Report the DM statistic, two-sided p-value, winner by mean loss, significance at `alpha = 0.05`, practical loss difference, and an effect size.
- Multiple-comparison adjustment, if used, must be declared alongside unadjusted p-values.

## Leakage-prevention and artifact rules

1. Never random-split the series.
2. Use only timestamps strictly before the target or forecast-window origin.
3. Fit scalers, transformations, hyperparameters, context choices, and calibration rules without final-test outcomes.
4. Do not update Protocol B with actuals inside its 48-step horizon.
5. Do not represent stitched rolling one-step forecasts as day-ahead forecasts.
6. Keep Protocol A, Protocol B, and optional Protocol C artifacts and rankings separately labelled.
7. Validate exact timestamp alignment, uniqueness, ordering, expected shape, missingness, and finiteness before scoring.
8. Save exact forecast vectors before downstream robustness, generalisation, trustworthiness, or significance analysis.
9. Never calibrate uncertainty with final-test residuals.
10. Failed or collapsed models remain documented failure cases and cannot enter authoritative rankings without passing the model-validation audit.

## Protocol validation table

| Check | Pass/Fail | Evidence |
|---|---|---|
| SA series = T4 | PASS | TSF row metadata explicitly pairs `T4` with `SA` |
| Frequency = 30 minutes | PASS | TSF declares `half_hourly`; reconstructed consecutive timestamps differ by 30 minutes |
| Frozen train length = 184,608 | PASS | Development 166,128 + validation 18,480 = 184,608 |
| Frozen test length = 46,176 | PASS | Timestamp-derived final-test count |
| No train–test overlap | PASS | Training ends 2012-07-12 23:30; test starts 2012-07-13 00:00 |
| Test starts at day boundary | PASS | First test timestamp is 2012-07-13 00:00 |
| Validation lies strictly inside training period | PASS | Validation is the final 18,480 observations of the frozen training partition and ends before test |
| Validation boundary is day-aligned | PASS | Validation starts 2011-06-24 00:00 and contains 385 complete days |
| No missing timestamps or values | PASS | Phase 1 audit found zero in both categories; reconstructed partitions are contiguous |
| Both partitions retain 30-minute frequency | PASS | Every partition is a contiguous slice of the audited half-hourly index |
| 48 observations per day verified | PASS | `48 × 30 minutes = 24 hours`; all partitions have lengths divisible by 48 |
| 336 observations per week verified | PASS | `336 × 30 minutes = 7 days` |
| Complete Protocol B test days = 962 | PASS | `46,176 / 48 = 962`, with zero remainder |
| Protocol B origins = 962 | PASS | One midnight origin for each timestamp-derived complete test day |
| No partial day or out-of-range horizon | PASS | Last origin 2015-03-01 00:00 ends at final test timestamp 23:30 |
| Protocol A uses no lookahead | PASS | Information cutoff and reveal/update sequence are explicitly defined |
| Protocol B uses no within-horizon actual updates | PASS | All 48 predictions precede revelation of forecast-window actuals |
| MASE denominator uses training only | PASS | MASE-48 policy prohibits final-test observations in the denominator |
| Model selection cannot access final-test results | PASS | Development/validation roles and allowed decisions are explicitly frozen |
| Foundation models remain zero-shot | PASS | Models and no-fine-tuning rule are pre-registered |
| Forecast protocols separately labelled | PASS | Protocol A, B, and optional C have distinct information sets, artifacts, and rankings |

Phase 2 ends with this validated protocol. Forecast generation and model training begin only after review.
