"""Canonical, artifact-driven utilities for the Bitcoin research workflow.

The module deliberately separates inexpensive analysis of frozen vectors from
model generation.  Nothing here trains a model or promotes a staged forecast
without explicit opt-in.
"""

from __future__ import annotations

import hashlib
import platform
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from src.data_loader import load_bitcoin_data
from src.metrics import mae, mape, mase, rmse, smape
from src.preprocessing import prepare_daily_bitcoin_data

EXPECTED_FORECAST_COLUMNS = [
    "Timestamp", "Actual", "Naive", "Persistence_Enhanced_LSTM",
    "Chronos_Bolt_Tiny", "TimesFM", "ARIMA_Rolling",
    "Prophet_Periodic_Refit", "Simple_Exp_Smoothing", "Holt_Winters",
    "Persistence_Enhanced_Transformer",
]

MODEL_COLUMNS = {
    "Naive": "Naive",
    "Simple Exponential Smoothing — Rolling One-Step": "Simple_Exp_Smoothing",
    "Additive-Trend Exponential Smoothing": "Holt_Winters",
    "ARIMA Rolling One-Step": "ARIMA_Rolling",
    "Prophet — 30-Day Periodic Refit": "Prophet_Periodic_Refit",
    "Persistence-Enhanced Log-Return LSTM": "Persistence_Enhanced_LSTM",
    "Persistence-Enhanced Log-Return Transformer": "Persistence_Enhanced_Transformer",
    "Chronos-Bolt-Tiny": "Chronos_Bolt_Tiny",
    "TimesFM": "TimesFM",
}

FINAL_MODEL_ORDER = [
    "Naive", "Simple Exponential Smoothing — Rolling One-Step",
    "Additive-Trend Exponential Smoothing", "ARIMA Rolling One-Step",
    "7-Day Moving Average", "Prophet — 30-Day Periodic Refit",
    "Persistence-Enhanced Log-Return LSTM",
    "Persistence-Enhanced Log-Return Transformer", "Chronos-Bolt-Tiny", "TimesFM",
]

CONTEXT_POLICY = {
    "Naive": "t-1 only",
    "7-Day Moving Average": "last 7 prices; daily update",
    "Simple Exponential Smoothing — Rolling One-Step": "last 128 prices; daily refit",
    "Additive-Trend Exponential Smoothing": "last 128 prices; daily refit",
    "ARIMA Rolling One-Step": "initial 128 returns plus daily state update",
    "Persistence-Enhanced Log-Return LSTM": "last 30 returns; fixed trained model",
    "Persistence-Enhanced Log-Return Transformer": "last 128 returns; fixed trained model",
    "Chronos-Bolt-Tiny": "last 128 prices; zero-shot; horizon 1",
    "TimesFM": "last 128 prices; zero-shot; horizon 1",
    "Prophet — 30-Day Periodic Refit": "128 prices at refit origin; refit every 30 targets",
}

TRUST_TERMINOLOGY = {
    "accuracy": "Point Forecast Accuracy",
    "robustness": "Regime-Conditional Robustness",
    "stability": "Temporal Stability",
    "uncertainty": "Uncertainty Calibration",
    "transparency": "Transparency and Auditability",
    "inference": "Statistical Significance / Practical Effect",
}


def find_project_root(start: str | Path | None = None) -> Path:
    path = Path(start or Path.cwd()).resolve()
    for candidate in (path, *path.parents):
        if (candidate / "src").is_dir() and (candidate / "results").is_dir():
            return candidate
    raise FileNotFoundError("Could not locate the TimeSeriesFoundationModels project root")


def load_bitcoin_target(root: str | Path) -> tuple[pd.DataFrame, pd.Series]:
    root = Path(root)
    raw = load_bitcoin_data(root / "data" / "bitcoin" / "btcusd_1-min_data.csv")
    daily = prepare_daily_bitcoin_data(raw)
    target = daily["Close"].dropna().asfreq("D").astype(float).rename("Close")
    if target.isna().any() or not target.index.is_unique:
        raise ValueError("Canonical Bitcoin target must be complete and unique")
    return daily, target


def canonical_split(target: pd.Series) -> tuple[pd.Series, pd.Series]:
    split = int(len(target) * 0.8)
    train, test = target.iloc[:split], target.iloc[split:]
    if len(target) != 5302 or len(train) != 4241 or len(test) != 1061:
        raise ValueError("Unexpected canonical Bitcoin split")
    if train.index.max() >= test.index.min():
        raise ValueError("Bitcoin split is not chronological")
    return train, test


