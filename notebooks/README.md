# Research Notebook Workflow

This directory contains the sequential experimental record for the two completed research domains: Bitcoin price forecasting and South Australian electricity-demand forecasting. The numbered notebooks separate data definition, forecast generation, evidence validation, downstream trustworthiness analysis, and cross-domain synthesis.

The canonical scientific results are the frozen artifacts under [`../results/`](../results/), not whichever values happen to be produced by an exploratory rerun. For headline findings and full result tables, see the [root research overview](../README.md). This guide answers where each stage lives, what question it addresses, and how it should be executed.

## Workflow at a Glance

```text
Bitcoin
Data and EDA
  → Classical baselines
  → Supervised neural models
  → Prophet and deferred-model registry
  → Zero-shot foundation models
  → Forecast freeze and validation
  → Independent Naive audit
  → Regime-Conditional Robustness and Temporal Stability
  → Uncertainty
  → Statistical inference
  → Trustworthiness synthesis

Electricity
EDA and frozen experimental design
  → Classical and statistical models
  → LSTM
  → Zero-shot foundation models
  → Model-validation audit
  → Regime-Conditional Robustness and Temporal Stability
  → Uncertainty
  → Trustworthiness synthesis
  → Statistical significance and practical effects

Bitcoin + Electricity
  → Cross-domain comparison
```

## Execution Status Legend

| Classification | Meaning |
|---|---|
| **Artifact-only** | Reads preserved evidence and performs lightweight downstream analysis; it does not regenerate model forecasts in normal execution. |
| **Generation-capable, gated** | Contains fitting or inference capability, but generation is disabled by default and candidate outputs are separated from authoritative artifacts. |
| **Data analysis** | Reconstructs and audits the canonical dataset, split, or diagnostics without creating final model forecasts. |
| **Validation / audit** | Independently checks frozen vectors, protocol semantics, alignment, metrics, or leakage-sensitive identities. |
| **Synthesis / inference** | Derives conditional, probabilistic, statistical, or composite evidence from validated forecasts. |

“Artifact-driven” describes the normal review path. It does not imply that every notebook is output-free, nor that expensive generation code has been removed.

# Bitcoin Research Workflow

The Bitcoin study forecasts daily Close over a frozen 1,061-target rolling one-step test. The sequence should normally be read from 01 through 12 because later evidence depends on the forecast and validation boundaries established earlier.

