# Trustworthy Foundation Models for Time-Series Forecasting: Evaluating Generalisation, Robustness, Uncertainty, and Explainability Across Domains

## Abstract

Time-series foundation models (TSFMs) are developing rapidly, offering broad zero-shot forecasting capability without conventional task-specific training. Chronos, TimesFM, and Moirai exemplify this shift towards large pretrained forecasters across heterogeneous datasets. Recent research, however, also identifies dataset-dependent performance, benchmark-integrity risks, horizon sensitivity, calibration variation, efficiency trade-offs, and limited interpretability. These concerns expose the central research problem: strong point accuracy does not by itself establish that a forecast is trustworthy.

This research asks when, and under what conditions, zero-shot TSFMs can be trusted. A completed preliminary study evaluates Bitcoin prices and South Australian electricity demand using chronological partitions, strong simple and statistical baselines, domain-adapted LSTMs, Chronos-Bolt-Tiny, and TimesFM. TimesFM changes from third place on Bitcoin to first place under both rolling one-step and true day-ahead electricity protocols. Chronos is generally less point-accurate but produces substantially more reliable native interval coverage. Naive persistence is the strongest Bitcoin forecaster, while statistical and seasonal baselines remain competitive in electricity. These results are preliminary and domain-bounded, but they demonstrate why accuracy, horizon, calibration, and baseline choice must be evaluated together.

The scholarship-stage research will extend the same frozen, artifact-based protocol to Weather and Transport, whose environmental dynamics, periodic behaviour, and regime effects provide contrasting temporal structures. It will integrate baseline-relative accuracy, robustness, temporal generalisation, uncertainty calibration, explainability and reproducibility evidence, forecast-horizon sensitivity, and statistical significance. Expected outputs are a protocol-aware cross-domain evaluation, evidence on rank stability and calibration, and a reproducible workflow for trustworthy operational comparison. The intended contribution is empirical and methodological rather than a claim of universal or theoretical novelty.

## 1. Background

Modern time-series forecasting has progressed from task-specific statistical and neural models towards reusable pretrained systems. In 2022–2023, reversible normalisation addressed a specific form of distribution shift, while PatchTST demonstrated the value of channel-independent temporal patches and self-supervised transfer (Kim et al., 2022; Nie et al., 2023). Simple linear models also remained difficult to dismiss, outperforming several contemporary Transformer baselines in a widely used long-horizon benchmark (Zeng et al., 2023). These results helped establish longer contexts, representation learning, and rigorous baseline selection as important parts of modern forecasting.

PatchTST and iTransformer are influential modern supervised forecasting architectures. PatchTST supports supervised forecasting and self-supervised transfer; iTransformer represents whole variate histories as tokens to model cross-variate relationships (Liu et al., 2024). Their primary papers do not establish the same general-purpose zero-shot claim as TSFMs, so they should not automatically be described as foundation models.

In 2024, large pretrained forecasters became prominent. Chronos casts scaled observations as tokens and learns probabilistic trajectories using T5-family models (Ansari et al., 2024). TimesFM uses a patched decoder-only architecture and reports strong zero-shot performance across frequencies and horizons (Das et al., 2024). Moirai uses a masked encoder, multi-patch projections, any-variate attention, and distributional outputs trained on the multi-domain LOTSA corpus (Woo et al., 2024). GIFT-Eval subsequently emphasised heterogeneous tasks and pretraining-overlap controls (Aksu et al., 2024).

Research in 2025–2026 increasingly examines what accuracy leaderboards omit. Studies report failures against simple baselines on cloud telemetry, benchmark leakage and representativeness risks, realistic multi-domain evaluation, inference-time adaptation, internal representations, calibration, regime-balanced benchmarking, and accuracy–energy trade-offs (Toner et al., 2025; Meyer et al., 2025; Shchur et al., 2025; Das et al., 2025; Wiliński et al., 2025; Adler et al., 2026; Guibert et al., 2026; Xue et al., 2026). Collectively, this literature supports a multidimensional and protocol-aware research programme.

## 2. Research Problem and Gap

The central question is: **when and under what conditions can zero-shot time-series foundation models be trusted?** Performance can depend on the domain, persistence and seasonality, volatility or other regimes, forecast horizon, permissible information updates, and probabilistic calibration. A system can achieve favourable average error while failing during extremes, changing rank under a different operational horizon, or issuing intervals that substantially undercover realised outcomes.

