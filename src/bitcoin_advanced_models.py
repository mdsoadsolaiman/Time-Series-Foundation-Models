"""Advanced Bitcoin forecasts using explicitly audited information protocols."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing, SimpleExpSmoothing


def rolling_arima_log_return_forecast(
    target: pd.Series,
    test_index: pd.DatetimeIndex,
    context_length: int = 128,
    order: tuple[int, int, int] = (1, 0, 1),
) -> pd.Series:
    """Forecast each test-day return and append only its subsequently observed return."""
    log_returns = np.log(target / target.shift(1)).dropna()
    train_returns = log_returns.loc[log_returns.index < test_index[0]].tail(context_length)
    fitted = ARIMA(train_returns, order=order, trend="c").fit()
    predictions = []
    for timestamp in test_index:
        predicted_return = float(fitted.forecast(1).iloc[0])
        previous_actual = float(target.loc[:timestamp].iloc[-2])
        predictions.append(previous_actual * np.exp(predicted_return))
        observed_return = pd.Series(
            [float(log_returns.loc[timestamp])],
            index=pd.DatetimeIndex([timestamp]),
            name=train_returns.name,
        )
        fitted = fitted.append(observed_return, refit=False)
    return pd.Series(predictions, index=test_index, name="ARIMA_Rolling")


def rolling_simple_exp_smoothing_forecast(
    target: pd.Series,
    test_index: pd.DatetimeIndex,
    context_length: int = 128,
) -> pd.Series:
    """Refit SES on the latest strictly-prior context for every forecast day."""
    predictions = []
    for timestamp in test_index:
        history = target.loc[target.index < timestamp].tail(context_length)
        if len(history) != context_length:
            raise ValueError(f"Insufficient SES context before {timestamp}")
        if not timestamp > history.index.max():
            raise ValueError("SES forecast date must follow the context window")
        fitted = SimpleExpSmoothing(
            history.astype(float), initialization_method="estimated"
        ).fit(optimized=True)
        predictions.append(float(fitted.forecast(1).iloc[0]))
    return pd.Series(predictions, index=test_index, name="Simple_Exp_Smoothing")


def rolling_holt_winters_forecast(
    target: pd.Series,
    test_index: pd.DatetimeIndex,
    context_length: int = 128,
) -> pd.Series:
    """Refit additive-trend, non-seasonal Holt-Winters for every forecast day."""
    predictions = []
    for timestamp in test_index:
        history = target.loc[target.index < timestamp].tail(context_length)
        if len(history) != context_length:
            raise ValueError(f"Insufficient Holt-Winters context before {timestamp}")
        if not timestamp > history.index.max():
            raise ValueError("Holt-Winters forecast date must follow the context window")
        fitted = ExponentialSmoothing(
            history.astype(float),
            trend="add",
            seasonal=None,
            initialization_method="estimated",
        ).fit(optimized=True)
        predictions.append(float(fitted.forecast(1).iloc[0]))
    return pd.Series(predictions, index=test_index, name="Holt_Winters")


def periodic_refit_prophet_forecast(
    target: pd.Series,
    test_index: pd.DatetimeIndex,
    context_length: int = 128,
    refit_every: int = 30,
) -> pd.Series:
    """Forecast with Prophet refitted every ``refit_every`` days using strict past data."""
    predictions = []
    model = None
    for position, timestamp in enumerate(test_index):
        if model is None or position % refit_every == 0:
            history = target.loc[target.index < timestamp].tail(context_length)
            frame = pd.DataFrame(
                {
                    "ds": history.index.tz_convert(None),
                    "y": history.to_numpy(dtype=float),
                }
            )
            model = Prophet(
                daily_seasonality=False,
                weekly_seasonality=False,
                yearly_seasonality=False,
                seasonality_mode="additive",
                uncertainty_samples=0,
            )
            model.fit(frame)
        future = pd.DataFrame({"ds": [timestamp.tz_convert(None)]})
        predictions.append(float(model.predict(future)["yhat"].iloc[0]))
    return pd.Series(predictions, index=test_index, name="Prophet_Periodic_Refit")


def validate_and_save_forecast(
    forecast: pd.Series,
    test_index: pd.DatetimeIndex,
    path: Path,
) -> pd.DataFrame:
    """Validate a forecast vector and save its timestamp/model columns."""
    if len(forecast) != 1061:
        raise ValueError(f"Expected 1061 forecasts, received {len(forecast)}")
    if not forecast.index.equals(test_index):
        raise ValueError("Forecast index does not exactly match the test index")
    if forecast.index.duplicated().any():
        raise ValueError("Forecast contains duplicate timestamps")
    values = forecast.to_numpy(dtype=float)
    if np.isnan(values).any() or not np.isfinite(values).all():
        raise ValueError("Forecast contains missing or non-finite values")
    frame = pd.DataFrame({"Timestamp": forecast.index, forecast.name: values})
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    return frame


def merge_advanced_forecasts(
    validated_path: Path,
    forecast_frames: list[pd.DataFrame],
) -> pd.DataFrame:
    """Merge validated advanced forecast vectors into the frozen comparison frame."""
    validated = pd.read_csv(validated_path, parse_dates=["Timestamp"])
    new_columns = [frame.columns[1] for frame in forecast_frames]
    validated = validated.drop(columns=new_columns, errors="ignore")
    for frame in forecast_frames:
        validated = validated.merge(frame, on="Timestamp", how="inner", validate="one_to_one")
    if validated.shape[0] != 1061 or validated["Timestamp"].duplicated().any():
        raise ValueError("Merged validated artifact has invalid row keys")
    numeric = validated.select_dtypes(include=[np.number]).to_numpy()
    if np.isnan(numeric).any() or not np.isfinite(numeric).all():
        raise ValueError("Merged validated artifact contains invalid numeric values")
    if np.array_equal(
        validated[new_columns[0]].to_numpy(),
        validated[new_columns[1]].to_numpy(),
    ):
        raise ValueError("Advanced model forecast vectors are duplicated")
    validated.to_csv(validated_path, index=False)
    return validated


def generate_arima_validation_artifact(project_root: Path) -> pd.DataFrame:
    """Save ARIMA forecasts for the final 1,061 training days without using test data."""
    from src.data_loader import load_bitcoin_data
    from src.preprocessing import prepare_daily_bitcoin_data

    raw = load_bitcoin_data(project_root / "data" / "bitcoin" / "btcusd_1-min_data.csv")
    target = prepare_daily_bitcoin_data(raw)["Close"].dropna().astype(float)
    split = int(len(target) * 0.8)
    train = target.iloc[:split]
    validation_index = train.tail(1061).index
    forecast = rolling_arima_log_return_forecast(target, validation_index).rename(
        "ARIMA_Rolling_Validation"
    )
    output = validate_and_save_forecast(
        forecast,
        validation_index,
        project_root / "results" / "arima_validation_forecast.csv",
    )
    if output["Timestamp"].max() >= target.iloc[split:].index.min():
        raise ValueError("ARIMA validation artifact overlaps the test period")
    return output


def generate_exponential_smoothing_validation_artifacts(
    project_root: Path,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Save strictly pre-test validation vectors for empirical uncertainty scoring."""
    from src.data_loader import load_bitcoin_data
    from src.preprocessing import prepare_daily_bitcoin_data

    raw = load_bitcoin_data(project_root / "data" / "bitcoin" / "btcusd_1-min_data.csv")
    target = prepare_daily_bitcoin_data(raw)["Close"].dropna().astype(float)
    split = int(len(target) * 0.8)
    validation_index = target.iloc[:split].tail(1061).index
    ses = rolling_simple_exp_smoothing_forecast(target, validation_index).rename(
        "Simple_Exp_Smoothing_Validation"
    )
    holt = rolling_holt_winters_forecast(target, validation_index).rename(
        "Holt_Winters_Validation"
    )
    ses_frame = validate_and_save_forecast(
        ses,
        validation_index,
        project_root / "results" / "simple_exp_smoothing_validation_forecast.csv",
    )
    holt_frame = validate_and_save_forecast(
        holt,
        validation_index,
        project_root / "results" / "holt_winters_validation_forecast.csv",
    )
    if max(ses_frame["Timestamp"].max(), holt_frame["Timestamp"].max()) >= target.iloc[split:].index.min():
        raise ValueError("Exponential-smoothing validation artifacts overlap the test period")
    return ses_frame, holt_frame
