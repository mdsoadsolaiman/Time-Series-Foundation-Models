# Research Figure Library

This directory contains standalone figures from the authoritative Bitcoin and Electricity notebooks. Each listed image is saved by its source plotting cell at 300 DPI using the evidence already loaded by that notebook. Model fitting and forecast generation are not required.

The `cross_domain/` collection is outside the scope of this domain-figure extraction and remains unchanged.

# Bitcoin Figures

| Figure | Source Notebook | Section | Purpose |
|---|---|---|---|
| `bitcoin/bitcoin_price_history.png` | `01_Bitcoin_Data_EDA.ipynb` | Raw Series Visualisation | Shows the full daily Bitcoin Close series. |
| `bitcoin/bitcoin_log_return_distribution.png` | `01_Bitcoin_Data_EDA.ipynb` | Distributional Analysis | Compares daily log returns with a normal reference. |
| `bitcoin/bitcoin_return_acf_pacf.png` | `01_Bitcoin_Data_EDA.ipynb` | Autocorrelation and Seasonality Analysis | Shows ACF and PACF evidence for daily log returns. |
| `bitcoin/bitcoin_returns_and_long_run_volatility.png` | `01_Bitcoin_Data_EDA.ipynb` | Structural Change and Regime Preview | Shows returns with 90-day rolling volatility. |
| `bitcoin/bitcoin_model_accuracy.png` | `07_Bitcoin_Forecast_Freeze_and_Validation.ipynb` | Full Ranking Visualisation | Ranks the validated Bitcoin models by RMSE. |
| `bitcoin/bitcoin_regime_conditional_rmse.png` | `09_Bitcoin_Robustness_and_Temporal_Stability.ipynb` | Regime RMSE Comparison | Compares model error across training-defined regimes. |
| `bitcoin/bitcoin_regime_rmse_bootstrap_intervals.png` | `09_Bitcoin_Robustness_and_Temporal_Stability.ipynb` | Bootstrap Uncertainty | Shows block-bootstrap intervals for regime RMSE. |
| `bitcoin/bitcoin_temporal_stability_rmse.png` | `09_Bitcoin_Robustness_and_Temporal_Stability.ipynb` | Segment RMSE Comparison | Compares Earlier, Middle, and Later test segments. |
| `bitcoin/bitcoin_uncertainty_coverage_comparison.png` | `10_Bitcoin_Uncertainty.ipynb` | Available-Evidence Coverage Comparison | Compares empirical interval coverage where evidence exists. |
| `bitcoin/bitcoin_holm_significance_matrix.png` | `11_Bitcoin_Statistical_Inference.ipynb` | Holm Significance Matrix | Shows corrected pairwise significance results. |
| `bitcoin/bitcoin_trustworthiness_ranking.png` | `12_Bitcoin_Trustworthiness_Synthesis.ipynb` | Trustworthiness Ranking | Shows the exploratory composite ranking. |
| `bitcoin/bitcoin_trustworthiness_weight_sensitivity.png` | `12_Bitcoin_Trustworthiness_Synthesis.ipynb` | Weight Sensitivity | Compares ranks under alternative component weights. |
| `bitcoin/bitcoin_trustworthiness_rank_stability.png` | `12_Bitcoin_Trustworthiness_Synthesis.ipynb` | Rank Distribution Plot | Shows bootstrap uncertainty in trustworthiness ranks. |

# Electricity Figures

