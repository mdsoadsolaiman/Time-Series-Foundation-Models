# Trustworthy Foundation Models for Time-Series Forecasting

## 1. Research Motivation

Point accuracy is necessary but insufficient for deployment. A forecast may be accurate on average yet fail during extremes, deteriorate over time, provide misleading intervals, or be difficult to audit. Primary evidence comprises point accuracy, regime-conditional robustness, temporal stability, uncertainty calibration, transparency/auditability, and statistical evidence.

## 2. Research Questions

1. **RQ1:** Do foundation models generalise consistently across domains?
2. **RQ2:** Does the strongest model depend on temporal structure?
3. **RQ3:** Can zero-shot foundation models outperform strong domain-specific baselines?
4. **RQ4:** Is uncertainty calibration consistent across domains?
5. **RQ5:** Does model complexity imply greater trustworthiness?
6. **RQ6:** How does forecast horizon change relative model performance?

## 3. Experimental Domains

Finance uses daily Bitcoin Close prices with a rolling one-step test of 1,061 days. Energy uses half-hourly South Australian electricity demand with 46,176 test observations under rolling one-step and 962 non-overlapping 48-step day-ahead origins.

## 4. Forecasting Models

- **Baselines:** Naive persistence, daily/weekly seasonal naive, moving average.
- **Statistical:** classical Bitcoin references where protocol permits; electricity DHR-ARIMA.
- **Deep learning:** Bitcoin Persistence-Enhanced LSTM and protocol-specific electricity LSTMs.
- **Foundation models:** zero-shot Chronos-Bolt-Tiny and TimesFM.

The two LSTMs are domain-adapted formulations and are compared as a family, not as identical architectures.

## 5. Validation Methodology

Both domains use chronological splits and prohibit lookahead. Bitcoin and Electricity Protocol A use rolling one-step information sets; Electricity Protocol B generates a full day without within-horizon actual updates. Selection uses validation evidence only, LSTM runs use deterministic controls, and downstream evaluations use exact saved forecast vectors. Diebold–Mariano tests use protocol-appropriate loss units and serial-dependence corrections. No cross-domain p-values are pooled.

## 6. Bitcoin Findings

| Rank | Model | MAE | RMSE | MAPE | sMAPE |
|---:|---|---:|---:|---:|---:|
| 1 | Naive | 1290.353242 | 1853.624774 | 1.742747 | 1.744142 |
| 2 | Persistence-Enhanced LSTM | 1323.040782 | 1886.566387 | 1.787392 | 1.794338 |
| 3 | TimesFM | 1349.946786 | 1924.199337 | 1.823179 | 1.823895 |
| 4 | Chronos-Bolt-Tiny | 1424.025828 | 1994.007926 | 1.934509 | 1.928782 |

Persistence is difficult to beat in this strongly persistent, nonstationary price series. Naive significantly outperforms PE-LSTM, TimesFM, and Chronos; TimesFM significantly outperforms Chronos; PE-LSTM and TimesFM are not significantly different at α = 0.05. Advanced models do not automatically improve on the appropriate simple baseline.

For native nominal 80% intervals, Chronos coverage is approximately 84.5%, compared with 33.1% for TimesFM. Chronos therefore has lower absolute marginal-coverage error in this task; coverage alone is insufficient because interval width and sharpness also matter.

## 7. Electricity Findings

TimesFM ranks first under both electricity protocols: MASE-48 0.1400 one-step and 0.6892 day-ahead. DHR-ARIMA ranks second one-step at 0.2276 but last day-ahead at 2.4557. Daily Seasonal Naive ranks third day-ahead at 1.1056. Chronos ranks third one-step (0.2762) and second day-ahead (1.0774). The LSTM is competitive but not dominant.

TimesFM's improvement over the strongest baseline is about 38% in each electricity protocol. The different DHR-ARIMA and seasonal-naive outcomes demonstrate that ranking depends on both temporal structure and information horizon.

## 8. Cross-Domain Findings

Raw MAE and RMSE are not compared between Bitcoin price units and electricity-demand units. Cross-domain conclusions use within-domain ranks, sMAPE, baseline-relative changes, calibration error, and comparative trust dimensions.

TimesFM trails Bitcoin Naive by about 4.6% in MAE and ranks third, but ranks first and decisively beats the strongest baselines in both electricity protocols. Chronos trails Bitcoin Naive, trails DHR-ARIMA one-step electricity, and narrowly beats Daily Seasonal Naive day-ahead. Foundation-model effectiveness is therefore domain- and horizon-dependent rather than universal.

## 9. Uncertainty Findings

Chronos is consistently closer to nominal 80% coverage: approximately 84.5% for Bitcoin, 91.1% for Electricity A, and 67.6% for Electricity B. TimesFM covers approximately 33.1%, 33.6%, and 24.6% respectively. TimesFM intervals are narrower, but the severe undercoverage shows that narrow intervals do not imply reliable uncertainty.

## 10. Trustworthiness Evidence and Exploratory Composite Synthesis

Dimension-level evidence is primary. The secondary exploratory composite retains Accuracy (35%), Robustness (20%), Temporal Stability (20%), Uncertainty (15%), and Transparency/Auditability (10%). Weights are researcher-defined, components are not statistically independent, and normalisation depends on the within-protocol comparison set.

The **Overall Trust Score — Missing Evidence Penalised** assigns zero contribution to unavailable evidence; the **Evidence-Available Trust Score** renormalises over observed components. Both are exploratory summaries and must be read after their dimensions. Missing uncertainty is not measured poor calibration. Model complexity does not ensure better evidence: Bitcoin Naive leads, transparent baselines score highly for auditability, and TimesFM's electricity point strength coexists with severe 80% undercoverage.

## 11. Statistical Significance

The central Bitcoin result is the statistically supported advantage of Naive over all three advanced models; PE-LSTM versus TimesFM is inconclusive at α = 0.05. In electricity, TimesFM significantly beats the strongest protocol-specific benchmark and Chronos under the primary squared-loss DM specifications. Chronos significantly improves on Daily Seasonal Naive in Protocol B squared loss, with a more cautious conclusion under absolute-loss sensitivity.

## 12. Practical Implications

- Always include simple and domain-specific baselines.
- Freeze the operational forecast protocol before comparing models.
- Zero-shot foundation models can be powerful without being universally dominant.
- Evaluate calibration independently of point accuracy.
- Inspect trust dimensions rather than treating an aggregate score as a substitute for evidence.

## 13. Limitations

Only two datasets and one electricity region are complete; domain effects cannot be separated cleanly from dataset, frequency, horizon, target, or evaluation-period effects. LSTM formulations differ and single runs do not quantify seed uncertainty. Native quantiles are limited; composite weights and transparency/auditability scores are researcher-defined. Moirai is absent, PatchTST and iTransformer are outside the authoritative final comparison, and foundation models are not fine-tuned.

## 14. Future Work

Extend the same frozen, artifact-first framework to Weather and Transport, additional electricity regions, more foundation-model scales, calibrated and conformal intervals, and additional domains. Future comparisons should preserve protocol-specific rankings and pre-register calibration and selection decisions.
