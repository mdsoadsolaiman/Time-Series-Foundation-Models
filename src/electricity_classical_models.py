"""Leakage-safe classical comparators for the electricity case study.

Parameters and periodic-refit cadences are selected on development/validation data.
Final test forecasts reuse those frozen choices.  No function mutates authoritative
artifacts unless the explicit generator script is run.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing, SimpleExpSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX


SCALE_MASE_48 = 117.057971280678
PERIODIC_CADENCES = (672, 1344, 2688)  # 14, 28, and 56 days of half-hourly targets.
# Simple Exponential Smoothing has no trend/seasonal term, so its multi-step forecast is
# flat for the whole cadence window; at the 14-56 day candidates above it collapses to
# too few distinct levels project-wide. Refitting is computationally trivial for this
# model (single smoothing weight), so a much finer, still genuinely "periodic" (not
# per-step) candidate set is used instead.
SES_PERIODIC_CADENCES = (48, 96, 168, 336)  # 1, 2, 3.5, and 7 days.
FIT_WINDOW = 17520  # trailing year, fixed before validation selection
STATE_FIT_WINDOW = 3360  # trailing ten weeks for bounded ARIMA/SARIMA estimation


@dataclass(frozen=True)
class Partitions:
    full: pd.Series
    development: pd.Series
    validation: pd.Series
    pretest: pd.Series
    test: pd.Series


def load_electricity_partitions(root: str | Path) -> Partitions:
    path = Path(root) / "data/electricity/australian_electricity_demand_dataset.tsf"
    attrs, rows = [], []
    with path.open(encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("@attribute"):
                _, name, kind = line.split(maxsplit=2)
                attrs.append((name, kind))
            elif not line.startswith("@"):
                parts = line.split(":", len(attrs))
                row = dict(zip((item[0] for item in attrs), parts[:-1]))
                row["series_value"] = np.fromstring(parts[-1], sep=",")
                rows.append(row)
    raw = pd.DataFrame(rows)
    row = raw[(raw.series_name == "T4") & (raw.state == "SA")].iloc[0]
    index = pd.date_range(
        pd.to_datetime(row.start_timestamp, format="%Y-%m-%d %H-%M-%S"),
        periods=len(row.series_value), freq="30min",
    )
    full = pd.Series(row.series_value, index=index, name="Demand", dtype=float)
    parts = Partitions(
        full=full,
        development=full.loc[:"2011-06-23 23:30"],
        validation=full.loc["2011-06-24":"2012-07-12 23:30"],
        pretest=full.loc[:"2012-07-12 23:30"],
        test=full.loc["2012-07-13":],
    )
    assert tuple(map(len, (parts.development, parts.validation, parts.pretest, parts.test))) == (166128, 18480, 184608, 46176)
    return parts


def mase48(actual, forecast, scale: float = SCALE_MASE_48) -> float:
    return float(np.mean(np.abs(np.asarray(actual) - np.asarray(forecast))) / scale)


def training_seasonality(series: pd.Series) -> dict[str, float]:
    values = series.to_numpy(float)
    return {
        "Lag_48_ACF": float(np.corrcoef(values[48:], values[:-48])[0, 1]),
        "Lag_336_ACF": float(np.corrcoef(values[336:], values[:-336])[0, 1]),
    }


def _fit_state_model(values: np.ndarray, model: str, specification):
    window = np.asarray(values[-STATE_FIT_WINDOW:], float)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if model == "ARIMA":
            return ARIMA(window, order=specification, trend="t", enforce_stationarity=False, enforce_invertibility=False).fit(method_kwargs={"maxiter": 60})
        return SARIMAX(
            window, order=(1, 0, 0), seasonal_order=specification,
            trend="c", enforce_stationarity=False, enforce_invertibility=False,
        ).fit(disp=False, maxiter=20)


def select_state_specification(parts: Partitions, model: str):
    candidates = [(1, 1, 0), (2, 1, 0), (1, 1, 1)] if model == "ARIMA" else [(1, 0, 0, 48), (0, 1, 0, 48)]
    rows = []
    # A bounded validation tail preserves the frozen validation-only decision while
    # avoiding repeated filtering of all 18,480 points for each candidate.
    validation = parts.validation.iloc[-3360:]
    history = pd.concat([parts.development, parts.validation.iloc[:-3360]])
    for spec in candidates:
        fit = _fit_state_model(history.to_numpy(), model, spec)
        updated = fit.extend(validation.to_numpy())
        pred = np.asarray(updated.fittedvalues, float)
        rows.append({"Model": model, "Specification": repr(spec), "Validation_MASE_48": mase48(validation, pred)})
    table = pd.DataFrame(rows).sort_values(["Validation_MASE_48", "Specification"]).reset_index(drop=True)
    return eval(table.iloc[0].Specification), table


def state_model_forecasts(parts: Partitions, model: str, specification):
    fit = _fit_state_model(parts.pretest.to_numpy(), model, specification)
    # At each day boundary, forecast Protocol B before observing that day, then
    # extend the fixed-parameter state with the complete actual day.  The returned
    # fitted values are Protocol A sequential one-step forecasts.  Daily chunks
    # prevent statsmodels from retaining an impractical full seasonal smoother cube.
    current = fit
    blocks_a, blocks_b = [], []
    for start in range(0, len(parts.test), 48):
        actual_day = parts.test.iloc[start:start + 48].to_numpy(float)
        blocks_b.append(np.asarray(current.forecast(48), float))
        current = current.extend(actual_day)
        blocks_a.append(np.asarray(current.fittedvalues, float))
    return np.concatenate(blocks_a), np.concatenate(blocks_b)


def _fit_periodic(history: pd.Series, model: str):
    history = history.iloc[-FIT_WINDOW:]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if model == "Simple_Exponential_Smoothing":
            return SimpleExpSmoothing(history.to_numpy(), initialization_method="estimated").fit(optimized=True)
        if model == "Holt_Winters":
            # damped_trend is required here: an undamped additive trend extrapolated
            # over a multi-day cadence window (up to ~15 days ahead) diverges without
            # bound (validation MASE-48 in the hundreds) because nothing pulls the
            # linear trend component back toward the series' actual range.
            return ExponentialSmoothing(
                history.to_numpy(), trend="add", damped_trend=True, seasonal="add", seasonal_periods=48,
                initialization_method="estimated",
            ).fit(optimized=True, use_brute=False)
    frame = pd.DataFrame({"ds": history.index, "y": history.to_numpy(float)})
    return Prophet(
        daily_seasonality=True, weekly_seasonality=True, yearly_seasonality=False,
        seasonality_mode="additive", uncertainty_samples=0,
    ).fit(frame)


def _periodic_predict(fit, model: str, timestamps: pd.DatetimeIndex) -> np.ndarray:
    if model == "Prophet":
        return fit.predict(pd.DataFrame({"ds": timestamps}))["yhat"].to_numpy(float)
    return np.asarray(fit.forecast(len(timestamps)), float)


def periodic_forecasts(history: pd.Series, target: pd.Series, model: str, cadence: int):
    protocol_a = np.empty(len(target), float)
    protocol_b = np.empty(len(target), float)
    combined = pd.concat([history, target])
    for start in range(0, len(target), cadence):
        fit_history = combined.iloc[:len(history) + start]
        fit = _fit_periodic(fit_history, model)
        stop = min(start + cadence, len(target))
        horizon = min(cadence + 47, len(target) - start)
        future_index = target.index[start:start + horizon]
        path = _periodic_predict(fit, model, future_index)
        protocol_a[start:stop] = path[:stop - start]
        for day in range(start, stop, 48):
            length = min(48, len(target) - day)
            offset = day - start
            protocol_b[day:day + length] = path[offset:offset + length]
    return protocol_a, protocol_b


def select_periodic_cadence(parts: Partitions, model: str):
    rows = []
    validation = parts.validation.iloc[-4032:]
    history = pd.concat([parts.development, parts.validation.iloc[:-4032]])
    candidates = SES_PERIODIC_CADENCES if model == "Simple_Exponential_Smoothing" else PERIODIC_CADENCES
    for cadence in candidates:
        pred_a, _ = periodic_forecasts(history, validation, model, cadence)
        rows.append({"Model": model, "Cadence": cadence, "Validation_MASE_48": mase48(validation, pred_a)})
    table = pd.DataFrame(rows).sort_values(["Validation_MASE_48", "Cadence"]).reset_index(drop=True)
    return int(table.iloc[0].Cadence), table


def forecast_frames(test: pd.Series, protocol_a: np.ndarray, protocol_b: np.ndarray, column: str):
    pa = pd.DataFrame({"Timestamp": test.index, column: protocol_a})
    origins = np.repeat(test.index[::48].to_numpy(), 48)
    pb = pd.DataFrame({
        "Origin": origins,
        "Timestamp": test.index,
        "Horizon": np.tile(np.arange(1, 49), len(test) // 48),
        column: protocol_b,
    })
    return pa, pb