| Figure | Source Notebook | Section | Purpose |
|---|---|---|---|
| `electricity/electricity_demand_history.png` | `electricity/10_Electricity_EDA.ipynb` | Raw Demand Series | Shows the full South Australian demand series. |
| `electricity/electricity_intraday_profile.png` | `electricity/10_Electricity_EDA.ipynb` | Intraday Variability Visualization | Shows the mean and variability of demand by half-hour. |
| `electricity/electricity_weekday_intraday_heatmap.png` | `electricity/10_Electricity_EDA.ipynb` | Weekday × Time-of-Day Heatmap | Shows recurring weekly demand structure. |
| `electricity/electricity_rolling_variability.png` | `electricity/10_Electricity_EDA.ipynb` | Rolling Variability | Shows short and weekly rolling variation. |
| `electricity/electricity_classical_protocol_a_ranking.png` | `electricity/11_Electricity_Classical_Baselines.ipynb` | Protocol A Ranked Visualisation | Ranks conventional models under rolling one-step forecasting. |
| `electricity/electricity_classical_protocol_b_ranking.png` | `electricity/11_Electricity_Classical_Baselines.ipynb` | Protocol B Ranked Visualisation | Ranks conventional models under fixed-origin day-ahead forecasting. |
| `electricity/electricity_protocol_b_horizon_rmse.png` | `electricity/11_Electricity_Classical_Baselines.ipynb` | RMSE by Horizon | Shows conventional-model RMSE across horizons 1–48. |
| `electricity/electricity_protocol_b_horizon_mase.png` | `electricity/11_Electricity_Classical_Baselines.ipynb` | MASE-48 by Horizon | Shows conventional-model MASE-48 across horizons 1–48. |
| `electricity/electricity_classical_rank_change_across_protocols.png` | `electricity/11_Electricity_Classical_Baselines.ipynb` | Ranking Change Across Protocols | Shows how conventional-model ranks change between protocols. |
| `electricity/electricity_foundation_protocol_a_comparison.png` | `electricity/13_Electricity_Foundation_Models.ipynb` | Protocol A Comparison | Compares zero-shot foundation models and reference baselines. |
| `electricity/electricity_foundation_protocol_b_comparison.png` | `electricity/13_Electricity_Foundation_Models.ipynb` | Protocol B Comparison | Compares foundation models under day-ahead forecasting. |
| `electricity/electricity_foundation_horizon_comparison.png` | `electricity/13_Electricity_Foundation_Models.ipynb` | Horizon-Wise Head-to-Head | Compares foundation-model MAE across day-ahead horizons. |
| `electricity/electricity_foundation_residuals.png` | `electricity/13_Electricity_Foundation_Models.ipynb` | Residual Comparison | Shows foundation-model residuals under both protocols. |
| `electricity/electricity_protocol_a_regime_performance.png` | `electricity/15_Electricity_Robustness.ipynb` | Protocol A Regime × Model Heatmap | Shows conditional performance under Protocol A. |
| `electricity/electricity_protocol_b_regime_performance.png` | `electricity/15_Electricity_Robustness.ipynb` | Protocol B Regime × Model Heatmap | Shows conditional performance under Protocol B. |
| `electricity/electricity_robustness_rank_change.png` | `electricity/15_Electricity_Robustness.ipynb` | Protocol-Sensitivity Visualization | Shows robustness-rank changes between protocols. |
| `electricity/electricity_temporal_stability_ranking.png` | `electricity/15_Electricity_Robustness.ipynb` | Temporal Stability Rankings | Compares Earlier, Middle, and Later performance ranks. |
| `electricity/electricity_protocol_a_uncertainty_coverage.png` | `electricity/16_Electricity_Uncertainty.ipynb` | Protocol A Coverage Calibration | Compares native interval coverage with the nominal level. |
| `electricity/electricity_protocol_b_uncertainty_coverage.png` | `electricity/16_Electricity_Uncertainty.ipynb` | Protocol B Coverage Calibration | Compares day-ahead native interval coverage. |
| `electricity/electricity_uncertainty_protocol_sensitivity.png` | `electricity/16_Electricity_Uncertainty.ipynb` | Protocol Sensitivity | Shows changes in absolute coverage error. |
| `electricity/electricity_accuracy_uncertainty_tradeoff.png` | `electricity/16_Electricity_Uncertainty.ipynb` | Point Accuracy vs Uncertainty Quality | Compares point MASE-48 with absolute coverage error. |
| `electricity/electricity_trustworthiness_composite.png` | `electricity/17_Electricity_Trustworthiness.ipynb` | Composite Ranking Visualization | Compares penalised and evidence-available composite scores. |
| `electricity/electricity_trustworthiness_rank_stability.png` | `electricity/17_Electricity_Trustworthiness.ipynb` | Rank-Stability Visualization | Shows ranking sensitivity to component weights. |
| `electricity/electricity_effect_size_statistical_evidence.png` | `electricity/18_Electricity_Statistical_Significance.ipynb` | Effect Size vs Statistical Evidence | Compares practical effect size with adjusted statistical evidence. |
| `electricity/electricity_horizon_significance.png` | `electricity/18_Electricity_Statistical_Significance.ipynb` | Horizon Significance Visualization | Shows selected horizon-specific significance results. |

Existing images not listed above are retained for audit continuity. Some were generated by the current paper-figure workflow or are older diagnostics. They should not be treated as notebook-authoritative without checking their original source.
