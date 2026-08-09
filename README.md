# Trustworthy Foundation Models for Time-Series Forecasting

This research project evaluates time-series foundation models as forecasting systems rather than point-metric contestants. Two completed case studies examine point accuracy, regime-conditional robustness, temporal stability, uncertainty calibration, transparency/auditability, and statistical significance under frozen, leakage-controlled protocols.

## Research Manuscript

[`paper/research_manuscript.md`](paper/research_manuscript.md) is a manuscript-style report of the completed Finance and Energy experiments.

## Key Figures

![Cross-domain model ranks](figures/cross_domain/model_rank_across_domains.png)

![Electricity day-ahead example](figures/electricity/protocol_b_day_ahead_example.png)

![Cross-domain uncertainty calibration](figures/cross_domain/uncertainty_calibration_across_domains.png)

## Research Objective

The central question is whether zero-shot foundation models are consistently trustworthy across domains and forecast horizons. Chronos-Bolt-Tiny and TimesFM are compared with strong simple baselines, statistical models, and deterministic LSTMs. Exact forecast vectors are frozen before downstream analysis.

## Completed Domains

### Domain 1 — Finance: Bitcoin

**Completed and rebuilt.** Daily Bitcoin Close is evaluated over 1,061 test days with ten analytical models. Nine vectors are frozen in `results/validated_forecasts.csv`; the 7-Day Moving Average is reconstructed deterministically. Corrected downstream analysis uses training-defined regimes, Temporal Stability, method-labelled uncertainty, HAC inference, and Holm correction.

### Domain 2 — Energy: South Australian Electricity Demand

**Completed.** Half-hourly South Australian demand is evaluated over 46,176 observations under rolling one-step Protocol A and 962 non-overlapping 48-step day-ahead origins under Protocol B.

### Domain 3 — Weather

**Planned.** This is the recommended next domain.

### Domain 4 — Transport

**Planned.** Protocol and dataset selection have not begun.

## Models Evaluated

- **Baselines:** Naive persistence, daily and weekly seasonal naive, moving average.
- **Statistical:** Bitcoin rolling ARIMA, Simple Exponential Smoothing, additive-trend non-seasonal Holt-Winters, and periodic-refit Prophet; electricity DHR-ARIMA.
- **Deep learning:** Bitcoin Persistence-Enhanced Log-Return LSTM, Persistence-Enhanced Log-Return Transformer, and protocol-specific electricity LSTMs.
- **Foundation models:** zero-shot Chronos-Bolt-Tiny and TimesFM.
- **Unavailable/optional:** Moirai/Uni2TS, PatchTST, and iTransformer have no authoritative results.

## Evaluation Framework

- **Accuracy:** MAE, RMSE, MAPE, sMAPE, Bitcoin MASE-1, and electricity MASE-48.
- **Regime-Conditional Robustness:** predeclared demand/volatility or market regimes; not comprehensive adversarial robustness.
- **Temporal Stability:** contiguous chronological test segments; not broad cross-dataset or out-of-distribution transfer.
- **Uncertainty:** supported native intervals, empirical coverage, and width.
- **Transparency and Auditability:** interpretation, complexity, reproducibility, and failure detectability; not direct XAI.
- **Statistical significance:** protocol-appropriate Diebold–Mariano tests; Bitcoin uses Newey–West HAC variance and Holm family-wise correction.

Dimension-level evidence is primary. The secondary **Exploratory Composite Trustworthiness Summary** retains researcher-defined 35/20/20/15/10 weights. Components are not statistically independent, normalisation depends on the comparison set, and neither summary is a universal measurement instrument.

## Key Bitcoin Results

| Rank | Model | MAE | RMSE | MASE |
|---:|---|---:|---:|---:|
| 1 | Naive | 1290.353 | 1853.625 | 4.576 |
| 2 | Simple Exponential Smoothing — Rolling One-Step | 1290.359 | 1855.731 | 4.576 |
| 3 | ARIMA Rolling One-Step | 1299.875 | 1866.303 | 4.609 |
| 4 | Additive-Trend Exponential Smoothing | 1308.541 | 1871.702 | 4.640 |
| 5 | Persistence-Enhanced Log-Return LSTM | 1321.365 | 1881.091 | 4.686 |
| 6 | TimesFM | 1349.947 | 1924.199 | 4.787 |
| 7 | Chronos-Bolt-Tiny | 1424.026 | 1994.008 | 5.050 |
| 8 | Persistence-Enhanced Log-Return Transformer | 2019.366 | 2559.750 | 7.161 |
| 9 | Prophet — 30-Day Periodic Refit | 8195.263 | 10781.163 | 29.061 |

The 7-Day Moving Average is the tenth analytical model and is reconstructed
downstream from seven strictly prior prices. The corrected inference artifact
covers all 45 pairs with HAC lag 6: 39 pairs are raw-significant and 33 remain
significant after Holm correction.

