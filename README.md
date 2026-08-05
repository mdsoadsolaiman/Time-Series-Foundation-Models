# TimeSeriesFoundationModels

This project investigates trustworthy foundation models for time-series forecasting.

Research direction:

**Trustworthy Foundation Models for Time-Series Forecasting: Evaluating Generalisation, Uncertainty, and Explainability.**

The first completed domain case study is Bitcoin daily price forecasting. The project compares deterministic baselines, classical statistical models, supervised neural models, and zero-shot foundation models under a clearly documented validation protocol.

## Domain 1 - Financial Time Series

**Bitcoin - Completed**

The Bitcoin experiment uses the physically present minute-level BTC/USD dataset at:

```text
data/bitcoin/btcusd_1-min_data.csv
```

The raw OHLCV data are resampled to daily frequency, with daily `Close` used as the forecasting target. The completed authoritative rolling one-step comparison is frozen in:

```text
results/validated_forecasts.csv
```

Authoritative forecast columns:

- `Actual`
- `Naive`
- `Persistence_Enhanced_LSTM`
- `Chronos_Bolt_Tiny`
- `TimesFM`

The Bitcoin case-study summary is documented in:

```text
docs/bitcoin_case_study.md
```

## Cross-Domain Evaluation Plan

- Domain 1 - Finance: Bitcoin - Completed
- Domain 2 - Energy - Planned
- Domain 3 - Weather - Planned
- Domain 4 - Transport - Planned

No results are reported yet for the planned future domains.

## Current Project Structure

```text
TimeSeriesFoundationModels/
|-- data/
|   |-- bitcoin/
|   |   `-- btcusd_1-min_data.csv
|   |-- exchange_rate/
|   |-- traffic/
|   `-- weather/
|-- docs/
|   |-- bitcoin_case_study.md
|   `-- patchtst_itransformer_environment.md
|-- figures/
|-- notebooks/
|   |-- 01_EDA.ipynb
|   |-- 02_Classical_Models.ipynb
|   |-- 03_Deep_Learning_LSTM.ipynb
|   |-- 03b_LSTM_Improved.ipynb
|   |-- 04_Transformers.ipynb
|   |-- 05_Advanced_Forecasting_Models.ipynb
|   |-- 05_Foundation_Models.ipynb
|   |-- 06_Trustworthiness.ipynb
|   |-- 07_Model_Validation_Audit.ipynb
|   |-- 08_Naive_Forecast_Audit.ipynb
|   `-- 09_Statistical_Significance_Test.ipynb
|-- papers/
|-- proposal/
|-- results/
|   |-- baseline_forecasts.csv
|   |-- chronos_bolt_tiny_forecast.csv
|   |-- persistence_enhanced_lstm_forecast.csv
|   |-- timesfm_forecast.csv
|   `-- validated_forecasts.csv
|-- src/
|   |-- data_loader.py
|   |-- metrics.py
|   |-- plots.py
|   `-- preprocessing.py
|-- README.md
`-- requirements.txt
```

## Reusable Bitcoin Pipeline Modules

- `src/data_loader.py`: loads the raw Bitcoin CSV and converts the Unix-seconds `Timestamp` column to UTC datetimes.
- `src/preprocessing.py`: prepares daily OHLCV Bitcoin data from the minute-level dataset.
- `src/plots.py`: provides a reusable daily time-series plotting helper.
- `src/metrics.py`: implements MAE, RMSE, MAPE, and sMAPE.

Example:

```python
from src.data_loader import load_bitcoin_data
from src.preprocessing import prepare_daily_bitcoin_data

df = load_bitcoin_data("data/bitcoin/btcusd_1-min_data.csv")
df_daily = prepare_daily_bitcoin_data(df)
```

## Bitcoin Model Status

Authoritative rolling one-step models:

- Naive persistence baseline
- Persistence-Enhanced LSTM
- Chronos-Bolt-Tiny
- TimesFM

Deterministic benchmark recreated from historical actuals:

- 7-Day Moving Average

Exploratory or failed models, not part of the authoritative saved-vector ranking:

- Original raw-price LSTM
- Improved experimental LSTM
- Collapsed Transformer
- Corrected but over-smoothed Transformer

Protocol-limited statistical models:

- ARIMA and SARIMA are not included in the main rolling one-step Trust Score unless exact rolling one-step saved vectors are available.

## Reproducibility Notes

- Do not overwrite `results/validated_forecasts.csv` unless intentionally regenerating the frozen Bitcoin artifact.
- Notebook 06 is intended to be artifact-only: it should load saved forecasts and must not train, refit, or load model checkpoints.
- Notebook 09 performs statistical-significance testing from saved forecast vectors.
- PatchTST, iTransformer, and Moirai/Uni2TS remain outside the completed Bitcoin scope because of environment compatibility blockers.
