# Bitcoin Reproducibility Record

## Forecast freeze

`bitcoin-v1` is the current point-forecast freeze. Its nine saved model vectors
and `results/validated_forecasts.csv` are immutable inputs to the final
downstream analysis. Model generation must write to
`results/staging/bitcoin/<run-id>/`; promotion requires explicit opt-in and the
schema, timestamp, row-count, finite-value, and optional hash checks in
`src.bitcoin_pipeline.promote_staged_forecast`.

## Artifact-level reproduction

The supported lightweight environment is Python 3.12 on Windows x86-64 using
`requirements-bitcoin-artifact.txt`. It runs the artifact verifier, rebuilt
notebooks, training-defined robustness, temporal stability, uncertainty
summaries, HAC/Holm inference, Trust Score sensitivity, and figures. It does
not load or execute forecasting models.

Create it with:

```powershell
py -3.12 -m venv .artifact-venv
.\.artifact-venv\Scripts\python.exe -m pip install -r requirements-bitcoin-artifact.txt
.\.artifact-venv\Scripts\python.exe src\verify_research_artifacts.py
.\.artifact-venv\Scripts\python.exe tools\rebuild_bitcoin_domain.py
```

## Full model regeneration

Full regeneration was not performed during the final structural rebuild. The
previous research environment recorded Python 3.13.2 on Windows, CPU-only
execution, TensorFlow 2.21.0, Torch 2.12.1, Chronos Forecasting 2.3.1, and
TimesFM 2.0.2. The original `.venv` launcher references a removed Python 3.13
installation and is not operational. `requirements-research.txt` preserves the
intended package set, but frozen artifact hashes—not a claim of demonstrated
end-to-end regeneration—are the current reproducibility boundary.

Checkpoint identifiers are `amazon/chronos-bolt-tiny` and
`google/timesfm-2.5-200m-pytorch`. Immutable remote checkpoint commit IDs were
not preserved, so exact external-model regeneration is not claimed.

External fresh-kernel PE-LSTM checks previously produced bit-identical
forecasts, but the three independent vectors were not retained as separate
authoritative artifacts. No synthetic three-run determinism figure is used.

## Platform record

- Artifact rebuild: Python 3.12.13, Windows x86-64, CPU analysis.
- Forecast-generation record: Python 3.13.2, Windows x86-64, CPU-only.
- GPU acceleration: not used in the recorded Bitcoin runs.
- Final data limitation: 2026-07-07 contains observations only through 01:57
  UTC and is a partial daily observation.
