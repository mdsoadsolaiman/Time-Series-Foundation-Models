"""Deterministic Bitcoin Transformer experiments under past-only protocols.

The authoritative candidate predicts scaled log returns from 128 strictly prior
daily returns and reconstructs price from the previous observed close.  The
module deliberately avoids importing TensorFlow until deterministic environment
controls are set.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras import Model
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import (
    Dense,
    Dropout,
    Embedding,
    GlobalAveragePooling1D,
    Input,
    Layer,
    LayerNormalization,
    MultiHeadAttention,
)

from src.data_loader import load_bitcoin_data
from src.preprocessing import prepare_daily_bitcoin_data


SEED = 42
LOOKBACK = 128
MODEL_COLUMN = "Persistence_Enhanced_Transformer"


def configure_determinism() -> None:
    """Apply the project's audited single-thread deterministic TensorFlow setup."""
    tf.config.threading.set_intra_op_parallelism_threads(1)
    tf.config.threading.set_inter_op_parallelism_threads(1)
    tf.keras.utils.set_random_seed(SEED)
    tf.config.experimental.enable_op_determinism()


class PositionalEmbedding(Layer):
    def __init__(self, lookback: int, d_model: int, **kwargs):
        super().__init__(**kwargs)
        self.lookback = lookback
        self.d_model = d_model
        self.embedding = Embedding(
            input_dim=lookback,
            output_dim=d_model,
            embeddings_initializer=tf.keras.initializers.RandomUniform(seed=SEED),
        )

    def call(self, inputs):
        positions = tf.range(start=0, limit=self.lookback, delta=1)
        return inputs + tf.expand_dims(self.embedding(positions), axis=0)

    def get_config(self):
        config = super().get_config()
        config.update({"lookback": self.lookback, "d_model": self.d_model})
        return config


def build_transformer(
    lookback: int = LOOKBACK,
    d_model: int = 64,
    num_heads: int = 4,
    ff_dim: int = 128,
    dropout: float = 0.1,
    use_positional_embedding: bool = False,
) -> Model:
    """Build the corrected encoder with projection before normalization."""
    tf.keras.utils.set_random_seed(SEED)
    inputs = Input(shape=(lookback, 1), name="return_window")
    x = Dense(
        d_model,
        name="input_projection",
        kernel_initializer=tf.keras.initializers.GlorotUniform(seed=SEED),
    )(inputs)
    if use_positional_embedding:
        x = PositionalEmbedding(lookback, d_model, name="positional_embedding")(x)
    attention = MultiHeadAttention(
        key_dim=d_model // num_heads,
        num_heads=num_heads,
        dropout=dropout,
        kernel_initializer=tf.keras.initializers.GlorotUniform(seed=SEED),
        name="self_attention",
    )(x, x)
    attention = Dropout(dropout, seed=SEED, name="attention_dropout")(attention)
    x = LayerNormalization(epsilon=1e-6, name="attention_norm")(x + attention)
    feed_forward = Dense(
        ff_dim,
        activation="relu",
        name="ffn_expand",
        kernel_initializer=tf.keras.initializers.GlorotUniform(seed=SEED),
    )(x)
    feed_forward = Dropout(dropout, seed=SEED, name="ffn_dropout")(feed_forward)
    feed_forward = Dense(
        d_model,
        name="ffn_project",
        kernel_initializer=tf.keras.initializers.GlorotUniform(seed=SEED),
    )(feed_forward)
    x = LayerNormalization(epsilon=1e-6, name="ffn_norm")(x + feed_forward)
    x = GlobalAveragePooling1D(name="temporal_pooling")(x)
    x = Dropout(dropout, seed=SEED, name="prediction_dropout")(x)
    x = Dense(
        32,
        activation="relu",
        name="prediction_hidden",
        kernel_initializer=tf.keras.initializers.GlorotUniform(seed=SEED),
    )(x)
    outputs = Dense(
        1,
        name="return_prediction",
        kernel_initializer=tf.keras.initializers.GlorotUniform(seed=SEED),
    )(x)
    model = Model(inputs, outputs, name="PersistenceEnhancedTransformer")
    model.compile(optimizer="adam", loss="mse")
    return model


