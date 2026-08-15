# Trustworthy Foundation Models for Time-Series Forecasting:
## Evaluating Accuracy, Robustness, Temporal Stability, Uncertainty, and Auditability Across Domains

**Cross-Domain Empirical Study | Time-Series Foundation Models | Trustworthy AI | Forecasting | Uncertainty | Reproducibility**

Time-series foundation models promise transferable forecasting ability without conventional domain-specific training. That promise is important: a reusable model may reduce the cost of building forecasting systems for new datasets, horizons, and operational settings. Yet aggregate point accuracy alone does not establish whether a forecast can be trusted. A model may rank well on average while failing during volatile periods, becoming unstable over time, producing poorly calibrated intervals, or depending on mutable external checkpoints that are difficult to audit.

This research evaluates forecasting systems as **trustworthy systems**, not merely accuracy contestants. Zero-shot Chronos-Bolt-Tiny and TimesFM are compared with deterministic baselines, classical and statistical methods, and supervised neural models. The completed experiments cover two deliberately contrasting domains: daily Bitcoin prices in Finance and half-hourly South Australian electricity demand in Energy.

The study separates forecast generation from evaluation. Accepted forecast vectors are frozen and hash-protected before downstream analyses of Accuracy, Regime-Conditional Robustness, Temporal Stability, Uncertainty, Auditability/Transparency, and statistical inference. Weather and Transport are planned extensions; they are not part of the completed evidence.

## Research Question

> Under what domain, horizon, and information-update conditions can zero-shot time-series foundation models be considered trustworthy relative to strong deterministic, statistical, and supervised neural forecasting systems?

The empirical programme also asks:

1. Are foundation-model accuracy ranks stable across heterogeneous domains and protocols?
2. Does performance remain competitive in difficult domain-specific regimes and across the evaluation period?
3. Do native predictive intervals attain credible coverage without relying on width alone?
4. Can forecasts, assumptions, dependencies, and downstream results be independently inspected and reproduced from preserved evidence?
5. Do observed loss differences survive serial-dependence adjustment, multiple-comparison correction, and practical effect-size analysis?

## Why This Research Matters

Forecasting decisions are often consequential precisely when average conditions do not apply. Financial markets can enter extreme movement and volatility regimes. Electricity systems require forecasts at operational horizons where new observations may or may not be available. A model’s ranking can therefore change with the information set, target structure, loss function, and interval requirement.

> **Accuracy is evidence of forecast quality; it is not, by itself, evidence of trustworthiness.**

| Conventional benchmarking | This research |
|---|---|
| Aggregate error | Aggregate and conditional error |
| One leaderboard | Domain- and protocol-sensitive rankings |
| Point forecasts | Point forecasts and preserved uncertainty evidence |
| Average performance | Regime-conditional and temporal performance |
| Reproduction assumed | Forecast identity and artifact integrity audited |
| P-values alone | Dependence-aware inference, multiplicity correction, and effect sizes |

The distinction is central to trustworthy AI: a useful forecasting system must be evaluated not only by what it predicts, but also by when it fails, how confidence is expressed, whether evidence is stable under review, and what claims the completed experiment can legitimately support.

## Research Design

```text
Canonical domain data
        ↓
EDA, data quality, and chronological partitions
        ↓
Forecasting protocol and information boundary
        ↓
Deterministic │ Statistical │ Supervised Neural │ Foundation Models
        ↓
Frozen, validated forecast evidence
        ↓
Accuracy ─┬─ Regime-Conditional Robustness
          ├─ Temporal Stability
          ├─ Uncertainty Calibration
          ├─ Auditability / Transparency
          └─ Dependence-Aware Statistical Inference
        ↓
Component-first trustworthiness and cross-domain synthesis
```

The design holds final test periods and protocol rules fixed across each domain’s comparison set. It does not assume that every model has the same internal update mechanism: deterministic formulas, sequential state updates, periodic refits, supervised training, and zero-shot inference remain methodologically distinct but must obey the same legally available information at each forecast origin.

## Empirical Domains

| Domain | Series | Frequency | Forecasting task | Models | Status |
|---|---|---|---|---:|---|
| Finance | Bitcoin BTC/USD daily Close | Daily | Rolling one-step over 1,061 test targets | 10 | Completed |
| Energy | South Australia T4 electricity demand | 30 minutes | Rolling one-step and 962 fixed-origin 48-step day-ahead forecasts | 13 per protocol | Completed |
| Weather | Dataset and frozen protocol not selected | — | Future extension | — | Planned |
| Transport | Dataset and frozen protocol not selected | — | Future extension | — | Planned |