| No. | Notebook | Research role | Main evidence | Execution |
|---:|---|---|---|---|
| 01 | [01_Bitcoin_Data_EDA.ipynb](01_Bitcoin_Data_EDA.ipynb) | Defines the canonical UTC daily series, quality checks, chronological split, stationarity, returns, volatility, and seasonality evidence. | Audited daily target and frozen split definition from the local minute OHLCV source. | **Data analysis**; no final forecasts written. |
| 02 | [02_Bitcoin_Classical_Baselines.ipynb](02_Bitcoin_Classical_Baselines.ipynb) | Asks whether transparent classical systems improve on persistence under a fair past-only protocol. | Naive, MA7, SES, additive-trend smoothing, and rolling ARIMA metrics and diagnostics. | **Artifact-only** by default; generation flags are off. |
| 03 | [03_Bitcoin_PE_LSTM.ipynb](03_Bitcoin_PE_LSTM.ipynb) | Tests whether a supervised log-return LSTM improves on the classical floor. | Frozen PE-LSTM vector, architecture/training record, accuracy, residuals, and reproducibility limits. | **Artifact-only** by default; `RUN_TRAINING=False`. |
| 04 | [04_Bitcoin_PE_Transformer.ipynb](04_Bitcoin_PE_Transformer.ipynb) | Evaluates a persistence-enhanced log-return Transformer against Naive, ARIMA, and PE-LSTM. | Frozen PE-Transformer vector, diagnostics, and architecture comparison. | **Artifact-only** by default; `RUN_TRAINING=False`. |
| 05 | [05_Bitcoin_Prophet_and_Deferred_Models.ipynb](05_Bitcoin_Prophet_and_Deferred_Models.ipynb) | Evaluates periodic-refit Prophet and records models that are deferred or unavailable. | Frozen Prophet evidence and an explicit model-scope registry. | **Artifact-only** by default; Prophet generation is off. |
| 06 | [06_Bitcoin_Foundation_Models.ipynb](06_Bitcoin_Foundation_Models.ipynb) | Tests zero-shot Chronos-Bolt-Tiny and TimesFM point forecasts and preserved uncertainty. | Frozen foundation forecasts, native/calibrated interval evidence, diagnostics, and provenance. | **Generation-capable, gated**; default is artifact-driven, generation stages candidates, promotion is separate. |
| 07 | [07_Bitcoin_Forecast_Freeze_and_Validation.ipynb](07_Bitcoin_Forecast_Freeze_and_Validation.ipynb) | Establishes the authoritative forecast boundary and asks whether all final vectors are structurally and metrically valid. | Validated nine-vector matrix plus deterministically reconstructed MA7; canonical ten-model comparison. | **Validation / audit**; artifact-only. |
| 08 | [08_Bitcoin_Naive_Audit.ipynb](08_Bitcoin_Naive_Audit.ipynb) | Independently proves the persistence identity and verifies that the leading baseline uses only prior information. | Row-level Naive reconstruction, boundary checks, and independent metric reproduction. | **Validation / audit**; deterministic reconstruction only. |
| 09 | [09_Bitcoin_Robustness_and_Temporal_Stability.ipynb](09_Bitcoin_Robustness_and_Temporal_Stability.ipynb) | Examines model behavior under training-defined regimes and across contiguous test segments. | Regime metrics, robustness ranks, bootstrap diagnostics, segment evidence, and targeted conditional comparisons. | **Synthesis / inference**; artifact-only. |
| 10 | [10_Bitcoin_Uncertainty.ipynb](10_Bitcoin_Uncertainty.ipynb) | Determines which uncertainty evidence exists and how calibration, coverage, width, and proper scores differ by method. | Native, training-only CQR-adjusted, validation-residual, and unavailable-evidence classifications. | **Synthesis / inference**; artifact-only. |
| 11 | [11_Bitcoin_Statistical_Inference.ipynb](11_Bitcoin_Statistical_Inference.ipynb) | Tests whether pairwise squared-error differences survive serial-dependence adjustment and family-wise correction. | All 45 HAC Diebold–Mariano comparisons, Holm adjustment, practical differences, and a derived effects table. | **Synthesis / inference**; artifact-driven, with derived evidence output where invoked. |
| 12 | [12_Bitcoin_Trustworthiness_Synthesis.ipynb](12_Bitcoin_Trustworthiness_Synthesis.ipynb) | Integrates component evidence while treating the exploratory composite as secondary. | Corrected v2 dimensions, missing-evidence variants, weight sensitivity, and bootstrap rank stability. | **Synthesis / inference**; artifact-only. |

### Forecast Generation and Freeze

Notebooks 02–06 document the model-specific forecasting systems. Their normal review path loads frozen vectors; explicit generation flags are disabled. Notebook 06 retains controlled foundation-model regeneration but writes candidate artifacts beneath a staging location and does not promote them automatically.

Notebook 07 is the Bitcoin freeze boundary. It validates the aligned forecast matrix, reconstructs the deterministic 7-Day Moving Average, reproduces metrics, and establishes the ten-model evidence set used downstream. Forecast experiments performed outside this boundary are not authoritative merely because they produce a CSV.

### Audit and Trustworthiness Layer

Notebook 08 independently audits the Naive forecast. Notebooks 09 and 10 derive conditional, temporal, and uncertainty evidence from the frozen comparison. Notebook 11 performs corrected dependence-aware inference. Notebook 12 combines the resulting dimensions while keeping component evidence primary and explicitly distinguishing missing uncertainty from measured poor calibration.

# Electricity Research Workflow

The Electricity study uses the South Australia T4 demand series and two operationally distinct protocols: rolling one-step Protocol A and true 48-step day-ahead Protocol B. Both protocols flow through the same generation, validation, and downstream evidence architecture.

