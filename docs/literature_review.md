# Literature Review: Trustworthy Foundation Models for Time-Series Forecasting

## Scope and evidence standard

This review uses 2022–2026 as its primary evidence window. Central claims rely on peer-reviewed papers, official proceedings, or original author preprints (Tier 1); official project or institutional documentation is Tier 2. Older work is retained only for indispensable calibration and forecast-comparison methodology. Published findings and this repository’s preliminary results are kept separate.

The review contains 28 sources: 24 recent sources (85.7%) and four pre-2022 methodological sources. Thus, recent work exceeds the 80% target for background, current-state, and research-gap discussion.

## Evolution of Modern Time-Series Forecasting, 2022–2026

- **2022–2023:** RevIN addressed a specific form of distribution shift; PatchTST established patch-based, channel-independent Transformer forecasting and transfer; linear-baseline and forecast-evaluation studies challenged weak comparison practices. These are influential modern forecasting architectures or methods, not automatically foundation models.
- **2024:** Chronos, TimesFM, and Moirai made large-scale pretrained zero-shot forecasting a central research programme. iTransformer remained a supervised architecture. GIFT-Eval and contemporary surveys broadened leakage-aware, heterogeneous evaluation.
- **2025:** Research expanded into realistic benchmarks, cloud-domain failures, in-context and retrieval-based adaptation, sparse architectures, interpretability, and representation intervention.
- **2026:** Calibration, regime-balanced benchmarking, and accuracy–energy trade-offs became explicit evaluation targets. This chronology is an evidence-based organisation of the reviewed sources, not a claim of universal historical consensus.

## Literature evidence table

