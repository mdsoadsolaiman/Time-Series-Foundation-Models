# Trustworthy Foundation Models for Time-Series Forecasting

## A Cross-Domain Study of Finance and Energy

This repository is an empirical research evidence base for evaluating time-series foundation models as forecasting systems rather than point-metric contestants. Zero-shot Chronos-Bolt-Tiny and TimesFM are compared with deterministic baselines, classical/statistical methods, and supervised neural models in two completed domains: daily Bitcoin prices and half-hourly South Australian electricity demand.

The study examines point accuracy alongside Regime-Conditional Robustness, Temporal Stability, uncertainty calibration, transparency/auditability, and dependence-aware statistical inference. Forecast vectors are frozen before downstream analysis so that reported conclusions can be reconstructed without rerunning expensive models.

## Research Questions

> Under what domain, horizon, and information-update conditions can zero-shot time-series foundation models be considered trustworthy relative to strong simple, statistical, and supervised neural benchmarks?

Secondary questions ask whether ranks remain stable across domains; how rolling updates differ from fixed-origin forecasting; whether aggregate accuracy agrees with conditional and temporal performance; whether prediction intervals attain nominal coverage; whether evidence is reproducible and auditable; and whether loss differences survive dependence-aware testing, multiplicity correction, and effect-size analysis.

Only **Bitcoin / Finance** and **South Australian Electricity Demand / Energy** are completed. Weather and Transport are planned extensions with no reported results.

## Trustworthiness Framework

| Dimension | Meaning in this study | Does not establish |
|---|---|---|
| Accuracy | MAE, RMSE, MAPE, sMAPE, and task-specific MASE | Universal superiority under other losses or horizons |
| Regime-Conditional Robustness | Error within predeclared market, demand, volatility, and peak-event regimes | Adversarial or universal robustness |
| Temporal Stability | Error across contiguous Earlier, Middle, and Later test segments | Geographic, cross-dataset, causal, or broad OOD generalisation |
| Uncertainty Calibration | Nominal versus empirical coverage, width, and proper scores where available | Complete probabilistic quality from coverage alone |
| Transparency / Auditability | Mechanism clarity, implementation simplicity, reproducibility, determinism evidence, failure detectability, and checkpoint dependence | Explainable-AI attribution or faithfulness |
| Statistical Inference | Dependence-aware pairwise loss tests, multiplicity correction, and effects | A component of the Trust Score |

Component evidence is primary. A secondary **Exploratory Composite Trustworthiness Summary** uses researcher-defined weights: Accuracy 35%, Robustness 20%, Temporal Stability 20%, Uncertainty 15%, and Transparency/Auditability 10%.

`T = 0.35A + 0.20R + 0.20Ts + 0.15U + 0.10E`

Scores are comparison-set-relative: 100 means best observed in the evaluated roster, not perfect quality. Components overlap, weights are not empirically validated, and the composite is not a universal measurement instrument.

## Empirical Domains and Datasets

| Domain | Dataset and target | Frequency | Final protocol(s) | Test size | Status |
|---|---|---|---|---:|---|
| Finance | Bitcoin BTC/USD daily Close, aggregated from local minute OHLCV | Daily | Rolling one-step | 1,061 targets | Completed |
| Energy | Australian Electricity Demand, South Australia T4 | 30 minutes | A: rolling one-step; B: fixed-origin 48-step day-ahead | 46,176 targets; 962 origins | Completed |
| Weather | Dataset and protocol not selected | — | — | — | Planned |
| Transport | Dataset and protocol not selected | — | — | — | Planned |

Bitcoin covers 2012-01-01 through 2026-07-07. Its original provider, download URL, and redistribution licence are not verified locally and are not inferred here. The final date contains data only through 01:57 UTC and remains a documented partial daily observation in `bitcoin-v1`.

Electricity T4 contains 230,784 contiguous half-hourly observations from 2002-01-01 through 2015-03-01. Development, validation, and test partitions contain 166,128, 18,480, and 46,176 observations. See [data/README.md](data/README.md) and [data/bitcoin/README.md](data/bitcoin/README.md).