| No. | Notebook | Research role | Main evidence | Execution |
|---:|---|---|---|---|
| 10 | [electricity/10_Electricity_EDA.ipynb](electricity/10_Electricity_EDA.ipynb) | Selects South Australia, audits the half-hourly series, establishes partitions, and motivates the two protocols. | Dataset quality, temporal structure, lag/seasonality diagnostics, and frozen train/validation/test design. | **Data analysis**. |
| 11 | [electricity/11_Electricity_Classical_Baselines.ipynb](electricity/11_Electricity_Classical_Baselines.ipynb) | Establishes the deterministic and statistical benchmark floor under both protocols. | Baselines, ARIMA, SARIMA, Prophet, SES, Holt-Winters, and DHR-ARIMA forecasts, diagnostics, selection records, and horizon behavior. | **Generation-capable, gated**; `RUN_SELECTION=False`, `RUN_FITTING=False`; candidates stage outside authority. |
| 12 | [electricity/12_Electricity_LSTM.ipynb](electricity/12_Electricity_LSTM.ipynb) | Tests whether a supervised univariate LSTM improves on protocol-appropriate classical benchmarks. | Validation-only context selection, protocol-specific frozen forecasts, diagnostics, and training/determinism record. | **Generation-capable, gated**; selection and fitting are off by default; candidates are staged. |
| 13 | [electricity/13_Electricity_Foundation_Models.ipynb](electricity/13_Electricity_Foundation_Models.ipynb) | Evaluates zero-shot Chronos-Bolt-Tiny and TimesFM under identical legal information sets. | Frozen point forecasts, native 80% evidence, baseline context, diagnostics, and checkpoint provenance. | **Generation-capable, gated**; default is artifact-driven; candidates stage and promotion is separate. |
| 14 | [electricity/14_Electricity_Model_Validation_Audit.ipynb](electricity/14_Electricity_Model_Validation_Audit.ipynb) | Certifies the frozen Protocol A/B matrices and independently reconstructs protocol-defining evidence. | Shape, keys, alignment, baseline reconstruction, model distinctness, metric reproduction, and certification matrix. | **Validation / audit**; no model retraining. |
| 15 | [electricity/15_Electricity_Robustness.ipynb](electricity/15_Electricity_Robustness.ipynb) | Evaluates Regime-Conditional Robustness, worst regimes, cross-protocol sensitivity, and Temporal Stability. | Conditional metrics, robustness penalties/ranks, segment metrics, rank changes, and integrity checks. | **Synthesis / inference**; artifact-only. |
| 16 | [electricity/16_Electricity_Uncertainty.ipynb](electricity/16_Electricity_Uncertainty.ipynb) | Audits uncertainty availability and compares calibration, width, and protocol sensitivity without fabricating intervals. | Native Chronos/TimesFM 80% aggregates and explicit unavailable-evidence records for other models. | **Synthesis / inference**; artifact-only. |
| 17 | [electricity/17_Electricity_Trustworthiness.ipynb](electricity/17_Electricity_Trustworthiness.ipynb) | Synthesizes five evidence dimensions and tests missing-evidence and weight sensitivity. | Dimension ranks, model profiles, two exploratory composite variants, and cross-protocol sensitivity. | **Synthesis / inference**; artifact-only. |
| 18 | [electricity/18_Electricity_Statistical_Significance.ipynb](electricity/18_Electricity_Statistical_Significance.ipynb) | Tests aggregate and selected horizon-specific loss differences with protocol-appropriate sampling units. | Protocol A/B DM tests, BH correction, HAC sensitivity, effect sizes, and horizon evidence. | **Synthesis / inference**; artifact-only. |

### Generation Layer

Notebooks 11–13 contain the principal Electricity model-generation capability. Notebook 11 covers deterministic and classical/statistical models, Notebook 12 the supervised LSTM, and Notebook 13 zero-shot foundation inference. Their normal research-review path reads frozen artifacts. Expensive selection, fitting, or inference is opt-in, and generated candidates are separated from authoritative files.

### Validation Boundary

Notebook 14 is the Electricity evidence boundary. It validates both protocol matrices, including Protocol B’s 962 origins × 48 horizons and prohibition on within-horizon actual updates. It checks artifact structure and behavior but does not claim that artifact inspection is equivalent to independent source-code proof or retraining.

### Trustworthiness and Inference Layer

Notebooks 15–18 consume validated forecasts. Notebook 15 derives robustness and Temporal Stability evidence; 16 audits uncertainty; 17 performs component-first synthesis; and 18 applies protocol-specific statistical inference. These stages should not silently refit or replace the forecasting systems whose evidence they analyze.

# Cross-Domain Synthesis

[18_Cross_Domain_Comparison.ipynb](18_Cross_Domain_Comparison.ipynb) is the final artifact-only synthesis. It reads frozen Bitcoin and Electricity accuracy, robustness, Temporal Stability, uncertainty, significance, trust-component, and comparability tables.

The notebook compares within-task ranks, scale-independent metrics, baseline-relative performance, evidence availability, and carefully mapped model families. It does **not** pool raw Bitcoin and Electricity MAE/RMSE as if the tasks were interchangeable. Interpretations preserve differences in target, scale, frequency, horizon, protocol, information updates, model specification, and statistical methodology.

# Master / Convenience Notebooks

