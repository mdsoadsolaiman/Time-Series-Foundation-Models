# Reusable Source Modules

- `data_loader.py` loads the minute-level Bitcoin CSV, converts Unix timestamps to UTC datetimes, sorts observations, and validates required columns.
- `preprocessing.py` resamples Bitcoin OHLCV observations to daily frequency and prepares the daily forecasting series.
- `metrics.py` implements MAE, RMSE, MAPE, and sMAPE with explicit array validation and percentage-error handling.
- `plots.py` provides a reusable time-series plotting helper.
- `__init__.py` exposes the source package.

The electricity notebooks contain their domain-specific TSF parsing and protocol logic. The authoritative results are saved under `results/`; importing these modules does not identify a result as authoritative.
