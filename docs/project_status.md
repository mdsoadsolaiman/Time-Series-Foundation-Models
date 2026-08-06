# Project Status

## Completed

- **Finance — Bitcoin:** authoritative rolling one-step comparison, trustworthiness evaluation, audit, and significance testing.
- **Energy — South Australian electricity demand:** EDA, two frozen forecast protocols, baselines, DHR-ARIMA, LSTM, foundation models, validation, trustworthiness, and significance testing.
- **Cross-domain comparison:** artifact-only comparison using ranks, scale-independent metrics, baseline-relative changes, calibration, and trust components.

## Planned

- **Weather:** next recommended domain because it adds multiscale seasonality, exogenous drivers, and operational uncertainty requirements.
- **Transport:** planned after Weather, with attention to network effects, events, and spatial heterogeneity.

## Blocked or optional models

- Moirai / Uni2TS: blocked in the completed Python 3.13 environment.
- PatchTST and iTransformer: require a separate supported NeuralForecast environment.
- None has an authoritative forecast vector, so none appears in final rankings.

## Notebook classification

### Authoritative or authoritative-analysis notebooks

- `01_EDA.ipynb`
- `05_Foundation_Models.ipynb`
- `06_Trustworthiness.ipynb`
- `07_Model_Validation_Audit.ipynb`
- `08_Naive_Forecast_Audit.ipynb`
- `09_Statistical_Significance_Test.ipynb`
- `18_Cross_Domain_Comparison.ipynb`
- Electricity notebooks `10` through `17`, including inserted phase `11b`

Model-generation notebooks are authoritative for their documented experiment but frozen downstream analysis should load saved vectors rather than rerun them.

### Exploratory or historical

- `03_Deep_Learning_LSTM.ipynb`: raw-price LSTM.
- `03b_LSTM_Improved.ipynb`: improved experimental LSTM.
- `04_Transformers.ipynb`: failed/collapsed Transformer case study.

### Protocol-limited

- `02_Classical_Models.ipynb`: historical statistical forecasts not admitted to the frozen rolling one-step ranking without equivalent saved vectors.

### Compatibility-only

- `05_Advanced_Forecasting_Models.ipynb`: unavailable-model scaffold.

## Authoritative result files

The principal frozen forecast artifacts are:

- `results/validated_forecasts.csv`
- `results/electricity/protocol_a_validated_forecasts.csv`
- `results/electricity/protocol_b_validated_forecasts.csv`
- `results/electricity/protocol_b_validated_horizon_metrics.csv`
- electricity robustness, generalisation, uncertainty, Trust Score, effect-size, and DM CSVs
- four `results/cross_domain_*.csv` synthesis files

See [`authoritative_artifact_hashes.md`](authoritative_artifact_hashes.md) for the complete protected set.

## Environment constraints

The audited system is CPU-only Windows 11 with Python 3.13.2. Foundation-model inference completed without a GPU. Notebook tooling partly resolves outside `.venv`; clean reproduction must install it explicitly. See [`environment.md`](environment.md).

## Current conclusions

TimesFM is strongest for both electricity horizons but not for Bitcoin. Chronos is better calibrated than TimesFM in every completed protocol. Strong baselines remain indispensable, horizon changes rankings, and point accuracy is not a proxy for uncertainty quality or overall trustworthiness.

## Next research options

1. Weather with chronological station/region protocols and native versus conformal uncertainty.
2. Additional electricity regions to test spatial transfer.
3. Calibration of TimesFM intervals without test leakage.
4. Python 3.11/3.12 environment for additional model families.
5. Transport after protocol and data-quality criteria are pre-registered.