| Notebook | Current status | Recommended use |
|---|---|---|
| [Bitcoin_Master.ipynb](Bitcoin_Master.ipynb) | Compact artifact-driven orchestration aligned with the frozen Bitcoin evidence boundary. | Safe high-level Bitcoin entry point; use numbered notebooks for methods and detailed evidence. |
| [Electricity_Master.ipynb](Electricity_Master.ipynb) | Historically consolidated workflow containing older phase organization and generation sections. | Useful for provenance and consolidated context, but the modular Electricity 10–18 sequence is the clearer current workflow and should be preferred. |

Master notebooks are convenience views, not substitutes for the numbered experimental record or the authoritative result artifacts.

# Evidence Freeze and Authority

```text
model fitting / zero-shot inference
  → candidate forecast artifacts
  → validation and explicit freeze
  → protected authoritative forecasts
  → downstream robustness, Temporal Stability, uncertainty,
    trustworthiness, statistical inference, and cross-domain synthesis
```

Bitcoin Notebook 07 and Electricity Notebook 14 enforce the central boundary between forecast creation and scientific interpretation. After forecasts are frozen, downstream notebooks should derive evidence from the preserved vectors rather than silently rerunning models or changing the comparison set.

Authoritative status depends on validation, schema/protocol integrity, and the protected hash ledger—not simply on location or filename. See the [result artifact guide](../results/README.md) and [`authoritative_artifact_hashes.md`](../results/authoritative_artifact_hashes.md).

# Protocol Interpretation

- **Bitcoin:** daily rolling one-step; the actual is released after each prediction.
- **Electricity A:** 30-minute rolling one-step; the latest actual may update the next origin.
- **Electricity B:** fixed-origin 48-step day-ahead; no actual is revealed inside the horizon.

Results must be interpreted within these information sets. A rank change between A and B can reflect operational horizon and update discipline rather than an intrinsic change in model quality.

# Recommended Reading Paths

### Fast Research Overview

[Root README](../README.md) → Bitcoin [07](07_Bitcoin_Forecast_Freeze_and_Validation.ipynb) and [12](12_Bitcoin_Trustworthiness_Synthesis.ipynb) → Electricity [14](electricity/14_Electricity_Model_Validation_Audit.ipynb), [17](electricity/17_Electricity_Trustworthiness.ipynb), and [18](electricity/18_Electricity_Statistical_Significance.ipynb) → [cross-domain synthesis](18_Cross_Domain_Comparison.ipynb).

### Bitcoin Deep Dive

Read Bitcoin 01 → 12 in order. This preserves the progression from dataset definition to generation evidence, validation, independent audit, conditional/probabilistic analysis, inference, and synthesis.

### Electricity Deep Dive

Read Electricity 10 → 18 in order. Keep Protocol A and Protocol B separate throughout.

### Reproducibility and Audit Review

- Bitcoin: [07](07_Bitcoin_Forecast_Freeze_and_Validation.ipynb) → [08](08_Bitcoin_Naive_Audit.ipynb) → [`verify_research_artifacts.py`](../src/verify_research_artifacts.py) → [results guide](../results/README.md).
- Electricity: [14](electricity/14_Electricity_Model_Validation_Audit.ipynb) → verifier → results guide.

# Execution Guidance

Use the repository’s documented environment and begin with artifact-driven notebooks when inspecting existing evidence. Do not enable selection, training, fitting, inference, or promotion flags unless deliberately creating a new experiment version. Foundation-model regeneration may require external checkpoints and a compatible full-generation environment.

Preserve authoritative forecasts. Normal downstream analysis should read validated artifacts and should not overwrite them. Artifact-level reproduction is intentionally cheaper and narrower than end-to-end model regeneration; environment details and current limitations are documented in the [root README](../README.md) and [Bitcoin reproducibility record](../docs/bitcoin_reproducibility.md).

# Notebook Output Policy

Saved notebook outputs may serve as readable research evidence, but authority ultimately rests with validated artifacts and their documented provenance. Some notebooks deliberately preserve result tables and figures; others are structured for inexpensive artifact analysis. “Run All” behavior is therefore notebook-specific.

Generation-capable notebooks use explicit safety flags and, where implemented, staging locations. Candidate forecasts do not become authoritative automatically. Downstream notebooks should remain deterministic and inexpensive where possible, and derived outputs must not silently replace frozen forecasts or alter the research comparison.

# Related Documentation

- [Research overview and findings](../README.md)
- [Result artifact taxonomy](../results/README.md)
- [Bitcoin case study](../docs/bitcoin_case_study.md)
- [Electricity case study](../docs/electricity_case_study.md)
- [Bitcoin reproducibility record](../docs/bitcoin_reproducibility.md)
- [Figure index](../figures/README.md)
- [Research manuscript](../paper/research_manuscript.md)
- [Research proposal](../proposal/Research_Proposal.md)
