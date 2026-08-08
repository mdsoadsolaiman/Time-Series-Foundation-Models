"""Forecast evaluation metrics."""

import numpy as np


def _as_arrays(y_true, y_pred):
    """Convert metric inputs to aligned NumPy arrays."""
    true = np.asarray(y_true, dtype=float)
    pred = np.asarray(y_pred, dtype=float)

    if true.shape != pred.shape:
        raise ValueError("y_true and y_pred must have the same shape.")

    mask = ~(np.isnan(true) | np.isnan(pred))
    return true[mask], pred[mask]


def mae(y_true, y_pred):
    """Calculate mean absolute error."""
    true, pred = _as_arrays(y_true, y_pred)
    return np.mean(np.abs(true - pred))


def rmse(y_true, y_pred):
    """Calculate root mean squared error."""
    true, pred = _as_arrays(y_true, y_pred)
    return np.sqrt(np.mean((true - pred) ** 2))


def mape(y_true, y_pred):
    """Calculate mean absolute percentage error as a percentage."""
    true, pred = _as_arrays(y_true, y_pred)
    nonzero = true != 0
    return np.mean(np.abs((true[nonzero] - pred[nonzero]) / true[nonzero])) * 100


def smape(y_true, y_pred):
    """Calculate symmetric mean absolute percentage error as a percentage."""
    true, pred = _as_arrays(y_true, y_pred)
    denominator = np.abs(true) + np.abs(pred)
    nonzero = denominator != 0
    return np.mean(2 * np.abs(pred[nonzero] - true[nonzero]) / denominator[nonzero]) * 100


def mase(y_true, y_pred, y_train, seasonal_period=1):
    """Calculate mean absolute scaled error from a training-only scale.

    The scale is the mean absolute seasonal difference in ``y_train``.
    Evaluation targets are never used to estimate the denominator.
    """
    true, pred = _as_arrays(y_true, y_pred)
    train = np.asarray(y_train, dtype=float).reshape(-1)

    if not isinstance(seasonal_period, (int, np.integer)) or seasonal_period < 1:
        raise ValueError("seasonal_period must be a positive integer.")
    if train.size <= seasonal_period:
        raise ValueError("y_train must contain more values than seasonal_period.")
    if not np.all(np.isfinite(train)):
        raise ValueError("y_train must contain only finite values.")

    scale = np.mean(np.abs(train[seasonal_period:] - train[:-seasonal_period]))
    if not np.isfinite(scale) or scale == 0:
        raise ValueError("MASE scaling denominator must be finite and non-zero.")

    return np.mean(np.abs(true - pred)) / scale


def forecast_metric_row(y_true, y_pred):
    """Return the four-metric dictionary duplicated across Bitcoin notebooks."""
    return {
        "MAE": mae(y_true, y_pred),
        "RMSE": rmse(y_true, y_pred),
        "MAPE": mape(y_true, y_pred),
        "sMAPE": smape(y_true, y_pred),
    }