The exploratory composite is secondary. Naive leads the missing-evidence-
penalised summary at `97.051891`, followed by SES at `96.970846`, ARIMA at
`96.266697`, and additive-trend smoothing at `96.179827`. PE-LSTM scores
`81.342547` with missing uncertainty penalised and `95.697114` on available
dimensions. Full evidence is generated in the versioned Bitcoin CSVs.

The final date, 2026-07-07, contains data only through 01:57 UTC and is retained
as a documented partial daily observation to preserve `bitcoin-v1`.

## Key Electricity Results

| Rank | Protocol A: rolling one-step | MASE-48 | Protocol B: 48-step day-ahead | MASE-48 |
|---:|---|---:|---|---:|
| 1 | TimesFM | 0.1400 | TimesFM | 0.6892 |
| 2 | DHR-ARIMA | 0.2276 | Chronos-Bolt-Tiny | 1.0774 |
| 3 | Chronos-Bolt-Tiny | 0.2762 | Daily Seasonal Naive | 1.1056 |
| 4 | Naive | 0.3611 | LSTM | 1.3064 |
| 5 | LSTM | 0.4017 | Weekly Seasonal Naive | 1.3088 |
| 6 | Daily Seasonal Naive | 1.1056 | Moving Average | 1.7359 |
| 7 | Weekly Seasonal Naive | 1.3088 | Naive | 2.0831 |
| 8 | Moving Average | 1.5302 | DHR-ARIMA | 2.4557 |

TimesFM leads both protocols and beats their strongest baselines by about 38%. Chronos 80% coverage is approximately 91.1% and 67.6%; TimesFM coverage is approximately 33.6% and 24.6%.

## Cross-Domain Findings

- TimesFM ranks third and trails Naive by about 4.6% in Bitcoin, but ranks first in both electricity protocols.
- Chronos has substantially lower absolute error from nominal 80% marginal coverage than TimesFM in every completed task; width and sharpness still matter.
- Strong baselines remain essential: persistence dominates Bitcoin, DHR-ARIMA is strong one-step, and Daily Seasonal Naive is strong day-ahead.
- In the completed tasks, rankings vary across dataset, domain, frequency, and forecasting protocol; one dataset per domain prevents isolation of a pure domain effect.
- Model complexity and point accuracy do not imply calibrated uncertainty or universal trustworthiness.

Raw Bitcoin and electricity MAE/RMSE values are never compared directly because their units and scales differ.

## Repository Structure

```text
TimeSeriesFoundationModels/
├── data/                         # Local datasets and dataset notes
├── docs/                         # Protocols, case studies, findings, environment, status
├── figures/
│   ├── bitcoin/                  # Bitcoin publication and diagnostic figures
│   ├── electricity/              # Protocol-specific electricity figures
│   └── cross_domain/             # Cross-domain synthesis figures
├── notebooks/
│   └── electricity/              # Electricity phases 1–9
├── paper/                        # Main research manuscript and references
├── proposal/                     # Research proposal
├── results/
│   └── electricity/              # Frozen forecasts and evidence by protocol
├── src/                          # Reusable loading, preprocessing, metrics, plots
├── requirements-research.txt     # Authoritative direct dependencies
└── requirements.txt              # Historical minimal environment file
```

## Notebook Guide

