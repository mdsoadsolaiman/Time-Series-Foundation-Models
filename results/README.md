# Research Results and Evidence Artifacts

This directory is the repository’s machine-readable research evidence store. It contains frozen forecast vectors, deterministic analytical derivatives, validation evidence, conditional and probabilistic evaluations, statistical inference, exploratory trustworthiness synthesis, and cross-domain comparison tables.

This guide describes evidence lineage and authority. It is not a scientific-results summary; headline findings and model rankings belong in the [root research overview](../README.md), while notebook ownership and execution order are documented in the [notebook workflow guide](../notebooks/README.md).

## Evidence Architecture

```text
model fitting or zero-shot inference
  → candidate/model-specific forecast vectors
  → alignment, protocol validation, and explicit freeze
  → authoritative validated forecast matrices
  → deterministic metrics and downstream analytical evidence
  → protocol-specific inference and trustworthiness synthesis
  → cross-domain comparison
```

The architecture separates expensive, environment-dependent forecast generation from inexpensive and repeatable analysis. A downstream notebook displaying an artifact does not become its scientific owner and must not silently replace its upstream evidence.

## Evidence Authority Levels

| Level | Definition | Typical examples |
|---|---|---|
| **Level 1 — Frozen Authoritative Evidence** | Accepted primary empirical vectors protected against silent change. | `validated_forecasts.csv`; Electricity Protocol A/B validated matrices. |
| **Level 2 — Authoritative Derived Evidence** | Deterministically derived from Level 1 or other declared preserved evidence and canonical for a specific analysis. | Corrected metrics, robustness, Temporal Stability, uncertainty summaries, DM tests, trust components, and cross-domain tables recorded in the ledger. |
| **Level 3 — Analytical / Diagnostic Evidence** | Supporting model-specific vectors, validation forecasts, selection records, checkpoints, derived convenience tables, or diagnostics that do not redefine the central freeze. | Individual Electricity forecast CSVs, validation-period Bitcoin forecasts, selection JSON, quantile checkpoints, derived effect-size table. |
| **Level 4 — Candidate / Staging Evidence** | Newly generated output awaiting review, validation, hashing, and explicit promotion. | Files created under gated `results/staging/...` paths. |
| **Historical — Provenance Only** | Retained superseded evidence that must not support current headline claims. | Uncorrected Bitcoin DM/trust files and the unvalidated Electricity horizon table. |

Authority is established by documented lineage, validation, protocol consistency, and—in the protected set—the SHA-256 ledger. A file is not authoritative merely because it is stored under `results/`.

## Results Directory Map

Only one result subdirectory currently exists. Staging directories are created on demand and are not presently materialized.

```text
results/
├── validated_forecasts.csv                 # Bitcoin Level 1 freeze
├── [Bitcoin model-specific forecasts]      # Source/supporting vectors
├── [Bitcoin corrected derived evidence]    # Metrics, robustness, stability,
│                                             uncertainty, inference, trust
├── cross_domain_*.csv                      # Cross-domain Level 2 synthesis
├── authoritative_artifact_hashes.md        # Protected-artifact ledger
└── electricity/
    ├── protocol_a_validated_forecasts.csv  # Electricity A Level 1 freeze
    ├── protocol_b_validated_forecasts.csv  # Electricity B Level 1 freeze
    ├── protocol_a_* / protocol_b_*         # Protocol-specific evidence
    ├── uncertainty_summary.csv
    └── trust_score_sensitivity.csv
```

# Bitcoin Evidence

The Bitcoin pipeline evaluates ten analytical models over one frozen rolling one-step daily test. Nine forecast vectors are stored in the canonical matrix; the 7-Day Moving Average is reconstructed deterministically from seven strictly prior prices.

## Bitcoin Source-of-Truth Table