Recent work already establishes broad zero-shot and cross-domain evaluation; calibration, adaptation, interpretability, efficiency, and benchmark quality are also active research topics. It would therefore be inaccurate to claim that these areas are absent. The defensible gap is that they are often examined separately. There remains scope for a single empirical framework that combines strong-baseline-relative accuracy, domain-specific robustness, temporal generalisation, native uncertainty calibration, explainability and reproducibility evidence, forecast-horizon effects, efficiency, and dependence-aware statistical comparison across heterogeneous domains (Meyer et al., 2025; Shchur et al., 2025; Adler et al., 2026; Guibert et al., 2026; Xue et al., 2026).

This project addresses that synthesis gap through frozen forecast protocols and exact saved vectors. It is not merely a model-ranking exercise: its purpose is to determine when different dimensions support the same operational choice and when they conflict.

## 3. Research Questions

1. **Cross-domain rank stability:** How stable are TSFM ranks and baseline-relative gains across heterogeneous domains under explicitly comparable evaluation rules?
2. **Temporal-structure effects:** How do persistence, seasonality, trend, volatility, and regime structure affect relative performance among foundation, statistical, deep-learning, and simple models?
3. **Baseline-relative superiority:** In which domain–horizon settings do zero-shot TSFMs significantly and materially outperform strong protocol-appropriate baselines?
4. **Calibration quality:** How do empirical coverage, sharpness, interval width, and proper interval scores of available TSFM forecasts vary across domains, regimes, and horizons?
5. **Complexity versus trustworthiness:** When do accuracy gains justify computational complexity after robustness, calibration, reproducibility, explainability, failure detectability, and efficiency are reported separately?
6. **Forecast-horizon dependence:** How do forecast horizon and allowable information updates change model ranking, robustness, and uncertainty calibration?

## 4. Preliminary Research

Two domains are complete. All statements below are preliminary findings from this repository rather than results attributed to the published literature.

### 4.1 Finance — Bitcoin

The Bitcoin study evaluates 1,061 daily test observations using rolling one-step forecasts. Naive persistence achieves the best point accuracy (MAE 1290.35), followed by the Persistence-Enhanced LSTM, TimesFM, and Chronos-Bolt-Tiny. Naive significantly outperforms both foundation models under the primary loss comparison, while TimesFM significantly outperforms Chronos. The Persistence-Enhanced LSTM and TimesFM are not significantly different at the 5% level.

Point ranking does not match uncertainty quality. For nominal 80% intervals, Chronos attains approximately 84.5% empirical coverage, compared with 33.1% for TimesFM. Thus, the weaker point forecaster is substantially better calibrated in this completed case.

### 4.2 Energy — South Australian Electricity Demand

Electricity is evaluated under two distinct operational protocols. **Protocol A** is rolling one-step forecasting at a 30-minute horizon, allowing the latest actual to become available before the following forecast. **Protocol B** is true 48-step, 24-hour day-ahead forecasting: all values for a day are generated from the midnight origin with no within-horizon actual updates.

TimesFM ranks first under both protocols, with MASE-48 of 0.1400 one-step and 0.6892 day-ahead. DHR-ARIMA is a strong one-step model (0.2276) but deteriorates substantially day-ahead (2.4557). Daily Seasonal Naive remains a strong operational day-ahead benchmark (1.1056), while Chronos ranks second (1.0774). TimesFM significantly outperforms its strongest protocol-specific baselines and Chronos under the primary squared-loss tests. Chronos nevertheless remains better calibrated: its 80% coverage is approximately 91.1% and 67.6% under Protocols A and B, compared with 33.6% and 24.6% for TimesFM.

### 4.3 Cross-domain implication

TimesFM changes from third on Bitcoin to first under both electricity protocols. DHR-ARIMA’s reversal between electricity horizons further shows that model performance depends on the information set as well as the domain. This is **convergent preliminary evidence** of domain- and horizon-dependent superiority, not proof of a universal ranking phenomenon. It motivates the proposed broader evaluation.

## 5. Connection Between Literature and Preliminary Evidence

