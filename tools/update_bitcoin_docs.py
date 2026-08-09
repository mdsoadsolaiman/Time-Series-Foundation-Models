"""Synchronize Bitcoin-only sections of the root project guide."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "README.md"
text = path.read_text(encoding="utf-8")


def replace_section(document: str, start: str, end: str, replacement: str) -> str:
    left = document.index(start)
    right = document.index(end, left)
    return document[:left] + replacement.rstrip() + "\n\n" + document[right:]


text = text.replace(
    "**Completed.** Daily Bitcoin Close is evaluated over 1,061 test days with rolling one-step forecasts. The authoritative comparison is `results/validated_forecasts.csv`.",
    "**Completed and rebuilt.** Daily Bitcoin Close is evaluated over 1,061 test days with ten analytical models. Nine vectors are frozen in `results/validated_forecasts.csv`; the 7-Day Moving Average is reconstructed deterministically. Corrected downstream analysis uses training-defined regimes, Temporal Stability, method-labelled uncertainty, HAC inference, and Holm correction.",
)

bitcoin_results = """## Key Bitcoin Results

| Rank | Model | MAE | RMSE | MASE |
|---:|---|---:|---:|---:|
| 1 | Naive | 1290.353 | 1853.625 | 4.576 |
| 2 | Simple Exponential Smoothing — Rolling One-Step | 1290.359 | 1855.731 | 4.576 |
| 3 | ARIMA Rolling One-Step | 1299.875 | 1866.303 | 4.609 |
| 4 | Additive-Trend Exponential Smoothing | 1308.541 | 1871.702 | 4.640 |
| 5 | Persistence-Enhanced Log-Return LSTM | 1321.365 | 1881.091 | 4.686 |
| 6 | TimesFM | 1349.947 | 1924.199 | 4.787 |
| 7 | Chronos-Bolt-Tiny | 1424.026 | 1994.008 | 5.050 |
| 8 | Persistence-Enhanced Log-Return Transformer | 2019.366 | 2559.750 | 7.161 |
| 9 | Prophet — 30-Day Periodic Refit | 8195.263 | 10781.163 | 29.061 |

The 7-Day Moving Average is the tenth analytical model and is reconstructed
downstream from seven strictly prior prices. The corrected inference artifact
covers all 45 pairs with HAC lag 6: 39 pairs are raw-significant and 33 remain
significant after Holm correction.

The exploratory composite is secondary. Naive leads the missing-evidence-
penalised summary at `97.051891`, followed by SES at `96.970846`, ARIMA at
`96.266697`, and additive-trend smoothing at `96.179827`. PE-LSTM scores
`81.342547` with missing uncertainty penalised and `95.697114` on available
dimensions. Full evidence is generated in the versioned Bitcoin CSVs.

The final date, 2026-07-07, contains data only through 01:57 UTC and is retained
as a documented partial daily observation to preserve `bitcoin-v1`.
"""
text = replace_section(text, "## Key Bitcoin Results", "## Key Electricity Results", bitcoin_results)

guide_start = text.index("## Notebook Guide")
electricity_row = text.index("| `electricity/10_Electricity_EDA.ipynb`", guide_start)
bitcoin_rows_start = text.index("| `Bitcoin_Master.ipynb`", guide_start)
bitcoin_rows = """| `Bitcoin_Master.ipynb` | MASTER / RECOMMENDED ENTRY POINT | Safe ten-model artifact-driven synthesis |
| `Electricity_Master.ipynb` | MASTER / RECOMMENDED ENTRY POINT | Safe Electricity orchestration, validation, and artifact-based analysis |
| `01_Bitcoin_Data_EDA.ipynb` | AUTHORITATIVE DATA | Canonical UTC aggregation, checks, and split |
| `02_Bitcoin_Classical_Baselines.ipynb` | AUTHORITATIVE ANALYSIS | Final past-only classical comparison |
| `03_Bitcoin_PE_LSTM.ipynb` | AUTHORITATIVE ANALYSIS | Frozen PE Log-Return LSTM evidence |
| `04_Bitcoin_PE_Transformer.ipynb` | AUTHORITATIVE ANALYSIS | Frozen PE Log-Return Transformer evidence |
| `05_Bitcoin_Prophet_and_Deferred_Models.ipynb` | SUPPORTING COMPARATOR | Periodic-refit Prophet and model-status table |
| `06_Bitcoin_Foundation_Models.ipynb` | AUTHORITATIVE ANALYSIS | Zero-shot Chronos and TimesFM evidence |
| `07_Bitcoin_Forecast_Freeze_and_Validation.ipynb` | AUTHORITATIVE GATE | Forecast-freeze boundary and validation |
| `08_Bitcoin_Naive_Audit.ipynb` | AUTHORITATIVE AUDIT | Persistence and leakage proof |
| `09_Bitcoin_Robustness_and_Temporal_Stability.ipynb` | AUTHORITATIVE ANALYSIS | Training-defined regimes and temporal segments |
| `10_Bitcoin_Uncertainty.ipynb` | AUTHORITATIVE ANALYSIS | Method-separated uncertainty evidence |
| `11_Bitcoin_Statistical_Inference.ipynb` | AUTHORITATIVE ANALYSIS | HAC DM tests and Holm adjustment |
| `12_Bitcoin_Trustworthiness_Synthesis.ipynb` | AUTHORITATIVE SYNTHESIS | Component-first evidence and secondary composite |
"""
text = text[:bitcoin_rows_start] + bitcoin_rows + text[electricity_row:]

text = text.replace(
    "- Bitcoin trust evidence: `bitcoin_trust_scores_penalised.csv` and `bitcoin_trust_scores_evidence_available.csv`",
    "- Rebuilt Bitcoin trust evidence: `bitcoin_trustworthiness_components_v2.csv` and `bitcoin_trust_score_sensitivity_v2.csv`",
).replace(
    "- Statistical evidence: `bitcoin_dm_pairwise_results.csv` plus electricity protocol-specific DM and effect-size CSVs",
    "- Corrected Bitcoin inference: `bitcoin_dm_pairwise_results_hac_holm.csv`; historical DM evidence is retained for provenance",
)

repro = """## Reproducibility

Routine Bitcoin Run All is artifact-only. Generation must write to staging and
requires explicit promotion. Run `python src/verify_research_artifacts.py` for
artifact verification. See [`docs/bitcoin_reproducibility.md`](docs/bitcoin_reproducibility.md)
for the separation between artifact-level reproduction and full model regeneration.

## Environment

The lightweight Bitcoin artifact environment is Python 3.12 on Windows and is
pinned in [`requirements-bitcoin-artifact.txt`](requirements-bitcoin-artifact.txt).
The historical full-generation record used CPU-only Python 3.13.2, TensorFlow
2.21.0, Torch 2.12.1, Chronos Forecasting 2.3.1, and TimesFM 2.0.2. The original
`.venv` references a removed Python installation; full regeneration was not
rerun or claimed during this rebuild.
"""
text = replace_section(text, "## Reproducibility", "## Limitations", repro)
text = text.replace("Diebold–Mariano tests.", "Diebold–Mariano tests; Bitcoin uses Newey–West HAC variance and Holm family-wise correction.")

path.write_text(text, encoding="utf-8")