| Artifact / family | Evidence role | Authority | Primary owning workflow | Notes |
|---|---|---|---|---|
| [`validated_forecasts.csv`](validated_forecasts.csv) | Central aligned test matrix: timestamp, actual, and nine saved model vectors | **Level 1** | Bitcoin [Notebook 07](../notebooks/07_Bitcoin_Forecast_Freeze_and_Validation.ipynb) | The Bitcoin forecast freeze and primary downstream input. |
| `baseline_forecasts.csv`; model-specific `*_forecast.csv` files | Source vectors for Naive, PE-LSTM, PE-Transformer, Prophet, ARIMA, smoothing, Chronos, and TimesFM | **Level 1 supporting** where ledger-protected; otherwise Level 3 as documented | Notebooks 02–06 | The MA7 vector is reconstructed, not stored in the validated matrix. |
| `*_validation_forecast.csv` | Pre-test validation forecasts used for empirical interval or method evidence | **Level 2/3 supporting** | Notebooks 02, 04, and 10 | These end before the final test and must not be confused with test forecasts. |
| [`bitcoin_point_forecast_metrics_v2.csv`](bitcoin_point_forecast_metrics_v2.csv) | Canonical ten-model point metrics | **Level 2** | Notebook 07 / corrected Bitcoin rebuild | Current metric source; derived from the freeze. |
| `bitcoin_regime_thresholds_training.csv`; `bitcoin_regime_robustness_training_defined.csv` | Training-only regime definitions and conditional error evidence | **Level 2** | [Notebook 09](../notebooks/09_Bitcoin_Robustness_and_Temporal_Stability.ipynb) | Current corrected robustness evidence. |
| [`bitcoin_temporal_stability.csv`](bitcoin_temporal_stability.csv) | Earlier/Middle/Later segment performance | **Level 2** | Notebook 09 | Public term is Temporal Stability. |
| `foundation_uncertainty_calibration.csv`; `foundation_uncertainty_summary.csv`; `bitcoin_uncertainty_evidence_v2.csv` | Preserved interval vectors/aggregates and method-separated uncertainty inventory | **Level 2** | [Notebook 10](../notebooks/10_Bitcoin_Uncertainty.ipynb) | Distinguishes native, CQR-adjusted, empirical, and unavailable evidence. |
| `bitcoin_dm_pairwise_results_hac_holm.csv` | Corrected 45-pair HAC DM inference with Holm adjustment | **Level 2** | [Notebook 11](../notebooks/11_Bitcoin_Statistical_Inference.ipynb) | Current inferential source. |
| `bitcoin_dm_pairwise_results_hac_holm_effects.csv` | Derived convenience/effect interpretation of corrected inference | **Level 3** | Notebook 11 | Not a replacement for the protected corrected DM table. |
| `bitcoin_transparency_auditability_rubric.csv`; `bitcoin_trustworthiness_components_v2.csv`; `bitcoin_trust_score_sensitivity_v2.csv` | Current component-first and sensitivity evidence | **Level 2** | [Notebook 12](../notebooks/12_Bitcoin_Trustworthiness_Synthesis.ipynb) | Corrected v2 trustworthiness source. |
| `bitcoin_dm_pairwise_results.csv`; `bitcoin_trust_scores_penalised.csv`; `bitcoin_trust_scores_evidence_available.csv` | Earlier inference/composite outputs | **Historical** | Earlier workflow | Retained for provenance; not current headline authority. |

## Forecast Evidence

Bitcoin’s source flow is:

```text
baseline_forecasts.csv + model-specific forecast CSVs
  → validated_forecasts.csv
  → bitcoin_point_forecast_metrics_v2.csv
  → corrected downstream evidence
```

`validated_forecasts.csv` is the central evidence boundary. Model-specific files preserve provenance and allow assembly checks; downstream analyses should use the validated matrix and the declared deterministic MA7 reconstruction rather than independently mixing source vectors.

## Robustness and Temporal Stability