Bitcoin is a volatile, non-stationary price-level task with heavy-tailed returns and weak weekly seasonality. Its completed comparison is strongly persistence-dominated. Electricity demand has pronounced daily and weekly structure and supports operationally distinct short-horizon and day-ahead protocols. This contrast tests whether zero-shot transfer remains useful when temporal structure and information-release rules change substantially.

Dataset provenance, quality checks, temporal coverage, and chronological partitions are documented in [`data/README.md`](data/README.md).

## Model Landscape

| Family | Evaluated systems |
|---|---|
| Deterministic | Naive persistence; 7-Day Moving Average; Daily and Weekly Seasonal Naive; Electricity Moving Average |
| Statistical | Simple Exponential Smoothing; additive-trend smoothing / Holt-Winters artifact; ARIMA; SARIMA; DHR-ARIMA; periodically refitted Prophet |
| Supervised neural | Bitcoin Persistence-Enhanced Log-Return LSTM and Transformer; protocol-specific Electricity LSTM |
| Zero-shot foundation | **Chronos-Bolt-Tiny**; **TimesFM** |

Chronos-Bolt-Tiny and TimesFM receive no Bitcoin- or Electricity-specific gradient training. They forecast from legally available historical context using pretrained checkpoints. The evidence applies to the evaluated checkpoints and configurations—not to every model size, release, or time-series foundation model.

Moirai/Uni2TS has no authoritative run in the current environment. PatchTST and iTransformer are planned supervised comparators rather than completed zero-shot foundation-model evidence.

## Trustworthiness Framework

### Accuracy

**Question:** Does the model forecast accurately over the aggregate frozen test?

**Evidence:** MAE, RMSE, MAPE, sMAPE, Bitcoin MASE-1, and Electricity MASE-48.

### Regime-Conditional Robustness

**Question:** Does performance remain competitive in difficult domain-specific conditions?

**Evidence:** Training/pre-test-defined volatility, movement, demand, and peak-event regimes evaluated from frozen forecast errors. This is conditional robustness, not adversarial robustness.

### Temporal Stability

**Question:** Is performance distributed across the evaluation period rather than concentrated in one interval?

**Evidence:** Comparable Earlier, Middle, and Later chronological segments. This is within-test stability, not broad geographic or out-of-distribution generalisation.

### Uncertainty

**Question:** Do preserved prediction intervals attain their nominal marginal coverage with interpretable width?

**Evidence:** Native foundation quantiles, training-only calibrated foundation intervals, validation-residual empirical intervals where supported, coverage error, width, and proper interval scores where available.

### Auditability / Transparency

**Question:** Can the evidence, mechanisms, protocol assumptions, dependencies, and failure modes be independently inspected?

**Evidence:** Frozen vectors, schemas, hashes, deterministic reconstruction, implementation and checkpoint provenance, reproducibility controls, and an explicit researcher-defined rubric. This is not direct explainable-AI attribution.

### Statistical Inference

Statistical inference is an additional layer, not a Trust Score component. It tests whether observed squared-error loss differences survive serial dependence, protocol-appropriate sampling, multiple-comparison correction, and consideration of practical effects.

## Experimental Protocols

| Property | Bitcoin | Electricity Protocol A | Electricity Protocol B |
|---|---|---|---|
| Target/horizon | Next daily Close | Next 30-minute demand | Next 48 half-hours / 24 hours |
| Update discipline | Actual revealed after each daily forecast | Actual revealed after each half-hour forecast | No actual revealed within the 48-step block |
| Final evaluation | 1,061 daily targets | 46,176 half-hourly targets | 962 origins × 48 horizons = 46,176 targets |
| Operational interpretation | Daily rolling one-step | Frequently updated short-horizon forecast | Fixed-origin day-ahead forecast |
| Foundation context | Last 128 prices | Last 336 demand observations | Same 336-observation context for the full day |

Protocol A and Protocol B use the same Electricity test series but answer different operational questions. Protocol A continually incorporates newly observed demand; Protocol B must sustain a full day’s forecast without within-horizon correction. Results are therefore reported separately.

## Headline Results