def create_sequences(values: np.ndarray, lookback: int) -> tuple[np.ndarray, np.ndarray]:
    x = np.asarray([values[i - lookback : i] for i in range(lookback, len(values))])
    y = np.asarray([values[i] for i in range(lookback, len(values))])
    return x, y


def load_target(root: Path) -> pd.Series:
    raw = load_bitcoin_data(root / "data" / "bitcoin" / "btcusd_1-min_data.csv")
    daily = prepare_daily_bitcoin_data(raw)
    return daily["Close"].dropna().asfreq("D").astype(float)


def metrics(actual: pd.Series, forecast: pd.Series) -> dict[str, float]:
    error = actual.to_numpy(float) - forecast.to_numpy(float)
    actual_values = actual.to_numpy(float)
    forecast_values = forecast.to_numpy(float)
    return {
        "MAE": float(np.mean(np.abs(error))),
        "RMSE": float(np.sqrt(np.mean(error**2))),
        "MAPE": float(100 * np.mean(np.abs(error / actual_values))),
        "sMAPE": float(100 * np.mean(2 * np.abs(error) / (np.abs(actual_values) + np.abs(forecast_values)))),
    }


def generate_pe_transformer_forecast(
    root: Path,
    *,
    use_positional_embedding: bool = False,
    verbose: int = 0,
) -> tuple[pd.Series, dict[str, list[float]], dict[str, float]]:
    """Train once on training returns and forecast all test dates past-only."""
    configure_determinism()
    target = load_target(root)
    split = int(len(target) * 0.8)
    train, test = target.iloc[:split], target.iloc[split:]
    log_returns = np.log(target / target.shift(1)).dropna().rename("log_return")
    train_returns = log_returns.reindex(train.index).dropna()

    scaler = MinMaxScaler(feature_range=(-1, 1))
    train_scaled = scaler.fit_transform(train_returns.to_numpy().reshape(-1, 1))
    x_train, y_train = create_sequences(train_scaled, LOOKBACK)
    model = build_transformer(use_positional_embedding=use_positional_embedding)
    history = model.fit(
        x_train,
        y_train,
        epochs=20,
        batch_size=32,
        validation_split=0.1,
        callbacks=[EarlyStopping(monitor="val_loss", patience=4, restore_best_weights=True)],
        shuffle=False,
        verbose=verbose,
    )

    context = pd.concat([train_returns.tail(LOOKBACK), log_returns.reindex(test.index)])
    context_scaled = scaler.transform(context.to_numpy().reshape(-1, 1))
    x_test, _ = create_sequences(context_scaled, LOOKBACK)
    if len(x_test) != len(test):
        raise AssertionError("Transformer test sequence count does not match test dates")
    predicted_scaled = model(x_test, training=False).numpy()
    predicted_returns = scaler.inverse_transform(predicted_scaled).ravel()
    previous_actual = target.shift(1).reindex(test.index).to_numpy(float)
    forecast = pd.Series(
        previous_actual * np.exp(predicted_returns),
        index=test.index,
        name=MODEL_COLUMN,
    )
    if not forecast.index.equals(test.index) or not np.isfinite(forecast).all():
        raise AssertionError("Invalid PE-Transformer forecast alignment or values")
    return forecast, {k: [float(v) for v in values] for k, values in history.history.items()}, metrics(test, forecast)


