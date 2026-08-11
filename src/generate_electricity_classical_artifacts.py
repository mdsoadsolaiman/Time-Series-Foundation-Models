"""Explicit generator for the five validated electricity classical comparators."""

from __future__ import annotations

from pathlib import Path
import json
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.electricity_classical_models import (
    SCALE_MASE_48, forecast_frames, load_electricity_partitions, mase48,
    periodic_forecasts, select_periodic_cadence, select_state_specification,
    state_model_forecasts, training_seasonality,
)


RESULTS = ROOT / "results/electricity"
MODELS = ["ARIMA", "SARIMA", "Prophet", "Simple_Exponential_Smoothing", "Holt_Winters"]


def validate_frame(pa, pb, test, column):
    assert pa.shape == (46176, 2) and pb.shape == (46176, 4)
    assert pa.Timestamp.equals(pd.Series(test.index, name="Timestamp"))
    assert pb.Timestamp.equals(pd.Series(test.index, name="Timestamp"))
    assert pb.Origin.nunique() == 962 and pb.groupby("Origin").size().eq(48).all()
    assert pb.groupby("Origin").Horizon.apply(lambda values: values.tolist() == list(range(1, 49))).all()
    assert np.isfinite(pa[column]).all() and np.isfinite(pb[column]).all()
    assert pa[column].nunique() > 100 and pb[column].nunique() > 100
    actual = test.to_numpy(float)
    for values in (pa[column].to_numpy(float), pb[column].to_numpy(float)):
        assert np.ptp(values) / np.ptp(actual) > 0.05
        assert np.std(values, ddof=1) / np.std(actual, ddof=1) > 0.05


def main():
    parts = load_electricity_partitions(ROOT)
    assert np.isclose(np.mean(np.abs(parts.pretest.to_numpy()[48:] - parts.pretest.to_numpy()[:-48])), SCALE_MASE_48, atol=1e-12)
    metadata = {"Training_Seasonality": training_seasonality(parts.development), "Models": {}}
    generated_a, generated_b = {}, {}

    for model in MODELS:
        print("SELECTING", model, flush=True)
        if model in {"ARIMA", "SARIMA"}:
            choice, selection = select_state_specification(parts, model)
            pred_a, pred_b = state_model_forecasts(parts, model, choice)
            metadata["Models"][model] = {
                "Update": "Sequential fixed-parameter statsmodels state update (extend; append-equivalent without history copy)",
                "Specification": repr(choice), "Selection": selection.to_dict("records"),
            }
        else:
            cadence, selection = select_periodic_cadence(parts, model)
            pred_a, pred_b = periodic_forecasts(parts.pretest, parts.test, model, cadence)
            metadata["Models"][model] = {
                "Update": "Validation-selected periodic refit",
                "Cadence_Half_Hours": cadence, "Cadence_Days": cadence / 48,
                "Selection": selection.to_dict("records"),
            }
        pa, pb = forecast_frames(parts.test, pred_a, pred_b, model)
        validate_frame(pa, pb, parts.test, model)
        pa.to_csv(RESULTS / f"protocol_a_{model.lower()}_forecast.csv", index=False, date_format="%Y-%m-%d %H:%M:%S")
        pb.to_csv(RESULTS / f"protocol_b_{model.lower()}_forecast.csv", index=False, date_format="%Y-%m-%d %H:%M:%S")
        generated_a[model], generated_b[model] = pa[model], pb[model]
        print(model, "A MASE", mase48(parts.test, pred_a), "B MASE", mase48(parts.test, pred_b), flush=True)

    existing_a = pd.read_csv(RESULTS / "protocol_a_validated_forecasts.csv", parse_dates=["Timestamp"])
    existing_b = pd.read_csv(RESULTS / "protocol_b_validated_forecasts.csv", parse_dates=["Origin", "Timestamp"])
    old_a, old_b = existing_a.copy(), existing_b.copy()
    final_order = [
        "Naive", "Daily_Seasonal_Naive", "Weekly_Seasonal_Naive", "Moving_Average",
        "ARIMA", "SARIMA", "Prophet", "Simple_Exponential_Smoothing", "Holt_Winters",
        "DHR_ARIMA", "LSTM", "Chronos_Bolt_Tiny", "TimesFM",
    ]
    for model in MODELS:
        existing_a[model] = generated_a[model].to_numpy()
        existing_b[model] = generated_b[model].to_numpy()
    existing_a = existing_a[["Timestamp", "Actual", *final_order]]
    existing_b = existing_b[["Origin", "Timestamp", "Horizon", "Actual", *final_order]]
    # Prove every vector NOT owned by this generator is byte-for-byte numerically
    # unchanged. Columns in MODELS are this script's own output, so on a rerun (e.g.
    # after fixing a bug in one of them) they are legitimately allowed to change; only
    # columns outside MODELS -- frozen elsewhere -- must reproduce exactly.
    protected = [c for c in old_a.columns if c not in MODELS]
    for column in protected:
        assert np.array_equal(old_a[column].to_numpy(), existing_a[column].to_numpy())
    protected_b = [c for c in old_b.columns if c not in MODELS]
    for column in protected_b:
        assert np.array_equal(old_b[column].to_numpy(), existing_b[column].to_numpy())
    existing_a.to_csv(RESULTS / "protocol_a_validated_forecasts.csv", index=False, date_format="%Y-%m-%d %H:%M:%S")
    existing_b.to_csv(RESULTS / "protocol_b_validated_forecasts.csv", index=False, date_format="%Y-%m-%d %H:%M:%S")
    (RESULTS / "classical_model_selection.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
