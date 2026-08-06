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
    v.check(len(entries) == 25, "ledger contains 25 protected artifacts")
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
        observed = metrics(frame["Actual"], frame[column])
        for metric, value in observed.items():
            target = float(expected.loc[label, metric])
            v.check(np.isclose(value, target, rtol=1e-10, atol=1e-10), f"{protocol}: {label} {metric}")


def main() -> int:
    v = Verification()
    verify_hashes(v)
    comparison = pd.read_csv(ROOT / "results" / "cross_domain_model_comparison.csv")
    verify_forecast(
        ROOT / "results" / "validated_forecasts.csv", 1061,
        ["Timestamp", "Actual", "Naive", "Persistence_Enhanced_LSTM", "Chronos_Bolt_Tiny", "TimesFM"],
        "Rolling one-step daily", comparison, v,
    )
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