Notebook 09 derives conditional errors from frozen forecasts using thresholds estimated from training data only. It evaluates four implemented Bitcoin regimes, bootstrap uncertainty for conditional RMSE, block-length and threshold sensitivity, and three contiguous temporal segments. These are conditional diagnostics, not adversarial robustness or broad out-of-distribution generalisation.

## Uncertainty and Calibration

Bitcoin preserves four evidence classes in `bitcoin_uncertainty_evidence_v2.csv`:

1. native Chronos and TimesFM quantiles;
2. training-only CQR-adjusted foundation quantiles;
3. validation-residual empirical intervals for models with sufficient preserved pre-test forecasts; and
4. explicitly unavailable evidence.

The row-level foundation interval evidence is in `foundation_uncertainty_calibration.csv`; its aggregate companion is `foundation_uncertainty_summary.csv`. Coverage and width from different interval-construction methods are labeled rather than assumed directly equivalent.

## Statistical Inference

The current Bitcoin inference artifact is `bitcoin_dm_pairwise_results_hac_holm.csv`: 10 models, 45 pairwise squared-error comparisons, Bartlett/Newey–West HAC variance with lag 6, and Holm family-wise correction. The similarly named uncorrected `bitcoin_dm_pairwise_results.csv` is historical provenance.

## Trustworthiness Synthesis

Current authority rests with `bitcoin_trustworthiness_components_v2.csv` and `bitcoin_trust_score_sensitivity_v2.csv`, supported by the published transparency/auditability rubric. The synthesis is exploratory, researcher-defined, comparison-set-relative, and secondary to component evidence.

The v2 components preserve both missing-evidence-penalised and evidence-available interpretations. Missing uncertainty denotes unavailable evidence, not measured zero uncertainty or demonstrated poor calibration. The older standalone trust-score CSVs remain only for provenance.

# Electricity Evidence

Electricity maintains two separate 13-model evidence pipelines:

- **Protocol A:** rolling one-step at 30-minute resolution; actuals update the next forecast origin.
- **Protocol B:** 962 fixed midnight origins × 48 forecasts; no actual is revealed within a day-ahead horizon.

The `protocol_a_*` and `protocol_b_*` files are not duplicates. They answer different operational questions and must not be merged into a single forecast matrix or statistical family.

## Electricity Source-of-Truth Table

| Artifact / family | Protocol | Evidence role | Authority | Primary owning workflow |
|---|---|---|---|---|
| [`protocol_a_validated_forecasts.csv`](electricity/protocol_a_validated_forecasts.csv) | A | Aligned 46,176-row matrix containing actuals and 13 model vectors | **Level 1** | Electricity [Notebook 14](../notebooks/electricity/14_Electricity_Model_Validation_Audit.ipynb) |
| [`protocol_b_validated_forecasts.csv`](electricity/protocol_b_validated_forecasts.csv) | B | 962-origin × 48-horizon matrix containing actuals and 13 model vectors | **Level 1** | Notebook 14 |
| `protocol_[ab]_baseline_forecasts.csv`; protocol-specific model forecast CSVs | A/B | Generation-layer source vectors for baselines, classical/statistical, LSTM, Chronos, and TimesFM | **Level 3 supporting** unless individually ledger-protected | Notebooks [11](../notebooks/electricity/11_Electricity_Classical_Baselines.ipynb)–[13](../notebooks/electricity/13_Electricity_Foundation_Models.ipynb) |
| `classical_model_selection.json` | A/B | Validation-only selection and configuration record | **Level 3** | Notebook 11 |
| `.phase5_*_checkpoint.npz` | A | Preserved Chronos/TimesFM quantile checkpoint arrays | **Level 3 supporting** | Notebook 13 / uncertainty workflow |
| [`protocol_b_validated_horizon_metrics.csv`](electricity/protocol_b_validated_horizon_metrics.csv) | B | Audited metrics for horizons 1–48 | **Level 2** | Notebook 14 |
| `protocol_[ab]_robustness.csv` | A/B | Regime-conditional error evidence | **Level 2** | [Notebook 15](../notebooks/electricity/15_Electricity_Robustness.ipynb) |
| `protocol_[ab]_generalisation.csv` | A/B | Earlier/Middle/Later segment evidence | **Level 2** | Notebook 15 |
| [`uncertainty_summary.csv`](electricity/uncertainty_summary.csv) | A/B | Native 80% coverage/width and explicit availability inventory | **Level 2** | [Notebook 16](../notebooks/electricity/16_Electricity_Uncertainty.ipynb) |
| `protocol_[ab]_trust_scores.csv`; `trust_score_sensitivity.csv` | A/B | Component scores, two exploratory composite variants, and weight sensitivity | **Level 2** | [Notebook 17](../notebooks/electricity/17_Electricity_Trustworthiness.ipynb) |
| `protocol_a_dm_tests.csv`; `protocol_b_dm_tests.csv`; `protocol_a_effect_sizes.csv`; `protocol_b_effect_sizes.csv` | A/B | Pairwise DM inference, BH correction, sensitivity, and practical effects | **Level 2** | [Notebook 18](../notebooks/electricity/18_Electricity_Statistical_Significance.ipynb) |
| `protocol_b_horizon_significance.csv` | B | Focused selected-horizon inference | **Level 2** | Notebook 18 |
| `protocol_b_horizon_metrics.csv` | B | Earlier, nonvalidated horizon table | **Historical** | Earlier workflow | Use the explicitly validated counterpart. |