def generate_validation_forecast(
    root: Path,
    *,
    verbose: int = 0,
) -> tuple[pd.Series, dict[str, list[float]], dict[str, float]]:
    """Forecast a training-only holdout for empirical uncertainty calibration."""
    configure_determinism()
    target = load_target(root)
    split = int(len(target) * 0.8)
    development = target.iloc[:split]
    fit_target, validation = development.iloc[:-1061], development.iloc[-1061:]
    log_returns = np.log(target / target.shift(1)).dropna().rename("log_return")
    fit_returns = log_returns.reindex(fit_target.index).dropna()

    scaler = MinMaxScaler(feature_range=(-1, 1))
    fit_scaled = scaler.fit_transform(fit_returns.to_numpy().reshape(-1, 1))
    x_fit, y_fit = create_sequences(fit_scaled, LOOKBACK)
    model = build_transformer(use_positional_embedding=False)
    history = model.fit(
        x_fit,
        y_fit,
        epochs=20,
        batch_size=32,
        validation_split=0.1,
        callbacks=[EarlyStopping(monitor="val_loss", patience=4, restore_best_weights=True)],
        shuffle=False,
        verbose=verbose,
    )
    context = pd.concat([fit_returns.tail(LOOKBACK), log_returns.reindex(validation.index)])
    x_validation, _ = create_sequences(
        scaler.transform(context.to_numpy().reshape(-1, 1)), LOOKBACK
    )
    predicted_returns = scaler.inverse_transform(
        model(x_validation, training=False).numpy()
    ).ravel()
    forecast = pd.Series(
        target.shift(1).reindex(validation.index).to_numpy(float) * np.exp(predicted_returns),
        index=validation.index,
        name=MODEL_COLUMN,
    )
    return (
        forecast,
        {k: [float(v) for v in values] for k, values in history.history.items()},
        metrics(validation, forecast),
    )


def generate_raw_price_diagnostic(
    root: Path,
    *,
    use_positional_embedding: bool,
    verbose: int = 0,
) -> tuple[pd.Series, dict[str, list[float]], dict[str, float]]:
    """Matched raw-price ablation for explaining the Section 13/14 regression."""
    configure_determinism()
    target = load_target(root)
    split = int(len(target) * 0.8)
    train, test = target.iloc[:split], target.iloc[split:]
    scaler = MinMaxScaler(feature_range=(0, 1))
    train_scaled = scaler.fit_transform(train.to_numpy().reshape(-1, 1))
    x_train, y_train = create_sequences(train_scaled, LOOKBACK)
    model = build_transformer(use_positional_embedding=use_positional_embedding)
    history = model.fit(
        x_train,
        y_train,
        epochs=20,
        batch_size=32,
        validation_split=0.1,
        shuffle=False,
        verbose=verbose,
    )
    context = pd.concat([train.tail(LOOKBACK), test])
    x_test, _ = create_sequences(
        scaler.transform(context.to_numpy().reshape(-1, 1)), LOOKBACK
    )
    forecast = pd.Series(
        scaler.inverse_transform(model(x_test, training=False).numpy()).ravel(),
        index=test.index,
        name="Raw_Price_Transformer",
    )
    return (
        forecast,
        {k: [float(v) for v in values] for k, values in history.history.items()},
        metrics(test, forecast),
    )


def validate_and_save_forecast(forecast: pd.Series, output: Path) -> None:
    if len(forecast) != 1061 or not forecast.index.is_unique or not forecast.index.is_monotonic_increasing:
        raise AssertionError("Expected 1,061 ordered unique PE-Transformer forecasts")
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"Timestamp": forecast.index, MODEL_COLUMN: forecast.to_numpy(float)}).to_csv(output, index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--positional", action="store_true")
    parser.add_argument("--raw-price-diagnostic", action="store_true")
    parser.add_argument("--validation-forecast", action="store_true")
    parser.add_argument("--history-output", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.raw_price_diagnostic:
        forecast, history, score = generate_raw_price_diagnostic(
            root, use_positional_embedding=args.positional
        )
    elif args.validation_forecast:
        forecast, history, score = generate_validation_forecast(root)
    else:
        forecast, history, score = generate_pe_transformer_forecast(
            root, use_positional_embedding=args.positional
        )
    validate_and_save_forecast(forecast, args.output)
    if args.history_output:
        args.history_output.write_text(json.dumps(history, indent=2), encoding="utf-8")
    print(json.dumps({
        "metrics": score,
        "epochs": len(history["loss"]),
        "positional": args.positional,
        "raw_price_diagnostic": args.raw_price_diagnostic,
        "validation_forecast": args.validation_forecast,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
