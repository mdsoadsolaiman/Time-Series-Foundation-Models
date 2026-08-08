"""Training-only conformal calibration for Bitcoin foundation-model intervals."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.data_loader import load_bitcoin_data
from src.preprocessing import prepare_daily_bitcoin_data


CONTEXT_LENGTH = 128
CALIBRATION_LENGTH = 180
NOMINAL_COVERAGE = 0.80


def rolling_contexts(target: pd.Series, forecast_index: pd.DatetimeIndex) -> list[np.ndarray]:
    """Return strict 128-observation contexts ending before each forecast timestamp."""
    contexts = []
    for timestamp in forecast_index:
        context = target.loc[target.index < timestamp].tail(CONTEXT_LENGTH)
        if len(context) != CONTEXT_LENGTH or context.index.max() >= timestamp:
            raise ValueError(f"Invalid context for {timestamp}")
        contexts.append(context.to_numpy(dtype=np.float32))
    return contexts


def conformal_adjustment(
    actual: np.ndarray,
    lower: np.ndarray,
    upper: np.ndarray,
    coverage: float = NOMINAL_COVERAGE,
) -> float:
    """Return the finite-sample CQR adjustment from calibration observations only."""
    scores = np.maximum(lower - actual, actual - upper)
    probability = min(1.0, np.ceil((len(scores) + 1) * coverage) / len(scores))
    return float(np.quantile(scores, probability, method="higher"))


def _chronos_intervals(contexts: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    import torch
    from chronos import BaseChronosPipeline

    pipeline = BaseChronosPipeline.from_pretrained(
        "amazon/chronos-bolt-tiny", device_map="cpu", torch_dtype=torch.float32
    )
    tensor = torch.tensor(np.stack(contexts), dtype=torch.float32)
    batches = []
    for start in range(0, len(tensor), 32):
        quantiles, _ = pipeline.predict_quantiles(
            tensor[start : start + 32], prediction_length=1, quantile_levels=[0.1, 0.9]
        )
        batches.append(quantiles.detach().cpu())
    values = torch.cat(batches, dim=0).numpy()[:, 0, :]
    return values[:, 0].astype(float), values[:, 1].astype(float)


def _timesfm_intervals(contexts: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    import timesfm

    model = timesfm.TimesFM_2p5_200M_torch.from_pretrained(
        "google/timesfm-2.5-200m-pytorch", torch_compile=False
    )
    model.compile(
        timesfm.ForecastConfig(
            max_context=CONTEXT_LENGTH,
            max_horizon=1,
            normalize_inputs=True,
            per_core_batch_size=32,
        )
    )
    _, quantiles = model.forecast(horizon=1, inputs=contexts)
    values = np.asarray(quantiles, dtype=float)
    levels = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    return values[:, 0, levels.index(0.1)], values[:, 0, levels.index(0.9)]


def generate_calibration_artifact(project_root: Path) -> pd.DataFrame:
    """Generate native and CQR-calibrated 80% test intervals for Chronos and TimesFM."""
    raw = load_bitcoin_data(project_root / "data" / "bitcoin" / "btcusd_1-min_data.csv")
    target = prepare_daily_bitcoin_data(raw)["Close"].dropna().astype(float)
    split = int(len(target) * 0.8)
    train, test = target.iloc[:split], target.iloc[split:]
    calibration = train.tail(CALIBRATION_LENGTH)
    combined_index = calibration.index.append(test.index)
    contexts = rolling_contexts(target, combined_index)

    frame = pd.DataFrame({"Timestamp": test.index, "Actual": test.to_numpy(dtype=float)})
    summary_rows = []
    for model_name, predictor in (
        ("Chronos_Bolt_Tiny", _chronos_intervals),
        ("TimesFM", _timesfm_intervals),
    ):
        lower, upper = predictor(contexts)
        calibration_lower, test_lower = lower[:CALIBRATION_LENGTH], lower[CALIBRATION_LENGTH:]
        calibration_upper, test_upper = upper[:CALIBRATION_LENGTH], upper[CALIBRATION_LENGTH:]
        adjustment = conformal_adjustment(
            calibration.to_numpy(dtype=float), calibration_lower, calibration_upper
        )
        calibrated_lower = test_lower - adjustment
        calibrated_upper = test_upper + adjustment
        frame[f"{model_name}_Native_Lower_80"] = test_lower
        frame[f"{model_name}_Native_Upper_80"] = test_upper
        frame[f"{model_name}_Calibrated_Lower_80"] = calibrated_lower
        frame[f"{model_name}_Calibrated_Upper_80"] = calibrated_upper
        summary_rows.append(
            {
                "Model": model_name,
                "Calibration_Rows": CALIBRATION_LENGTH,
                "Calibration_Start": calibration.index.min(),
                "Calibration_End": calibration.index.max(),
                "Conformal_Adjustment": adjustment,
                "Native_Test_Coverage_80": np.mean((test >= test_lower) & (test <= test_upper)),
                "Calibrated_Test_Coverage_80": np.mean(
                    (test >= calibrated_lower) & (test <= calibrated_upper)
                ),
                "Native_Average_Width_80": np.mean(test_upper - test_lower),
                "Calibrated_Average_Width_80": np.mean(calibrated_upper - calibrated_lower),
            }
        )

    if frame.shape != (1061, 10) or frame["Timestamp"].duplicated().any():
        raise ValueError(f"Invalid calibration artifact shape or timestamps: {frame.shape}")
    numeric = frame.drop(columns="Timestamp").to_numpy(dtype=float)
    if not np.isfinite(numeric).all():
        raise ValueError("Calibration artifact contains non-finite values")
    results = project_root / "results"
    frame.to_csv(results / "foundation_uncertainty_calibration.csv", index=False)
    pd.DataFrame(summary_rows).to_csv(results / "foundation_uncertainty_summary.csv", index=False)
    return frame


if __name__ == "__main__":
    output = generate_calibration_artifact(Path(__file__).resolve().parents[1])
    print(f"Saved calibrated uncertainty artifact with shape {output.shape}")