## Forecast Evidence

Notebooks 11–13 own generation-layer meaning: classical/statistical models, LSTM, and foundation models respectively. Notebook 14 validates alignment, information-set semantics, actual identity, model distinctness, baseline reconstruction, and metric reproduction before downstream use.

Individual model files support provenance, but the two validated matrices are the central sources of truth. Protocol A and B preserve different keys and information sets; neither can substitute for the other.

## Robustness and Temporal Stability

`protocol_a_robustness.csv` and `protocol_b_robustness.csv` preserve conditional error tables for implemented demand, peak-event, and volatility regimes. The corresponding `generalisation` filenames retain historical terminology to protect artifact identity; their current scientific interpretation is **Temporal Stability** across Earlier, Middle, and Later segments.

The artifacts support descriptive regime and temporal comparisons. They do not contain completed adversarial testing, causal explanations, or formal regime-conditional significance tests.

## Uncertainty and Calibration

`uncertainty_summary.csv` records native probabilistic evidence for Chronos-Bolt-Tiny and TimesFM and explicit unavailability for the remaining models. It contains nominal coverage, empirical coverage, width, evidence type, and provenance notes.

Protocol A quantile arrays are preserved in the two hidden NPZ checkpoint files. Protocol B exact interval vectors were not retained; only the authoritative aggregate evidence survives. No 95% Electricity interval or fabricated deterministic-model interval is presented as current evidence.

## Trustworthiness Synthesis

The protocol-specific trust-score files combine Accuracy, Regime-Conditional Robustness, Temporal Stability, Uncertainty, and Transparency/Auditability. They preserve missing-evidence-penalised and evidence-available formulations. `trust_score_sensitivity.csv` records alternative weight schemes.

These artifacts are exploratory and researcher-defined. Scores are relative to the 13-model protocol-specific comparison set and are not validated universal scales.

## Statistical Inference

Each protocol contains 13 models and 78 pairwise comparisons:

- Protocol A uses half-hourly squared-error differentials, HAC lag 48, and a documented sensitivity lag of 336.
- Protocol B uses daily-origin mean squared error, HAC lag 7, and a documented sensitivity lag of 14.
- Both use Benjamini–Hochberg false-discovery-rate correction and separate effect-size tables.
- Protocol B additionally preserves selected horizon-specific tests.

Bitcoin uses Holm correction, whereas Electricity uses Benjamini–Hochberg. Their adjusted significance counts are therefore not interchangeable cross-domain quantities.

# Forecast Freeze and Evidence Boundary