## Evaluated Models

| Family | Models |
|---|---|
| Deterministic | Naive; 7-Day Moving Average; Electricity Daily/Weekly Seasonal Naive and Moving Average |
| Statistical | SES; additive-trend smoothing/Holt-Winters artifact; ARIMA; SARIMA; DHR-ARIMA; Prophet |
| Supervised neural | Bitcoin PE Log-Return LSTM and Transformer; protocol-specific Electricity LSTM |
| Zero-shot foundation | Chronos-Bolt-Tiny; TimesFM |

Bitcoin has **10 final analytical models**. Electricity has **13 models per protocol**. Moirai/Uni2TS is deferred; PatchTST and iTransformer are possible future supervised comparators, not current evidence.

## Experimental Protocols

### Bitcoin

Each model predicts day `t` from information strictly before `t`. Actual `t` is revealed only afterward and may inform the next origin. Models retain auditable but intentionally different state rules: deterministic formulas, per-origin fitting, sequential state updates, periodic refits, supervised training, or zero-shot inference. Chronos and TimesFM use the last 128 prices.

### Electricity Protocol A

At every half-hour, a model predicts `t` using earlier observations. Actual `t` is released after prediction and may update the context for `t+1`. Each model supplies 46,176 forecasts.

### Electricity Protocol B

At each of 962 midnight origins, a model produces all 48 half-hour forecasts from one fixed information set. No actual inside that day is revealed before the vector is complete. Protocol B is not stitched from rolling one-step predictions. Separating A and B exposes the effect of information-update discipline and operational horizon.

## Authoritative Accuracy Results

Tables are reconstructed from frozen vectors. Rankings use MAE; MASE has the same within-task ordering.

### Bitcoin — 10 models

Source: [`bitcoin_point_forecast_metrics_v2.csv`](results/bitcoin_point_forecast_metrics_v2.csv).

| Rank | Model | MAE | RMSE | MASE |
|---:|---|---:|---:|---:|
| 1 | Naive | 1290.353242 | 1853.624774 | 4.575633 |
| 2 | SES — Rolling One-Step | 1290.358684 | 1855.731424 | 4.575652 |
| 3 | ARIMA Rolling One-Step | 1299.874638 | 1866.302859 | 4.609396 |
| 4 | Additive-Trend Exponential Smoothing | 1308.541314 | 1871.702185 | 4.640128 |
| 5 | PE Log-Return LSTM | 1321.365311 | 1881.091190 | 4.685603 |
| 6 | TimesFM | 1349.946786 | 1924.199337 | 4.786953 |
| 7 | Chronos-Bolt-Tiny | 1424.025828 | 1994.007926 | 5.049640 |
| 8 | PE Log-Return Transformer | 2019.366342 | 2559.749810 | 7.160736 |
| 9 | 7-Day Moving Average | 2209.776153 | 2999.605073 | 7.835935 |
| 10 | Prophet — 30-Day Periodic Refit | 8195.262862 | 10781.162873 | 29.060658 |

Bitcoin strongly rewards persistence: neither foundation model beats the four leading simple/statistical systems or PE-LSTM.

### Electricity Protocol A — 13 models

Source: [`protocol_a_validated_forecasts.csv`](results/electricity/protocol_a_validated_forecasts.csv).