The detailed metric tables remain in machine-readable artifacts and the [result evidence guide](results/README.md). The scholarship-facing findings are summarized here.

### Bitcoin

The final comparison contains ten models. By MAE, Naive ranks first, rolling Simple Exponential Smoothing second, and rolling ARIMA third. TimesFM ranks sixth and Chronos-Bolt-Tiny seventh. The result indicates that transferable model complexity does not overcome a strong persistence-dominated benchmark in this daily financial task.

### Electricity — Protocol A

Among 13 models, TimesFM ranks first by MAE, SARIMA second, and DHR-ARIMA third. SARIMA nevertheless has lower RMSE than TimesFM, demonstrating that the leading model depends on the loss definition as well as the protocol.

### Electricity — Protocol B

Among the same 13 model families under fixed-origin day-ahead forecasting, TimesFM ranks first by MAE, SARIMA second, and Chronos-Bolt-Tiny third. Daily Seasonal Naive ranks fourth, remaining a strong operational benchmark.

| Task | Best model by MAE | Foundation-model result | Main lesson |
|---|---|---|---|
| Bitcoin rolling one-step | Naive | TimesFM 6th; Chronos 7th | Simple persistence/statistical systems dominate |
| Electricity A | TimesFM | TimesFM 1st; Chronos 5th | Zero-shot transfer is strong, but SARIMA is highly competitive and has lower RMSE |
| Electricity B | TimesFM | TimesFM 1st; Chronos 3rd | Day-ahead information constraints change the competitive order |

<p align="center">
  <img src="figures/cross_domain/model_rank_across_domains.png" width="820" alt="Within-task model ranks across Bitcoin and Electricity protocols">
</p>
<p align="center"><em>Within-task ranks change materially across the completed domain–protocol combinations; lower rank is better.</em></p>

## Cross-Domain Key Finding

**TimesFM is not universally dominant.** It trails several simple, statistical, and supervised systems in Bitcoin while leading both Electricity protocols by MAE. Chronos also changes position across the tasks. The evidence therefore supports a task-bounded conclusion: foundation-model value is conditional on domain structure, horizon, benchmark strength, and information-update discipline.

This is evidence of domain- and protocol-dependent performance within two completed datasets, not proof of a pure causal “domain effect.” Frequency, target semantics, evaluation period, and horizon also differ.

## Accuracy versus Uncertainty

The most accurate point forecaster is not necessarily the best calibrated probabilistic forecaster. The current common native evidence uses nominal 80% intervals:

| Task | Nominal | Chronos coverage | TimesFM coverage | Lower absolute coverage error |
|---|---:|---:|---:|---|
| Bitcoin rolling one-step | 80% | 84.5429% | 33.0820% | Chronos |
| Electricity A | 80% | 91.1231% | 33.6495% | Chronos |
| Electricity B | 80% | 67.6239% | 24.5604% | Chronos |

Chronos is closer to nominal coverage in all three evaluated native-interval tasks, despite TimesFM’s stronger Electricity point accuracy. This does not establish universal calibration superiority: coverage must be considered alongside width, conditional behavior, checkpoint, interval construction, and task.

Bitcoin also preserves training-only CQR adjustment. Chronos moves from 84.5429% to 81.5269% coverage; TimesFM moves from 33.0820% to 55.6079% and remains below nominal. Electricity does not fabricate intervals for deterministic models without preserved pre-test uncertainty evidence.

<p align="center">
  <img src="figures/cross_domain/uncertainty_calibration_across_domains.png" width="760" alt="Native 80 percent interval coverage for Chronos and TimesFM">
</p>
<p align="center"><em>Native 80% marginal coverage differs sharply from the nominal target, particularly for TimesFM.</em></p>

## Robustness and Temporal Stability

Aggregate winners need not be conditional winners. Bitcoin evaluates low/high volatility and major upward/downward movements using thresholds fixed from training data. Electricity evaluates pre-test-defined demand, peak-event, and volatility conditions under each protocol. The analyses report regime error and comparison-relative robustness rather than claiming resilience to arbitrary perturbations.

Temporal Stability divides each test into contiguous Earlier, Middle, and Later segments. It reveals whether an aggregate score is supported throughout the period or disproportionately driven by one interval. Bitcoin’s PE Transformer, for example, is weak in aggregate but unusually competitive during major downward movements; such behavior would be hidden by a single leaderboard.