| Recent literature theme | Project preliminary observation | Research motivation |
|---|---|---|
| Dataset- and regime-dependent performance (Toner et al., 2025; Xue et al., 2026) | TimesFM changes from third on Bitcoin to first on electricity | Test rank stability across more temporal structures without inferring causality |
| Calibration varies across TSFMs, prediction heads, and horizons (Adler et al., 2026) | Chronos is consistently closer to nominal coverage than TimesFM | Audit model version, interval construction, domain, and horizon jointly |
| Simple baselines can remain competitive (Zeng et al., 2023; Toner et al., 2025) | Bitcoin Naive wins; Daily Seasonal Naive remains strong day-ahead | Make strong protocol-appropriate baselines mandatory |
| Context and horizon influence outcomes (Aksu et al., 2024; Xue et al., 2026) | DHR-ARIMA is strong one-step but poor day-ahead | Treat horizon and permissible updates as first-class variables |
| Benchmark integrity requires overlap and protocol controls (Meyer et al., 2025) | Forecast vectors, keys, information sets, and hashes are audited | Preserve artifact-based evaluation and disclose unknown pretraining overlap |

## 6. Methodology

### 6.1 Domains and model families

The completed Finance and Energy studies will be extended to Weather and Transport. Weather provides environmental dynamics, seasonal and physical patterns; Transport provides strong periodicity, behavioural variation, congestion, and event-like regimes. Their purpose is not simply to enlarge the dataset count, but to test whether rankings and trustworthiness conclusions transfer to different temporal structures.

Four model families will be compared:

- **Baselines:** Naive, Seasonal Naive, and Moving Average.
- **Statistical models:** ARIMA or DHR-ARIMA where appropriate to the domain and protocol.
- **Deep learning:** domain-adapted LSTM models selected without final-test access.
- **Foundation models:** zero-shot Chronos-Bolt-Tiny and TimesFM.

Moirai or another verified TSFM may be added if the software environment permits, but no optional model is necessary for project completion. Foundation models remain zero-shot so that the research question concerns general-purpose transfer rather than fine-tuned performance.

### 6.2 Forecast protocols and evidence preservation

Each task will declare either rolling one-step or true multi-step forecasting. Rolling evaluation may incorporate an actual only after its forecast is recorded. In true multi-step evaluation, no actual inside the forecast horizon may update the model. This distinction prevents an artificially easier rolling task from being labelled day-ahead.

All splits will be chronological. Model selection, early stopping, scaling, and any calibration decisions will use training or validation information only; random time-series splitting, target leakage, and final-test tuning are prohibited. Exact forecast vectors, timestamps, origins, horizons, versions, and validation checks will be saved before downstream analysis. These controls respond directly to contemporary benchmark-integrity concerns (Hewamalage et al., 2023; Meyer et al., 2025).

### 6.3 Evaluation

Point performance will use MAE, RMSE, MAPE, sMAPE, and MASE where applicable. Cross-domain synthesis will use scale-independent metrics, relative improvement over the strongest eligible baseline, and within-domain ranks rather than comparing raw units.

Robustness will be assessed using predeclared domain-specific regimes, such as volatility and movement regimes in Finance, demand-level and variability regimes in Energy, meteorological states in Weather, and congestion states in Transport. These regimes are bespoke empirical stress tests, not a standard universal taxonomy. Temporal generalisation will compare earlier, middle, and later contiguous test segments while preserving complete multi-step origins.

Probabilistic evaluation will report nominal and empirical coverage, interval width, coverage error, and the calibration–sharpness trade-off. A proper interval score will be added where saved quantiles support it. Missing native intervals will remain missing rather than being fabricated. Leakage-free conformal calibration is a proposed extension grounded in established time-series conformal methodology (Stankevičiūtė et al., 2021).

Explainability evidence will cover transparency, ease of interpretation, reproducibility, computational complexity, and failure detectability. This is broader than standard feature-attribution XAI. Representation probes or validated attribution methods may supplement the rubric, informed by recent TSFM intervention research (Wiliński et al., 2025).

Statistical comparison will use Diebold–Mariano tests as foundational methodology (Diebold & Mariano, 1995), with HAC/Newey–West variance adjustment for serial dependence. Multi-step electricity losses are aggregated by daily origin before testing; Benjamini–Hochberg correction controls the reported comparison family; effect sizes accompany p-values. Dimension-level results remain primary evidence.

## 7. Trustworthiness Framework

The existing framework weights Accuracy at 35%, Robustness at 20%, Generalisation at 20%, Uncertainty at 15%, and Explainability at 10%. This is a **researcher-defined composite evaluation framework**, not an established universal TSFM metric. Weights will be justified and sensitivity-tested, and the underlying component results will remain more important than the aggregate.