| Rank | Model | MAE | RMSE | MASE-48 |
|---:|---|---:|---:|---:|
| 1 | TimesFM | 16.388292 | 26.500200 | 0.140002 |
| 2 | SARIMA | 17.131137 | 25.350360 | 0.146347 |
| 3 | DHR-ARIMA | 26.646643 | 50.289317 | 0.227636 |
| 4 | ARIMA | 28.881334 | 51.681366 | 0.246727 |
| 5 | Chronos-Bolt-Tiny | 32.332012 | 44.879089 | 0.276205 |
| 6 | Naive | 42.271787 | 58.272152 | 0.361118 |
| 7 | LSTM | 47.019068 | 71.565540 | 0.401673 |
| 8 | Daily Seasonal Naive | 129.416180 | 200.442098 | 1.105573 |
| 9 | Weekly Seasonal Naive | 153.210769 | 267.161682 | 1.308845 |
| 10 | Prophet | 177.109255 | 243.849558 | 1.513005 |
| 11 | Moving Average | 179.122226 | 227.658772 | 1.530201 |
| 12 | Holt-Winters | 179.622941 | 269.632642 | 1.534479 |
| 13 | Simple Exponential Smoothing | 243.838177 | 301.681215 | 2.083055 |

### Electricity Protocol B — 13 models

Source: [`protocol_b_validated_forecasts.csv`](results/electricity/protocol_b_validated_forecasts.csv).

| Rank | Model | MAE | RMSE | MASE-48 |
|---:|---|---:|---:|---:|
| 1 | TimesFM | 80.675384 | 126.984300 | 0.689192 |
| 2 | SARIMA | 122.782256 | 196.035241 | 1.048901 |
| 3 | Chronos-Bolt-Tiny | 126.119534 | 188.844105 | 1.077411 |
| 4 | Daily Seasonal Naive | 129.416180 | 200.442098 | 1.105573 |
| 5 | LSTM | 152.926817 | 210.523254 | 1.306420 |
| 6 | Weekly Seasonal Naive | 153.210769 | 267.161682 | 1.308845 |
| 7 | Prophet | 177.109255 | 243.849558 | 1.513005 |
| 8 | Holt-Winters | 179.622941 | 269.632642 | 1.534479 |
| 9 | Moving Average | 203.199277 | 260.260560 | 1.735886 |
| 10 | Simple Exponential Smoothing | 243.838177 | 301.681215 | 2.083055 |
| 11 | Naive | 243.838179 | 301.681217 | 2.083055 |
| 12 | DHR-ARIMA | 287.456183 | 329.891048 | 2.455674 |
| 13 | ARIMA | 521.970508 | 569.249822 | 4.459077 |

TimesFM has the lowest MAE under both Electricity protocols, but not the lowest Protocol A RMSE: SARIMA has lower squared-error loss. DHR-ARIMA’s fall from third one-step to twelfth day-ahead demonstrates protocol sensitivity.

![Model ranks across completed tasks](figures/cross_domain/model_rank_across_domains.png)

## Accuracy Is Not Trustworthiness

TimesFM leads Electricity by MAE but its native intervals substantially under-cover. Chronos is less point-accurate but closer to nominal marginal coverage. Bitcoin’s strongest models are simple or classical, and conditional analyses expose behavior hidden by aggregate ranks. Complexity therefore does not imply trustworthy performance.

## Uncertainty Calibration

| Task | Nominal | Chronos coverage | TimesFM coverage | Lower absolute coverage error |
|---|---:|---:|---:|---|
| Bitcoin rolling one-step | 80% | 84.5429% | 33.0820% | Chronos |
| Electricity A | 80% | 91.1231% | 33.6495% | Chronos |
| Electricity B | 80% | 67.6239% | 24.5604% | Chronos |

Chronos has lower absolute error from nominal 80% marginal coverage in these three tasks. This is not universal calibration superiority: width, sharpness, conditional coverage, checkpoint, and task matter. Bitcoin training-only conformal adjustment changes Chronos to 81.5269% and TimesFM to 55.6079%; TimesFM remains below nominal. Electricity reports only preserved native foundation-model intervals and does not fabricate deterministic-model uncertainty.

![Native 80% interval calibration](figures/cross_domain/uncertainty_calibration_across_domains.png)

## Regime-Conditional Robustness and Temporal Stability

Bitcoin regimes use training-only return and volatility thresholds. Electricity uses frozen pre-test demand, peak-event, and volatility thresholds. Conditional rankings can differ from aggregate rankings—for example, Bitcoin’s PE Transformer is weak overall but unusually strong in the major-downward regime.