Forecast generation is expensive and sensitive to software, checkpoint, and hardware environments. Once vectors have been generated, aligned, checked for finite and nonmissing values, matched to actual timestamps/keys, tested against protocol constraints, and accepted into a validated matrix, downstream analysis should operate on that frozen evidence.

Freezing provides stable comparisons, repeatable downstream analysis, auditable inference, and protection against accidental model drift. It does **not** prove that a model is correctly specified, free from all leakage, or scientifically superior. It protects the identity and integrity of accepted evidence.

Bitcoin Notebook 07 and Electricity Notebook 14 establish the principal validation boundaries. The hash ledger protects accepted artifacts after those boundaries.

# Staging and Promotion

No staging directory is currently present in the checked-in result tree. Gated notebooks create staging paths only when generation is explicitly enabled.

Bitcoin foundation regeneration uses:

```text
results/staging/bitcoin/<run-id>/
```

Notebook 06 writes candidate forecasts there. Promotion uses `src.bitcoin_pipeline.promote_staged_forecast`, requires explicit opt-in and a reviewed expected hash, and rechecks schema, 1,061 timestamps/rows, finite values, and hash identity before replacement.

Electricity Notebooks 11 and 12 write enabled fitting candidates under a results staging path rather than `results/electricity/`. Notebook 13 uses `results/staging/foundation_models/`. Its normal path has generation and promotion disabled; promotion is outside normal execution and requires human review of shape, origins/timestamps, actual identity, finite values, horizons, and vector distinctness.

```text
generation
  → candidate artifact
  → structural/protocol validation
  → hash and scientific review
  → explicit promotion
  → authoritative evidence
```

Staged files are Level 4 evidence until that process is completed.

# Artifact Ownership

Ownership is the workflow responsible for establishing an artifact’s scientific meaning:

- A **producer** creates forecasts or analytical evidence.
- A **validator** certifies integrity and protocol consistency.
- A **consumer** reads accepted evidence for later analysis.

For Bitcoin, Notebooks 02–06 own model evidence; 07 owns the freeze; 09 robustness/Temporal Stability; 10 uncertainty; 11 inference; and 12 trustworthiness. For Electricity, Notebooks 11–13 own generation-layer evidence; 14 validation; 15 robustness/Temporal Stability; 16 uncertainty; 17 trustworthiness; and 18 inference. Cross-domain Notebook 18 consumes both domains but does not become the owner of their forecasts.

# Derived Evidence Rule

Every current downstream artifact should be reproducible from declared upstream evidence:

```text
frozen forecasts                         → point metrics
frozen forecast errors + fixed regimes → robustness / Temporal Stability
forecasts + preserved interval evidence → calibration
frozen forecast losses                  → DM tests and effects
validated component evidence            → exploratory trustworthiness synthesis
domain-level derived evidence           → cross-domain comparison
```

If a result cannot be traced to preserved upstream evidence, it should be labeled as a reproducibility limitation or historical provenance—not silently hard-coded as a current result.

# Validation and Audit Evidence

Forecast-performance evidence asks how models perform. Validation evidence asks whether the evidence pipeline is internally consistent. Implemented checks include:

- schemas, shapes, row counts, key uniqueness, sorting, and finite values;
- actual-value and timestamp/origin alignment;
- 48 horizons per Electricity B origin and no within-horizon update interpretation;
- independent deterministic baseline reconstruction;
- Bitcoin Naive persistence identity and boundary checks;
- metric and MASE-denominator reproduction;
- cross-model exact-identity and distribution sanity checks;
- pre-test endings for validation artifacts; and
- training-only provenance for corrected Bitcoin regime thresholds.

Audit coverage differs by model and domain. Artifact validation is not identical to source-code proof or independent model retraining.

# Cross-Domain Evidence

Eight Level 2 artifacts support [cross-domain Notebook 18](../notebooks/18_Cross_Domain_Comparison.ipynb):