The current publication figure set contains no standalone robustness or Temporal Stability plot that is both cross-domain and traceable through the paper-figure catalog. This README therefore reports the implemented evidence without substituting a diagnostic or fabricating a new visualization. Detailed tables and notebook plots are available through the [workflow guide](notebooks/README.md).

## Trustworthiness Synthesis

The exploratory composite provides a compact sensitivity-oriented summary across heterogeneous evidence. It is useful for asking whether conclusions remain recognizable when more than accuracy is considered; it does not replace the underlying dimensions.

`T = 0.35A + 0.20R + 0.20Ts + 0.15U + 0.10E`

where `A` is Accuracy, `R` Regime-Conditional Robustness, `Ts` Temporal Stability, `U` Uncertainty, and `E` Auditability/Transparency. The weights are researcher-defined, components are dependent, normalization changes with the comparison set, and the score is not a validated universal scale.

Two formulations are retained:

- **Missing-evidence-penalised:** an unavailable dimension contributes zero.
- **Evidence-available:** weights are renormalized over measured dimensions.

| Task | Leading penalised composite | Interpretation |
|---|---|---|
| Bitcoin | Naive, 97.051891 | Leading simple/classical systems combine strong accuracy, stability, and auditability |
| Electricity A | TimesFM, 92.033198 | Broad component strength, but poor interval coverage remains visible |
| Electricity B | TimesFM, 91.078842 | Leading exploratory synthesis under the day-ahead protocol |

Missing uncertainty means “not measured,” not “measured and poor.” Component evidence should be read before composite ranks.

<p align="center">
  <img src="figures/cross_domain/trustworthiness_evidence_matrix.png" width="820" alt="Cross-domain trustworthiness component evidence matrix">
</p>
<p align="center"><em>Component evidence exposes accuracy, robustness, stability, calibration, and availability trade-offs without relying on a single universal score.</em></p>

## Statistical Inference

| Task | Models / pairs | Primary loss and sampling unit | HAC lag | Multiple-comparison control |
|---|---:|---|---:|---|
| Bitcoin | 10 / 45 | Daily squared-error differential | 6 | Holm family-wise error rate |
| Electricity A | 13 / 78 | Half-hourly squared-error differential | 48 | Benjamini–Hochberg false discovery rate |
| Electricity B | 13 / 78 | Daily-origin mean squared error across 48 horizons | 7 | Benjamini–Hochberg false discovery rate |

Bitcoin records 33 Holm-significant pairs at 5%. Electricity records 77 BH-significant pairs under Protocol A and 68 under Protocol B. Effect-size artifacts accompany the tests, and Electricity includes HAC sensitivity and selected horizon-specific evidence.

Two findings illustrate why inference is separate from rank reporting. First, the leading Bitcoin systems Naive and SES are not significantly distinguishable under the corrected family-wide analysis. Second, TimesFM has lower Protocol A MAE than SARIMA, while SARIMA has significantly lower squared-error loss in their BH-adjusted comparison. Non-significance is not interpreted as equivalence, and adjusted counts are not compared across Holm and BH as if the procedures were identical.

## Research Contributions

This study contributes:

1. A cross-domain empirical comparison of zero-shot foundation forecasters against deterministic, statistical, and supervised neural baselines.
2. A multidimensional evaluation framework that extends beyond aggregate point accuracy.
3. Explicit separation of forecasting horizon and information-update discipline through two Electricity protocols.
4. Training/pre-test-defined regime diagnostics and contiguous Temporal Stability analysis.
5. Method-labeled uncertainty evaluation that distinguishes native, calibrated, empirical, and unavailable evidence.
6. Dependence-aware statistical inference with domain-specific multiple-comparison procedures and practical effect sizes.
7. Frozen forecast artifacts that enable low-cost reconstruction of downstream results without silently rerunning models.
8. A transparent boundary between demonstrated artifact reproducibility and unverified complete end-to-end regeneration.

These contributions are methodological and empirical. They do not establish universal model superiority, universal trustworthiness, or deployment readiness.

## Reproducibility and Auditability

```text
model generation → validated forecast vectors → SHA-256 freeze → downstream evidence
```

The protected ledger currently contains 52 artifacts. A live read-only execution of `python src/verify_research_artifacts.py` during this README update returned:

```text
SUMMARY: 313 PASS, 0 FAIL
```

