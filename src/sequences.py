"""Shared sequence construction for Bitcoin supervised forecasting notebooks."""

from __future__ import annotations

import numpy as np


def create_sequences(values, lookback: int) -> tuple[np.ndarray, np.ndarray]:
    """Create the legacy sliding input/next-value arrays without changing dtype."""
    x_values, y_values = [], []
    for position in range(lookback, len(values)):
        x_values.append(values[position - lookback : position])
        y_values.append(values[position])
    return np.asarray(x_values), np.asarray(y_values)


def create_indexed_sequences(values, index, lookback: int):
    """Create sliding arrays plus the timestamp associated with each target value."""
    x_values, y_values, timestamps = [], [], []
    for position in range(lookback, len(values)):
        x_values.append(values[position - lookback : position])
        y_values.append(values[position])
        timestamps.append(index[position])
    return np.asarray(x_values), np.asarray(y_values), np.asarray(timestamps)
