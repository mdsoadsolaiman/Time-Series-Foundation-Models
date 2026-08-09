# Bitcoin Case Study

## Research objective

The final Bitcoin domain tests whether increasingly complex forecasting systems
improve daily Close forecasts under a past-only evaluation protocol and whether
their evidence remains trustworthy across accuracy, regime behavior, temporal
stability, uncertainty, transparency, and corrected statistical inference.

## Data and canonical split

The source contains 7,633,557 minute observations from 2012-01-01 through
2026-07-07. Timestamps are interpreted in UTC and aggregated by UTC calendar
day using first Open, maximum High, minimum Low, last Close, and summed Volume.
The resulting target has 5,302 complete daily rows with no missing dates or
duplicate daily timestamps.

The chronological split is fixed:

| Partition | Rows | Start | End |
|---|---:|---|---|
| Training | 4,241 | 2012-01-01 | 2023-08-11 |
| Test | 1,061 | 2023-08-12 | 2026-07-07 |

The final UTC date contains only the available observations through 01:57 UTC
and therefore represents a partial daily observation rather than a completed
24-hour UTC trading day. It is retained to preserve the `bitcoin-v1` freeze.

## Forecasting protocol

At target date *t*, only observations strictly before *t* are available. A
forecast is recorded, actual *t* is revealed, and it may then enter history for
*t+1*. Prophet is a qualified comparator: it is past-only but refits only every
30 forecast dates rather than updating daily.

Different context lengths are not leakage. They are a methodological
sensitivity because the comparison is between complete forecasting systems:

| Model | Context/update policy |
|---|---|
| Naive | *t−1* only |
| 7-Day Moving Average | Last 7 prices |
| Simple Exponential Smoothing — Rolling One-Step | Last 128 prices; daily refit |
| Additive-Trend Exponential Smoothing | Last 128 prices; daily refit |
| ARIMA Rolling One-Step | Initial 128 returns plus daily state update |
| PE Log-Return LSTM | Last 30 returns |
| PE Log-Return Transformer | Last 128 returns |
| Chronos-Bolt-Tiny | Last 128 prices; zero-shot |
| TimesFM | Last 128 prices; zero-shot |
| Prophet — 30-Day Periodic Refit | 128 prices at periodic refit origin |

## Authoritative forecast artifact

`results/validated_forecasts.csv` is the immutable `bitcoin-v1` point-forecast
freeze. It contains 1,061 rows and 11 columns:

- `Timestamp`
- `Actual`
- `Naive`
- `Persistence_Enhanced_LSTM`
- `Chronos_Bolt_Tiny`
- `TimesFM`
- `ARIMA_Rolling`
- `Prophet_Periodic_Refit`
- `Simple_Exp_Smoothing`
- `Holt_Winters`
- `Persistence_Enhanced_Transformer`

The 7-Day Moving Average is reconstructed deterministically from the seven
strictly prior observations. The verifier reports 253 PASS and 0 FAIL for the
protected research artifacts.

## Final ten-model analytical set

The final set is Naive; Simple Exponential Smoothing — Rolling One-Step;
Additive-Trend Exponential Smoothing; ARIMA Rolling One-Step; 7-Day Moving
Average; Prophet — 30-Day Periodic Refit; Persistence-Enhanced Log-Return LSTM;
Persistence-Enhanced Log-Return Transformer; Chronos-Bolt-Tiny; and TimesFM.

Raw-price LSTMs, raw-price Transformer variants, static classical forecasts,
SARIMA, Moirai, PatchTST, iTransformer, Informer, and Autoformer are historical,
superseded, deferred, or unavailable and are not final comparison models.

## Point-forecast accuracy

All values are derived from `bitcoin_point_forecast_metrics_v2.csv`.