| Notebook | Status | Purpose |
|---|---|---|
| `Bitcoin_Master.ipynb` | MASTER / RECOMMENDED ENTRY POINT | Safe ten-model artifact-driven synthesis |
| `Electricity_Master.ipynb` | MASTER / RECOMMENDED ENTRY POINT | Safe Electricity orchestration, validation, and artifact-based analysis |
| `01_Bitcoin_Data_EDA.ipynb` | AUTHORITATIVE DATA | Canonical UTC aggregation, checks, and split |
| `02_Bitcoin_Classical_Baselines.ipynb` | AUTHORITATIVE ANALYSIS | Final past-only classical comparison |
| `03_Bitcoin_PE_LSTM.ipynb` | AUTHORITATIVE ANALYSIS | Frozen PE Log-Return LSTM evidence |
| `04_Bitcoin_PE_Transformer.ipynb` | AUTHORITATIVE ANALYSIS | Frozen PE Log-Return Transformer evidence |
| `05_Bitcoin_Prophet_and_Deferred_Models.ipynb` | SUPPORTING COMPARATOR | Periodic-refit Prophet and model-status table |
| `06_Bitcoin_Foundation_Models.ipynb` | AUTHORITATIVE ANALYSIS | Zero-shot Chronos and TimesFM evidence |
| `07_Bitcoin_Forecast_Freeze_and_Validation.ipynb` | AUTHORITATIVE GATE | Forecast-freeze boundary and validation |
| `08_Bitcoin_Naive_Audit.ipynb` | AUTHORITATIVE AUDIT | Persistence and leakage proof |
| `09_Bitcoin_Robustness_and_Temporal_Stability.ipynb` | AUTHORITATIVE ANALYSIS | Training-defined regimes and temporal segments |
| `10_Bitcoin_Uncertainty.ipynb` | AUTHORITATIVE ANALYSIS | Method-separated uncertainty evidence |
| `11_Bitcoin_Statistical_Inference.ipynb` | AUTHORITATIVE ANALYSIS | HAC DM tests and Holm adjustment |
| `12_Bitcoin_Trustworthiness_Synthesis.ipynb` | AUTHORITATIVE SYNTHESIS | Component-first evidence and secondary composite |
| `electricity/10_Electricity_EDA.ipynb` | AUTHORITATIVE | Dataset selection and audit |
| `electricity/11_Electricity_Baselines.ipynb` | AUTHORITATIVE GENERATION | Protocol-specific deterministic baselines |
| `electricity/11b_Electricity_Statistical_Model.ipynb` | AUTHORITATIVE GENERATION | DHR-ARIMA |
| `electricity/12_Electricity_LSTM.ipynb` | AUTHORITATIVE GENERATION | Deterministic LSTM forecasts |
| `electricity/13_Electricity_Foundation_Models.ipynb` | AUTHORITATIVE GENERATION | Zero-shot Chronos and TimesFM |
| `electricity/14_Electricity_Model_Validation_Audit.ipynb` | AUTHORITATIVE AUDIT | Protocol and vector audit |
| `electricity/15_Electricity_Trustworthiness_Evidence.ipynb` | ARTIFACT-ONLY ANALYSIS (saved without outputs) | Regime-conditional robustness, temporal stability, and uncertainty evidence |
| `electricity/16_Electricity_Trustworthiness.ipynb` | ARTIFACT-ONLY ANALYSIS (saved without outputs) | Exploratory composite scores and sensitivity |
| `electricity/17_Electricity_Statistical_Significance.ipynb` | AUTHORITATIVE ANALYSIS | Protocol-specific DM tests |
| `18_Cross_Domain_Comparison.ipynb` | AUTHORITATIVE SYNTHESIS | Artifact-only two-domain comparison |

The inserted `11b` name preserves the historical electricity phase order; notebooks are intentionally not renamed.

Use the master notebooks for routine inspection and artifact-based analysis. Use the phase-specific notebooks for model generation, audits, and historical implementation detail. Both master notebooks default to safe mode and do not load or train forecasting models.

## Authoritative Artifacts

- Bitcoin: `results/validated_forecasts.csv`
- Electricity A: `results/electricity/protocol_a_validated_forecasts.csv`
- Electricity B: `results/electricity/protocol_b_validated_forecasts.csv`
- Rebuilt Bitcoin trust evidence: `bitcoin_trustworthiness_components_v2.csv` and `bitcoin_trust_score_sensitivity_v2.csv`
- Corrected Bitcoin inference: `bitcoin_dm_pairwise_results_hac_holm.csv`; historical DM evidence is retained for provenance
- Cross-domain: the four `results/cross_domain_*.csv` files

The complete protected set and SHA-256 values are in [`results/authoritative_artifact_hashes.md`](results/authoritative_artifact_hashes.md). See [`results/README.md`](results/README.md) for artifact classification.

## Reproducibility

Routine Bitcoin Run All is artifact-only. Generation must write to staging and
requires explicit promotion. Run `python src/verify_research_artifacts.py` for
artifact verification. See [`docs/bitcoin_reproducibility.md`](docs/bitcoin_reproducibility.md)
for the separation between artifact-level reproduction and full model regeneration.

## Environment

The lightweight Bitcoin artifact environment is Python 3.12 on Windows and is
pinned in [`requirements-bitcoin-artifact.txt`](requirements-bitcoin-artifact.txt).
The historical full-generation record used CPU-only Python 3.13.2, TensorFlow
2.21.0, Torch 2.12.1, Chronos Forecasting 2.3.1, and TimesFM 2.0.2. The original
`.venv` references a removed Python installation; full regeneration was not
rerun or claimed during this rebuild.

## Limitations

Only two domains, one Bitcoin asset, and one electricity region are complete. Frequencies, targets, horizons, and LSTM formulations differ; single deterministic runs do not quantify seed uncertainty. Composite weights and transparency/auditability scores are researcher-defined. Supported uncertainty quantiles are limited. Moirai is absent, while PatchTST and iTransformer are outside the authoritative comparison and are not assumed to be zero-shot foundation models. No foundation model is fine-tuned.

## Future Work

Weather is the recommended next case study, followed by Transport. Other priorities are additional electricity regions, foundation-model scaling, and compatible Python 3.12 evaluation of Moirai, PatchTST, and iTransformer.

Detailed reports: [`Bitcoin case study`](docs/bitcoin_case_study.md) and [`Electricity case study`](docs/electricity_case_study.md). The primary cross-domain narrative is the [`research manuscript`](paper/research_manuscript.md).