The count may grow as verification coverage expands; it is not a permanent research result. The verifier checks hashes, schemas, rows and keys, timestamps, finiteness, metric reproduction, protocol structure, and corrected evidence families.

- **Artifact-level reproducibility is demonstrated:** accepted forecasts can be validated and used to reproduce metrics, conditional analyses, calibration summaries, inference, synthesis, and figures.
- **Full end-to-end regeneration is not claimed:** it additionally requires exact raw-source acquisition, compatible full-generation dependencies, external checkpoints, and substantial computation. Remote checkpoint revisions were not pinned.

See the [research artifact guide](results/README.md) and [SHA-256 ledger](results/authoritative_artifact_hashes.md) for evidence authority, lineage, staging, promotion, and historical-file status.

## Research Workflow

| Stage | Bitcoin | Electricity |
|---|---|---|
| Data and EDA | [01](notebooks/01_Bitcoin_Data_EDA.ipynb) | [10](notebooks/electricity/10_Electricity_EDA.ipynb) |
| Classical/statistical benchmarks | [02](notebooks/02_Bitcoin_Classical_Baselines.ipynb), [05](notebooks/05_Bitcoin_Prophet_and_Deferred_Models.ipynb) | [11](notebooks/electricity/11_Electricity_Classical_Baselines.ipynb) |
| Supervised neural models | [03](notebooks/03_Bitcoin_PE_LSTM.ipynb), [04](notebooks/04_Bitcoin_PE_Transformer.ipynb) | [12](notebooks/electricity/12_Electricity_LSTM.ipynb) |
| Foundation models | [06](notebooks/06_Bitcoin_Foundation_Models.ipynb) | [13](notebooks/electricity/13_Electricity_Foundation_Models.ipynb) |
| Forecast validation | [07](notebooks/07_Bitcoin_Forecast_Freeze_and_Validation.ipynb), [08](notebooks/08_Bitcoin_Naive_Audit.ipynb) | [14](notebooks/electricity/14_Electricity_Model_Validation_Audit.ipynb) |
| Robustness / Temporal Stability | [09](notebooks/09_Bitcoin_Robustness_and_Temporal_Stability.ipynb) | [15](notebooks/electricity/15_Electricity_Robustness.ipynb) |
| Uncertainty | [10](notebooks/10_Bitcoin_Uncertainty.ipynb) | [16](notebooks/electricity/16_Electricity_Uncertainty.ipynb) |
| Trustworthiness synthesis | [12](notebooks/12_Bitcoin_Trustworthiness_Synthesis.ipynb) | [17](notebooks/electricity/17_Electricity_Trustworthiness.ipynb) |
| Statistical inference | [11](notebooks/11_Bitcoin_Statistical_Inference.ipynb) | [18](notebooks/electricity/18_Electricity_Statistical_Significance.ipynb) |

The final synthesis is [`18_Cross_Domain_Comparison.ipynb`](notebooks/18_Cross_Domain_Comparison.ipynb). It compares within-task ranks, scale-independent and baseline-relative evidence, calibration, components, and explicitly mapped model families. It does not pool raw Bitcoin and Electricity errors into one homogeneous task.

See [`notebooks/README.md`](notebooks/README.md) for research questions, inputs, outputs, execution classes, and reading paths for every notebook.

## Repository Structure

```text
Time-Series-Foundation-Models/
├── data/          # Canonical local datasets and provenance documentation
├── notebooks/     # Bitcoin 01–12, Electricity 10–18, cross-domain synthesis
├── results/       # Frozen forecasts, derived evidence, and hash ledger
├── figures/       # Bitcoin, Electricity, and cross-domain research figures
├── src/           # Data, metric, pipeline, validation, and figure utilities
├── tests/         # Helper and pipeline tests
├── tools/         # Controlled rebuild utilities
├── paper/         # Verified academic bibliography
└── proposal/      # Forward-looking research proposal
```

Navigation:

- [Research data](data/README.md)
- [Notebook workflow](notebooks/README.md)
- [Result and evidence architecture](results/README.md)
- [Figure catalog](figures/README.md)
- [Verified bibliography](paper/references.md)
- [Research proposal](proposal/Research_Proposal.md)

## Limitations