| Model | MAE | RMSE | MASE |
|---|---:|---:|---:|
| Naive | 1290.353 | 1853.625 | 4.576 |
| Simple Exponential Smoothing — Rolling One-Step | 1290.359 | 1855.731 | 4.576 |
| ARIMA Rolling One-Step | 1299.875 | 1866.303 | 4.609 |
| Additive-Trend Exponential Smoothing | 1308.541 | 1871.702 | 4.640 |
| PE Log-Return LSTM | 1321.365 | 1881.091 | 4.686 |
| TimesFM | 1349.947 | 1924.199 | 4.787 |
| Chronos-Bolt-Tiny | 1424.026 | 1994.008 | 5.050 |
| PE Log-Return Transformer | 2019.366 | 2559.750 | 7.161 |
| Prophet — 30-Day Periodic Refit | 8195.263 | 10781.163 | 29.061 |

MASE uses the training-only one-day Naive scale. Naive remains the best
point-forecast system; model complexity does not guarantee improvement.

## Regime-Conditional Robustness

The corrected thresholds are estimated once from training data only and then
applied unchanged to test returns:

- low volatility: 14-day volatility ≤ 0.0243102;
- high volatility: 14-day volatility ≥ 0.0375321;
- major upward movement: daily return ≥ 0.0250948;
- major downward movement: daily return ≤ −0.0184764.

Complete results are in
`bitcoin_regime_robustness_training_defined.csv`. These diagnostics are not a
claim of comprehensive robustness.

## Temporal Stability

The test is divided into Earlier, Middle, and Later contiguous segments of 354,
354, and 353 targets. Every model is evaluated on identical segment indices.
Temporal Stability is a within-test diagnostic, not broad transfer evidence.

## Uncertainty

`bitcoin_uncertainty_evidence_v2.csv` separates four evidence classes:

1. native Chronos and TimesFM quantiles;
2. training-only CQR-adjusted foundation quantiles;
3. validation-residual empirical intervals for Naive, MA7, ARIMA, SES,
   additive-trend smoothing, and PE Transformer;
4. unavailable evidence for PE-LSTM and Prophet.

Chronos native and calibrated 80% coverages are 0.8454 and 0.8153. TimesFM
native and calibrated coverages are 0.3308 and 0.5561. Chronos has a negative
CQR adjustment because its native intervals over-covered on the training
calibration window, so the conformal correction narrows them. Interval widths
are not compared blindly across heterogeneous methods. No test residuals are
used for calibration.

## Statistical inference

`bitcoin_dm_pairwise_results_hac_holm.csv` contains all 45 pairs among ten
models. It uses squared-error loss, a Bartlett/Newey–West HAC long-run variance,
and lag rule `floor(4*(N/100)^(2/9))`, giving lag 6 for N=1,061. Raw and
Holm-adjusted p-values are both retained. There are 39 raw-significant and 33
Holm-significant pairs at 0.05. Holm significance is the primary family-wise
interpretation.

## Transparency and Auditability

The published rubric defines mechanism transparency, artifact reproducibility,
deterministic behavior, implementation simplicity, failure detectability, and
external-checkpoint independence before scoring models. The complete rubric is
stored in `bitcoin_transparency_auditability_rubric.csv`.

## Exploratory composite trustworthiness

Dimension-level evidence is primary. The 35/20/20/15/10 composite is secondary
because components are correlated, weights are researcher-defined, results
depend on the comparison set, missing-evidence penalties measure completeness
rather than observed poor uncertainty, and uncertainty methods are
heterogeneous. Its uncertainty component uses coverage error only; interval
width is not ranked across evidence types.

Naive leads the missing-evidence-penalised summary at 97.052, followed closely
by SES at 96.971, ARIMA at 96.267, and additive-trend smoothing at 96.180.
PE-LSTM scores 81.343 under missing-evidence penalisation but 95.697 on its
available dimensions. Sensitivity results are stored in
`bitcoin_trust_score_sensitivity_v2.csv`.

## Reproducibility

Artifact-level reproduction and full model regeneration are deliberately
separated in `docs/bitcoin_reproducibility.md`. Safe Run All loads frozen
vectors. Model generation must use staging and explicit promotion. Full
end-to-end regeneration was not claimed during this rebuild.

## Final conclusion

For this daily, rolling one-step Bitcoin task, persistence is exceptionally
strong. The rebuilt workflow preserves the validated point vectors while
repairing test-derived regimes, serial-correlation-blind inference,
multiple-testing interpretation, uncertainty categorisation, Trust Score
terminology, and notebook orchestration.