Temporal Stability divides the test into contiguous Earlier, Middle, and Later segments and asks whether aggregate results are concentrated in one period. It does not establish broad OOD generalisation. Electricity artifact filenames retain historical `generalisation` terminology for hash stability; public analysis uses **Temporal Stability**.

## Trustworthiness Synthesis

Two variants expose missing evidence:

- **Missing-evidence-penalised:** an unavailable dimension contributes zero.
- **Evidence-available:** weights are renormalized across measured dimensions.

Missing uncertainty means “not measured,” not “measured and poor.” Corrected Bitcoin v2 penalised leaders are Naive (`97.051891`), SES (`96.970846`), ARIMA (`96.266697`), and additive-trend smoothing (`96.179827`). PE-LSTM changes from `81.342547` penalised to `95.697114` on available dimensions.

In the 13-model Electricity artifacts, TimesFM leads both variants under both protocols. Protocol A’s penalised leaders are TimesFM (`92.033198`) and SARIMA (`77.218028`); Protocol B’s are TimesFM (`91.078842`) and Chronos (`66.311491`). Composite scores remain secondary and do not erase component weaknesses such as undercoverage.

## Statistical Inference

| Task | Models / pairs | Design | HAC lag | Correction |
|---|---:|---|---:|---|
| Bitcoin | 10 / 45 | Daily squared-error DM tests | 6 | Holm family-wise control |
| Electricity A | 13 / 78 | Half-hourly squared-error differentials | 48 | Benjamini–Hochberg FDR |
| Electricity B | 13 / 78 | Daily-origin mean squared error | 7 | Benjamini–Hochberg FDR |

Bitcoin has 39 raw-significant and 33 Holm-significant pairs at 5%. Electricity has 77 BH-significant pairs in A and 68 in B. Effect-size tables accompany p-values. In Protocol A, TimesFM has lower MAE than SARIMA, but SARIMA wins their squared-error comparison (`BH p = 0.0000956209577590908`). Non-significance does not establish equivalence.

## Cross-Domain Findings

1. Foundation models are not universally dominant: TimesFM ranks sixth in Bitcoin and first in both Electricity protocols.
2. Strong baselines remain essential: persistence leads Bitcoin, while SARIMA ranks second by MAE in both Electricity protocols.
3. Horizon and update discipline materially affect ranks.
4. Point accuracy and calibration can disagree sharply.
5. Complexity does not guarantee trustworthiness.
6. Frozen, protocol-specific evidence makes comparisons auditable without conflating artifact reproduction with model regeneration.

## Reproducibility and Artifact Integrity

The protected ledger contains **52 artifacts**. A live read-only verifier run on 2026-08-15 returned:

```text
SUMMARY: 313 PASS, 0 FAIL
```

The verifier checks hashes, schemas, row counts, keys, timestamps, finite values, metric reproduction, corrected Bitcoin evidence structures, Electricity Protocol B horizon completeness, and cross-domain loading. See [`authoritative_artifact_hashes.md`](results/authoritative_artifact_hashes.md) and [`results/README.md`](results/README.md).

- **Artifact-level reproducibility is demonstrated:** frozen vectors support repeatable validation, metrics, conditional analysis, inference, synthesis, and figures without model packages.
- **Full end-to-end regeneration is not claimed:** it requires raw-data access, exact checkpoints, compatible full dependencies, and substantial computation. Remote checkpoint revisions were not pinned, and the historical generation environment has not been freshly reconstructed.

Candidate generation is separated from validation and explicit promotion; routine analysis does not overwrite frozen evidence.

## Notebook Workflow