- Only two domains, one Bitcoin asset, and one Electricity region are complete.
- Each domain has one frozen evaluation period; domain, target, frequency, horizon, and period effects cannot be isolated cleanly.
- The foundation-model roster contains only Chronos-Bolt-Tiny and one TimesFM checkpoint, with no fine-tuning.
- Bitcoin and Electricity use different operational protocols and nonidentical supervised neural formulations.
- Unknown foundation-model pretraining overlap or contamination cannot be excluded.
- Uncertainty evidence is heterogeneous; several models have no preserved intervals, and Electricity uses one principal 80% level.
- The Trust Score and auditability rubric are researcher-defined and comparison-relative.
- The final Bitcoin day is partial, and its source provider and licence remain unresolved.
- Artifact-level reproducibility is demonstrated, but fresh end-to-end regeneration and exact remote-checkpoint reproduction are not.

## Future Research

The proposal extends the completed evidence rather than redefining it. Planned directions include:

- Weather and Transport case studies under new frozen protocols;
- additional Electricity regions, financial assets, and forecast horizons;
- additional foundation-model families and model scales;
- Moirai in a compatible environment and PatchTST/iTransformer as supervised comparators;
- richer nominal interval levels, proper scores, and conditional calibration;
- broader rolling-origin and stress-test evaluation;
- checkpoint-version and pretraining-contamination audits; and
- sensitivity analysis for trust-component normalization, missing-evidence treatment, and weighting.

These are research objectives, not completed results. The forward-looking programme is described in [`proposal/Research_Proposal.md`](proposal/Research_Proposal.md).

# References

1. Adler, C., Chang, Y., Draxler, F., Abdi, S., & Smyth, P. (2026). Beyond accuracy: Are time series foundation models well-calibrated? *International Conference on Learning Representations*. https://openreview.net/forum?id=nGBN7UjHcy
2. Meyer, M., Kaltenpoth, S., Zalipski, K., & Müller, O. (2025). Time series foundation models: Benchmarking challenges and requirements. *arXiv:2510.13654*. https://arxiv.org/abs/2510.13654
3. Aksu, T., Woo, G., Liu, J., Liu, X., Liu, C., Savarese, S., Xiong, C., & Sahoo, D. (2024). GIFT-Eval: A benchmark for general time series forecasting model evaluation. *NeurIPS Workshop / arXiv:2410.10393*. https://arxiv.org/abs/2410.10393
4. Ansari, A. F., Stella, L., Turkmen, C., Zhang, X., Mercado, P., Shen, H., et al. (2024). Chronos: Learning the language of time series. *Transactions on Machine Learning Research*. https://openreview.net/forum?id=gerNCVqqtR
5. Das, A., Kong, W., Sen, R., & Zhou, Y. (2024). A decoder-only foundation model for time-series forecasting. In *Proceedings of the 41st International Conference on Machine Learning* (PMLR 235). https://proceedings.mlr.press/v235/das24c.html
6. Liang, Y., Wen, H., Nie, Y., Jiang, Y., Jin, M., Song, D., Pan, S., & Wen, Q. (2024). Foundation models for time series analysis: A tutorial and survey. *KDD / arXiv:2403.14735*. https://arxiv.org/abs/2403.14735
7. Hewamalage, H., Ackermann, K., & Bergmeir, C. (2023). Forecast evaluation for data scientists: Common pitfalls and best practices. *Data Mining and Knowledge Discovery, 37*, 788–832. https://doi.org/10.1007/s10618-022-00894-5
8. National Institute of Standards and Technology. (2023). *Artificial intelligence risk management framework (AI RMF 1.0)* (NIST AI 100-1). https://doi.org/10.6028/NIST.AI.100-1
9. Diebold, F. X., & Mariano, R. S. (1995). Comparing predictive accuracy. *Journal of Business & Economic Statistics, 13*(3), 253–263. https://doi.org/10.1080/07350015.1995.10524599
10. Gneiting, T., Balabdaoui, F., & Raftery, A. E. (2007). Probabilistic forecasts, calibration and sharpness. *Journal of the Royal Statistical Society: Series B, 69*(2), 243–268. https://doi.org/10.1111/j.1467-9868.2007.00587.x
11. Stankevičiūtė, K., Alaa, A. M., & van der Schaar, M. (2021). Conformal time-series forecasting. *Advances in Neural Information Processing Systems, 34*, 6216–6228. https://papers.nips.cc/paper_files/paper/2021/hash/312f1ba2a72318edaaa995a67835fad5-Abstract.html

See [`paper/references.md`](paper/references.md) for the extended verified bibliography.