| Reference ID | Authors | Year | Title | Venue / Source | Model / Topic | Datasets / Domains | Forecast Setting | Zero-shot? | Probabilistic? | Cross-domain? | Robustness? | Explainability? | Key Findings | Limitations | Relevance to This Project | Verified URL / DOI | Source Tier |
|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R01 | Kim et al. | 2022 | Reversible Instance Normalization for Accurate Time-Series Forecasting against Distribution Shift | ICLR | RevIN / shift | Electricity and other benchmarks | Supervised | No | No | Yes | Specific mean/variance shift | No | Reversible instance normalisation improves evaluated forecasts under changing statistics | Does not cover arbitrary regimes | Supports shift as a separate evaluation axis | [OpenReview](https://openreview.net/forum?id=cGDAkQo1C0p) | Tier 1 |
| R02 | Nie et al. | 2023 | A Time Series Is Worth 64 Words | ICLR | PatchTST | Standard long-horizon datasets | Supervised and self-supervised transfer | No universal claim | No native focus | Transfer | Limited | No | Patches permit longer contexts and strong evaluated performance | Not a universal zero-shot FM | Correct comparator classification | [OpenReview](https://openreview.net/forum?id=Jbdc0vTOcol) | Tier 1 |
| R03 | Zeng et al. | 2023 | Are Transformers Effective for Time Series Forecasting? | AAAI | Linear baselines | Nine datasets | Long-horizon | No | No | Yes | No dedicated tests | No | Simple linear models beat evaluated Transformer baselines | Predates modern TSFMs; benchmark-specific | Justifies strong simple baselines | [DOI](https://doi.org/10.1609/aaai.v37i9.26317) | Tier 1 |
| R04 | Hewamalage et al. | 2023 | Forecast Evaluation for Data Scientists | Data Mining and Knowledge Discovery | Evaluation practice | General | Out-of-sample | N/A | Discussed | General | Nonstationarity | No | Documents leakage, split, metric, horizon, and testing pitfalls | Tutorial synthesis | Supports protocol-aware evaluation | [DOI](https://doi.org/10.1007/s10618-022-00894-5) | Tier 1 |
| R05 | NIST | 2023 | AI Risk Management Framework 1.0 | NIST AI 100-1 | Trustworthiness | Cross-sector | Lifecycle | N/A | Broad reliability | Cross-sector | Yes | Yes | Trustworthiness is multidimensional and contextual | Not forecasting-specific or a score | Frames components, not weights | [DOI](https://doi.org/10.6028/NIST.AI.100-1) | Tier 2 |
| R06 | Ansari et al. | 2024 | Chronos: Learning the Language of Time Series | TMLR | Chronos | 42 public/synthetic datasets | Pretrained zero-shot | Yes | Sampled trajectories | Yes | Benchmark splits | No | Tokenised T5 models are competitive on unseen datasets | Original Chronos differs from Bolt | Establishes TSFM and probabilistic rationale | [OpenReview](https://openreview.net/forum?id=gerNCVqqtR) | Tier 1 |
| R07 | Das et al. | 2024 | A Decoder-Only Foundation Model for Time-Series Forecasting | ICML | TimesFM | Multiple domains/frequencies | Zero-shot | Yes | Point focus | Yes | Limited | No | Patched decoder-only model approaches supervised methods on evaluated tasks | Does not validate installed 2.5 interval behaviour | Supports zero-shot comparison | [PMLR](https://proceedings.mlr.press/v235/das24c.html) | Tier 1 |
| R08 | Woo et al. | 2024 | Unified Training of Universal Time Series Forecasting Transformers | ICML | Moirai | LOTSA, nine domains | Zero-shot universal | Yes | Distributional | Yes | Diversity, not stress suite | No | Handles varied frequency, dimensionality, and distributions | Not executed in this environment | Important missing comparator | [ICML](https://icml.cc/virtual/2024/poster/33767) | Tier 1 |
| R09 | Liu et al. | 2024 | iTransformer | ICLR | Inverted Transformer | Multivariate benchmarks | Supervised | No | No native focus | Across trained tasks | Some analyses | Limited | Variate tokens model cross-variate relations effectively | Not pretrained universal model | Prevents category error | [OpenReview](https://openreview.net/forum?id=JePfAI8fah) | Tier 1 |
| R10 | Aksu et al. | 2024 | GIFT-Eval | NeurIPS workshop / arXiv | Leakage-aware benchmark | 23 datasets, seven domains | Short/long horizons | Evaluates both | Yes for capable models | Yes | Horizon/frequency slices | No | Broad benchmark with explicit pretraining-overlap controls | Workshop/preprint; not deployment regimes | Supports heterogeneous fair evaluation | [arXiv](https://arxiv.org/abs/2410.10393) | Tier 1 |
| R11 | Liang et al. | 2024 | Foundation Models for Time Series Analysis: A Tutorial and Survey | KDD / arXiv | TSFM taxonomy | Broad | Survey | Discussed | Discussed | Yes | Discussed | Discussed | Organises architectures, tasks, and challenges | Secondary synthesis | Terminology and field context | [arXiv](https://arxiv.org/abs/2403.14735) | Tier 1 |
| R12 | Amazon Science | 2024–2026 | Chronos Forecasting Repository | Official documentation | Chronos-Bolt | Model family | Direct multi-step | Yes | Direct quantiles | N/A | No study | No | Documents Bolt’s patch encoder and quantile decoder | Documentation, not an evaluation paper | Correct model/version description | [GitHub](https://github.com/amazon-science/chronos-forecasting) | Tier 2 |
| R13 | Toner et al. | 2025 | Performance of Zero-Shot Time Series Foundation Models on Cloud Data | PMLR 296 | TSFM benchmark | Cloud telemetry | Zero-shot | Yes | Model-dependent | Single domain, many series | Failure behaviour | No | Several TSFMs lose to simple linear baselines and can be erratic | Cloud-specific | Direct evidence against universal superiority | [PMLR](https://proceedings.mlr.press/v296/toner25a.html) | Tier 1 |
| R14 | Meyer et al. | 2025 | Time Series Foundation Models: Benchmarking Challenges and Requirements | arXiv | Benchmark integrity | Cross-domain benchmarks | Zero-shot evaluation | Yes | Discussed | Yes | Events/overlap | No | Identifies leakage, representativeness, overlap, and event-memorisation risks | Preprint | Supports protocol and auditability gap | [arXiv](https://arxiv.org/abs/2510.13654) | Tier 1 |
| R15 | Shchur et al. | 2025 | fev-bench: A Realistic Benchmark for Time Series Forecasting | arXiv | Realistic benchmark | 100 tasks, seven domains | Mixed, including covariates | Evaluates both | Model-dependent | Yes | Task diversity | No | Uses confidence intervals, win rates, skill scores, and reproducible tasks | Preprint | Supports uncertainty-aware comparison | [arXiv](https://arxiv.org/abs/2509.26468) | Tier 1 |
| R16 | Shi et al. | 2025 | Time-MoE | ICLR | Sparse MoE TSFM | Large mixed corpus | Zero-shot | Yes | Model outputs | Yes | Scaling tests | No | Sparse experts improve scaling efficiency in reported experiments | Resource-intensive; no integrated trust audit | Efficiency/complexity comparator | [ICLR](https://proceedings.iclr.cc/paper_files/paper/2025/file/558d48c1f08675daa636e09bfe94a89e-Paper-Conference.pdf) | Tier 1 |
| R17 | Das et al. | 2025 | In-Context Fine-Tuning for Time-Series Foundation Models | ICML | In-context adaptation | Related-series benchmarks | Few-shot at inference | Base is zero-shot | Model-dependent | Yes | Adaptation | Limited | Retrieved examples can adapt forecasts without parameter updates | Requires relevant examples; not pure zero-shot | Motivates controlled adaptation | [arXiv](https://arxiv.org/abs/2410.24087) | Tier 1 |
| R18 | Ning et al. | 2025 | TS-RAG | arXiv | Retrieval adaptation | Seven benchmarks | Zero-shot plus retrieval | Yes | Model-dependent | Yes | Retrieval under variation | Retrieval trace | Retrieval-augmented TSFMs improve reported zero-shot forecasts | Preprint; retrieval adds infrastructure | Adaptation and inspectability extension | [arXiv](https://arxiv.org/abs/2503.07649) | Tier 1 |
| R19 | Boileau et al. | 2025 | Towards Interpretable Time Series Foundation Models | ICML workshop / arXiv | Interpretable TSFM | Synthetic mean-reverting data | Instruction-tuned | Not central | No | Limited | Synthetic interventions | Yes | Language annotations expose learned time-series concepts | Synthetic, narrow setting | Shows emerging TSFM-specific XAI | [arXiv](https://arxiv.org/abs/2507.07439) | Tier 1 |
| R20 | Wiliński et al. | 2025 | Exploring Representations and Interventions in Time Series Foundation Models | ICML | Representation analysis | Multiple TSFMs/tasks | Representation probing | Models include zero-shot | Model-dependent | Yes | Intervention tests | Yes | Finds redundancy and steerable trend/periodicity representations | Internal probes do not establish causal explanations | Extends beyond scalar explainability | [arXiv](https://arxiv.org/abs/2409.12915) | Tier 1 |
| R21 | Kottapalli et al. | 2025 | Foundation Models for Time Series: A Survey | arXiv | Survey | Broad | Survey | Discussed | Discussed | Yes | Discussed | Discussed | Synthesises rapidly expanding TSFM methods and gaps | Secondary and preprint | Current taxonomy only | [arXiv](https://arxiv.org/abs/2504.04011) | Tier 1 |
| R22 | Adler et al. | 2026 | Beyond Accuracy: Are Time Series Foundation Models Well-Calibrated? | ICLR | TSFM calibration | Multiple benchmarks/models | Multi-horizon | Yes | Yes | Yes | Horizon/head analyses | No | TSFMs are generally better calibrated than tested baselines, without uniform over/underconfidence | Versions and protocols differ from this project | Direct tension/comparison for coverage results | [OpenReview](https://openreview.net/forum?id=nGBN7UjHcy) | Tier 1 |
| R23 | Guibert et al. | 2026 | Benchmarking Time Series Foundation Models on their Accuracy and Energy Consumption | PMLR 309 | Accuracy/energy | School and MeteoSwiss | Fixed context/horizon | Yes | Model-dependent | Two domains | Dataset sensitivity | No | Accuracy and energy rankings depend on dataset and architecture | Two datasets; fixed 512/64 design | Supports efficiency as trust dimension | [PMLR](https://proceedings.mlr.press/v309/guibert26a.html) | Tier 1 |
| R24 | Xue et al. | 2026 | QuitoBench | arXiv | Regime-balanced benchmark | 232,200 instances; eight regimes | Context/horizon studies | Evaluates FMs | Model-dependent | Yes | Explicit regimes | No | Performance depends on regime and context; compact models can match FMs | Preprint; constructed regime taxonomy | Strong alignment with regime-aware evaluation | [arXiv](https://arxiv.org/abs/2603.26017) | Tier 1 |
| F01 | Gneiting et al. | 2007 | Probabilistic Forecasts, Calibration and Sharpness | JRSS B | Calibration theory | General | Predictive distributions | N/A | Yes | General | Calibration | No | Sharpness should be maximised subject to calibration | Not TSFM-specific | Necessary probabilistic foundation | [DOI](https://doi.org/10.1111/j.1467-9868.2007.00587.x) | Tier 1 |
| F02 | Diebold & Mariano | 1995 | Comparing Predictive Accuracy | JBES | Forecast comparison | General | Paired losses | N/A | N/A | General | Dependence-aware variance | No | Establishes equal-predictive-accuracy testing | Requires finite-sample care | Necessary test foundation | [DOI](https://doi.org/10.1080/07350015.1995.10524599) | Tier 1 |
| F03 | Harvey et al. | 1997 | Testing the Equality of Prediction Mean Squared Errors | IJF | DM correction | General | Forecast comparison | N/A | N/A | General | Error dependence | No | Studies small-sample modification of DM | Does not solve multiplicity | Necessary interpretation safeguard | [DOI](https://doi.org/10.1016/S0169-2070(96)00719-4) | Tier 1 |
| F04 | Stankevičiūtė et al. | 2021 | Conformal Time-Series Forecasting | NeurIPS | Conformal uncertainty | Synthetic and real series | Multi-horizon | Wrapper | Yes | Multiple datasets | Dependence-aware | No | Provides assumption-dependent multi-horizon coverage | Guarantees depend on assumptions | Foundation for future recalibration | [NeurIPS](https://papers.nips.cc/paper_files/paper/2021/hash/312f1ba2a72318edaaa995a67835fad5-Abstract.html) | Tier 1 |

## Foundation Models and Modern Comparators

Chronos tokenises scaled observations and samples trajectories from T5-family models; TimesFM uses a patched decoder-only design; Moirai uses a masked encoder, multi-patch projections, any-variate attention, and distributional outputs. All make broad zero-shot claims within specified benchmarks, not universal dominance. The project used **Chronos-Bolt-Tiny**, whose official documentation describes a patch encoder and direct multi-step quantile decoder; claims about original Chronos sampling must not be transferred mechanically.

PatchTST and iTransformer are modern supervised architectures. PatchTST also supports self-supervised transfer, but neither primary paper establishes the universal zero-shot deployment claim used by Chronos, TimesFM, or Moirai. Time-MoE demonstrates sparse scaling; in-context fine-tuning and TS-RAG indicate that controlled inference-time adaptation is an active alternative to fixed zero-shot deployment.

## Cross-Domain Generalisation and Strong Baselines

Recent TSFM papers already evaluate heterogeneous datasets, so the project must not claim that cross-domain evaluation is absent. GIFT-Eval, fev-bench, Toner et al., Guibert et al., and QuitoBench instead show why aggregate leaderboards are insufficient: outcome depends on domain, task composition, frequency, context, horizon, regime, overlap controls, and baseline strength.

The repository provides **convergent preliminary evidence**, not proof of a universal phenomenon: TimesFM ranks third on Bitcoin but first under Electricity Protocols A and B. Bitcoin Naive significantly beats both foundation models; Daily Seasonal Naive remains strong for electricity day-ahead forecasts; DHR-ARIMA is strong one-step but poor day-ahead. These results align with recent warnings about dataset dependence and weak baselines while remaining specific to two domains and declared protocols.

## Uncertainty and Calibration

Calibration, coverage, sharpness, interval width, and proper interval scores answer different questions. Adler et al. directly show that TSFM calibration varies with model, prediction head, and autoregressive horizon and report generally favourable calibration relative to tested baselines. The repository shows a sharper model contrast: nominal 80% coverage is approximately Chronos 84.5% versus TimesFM 33.1% on Bitcoin; 91.1% versus 33.7% on Electricity A; and 67.6% versus 24.6% on Electricity B. This is a tension, not a contradiction: model versions, datasets, interval construction, and protocols differ. No universal TimesFM or Chronos calibration claim follows.

Conformal recalibration is promising but is future work. It must use only eligible past calibration data and declare its dependence and coverage assumptions; post-hoc access to final-test residuals would invalidate the result.

## Robustness, Drift, and Horizon Dependence

RevIN addresses shifting input/output statistics, while current benchmarking work tests broader domain, regime, and context sensitivity. QuitoBench’s regime balance particularly supports stratified evaluation, but its eight-regime construction is not identical to this project. The repository’s volatility, seasonal-strength, trend, and demand-level slices are therefore **bespoke empirical stress tests**, not an adopted standard taxonomy.

Electricity Protocol A permits sequential one-step updates; Protocol B fixes a day-ahead information set. Their ranking and coverage changes are evidence that horizon and information availability must be declared. They are not interchangeable estimates of the same operational task.

## Direct XAI, Transparency, and Trustworthiness

Recent TSFM explainability work probes internal representations, steering, synthetic concept annotations, and retrieval traces. These methods go beyond attention inspection but remain early and do not establish causal explanations. The project’s dimensions—Transparency, Ease of Interpretation, Computational Complexity, Reproducibility, and Failure Detectability—are broader than feature-attribution XAI.

Accordingly, the project's **Transparency/Auditability Score** (historical artifact label: Explainability) is researcher-defined, and the composite is an **Exploratory Composite Trustworthiness Summary**, not a validated universal metric. NIST supports multidimensional contextual assessment; recent energy benchmarking supports adding efficiency; neither validates these weights. Components are not statistically independent and normalisation depends on the comparison set. Dimension-level evidence and sensitivity analysis must accompany any composite.

## Statistical Significance

Diebold–Mariano is methodologically old but remains the foundational paired-loss comparison. The project supplements it with HAC/Newey–West variance estimation, grouped daily losses for day-ahead vectors, Benjamini–Hochberg correction, and effect sizes. These are practical safeguards; they do not make DM recent literature or remove all small-sample and multiplicity limitations. Recent fev-bench practice also supports confidence intervals, win rates, and skill scores rather than rank-only conclusions.

## Recent Literature vs Project Evidence

| Recent Literature Finding | Project Preliminary Evidence | Agreement / Tension | Research Implication |
|---|---|---|---|
| TSFM accuracy is dataset- and regime-dependent (Toner; Guibert; QuitoBench) | TimesFM rank: Bitcoin 3; Electricity A 1; Electricity B 1 | Agreement; only two domains | Test rank stability using declared domains and uncertainty, not universal claims |
| TSFM calibration varies by model/head/horizon (Adler et al.) | Chronos coverage is consistently closer to 80% than TimesFM in completed cases | Partial agreement, with tension against generally favourable aggregate calibration | Audit exact versions and interval construction per horizon |
| Simple baselines can remain competitive (Zeng; Toner) | Bitcoin Naive wins significantly; Electricity Seasonal Naive is strong day-ahead | Agreement | Require strong protocol-appropriate baselines |
| Context and horizon alter outcomes (GIFT-Eval; QuitoBench) | Electricity A/B change DHR-ARIMA behaviour, ranks, and coverage | Agreement | Treat information set and horizon as first-class design variables |
| Efficiency depends on architecture and dataset (Guibert et al.) | Project complexity rubric distinguishes inference burden but lacks measured energy | Evidence gap | Measure runtime/memory/energy where feasible; avoid proxy-only claims |
| Interpretability research increasingly probes representations (Wiliński; Boileau) | Current Transparency/Auditability score is rubric-based, not direct XAI | Tension | Add validated, model-specific explanation evidence in future work |

## Research Gap

Recent TSFM research has established broad zero-shot evaluation and increasingly studies calibration, adaptation, internal representations, inference efficiency, and benchmark integrity. Yet primary studies usually emphasise one or a subset of these dimensions. There remains scope for a protocol-aware, artifact-auditable synthesis of baseline-relative accuracy, regime-conditional robustness, temporal stability, native uncertainty calibration, transparency/auditability, forecast-horizon sensitivity, efficiency, and dependence-aware statistical comparison. This is a synthesis gap, not a claim that cross-domain TSFM benchmarking is absent.

## Refined Research Questions

1. **Cross-domain rank stability:** How stable are TSFM ranks and baseline-relative gains across heterogeneous domains under explicitly comparable evaluation rules?
2. **Temporal-structure effects:** How do persistence, seasonality, trend, volatility, and regime structure affect relative performance among foundation, statistical, deep-learning, and simple models?
3. **Baseline-relative superiority:** In which domain–horizon settings do zero-shot TSFMs significantly and materially outperform strong protocol-appropriate baselines?
4. **Calibration quality:** How do empirical coverage, sharpness, interval width, and proper interval scores of available TSFM forecasts vary across domains, regimes, and horizons?
5. **Complexity versus trustworthiness:** When do accuracy gains justify computational complexity after robustness, calibration, reproducibility, transparency, failure detectability, and efficiency are reported separately?
6. **Forecast-horizon dependence:** How do forecast horizon and allowable information updates change model ranking, robustness, and uncertainty calibration?

## Papers Requiring University Access

No important 2022–2026 source used for a central claim was found to require subscription-only full text; accessible official papers or author preprints were verified. The following foundational publisher version remains a high-priority methodological check. No strong claim here depends only on inaccessible text.

### Priority 1 — essential to methodology

- **Authors:** Francis X. Diebold and Roberto S. Mariano
- **Year:** 1995
- **Title:** Comparing Predictive Accuracy
- **Venue:** Journal of Business & Economic Statistics, 13(3), 253–263
- **DOI / official URL:** [10.1080/07350015.1995.10524599](https://doi.org/10.1080/07350015.1995.10524599)
- **Reason required:** Foundational source for the project’s paired loss-differential tests.
- **Claim potentially supported:** Conditions and interpretation of equal-predictive-accuracy testing.
- **Verify from full text:** Exact assumptions, long-run variance treatment, overlapping-horizon guidance, and stated limitations.
- **Status:** **FULL TEXT REQUIRED — USER CAN ACCESS THROUGH UNIVERSITY**

### Priority 2 — useful supporting literature

None currently required.

### Priority 3 — optional background

None currently required.

## Source composition

| Publication year | Sources |
|---|---:|
| 2026 | 3 |
| 2025 | 9 |
| 2024 | 7 |
| 2023 | 4 |
| 2022 | 1 |
| Pre-2022 | 4 |
| **Total** | **28** |

Recent sources constitute **24/28 (85.7%)** of the review and the central background/gap evidence. The four older sources are confined to calibration, conformal uncertainty, and statistical-comparison foundations.

## Conclusion

The literature supports a conservative, current proposal: broad TSFM benchmarks already exist, but integrated protocol-aware trustworthiness evidence remains fragmented. The project’s strongest preliminary contribution is not another universal leaderboard; it is an auditable comparison showing where point accuracy, strong baselines, calibration, robustness, and horizon-specific inference agree or conflict.