- **Bitcoin:** [`01_Bitcoin_Data_EDA.ipynb`](notebooks/01_Bitcoin_Data_EDA.ipynb) through [`12_Bitcoin_Trustworthiness_Synthesis.ipynb`](notebooks/12_Bitcoin_Trustworthiness_Synthesis.ipynb), with [`Bitcoin_Master.ipynb`](notebooks/Bitcoin_Master.ipynb) as the compact artifact-driven entry point.
- **Electricity:** [`10_Electricity_EDA.ipynb`](notebooks/electricity/10_Electricity_EDA.ipynb) through [`18_Electricity_Statistical_Significance.ipynb`](notebooks/electricity/18_Electricity_Statistical_Significance.ipynb): EDA → classical models → LSTM → foundation models → validation → robustness/Temporal Stability → uncertainty → trustworthiness → inference.
- **Cross-domain:** [`18_Cross_Domain_Comparison.ipynb`](notebooks/18_Cross_Domain_Comparison.ipynb), an artifact-only synthesis using within-task ranks and scale-independent evidence.

## Repository Structure

```text
Time-Series-Foundation-Models/
├── data/          # Datasets, provenance, and policy
├── notebooks/     # Domain workflows and synthesis
├── results/       # Frozen forecasts and evidence
├── figures/       # Publication and diagnostic figures
├── docs/          # Case studies and reproducibility
├── src/           # Pipelines, metrics, validation, builders
├── tests/         # Helper and pipeline tests
├── tools/         # Controlled rebuild utilities
├── paper/         # Manuscript and bibliography
└── proposal/      # Forward-looking proposal
```

## Environment

[`requirements-research.txt`](requirements-research.txt) records the historical research dependency set, including TensorFlow 2.21.0, PyTorch 2.12.1, `chronos-forecasting` 2.3.1, and TimesFM 2.0.2. The CPU-only forecast-generation record used Python 3.13.2 on Windows.

The supported lightweight artifact-analysis path is Python 3.12 on Windows using [`requirements-bitcoin-artifact.txt`](requirements-bitcoin-artifact.txt). It verifies frozen evidence but does not regenerate neural or foundation-model forecasts. [`requirements.txt`](requirements.txt) is a historical minimal file, not the complete research lock.

## Limitations

- Two completed domains and one asset/series per domain.
- One frozen evaluation period per domain; dataset, target, frequency, horizon, and domain effects cannot be separated.
- Different cross-domain protocols and neural formulations.
- Only two foundation-model checkpoints; no fine-tuning.
- Unknown pretraining overlap and unpinned checkpoint revisions.
- Missing uncertainty for several models and one principal Electricity interval level.
- Electricity B exact interval vectors were not preserved; aggregates remain.
- Researcher-defined, comparison-relative trust composite and transparency rubric.
- Conditional robustness is descriptive, not adversarial.
- Partial final Bitcoin day and unresolved Bitcoin provider/licence provenance.
- No repository licence file.
- Artifact reproducibility does not equal full regeneration.

## Future Work

Planned work includes Weather and Transport; additional Electricity regions; more foundation-model families/scales; Moirai in a compatible environment; PatchTST/iTransformer supervised comparators; richer interval levels and proper scoring; conditional calibration; broader rolling-origin evaluation; pretraining-contamination audits; and alternative trust-weight sensitivity. None is current evidence.

## Research Documentation

- [Bitcoin case study](docs/bitcoin_case_study.md) — detailed workflow; corrected v2 artifacts remain numeric authority.
- [Electricity case study](docs/electricity_case_study.md) — detailed background; some rankings and notebook references predate the 13-model 10–18 workflow.
- [Bitcoin reproducibility record](docs/bitcoin_reproducibility.md)
- [Result artifact guide](results/README.md)
- [Figure index](figures/README.md)
- [Research manuscript](paper/research_manuscript.md) and [verified references](paper/references.md) — some result summaries predate full-roster evidence.
- [Research proposal](proposal/Research_Proposal.md) — forward-looking, not authority for final rankings.

## Citation and Licence Status

Formal repository citation metadata has not been provided. Until an author-approved citation is added, cite the underlying datasets, model papers, and software using [`paper/references.md`](paper/references.md), and record the repository URL and accessed revision.

No repository licence file is present. Its absence must not be interpreted as permission to redistribute code or data. Bitcoin provider attribution and redistribution terms require external verification.