def load_validated_forecasts(root: str | Path) -> pd.DataFrame:
    path = Path(root) / "results" / "validated_forecasts.csv"
    frame = pd.read_csv(path, parse_dates=["Timestamp"])
    frame["Timestamp"] = pd.to_datetime(frame["Timestamp"], utc=True)
    if frame.columns.tolist() != EXPECTED_FORECAST_COLUMNS or frame.shape != (1061, 11):
        raise ValueError(f"Unexpected validated Bitcoin schema: {frame.shape}, {frame.columns.tolist()}")
    if frame["Timestamp"].duplicated().any() or not frame["Timestamp"].is_monotonic_increasing:
        raise ValueError("Validated Bitcoin timestamps must be ordered and unique")
    if frame.isna().any().any() or not np.isfinite(frame.drop(columns="Timestamp")).all().all():
        raise ValueError("Validated Bitcoin artifact contains invalid values")
    return frame.set_index("Timestamp")


def seven_day_moving_average(target: pd.Series, test_index: pd.DatetimeIndex) -> pd.Series:
    forecast = target.shift(1).rolling(7).mean().reindex(test_index)
    if forecast.isna().any() or not forecast.index.equals(test_index):
        raise ValueError("Invalid 7-Day Moving Average reconstruction")
    return forecast.rename("7-Day Moving Average")


def forecast_series(frame: pd.DataFrame, target: pd.Series) -> dict[str, pd.Series]:
    result = {name: frame[column].rename(name) for name, column in MODEL_COLUMNS.items()}
    result["7-Day Moving Average"] = seven_day_moving_average(target, frame.index)
    return {name: result[name] for name in FINAL_MODEL_ORDER}


def metric_table(actual: pd.Series, forecasts: dict[str, pd.Series], train: pd.Series) -> pd.DataFrame:
    rows = []
    for name, forecast in forecasts.items():
        rows.append({"Model": name, "MAE": mae(actual, forecast), "RMSE": rmse(actual, forecast),
                     "MAPE": mape(actual, forecast), "sMAPE": smape(actual, forecast),
                     "MASE": mase(actual, forecast, train, 1), "N": len(actual)})
    table = pd.DataFrame(rows).set_index("Model")
    if "Naive" in table.index:
        table["Relative MAE vs Naive"] = table["MAE"] / table.loc["Naive", "MAE"]
    return table


def training_regime_thresholds(train: pd.Series) -> dict[str, float]:
    returns = train.pct_change()
    volatility = returns.rolling(14, min_periods=7).std()
    return {
        "volatility_low_33": float(volatility.quantile(0.33)),
        "volatility_high_67": float(volatility.quantile(0.67)),
        "return_major_up_80": float(returns.quantile(0.80)),
        "return_major_down_20": float(returns.quantile(0.20)),
    }


def test_regime_masks(target: pd.Series, test_index: pd.DatetimeIndex,
                      thresholds: dict[str, float]) -> dict[str, pd.Series]:
    returns = target.pct_change().reindex(test_index)
    volatility = target.pct_change().rolling(14, min_periods=7).std().reindex(test_index)
    return {
        "Low Volatility": volatility <= thresholds["volatility_low_33"],
        "High Volatility": volatility >= thresholds["volatility_high_67"],
        "Major Upward Movement": returns >= thresholds["return_major_up_80"],
        "Major Downward Movement": returns <= thresholds["return_major_down_20"],
    }


def robustness_table(actual: pd.Series, forecasts: dict[str, pd.Series], train: pd.Series,
                     masks: dict[str, pd.Series]) -> pd.DataFrame:
    rows = []
    for regime, mask in masks.items():
        index = mask[mask.fillna(False)].index
        for model, forecast in forecasts.items():
            rows.append({"Regime": regime, "Model": model, "N": len(index),
                         "MAE": mae(actual.loc[index], forecast.loc[index]),
                         "RMSE": rmse(actual.loc[index], forecast.loc[index]),
                         "MAPE": mape(actual.loc[index], forecast.loc[index]),
                         "sMAPE": smape(actual.loc[index], forecast.loc[index]),
                         "MASE": mase(actual.loc[index], forecast.loc[index], train, 1)})
    return pd.DataFrame(rows)


