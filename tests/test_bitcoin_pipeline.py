from pathlib import Path

import numpy as np
import pandas as pd

from src.bitcoin_pipeline import hac_dm, holm_adjust, load_validated_forecasts, seven_day_moving_average


ROOT = Path(__file__).resolve().parents[1]


def test_validated_forecast_schema():
    frame = load_validated_forecasts(ROOT)
    assert frame.shape == (1061, 10)
    assert frame.index.is_unique


def test_moving_average_uses_strict_history():
    frame = load_validated_forecasts(ROOT)
    target = pd.concat([frame["Naive"].iloc[:1], frame["Actual"]])
    target.index = pd.date_range(frame.index[0] - pd.Timedelta(days=1), periods=len(target), tz="UTC")
    forecast = seven_day_moving_average(target, frame.index[6:])
    assert np.isclose(forecast.iloc[0], target.iloc[:7].mean())


def test_holm_is_monotone_in_sorted_order():
    raw = pd.Series([0.04, 0.001, 0.02])
    adjusted = holm_adjust(raw)
    order = np.argsort(raw.to_numpy())
    assert np.all(np.diff(adjusted.to_numpy()[order]) >= 0)


def test_hac_dm_identity_is_zero_or_undefined():
    actual = pd.Series([1.0, 2.0, 3.0, 4.0])
    forecast = pd.Series([1.1, 1.9, 3.2, 3.8])
    result = hac_dm(actual, forecast, forecast, max_lag=1)
    assert np.isnan(result["DM statistic"])