Two summaries are retained. The **Overall Trust Score — Missing Evidence Penalised** assigns no contribution to an unavailable component and therefore reflects evidence completeness or deployment readiness. The **Evidence-Available Trust Score** renormalises across observed components, allowing comparison without pretending that missing uncertainty evidence is measured poor calibration. Reporting both reveals whether a high observed-component score rests on incomplete evidence. Missing uncertainty is explicitly “not evaluated”, not interpreted as bad calibration.

## 8. Proposed Scholarship-Stage Research

The primary deliverables are two additional domain studies and a four-domain synthesis. The Weather study will freeze an operational horizon, appropriate seasonal/statistical baselines, meteorological regimes, and native uncertainty evidence. The Transport study will similarly declare horizon, sensor or aggregate structure, congestion regimes, and periodic baselines. Both will reuse the artifact audit rather than reproduce notebook development history.

Secondary work, ordered by feasibility, will: evaluate rank stability across the four domains; add another electricity region where a comparable series is available; test validation-only conformal calibration; examine sensitivity to trustworthiness weights; strengthen model-specific explanation evidence; and measure inference time and memory, with energy measurement included where reliable instrumentation exists. Additional models are optional extensions.

## 9. Expected Contributions and Significance

The expected contributions are:

1. A protocol-aware cross-domain evaluation of zero-shot TSFMs against strong baselines.
2. An integrated analysis of accuracy, robustness, temporal generalisation, calibration, explainability, reproducibility, and horizon sensitivity.
3. Empirical evidence on foundation-model rank stability across domains and forecast horizons.
4. Comparative calibration evidence for available native TSFM intervals and leakage-free recalibration experiments.
5. A reproducible, artifact-based workflow with saved vectors, protocol audits, and dependence-aware statistical testing.

The significance is practical rather than theoretical. Financial, energy, weather, and transport forecasts support decisions with different costs, horizons, and tolerance for failure. A model with slightly lower MAE but poorly calibrated uncertainty may not be the more trustworthy operational choice. Conversely, wider calibrated intervals do not compensate automatically for poor point accuracy. Reporting these dimensions separately can improve uncertainty communication, model selection, and failure detection in operational decision support.

## 10. Work Plan

| Stage | Semester-scale activity | Deliverable |
|---|---|---|
| 1 | Focused literature refinement and final protocol standardisation | Frozen Weather and Transport protocols, datasets, baselines, and audit templates |
| 2 | Weather forecasting study | Validated forecasts and multidimensional Weather case study |
| 3 | Transport forecasting study | Validated forecasts and multidimensional Transport case study |
| 4 | Cross-domain synthesis | Rank-stability, robustness, generalisation, horizon, and efficiency comparison |
| 5 | Uncertainty refinement | Validation-only conformal experiments and trust-weight sensitivity analysis |
| 6 | Final evaluation and communication | Final report, reproducible repository, scholarship presentation, and limitations register |

## 11. Responsible AI

Responsible reporting will emphasise calibrated uncertainty, explicit information sets, reproducibility, domain-specific validation, and visible failure cases. Negative results—including failure to beat simple baselines or obtain reliable intervals—will be reported rather than filtered from the comparison. Forecasts will be presented as decision-support evidence, not autonomous advice, and deployment claims will remain bounded by the evaluated region, period, horizon, and model version.

## 12. Limitations

Only two domains are complete, and electricity currently covers one region. Domain frequencies, targets, histories, and horizons differ, while LSTM formulations are adapted to each domain rather than architecturally identical. The Trust Score weights and explainability rubric are researcher-defined. Native quantile availability is limited, and missing uncertainty cannot be interpreted as measured poor calibration. Foundation models are evaluated zero-shot without comprehensive hyperparameter optimisation or fine-tuning. Some optional model families are unavailable in the current software environment. Finally, unknown overlap between TSFM pretraining data and evaluation series cannot be completely excluded; model providers’ corpora and benchmark controls will be documented, and conclusions will be qualified accordingly (Meyer et al., 2025).

## References

Aksu, T., Woo, G., Liu, J., Liu, X., Liu, C., Savarese, S., Xiong, C., & Sahoo, D. (2024). GIFT-Eval: A benchmark for general time series forecasting model evaluation. *NeurIPS Workshop / arXiv:2410.10393*. https://arxiv.org/abs/2410.10393

Adler, C., Chang, Y., Draxler, F., Abdi, S., & Smyth, P. (2026). Beyond accuracy: Are time series foundation models well-calibrated? *International Conference on Learning Representations*. https://openreview.net/forum?id=nGBN7UjHcy