def temporal_segments(index: pd.DatetimeIndex) -> dict[str, pd.DatetimeIndex]:
    return {name: pd.DatetimeIndex(values) for name, values in zip(
        ["Earlier", "Middle", "Later"], np.array_split(index, 3))}


def temporal_stability_table(actual: pd.Series, forecasts: dict[str, pd.Series], train: pd.Series) -> pd.DataFrame:
    rows = []
    for segment, index in temporal_segments(actual.index).items():
        for model, forecast in forecasts.items():
            rows.append({"Segment": segment, "Model": model, "N": len(index),
                         "Start": index.min(), "End": index.max(),
                         "MAE": mae(actual.loc[index], forecast.loc[index]),
                         "RMSE": rmse(actual.loc[index], forecast.loc[index]),
                         "MAPE": mape(actual.loc[index], forecast.loc[index]),
                         "sMAPE": smape(actual.loc[index], forecast.loc[index]),
                         "MASE": mase(actual.loc[index], forecast.loc[index], train, 1)})
    return pd.DataFrame(rows)


def hac_dm(actual: pd.Series, forecast_a: pd.Series, forecast_b: pd.Series,
           max_lag: int | None = None) -> dict[str, float]:
    """Two-sided DM test using squared loss and Bartlett Newey-West HAC variance."""
    aligned = pd.concat([actual, forecast_a, forecast_b], axis=1).dropna()
    a, fa, fb = (aligned.iloc[:, i].to_numpy(float) for i in range(3))
    differential = (a - fa) ** 2 - (a - fb) ** 2
    n = len(differential)
    lag = int(np.floor(4 * (n / 100) ** (2 / 9))) if max_lag is None else int(max_lag)
    centered = differential - differential.mean()
    long_run = float(np.dot(centered, centered) / n)
    for k in range(1, min(lag, n - 1) + 1):
        covariance = float(np.dot(centered[k:], centered[:-k]) / n)
        long_run += 2 * (1 - k / (lag + 1)) * covariance
    if long_run <= 0 or not np.isfinite(long_run):
        statistic, p_value = np.nan, np.nan
    else:
        statistic = float(differential.mean() / np.sqrt(long_run / n))
        p_value = float(2 * stats.norm.sf(abs(statistic)))
    return {"N": n, "HAC Lag": lag, "Mean loss differential": float(differential.mean()),
            "DM statistic": statistic, "Raw p-value": p_value}


def holm_adjust(p_values: pd.Series) -> pd.Series:
    values = p_values.to_numpy(float)
    order = np.argsort(values)
    adjusted_sorted = np.maximum.accumulate((len(values) - np.arange(len(values))) * values[order])
    adjusted = np.empty_like(values)
    adjusted[order] = np.minimum(adjusted_sorted, 1.0)
    return pd.Series(adjusted, index=p_values.index, name="Holm-adjusted p-value")


def sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def validate_staged_forecast(path: str | Path, model_column: str,
                             expected_index: pd.DatetimeIndex) -> pd.DataFrame:
    frame = pd.read_csv(path, parse_dates=["Timestamp"])
    frame["Timestamp"] = pd.to_datetime(frame["Timestamp"], utc=True)
    if frame.columns.tolist() != ["Timestamp", model_column] or len(frame) != len(expected_index):
        raise ValueError("Staged forecast schema or row count is invalid")
    if not pd.DatetimeIndex(frame["Timestamp"]).equals(expected_index):
        raise ValueError("Staged forecast timestamps do not match the canonical test")
    if frame.isna().any().any() or not np.isfinite(frame[model_column]).all():
        raise ValueError("Staged forecast contains invalid values")
    return frame


def promote_staged_forecast(staged_path: str | Path, authoritative_path: str | Path,
                            model_column: str, expected_index: pd.DatetimeIndex,
                            *, explicit_opt_in: bool = False,
                            expected_hash: str | None = None) -> None:
    if not explicit_opt_in:
        raise PermissionError("Promotion requires explicit_opt_in=True")
    validate_staged_forecast(staged_path, model_column, expected_index)
    if expected_hash and sha256(staged_path) != expected_hash.upper():
        raise ValueError("Staged forecast does not match the required hash")
    shutil.copy2(staged_path, authoritative_path)


def environment_summary() -> dict[str, str]:
    return {"Python": platform.python_version(), "OS": platform.platform(),
            "Machine": platform.machine(), "Processor": platform.processor() or "unknown"}
