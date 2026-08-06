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

**Completed.** Daily Bitcoin Close is evaluated over 1,061 test days with rolling one-step forecasts. The authoritative comparison is `results/validated_forecasts.csv`.

### Domain 2 — Energy: South Australian Electricity Demand

**Completed.** Half-hourly South Australian demand is evaluated over 46,176 observations under rolling one-step Protocol A and 962 non-overlapping 48-step day-ahead origins under Protocol B.

### Domain 3 — Weather

**Planned.** This is the recommended next domain.

### Domain 4 — Transport

**Planned.** Protocol and dataset selection have not begun.

## Models Evaluated

- **Baselines:** Naive persistence, daily and weekly seasonal naive, moving average.
- **Statistical:** historical Bitcoin classical models; electricity DHR-ARIMA.
- **Deep learning:** Bitcoin Persistence-Enhanced LSTM and protocol-specific electricity LSTMs.
- **Foundation models:** zero-shot Chronos-Bolt-Tiny and TimesFM.
- **Unavailable/optional:** Moirai/Uni2TS, PatchTST, and iTransformer have no authoritative results.

## Evaluation Framework

- **Accuracy:** MAE, RMSE, MAPE, sMAPE, and electricity MASE-48.
- **Regime-Conditional Robustness:** predeclared demand/volatility or market regimes; not comprehensive adversarial robustness.
- **Temporal Stability:** contiguous chronological test segments; not broad cross-dataset or out-of-distribution generalisation.
- **Uncertainty:** supported native intervals, empirical coverage, and width.
- **Transparency and Auditability:** interpretation, complexity, reproducibility, and failure detectability; not direct XAI.
- **Statistical significance:** protocol-appropriate Diebold–Mariano tests.

Dimension-level evidence is primary. The secondary **Exploratory Composite Trustworthiness Summary** retains researcher-defined 35/20/20/15/10 weights. Components are not statistically independent, normalisation depends on the comparison set, and neither summary is a universal measurement instrument.

## Key Bitcoin Results

| Rank | Model | MAE | RMSE | MAPE | sMAPE |
|---:|---|---:|---:|---:|---:|
| 1 | Naive | 1290.353242 | 1853.624774 | 1.742747 | 1.744142 |
| 2 | Persistence-Enhanced LSTM | 1323.040782 | 1886.566387 | 1.787392 | 1.794338 |
| 3 | TimesFM | 1349.946786 | 1924.199337 | 1.823179 | 1.823895 |
| 4 | Chronos-Bolt-Tiny | 1424.025828 | 1994.007926 | 1.934509 | 1.928782 |

Naive significantly outperforms the three advanced models. TimesFM significantly outperforms Chronos; PE-LSTM versus TimesFM is not significant at α = 0.05. For native nominal 80% intervals, Chronos coverage is approximately 84.5% versus TimesFM's 33.1%; this is lower absolute marginal-coverage error, not universal calibration superiority. Bitcoin provides authoritative rolling one-step evidence only.

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
| `01_EDA.ipynb` | AUTHORITATIVE | Bitcoin data audit and daily preparation |
| `02_Classical_Models.ipynb` | PROTOCOL-LIMITED / HISTORICAL | Classical Bitcoin forecasts without equivalent frozen rolling vectors |
| `03_Deep_Learning_LSTM.ipynb` | EXPLORATORY | Raw-price LSTM |
| `03b_LSTM_Improved.ipynb` | EXPLORATORY | Improved experimental LSTM |
| `04_Transformers.ipynb` | EXPLORATORY | Failed/collapsed Transformer case study |
| `05_Advanced_Forecasting_Models.ipynb` | COMPATIBILITY-ONLY | Unavailable-model scaffold |
| `05_Foundation_Models.ipynb` | AUTHORITATIVE GENERATION | Bitcoin foundation-model evidence |
| `06_Trustworthiness.ipynb` | AUTHORITATIVE ANALYSIS | Bitcoin multidimensional trust evaluation |
| `07_Model_Validation_Audit.ipynb` | AUTHORITATIVE AUDIT | Bitcoin saved-vector validation |
| `08_Naive_Forecast_Audit.ipynb` | AUTHORITATIVE AUDIT | Persistence verification |
| `09_Statistical_Significance_Test.ipynb` | AUTHORITATIVE ANALYSIS | Bitcoin DM tests |
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

Inserted names `03b` and `11b` preserve historical phase order; notebooks are intentionally not renamed.

## Authoritative Artifacts

- Bitcoin: `results/validated_forecasts.csv`
- Electricity A: `results/electricity/protocol_a_validated_forecasts.csv`
- Electricity B: `results/electricity/protocol_b_validated_forecasts.csv`
- Trust evidence: `protocol_a_trust_scores.csv`, `protocol_b_trust_scores.csv`, and `trust_score_sensitivity.csv`
- Statistical evidence: protocol-specific DM and effect-size CSVs
- Cross-domain: the four `results/cross_domain_*.csv` files

The complete protected set and SHA-256 values are in [`results/authoritative_artifact_hashes.md`](results/authoritative_artifact_hashes.md). See [`results/README.md`](results/README.md) for artifact classification.

## Reproducibility

Do not overwrite frozen artifacts during routine notebook execution. Downstream audit, trustworthiness, significance, and synthesis work loads saved forecast vectors. Several audit/analysis notebooks are intentionally saved without execution outputs; their authoritative evidence is the frozen CSV set, not a claimed executed notebook state. Protocols use chronological splits, past-only information, validation-only selection, deterministic LSTM controls, and exact timestamp alignment. Run `python src/verify_research_artifacts.py` for lightweight artifact-level verification.

Start with:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-research.txt
```

## Environment

The audited completed environment is CPU-only Windows 11 build 26100 with Python 3.13.2. [`requirements-research.txt`](requirements-research.txt) is authoritative for direct research dependencies. Notebook tooling must be installed explicitly because the audited workstation resolves some Jupyter components outside `.venv`. Chronos-Bolt-Tiny and TimesFM inference completed on CPU. Moirai / Uni2TS was unavailable in the completed Python 3.13 workflow; PatchTST and iTransformer require a separate supported Python 3.11 or 3.12 NeuralForecast environment and have no authoritative forecasts. Artifact-only verification does not require model checkpoints.

## Limitations

Only two domains, one Bitcoin asset, and one electricity region are complete. Frequencies, targets, horizons, and LSTM formulations differ; single deterministic runs do not quantify seed uncertainty. Composite weights and transparency/auditability scores are researcher-defined. Supported uncertainty quantiles are limited. Moirai is absent, while PatchTST and iTransformer are outside the authoritative comparison and are not assumed to be zero-shot foundation models. No foundation model is fine-tuned.

## Future Work

Weather is the recommended next case study, followed by Transport. Other priorities are additional electricity regions, conformal calibration, foundation-model scaling, and compatible evaluation of additional model families.

Detailed reports: [`Bitcoin case study`](docs/bitcoin_case_study.md) and [`Electricity case study`](docs/electricity_case_study.md). The primary cross-domain narrative is the [`research manuscript`](paper/research_manuscript.md).
