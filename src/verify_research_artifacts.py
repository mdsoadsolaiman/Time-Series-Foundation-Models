"""Lightweight, artifact-only verification of the frozen research evidence.

This script does not import or call any forecasting framework. It verifies byte
hashes, schemas, keys, row counts, and metrics reproducible from saved vectors.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "results" / "authoritative_artifact_hashes.md"
MODEL_NAMES = {
    "Persistence_Enhanced_LSTM": "Persistence-Enhanced LSTM",
    "Chronos_Bolt_Tiny": "Chronos-Bolt-Tiny",
    "Daily_Seasonal_Naive": "Daily Seasonal Naive",
    "Weekly_Seasonal_Naive": "Weekly Seasonal Naive",
    "Moving_Average": "Moving Average",
    "DHR_ARIMA": "DHR-ARIMA",
    "ARIMA_Rolling": "ARIMA Rolling One-Step",
    "Prophet_Periodic_Refit": "Prophet 30-Day Periodic Refit",
}
BITCOIN_METRICS = {
    "Naive": (1290.3532422243168, 1853.6247736716243, 1.742746521465369, 1.7441417265023809),
    "Persistence-Enhanced LSTM": (1321.3653105878764, 1881.0911899658583, 1.7839563296496557, 1.7916454886549884),
    "Chronos-Bolt-Tiny": (1424.0258275653864, 1994.0079263996643, 1.934509000360176, 1.928782487065369),
    "TimesFM": (1349.9467856090953, 1924.1993369259183, 1.8231794164362922, 1.823894758464343),
    "ARIMA Rolling One-Step": (1299.8746375937496, 1866.3028590728163, 1.754003843176303, 1.7542088564346432),
    "Prophet 30-Day Periodic Refit": (8195.262861996911, 10781.162873031499, 11.199767058617569, 11.287185079510287),
}


class Verification:
    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0

    def check(self, condition: bool, label: str) -> None:
        if condition:
            self.passed += 1
            print(f"PASS  {label}")
        else:
            self.failed += 1
            print(f"FAIL  {label}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def metrics(actual: pd.Series, predicted: pd.Series) -> dict[str, float]:
    a = actual.to_numpy(float)
    p = predicted.to_numpy(float)
    error = a - p
    return {
        "MAE": float(np.mean(np.abs(error))),
        "RMSE": float(np.sqrt(np.mean(error**2))),
        "MAPE": float(100 * np.mean(np.abs(error) / np.abs(a))),
        "sMAPE": float(100 * np.mean(2 * np.abs(error) / (np.abs(a) + np.abs(p)))),
    }


def verify_hashes(v: Verification) -> None:
    text = LEDGER.read_text(encoding="utf-8")
    entries = re.findall(r"\| `(?P<path>results/[^`]+)` \| `(?P<hash>[A-F0-9]{64})` \|", text)
    v.check(len(entries) == 33, "ledger contains 33 protected artifacts")
    for relative, expected in entries:
        path = ROOT / relative
        v.check(path.is_file(), f"exists: {relative}")
        if path.is_file():
            v.check(sha256(path) == expected, f"SHA-256: {relative}")


def verify_forecast(path: Path, expected_rows: int, expected_columns: list[str],
                    protocol: str, comparison: pd.DataFrame, v: Verification) -> None:
    frame = pd.read_csv(path)
    relative = path.relative_to(ROOT).as_posix()
    v.check(len(frame) == expected_rows, f"row count: {relative}")
    v.check(frame.columns.tolist() == expected_columns, f"schema: {relative}")
    v.check(not frame.isna().any().any(), f"no missing values: {relative}")
    v.check(np.isfinite(frame.select_dtypes(include=[np.number])).all().all(), f"finite numerics: {relative}")
    v.check(frame["Timestamp"].is_unique, f"unique timestamps: {relative}")
    v.check(pd.to_datetime(frame["Timestamp"]).is_monotonic_increasing, f"sorted timestamps: {relative}")
    if "Origin" in frame:
        v.check(not frame.duplicated(["Origin", "Horizon"]).any(), f"unique origin/horizon keys: {relative}")
        v.check(frame.groupby("Origin")["Horizon"].count().eq(48).all(), f"48 horizons per origin: {relative}")
        v.check(frame["Origin"].nunique() == 962, f"962 day-ahead origins: {relative}")
    expected = comparison[comparison["Protocol"].eq(protocol)].set_index("Model")
    for column in expected_columns:
        if column in {"Timestamp", "Origin", "Horizon", "Actual"}:
            continue
        label = MODEL_NAMES.get(column, column)
        if label not in expected.index:
            continue
        observed = metrics(frame["Actual"], frame[column])
        for metric, value in observed.items():
            target = float(expected.loc[label, metric])
            v.check(np.isclose(value, target, rtol=1e-10, atol=1e-10), f"{protocol}: {label} {metric}")


def verify_point_vector(path: Path, model_column: str, expected_timestamps: pd.Series,
                        v: Verification) -> None:
    """Verify a standalone 1,061-row Bitcoin point-forecast artifact."""
    frame = pd.read_csv(path)
    relative = path.relative_to(ROOT).as_posix()
    v.check(frame.shape == (1061, 2), f"shape: {relative}")
    v.check(frame.columns.tolist() == ["Timestamp", model_column], f"schema: {relative}")
    v.check(frame["Timestamp"].equals(expected_timestamps), f"aligned timestamps: {relative}")
    v.check(frame["Timestamp"].is_unique, f"unique timestamps: {relative}")
    v.check(not frame.isna().any().any(), f"no missing values: {relative}")
    v.check(np.isfinite(frame[model_column]).all(), f"finite forecasts: {relative}")


def verify_arima_validation(v: Verification) -> None:
    """Verify the training-only ARIMA vector used to construct empirical intervals."""
    path = ROOT / "results" / "arima_validation_forecast.csv"
    frame = pd.read_csv(path)
    timestamps = pd.to_datetime(frame["Timestamp"], utc=True)
    v.check(frame.shape == (1061, 2), "shape: results/arima_validation_forecast.csv")
    v.check(frame.columns.tolist() == ["Timestamp", "ARIMA_Rolling_Validation"],
            "schema: results/arima_validation_forecast.csv")
    v.check(timestamps.is_unique and timestamps.is_monotonic_increasing,
            "ordered unique timestamps: results/arima_validation_forecast.csv")
    v.check(timestamps.max() == pd.Timestamp("2023-08-11", tz="UTC"),
            "ends before Bitcoin test: results/arima_validation_forecast.csv")
    v.check(np.isfinite(frame["ARIMA_Rolling_Validation"]).all(),
            "finite forecasts: results/arima_validation_forecast.csv")


def main() -> int:
    v = Verification()
    verify_hashes(v)
    comparison = pd.read_csv(ROOT / "results" / "cross_domain_model_comparison.csv")
    bitcoin_comparison = pd.DataFrame(
        [
            {"Model": model, "Protocol": "Rolling one-step daily", "MAE": values[0],
             "RMSE": values[1], "MAPE": values[2], "sMAPE": values[3]}
            for model, values in BITCOIN_METRICS.items()
        ]
    )
    comparison = pd.concat(
        [comparison.loc[~comparison["Protocol"].eq("Rolling one-step daily")], bitcoin_comparison],
        ignore_index=True,
    )
    verify_forecast(
        ROOT / "results" / "validated_forecasts.csv", 1061,
        ["Timestamp", "Actual", "Naive", "Persistence_Enhanced_LSTM", "Chronos_Bolt_Tiny", "TimesFM", "ARIMA_Rolling", "Prophet_Periodic_Refit"],
        "Rolling one-step daily", comparison, v,
    )
    validated = pd.read_csv(ROOT / "results" / "validated_forecasts.csv")
    verify_point_vector(ROOT / "results" / "arima_rolling_forecast.csv", "ARIMA_Rolling", validated["Timestamp"], v)
    verify_point_vector(ROOT / "results" / "prophet_rolling_forecast.csv", "Prophet_Periodic_Refit", validated["Timestamp"], v)
    verify_arima_validation(v)
    verify_forecast(
        ROOT / "results" / "electricity" / "protocol_a_validated_forecasts.csv", 46176,
        ["Timestamp", "Actual", "Naive", "Daily_Seasonal_Naive", "Weekly_Seasonal_Naive", "Moving_Average", "DHR_ARIMA", "LSTM", "Chronos_Bolt_Tiny", "TimesFM"],
        "Protocol A: rolling one-step 30-minute", comparison, v,
    )
    verify_forecast(
        ROOT / "results" / "electricity" / "protocol_b_validated_forecasts.csv", 46176,
        ["Origin", "Timestamp", "Horizon", "Actual", "Naive", "Daily_Seasonal_Naive", "Weekly_Seasonal_Naive", "Moving_Average", "DHR_ARIMA", "LSTM", "Chronos_Bolt_Tiny", "TimesFM"],
        "Protocol B: 48-step day-ahead", comparison, v,
    )
    for name in ["cross_domain_foundation_model_comparison.csv", "cross_domain_uncertainty_comparison.csv", "cross_domain_significance_summary.csv"]:
        frame = pd.read_csv(ROOT / "results" / name)
        v.check(len(frame) > 0 and len(frame.columns) > 1, f"loads successfully: results/{name}")
    print(f"\nSUMMARY: {v.passed} PASS, {v.failed} FAIL")
    return 1 if v.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