Ansari, A. F., Stella, L., Turkmen, C., Zhang, X., Mercado, P., Shen, H., et al. (2024). Chronos: Learning the language of time series. *Transactions on Machine Learning Research*. https://openreview.net/forum?id=gerNCVqqtR

Das, A., Faw, M., Sen, R., & Zhou, Y. (2025). In-context fine-tuning for time-series foundation models. *Proceedings of the 42nd International Conference on Machine Learning*. https://arxiv.org/abs/2410.24087

Das, A., Kong, W., Sen, R., & Zhou, Y. (2024). A decoder-only foundation model for time-series forecasting. *Proceedings of the 41st International Conference on Machine Learning*. https://proceedings.mlr.press/v235/das24c.html

Diebold, F. X., & Mariano, R. S. (1995). Comparing predictive accuracy. *Journal of Business & Economic Statistics, 13*(3), 253–263. https://doi.org/10.1080/07350015.1995.10524599

Guibert, L., Pasquier, B., Montet, F., & Wolf, B. (2026). Benchmarking time series foundation models on their accuracy and energy consumption. *Proceedings of the Fourth Swiss AI Days* (PMLR 309). https://proceedings.mlr.press/v309/guibert26a.html

Hewamalage, H., Ackermann, K., & Bergmeir, C. (2023). Forecast evaluation for data scientists: Common pitfalls and best practices. *Data Mining and Knowledge Discovery, 37*, 788–832. https://doi.org/10.1007/s10618-022-00894-5

Kim, T., Kim, J., Tae, Y., Park, C., Choi, J.-H., & Choo, J. (2022). Reversible instance normalization for accurate time-series forecasting against distribution shift. *International Conference on Learning Representations*. https://openreview.net/forum?id=cGDAkQo1C0p

Liu, Y., Hu, T., Zhang, H., Wu, H., Wang, S., Ma, L., & Long, M. (2024). iTransformer: Inverted transformers are effective for time series forecasting. *International Conference on Learning Representations*. https://openreview.net/forum?id=JePfAI8fah

Meyer, M., Kaltenpoth, S., Zalipski, K., & Müller, O. (2025). Time series foundation models: Benchmarking challenges and requirements. *arXiv:2510.13654*. https://arxiv.org/abs/2510.13654

Nie, Y., Nguyen, N. H., Sinthong, P., & Kalagnanam, J. (2023). A time series is worth 64 words: Long-term forecasting with transformers. *International Conference on Learning Representations*. https://openreview.net/forum?id=Jbdc0vTOcol

Shchur, O., Ansari, A. F., Turkmen, C., Stella, L., Erickson, N., Guerron, P., Bohlke-Schneider, M., & Wang, Y. (2025). fev-bench: A realistic benchmark for time series forecasting. *arXiv:2509.26468*. https://arxiv.org/abs/2509.26468

Stankevičiūtė, K., Alaa, A. M., & van der Schaar, M. (2021). Conformal time-series forecasting. *Advances in Neural Information Processing Systems, 34*, 6216–6228. https://papers.nips.cc/paper_files/paper/2021/hash/312f1ba2a72318edaaa995a67835fad5-Abstract.html

Toner, W., Lee, T. L., Joosen, A., Singh, R., & Asenov, M. (2025). Performance of zero-shot time series foundation models on cloud data. *Proceedings of the First Workshop on Foundation Models for Science* (PMLR 296). https://proceedings.mlr.press/v296/toner25a.html

Wiliński, M., Goswami, M., Potosnak, W., Żukowska, N., & Dubrawski, A. (2025). Exploring representations and interventions in time series foundation models. *Proceedings of the 42nd International Conference on Machine Learning*. https://arxiv.org/abs/2409.12915

Woo, G., Liu, C., Kumar, A., Xiong, C., Savarese, S., & Sahoo, D. (2024). Unified training of universal time series forecasting transformers. *Proceedings of the 41st International Conference on Machine Learning*. https://icml.cc/virtual/2024/poster/33767

Xue, S., Zhu, Z., Zhang, W., Cai, R., Wang, R., Mu, Y., Zhou, F., Li, J., Di, P., & Yu, H. (2026). QuitoBench: A high-quality open time series forecasting benchmark. *arXiv:2603.26017*. https://arxiv.org/abs/2603.26017

Zeng, A., Chen, M., Zhang, L., & Xu, Q. (2023). Are transformers effective for time series forecasting? *Proceedings of the AAAI Conference on Artificial Intelligence, 37*(9), 11121–11128. https://doi.org/10.1609/aaai.v37i9.26317
