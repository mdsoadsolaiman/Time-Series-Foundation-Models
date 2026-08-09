"""Byte-equivalence tests for helpers extracted from Bitcoin notebooks."""

import unittest

import numpy as np
import pandas as pd

from src.metrics import forecast_metric_row, mae, mape, rmse, smape
from src.sequences import create_indexed_sequences, create_sequences


class SequenceEquivalenceTests(unittest.TestCase):
    def test_plain_sequences_are_byte_identical_to_legacy_loop(self):
        values = np.arange(24, dtype=np.float32).reshape(-1, 1)
        legacy_x, legacy_y = [], []
        for position in range(5, len(values)):
            legacy_x.append(values[position - 5 : position])
            legacy_y.append(values[position])
        expected_x, expected_y = np.asarray(legacy_x), np.asarray(legacy_y)
        actual_x, actual_y = create_sequences(values, 5)
        self.assertEqual(actual_x.tobytes(), expected_x.tobytes())
        self.assertEqual(actual_y.tobytes(), expected_y.tobytes())
        self.assertEqual(actual_x.dtype, expected_x.dtype)
        self.assertEqual(actual_y.dtype, expected_y.dtype)

    def test_indexed_sequences_are_byte_identical_to_legacy_loop(self):
        values = np.linspace(1, 12, 12, dtype=np.float64).reshape(-1, 1)
        index = pd.date_range("2024-01-01", periods=12, tz="UTC")
        legacy_x, legacy_y, legacy_index = [], [], []
        for position in range(4, len(values)):
            legacy_x.append(values[position - 4 : position])
            legacy_y.append(values[position])
            legacy_index.append(index[position])
        actual_x, actual_y, actual_index = create_indexed_sequences(values, index, 4)
        self.assertEqual(actual_x.tobytes(), np.asarray(legacy_x).tobytes())
        self.assertEqual(actual_y.tobytes(), np.asarray(legacy_y).tobytes())
        np.testing.assert_array_equal(actual_index, np.asarray(legacy_index))


class MetricEquivalenceTests(unittest.TestCase):
    def test_metric_row_exactly_matches_legacy_dictionary(self):
        actual = np.array([1.0, 2.0, 4.0, 8.0])
        predicted = np.array([1.1, 1.8, 4.2, 7.5])
        legacy = {
            "MAE": mae(actual, predicted),
            "RMSE": rmse(actual, predicted),
            "MAPE": mape(actual, predicted),
            "sMAPE": smape(actual, predicted),
        }
        refactored = forecast_metric_row(actual, predicted)
        self.assertEqual(refactored.keys(), legacy.keys())
        for name in legacy:
            self.assertEqual(refactored[name], legacy[name])


if __name__ == "__main__":
    unittest.main()