| Artifact | Purpose |
|---|---|
| `cross_domain_model_comparison.csv` | Within-task metrics and ranks across the full domain rosters |
| `cross_domain_foundation_model_comparison.csv` | Foundation-model ranks, baseline-relative performance, components, calibration, and evidence metadata |
| `cross_domain_uncertainty_comparison.csv` | Method-labeled calibration, coverage error, and width |
| `cross_domain_significance_summary.csv` | Selected domain-specific inference summaries with correction labels |
| `cross_domain_rank_stability.csv` | Rank level and variation for mapped model families |
| `cross_domain_trust_comparison.csv` | Component and composite evidence for comparable families |
| `cross_domain_comparable_families.csv` | Explicit mapping between nonidentical domain representatives |
| `cross_domain_not_comparable.csv` | Items excluded from direct comparison and why |

These files do not pool raw Bitcoin and Electricity errors into one homogeneous task. They compare within-task ranks, scale-independent or baseline-relative performance, calibration, components, evidence availability, and mapped model-family behavior while preserving differences in target, scale, frequency, horizon, information updates, model formulation, and inference method.

# Artifact Integrity and SHA-256 Verification

[`authoritative_artifact_hashes.md`](authoritative_artifact_hashes.md) records the protected set and expected SHA-256 digest of each artifact. At this documentation update, it contains **52 protected artifacts**.

[`src/verify_research_artifacts.py`](../src/verify_research_artifacts.py) performs read-only existence, hash, schema, row/key, finiteness, alignment, metric, and analysis-structure checks. A live run at this update reported:

```text
SUMMARY: 313 PASS, 0 FAIL
```

The count is not a permanent architectural constant; it may increase when verification coverage expands. Run the verifier to obtain the current result. Stable claims are that the ledger defines the protected set and the verifier checks artifact identity and documented invariants.

# Research Artifact Policy

Scientific result tables should follow:

```text
authoritative artifact → load → validate → derive → display
```

They should not be manually transcribed into executable research code when machine-readable evidence exists. Appropriate constants include documented protocol settings, fixed configuration values, mathematically defined thresholds, and explicitly labeled historical provenance where no machine-readable evidence survives.

## Recommended Evidence Reading Order

### Bitcoin

1. `validated_forecasts.csv`
2. `bitcoin_point_forecast_metrics_v2.csv`
3. training-defined robustness and `bitcoin_temporal_stability.csv`
4. `bitcoin_uncertainty_evidence_v2.csv` and foundation interval artifacts
5. `bitcoin_dm_pairwise_results_hac_holm.csv`
6. v2 trustworthiness components and sensitivity

### Electricity

1. the appropriate Protocol A or B validated forecast matrix
2. validated overall/horizon metrics as applicable
3. protocol-specific robustness and Temporal Stability
4. `uncertainty_summary.csv`
5. protocol-specific trust scores and sensitivity
6. protocol-specific DM tests, effects, and horizon inference

Then consult the cross-domain artifacts, preserving the declared comparability mappings and exclusions.

# Safe Use of Research Artifacts

Do not:

- overwrite authoritative CSVs during exploration;
- manually edit numerical values in result artifacts;
- treat staging candidates as authoritative before validation and promotion;
- cite historical or superseded files as current conclusions;
- mix Electricity Protocol A and Protocol B evidence;
- interpret missing uncertainty evidence as zero uncertainty;
- treat non-significance as equivalence;
- treat the exploratory trust composite as a validated universal scale; or
- infer that hash validity alone proves scientific correctness.

# Related Documentation

- [Research overview](../README.md)
- [Notebook workflow](../notebooks/README.md)
- [Bitcoin case study](../docs/bitcoin_case_study.md)
- [Electricity case study](../docs/electricity_case_study.md)
- [Bitcoin reproducibility record](../docs/bitcoin_reproducibility.md)
- [Figure index](../figures/README.md)
- [Reusable source modules](../src/README.md)
