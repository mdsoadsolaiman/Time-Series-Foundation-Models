# Trustworthy Foundation Models for Time-Series Forecasting: Evaluating Accuracy, Robustness, and Uncertainty Across Domains

## 1. Background and Motivation

Time-series forecasts inform decisions in finance, energy, environmental management, and transport. Conventional systems are usually developed for a particular dataset and horizon; foundation models instead aim to forecast unseen series without task-specific training. Chronos and TimesFM are prominent examples of this zero-shot approach (Ansari et al., 2024; Das et al., 2024).

Reusable forecasting is attractive, but favorable average error does not establish trustworthiness. A model can deteriorate in extreme regimes, change rank with horizon or update rules, or issue poorly calibrated intervals. External checkpoints also complicate exact reproduction. Strong baselines remain necessary because architectural complexity does not guarantee improvement (Zeng et al., 2023; Hewamalage et al., 2023).

Recent research has raised concerns about calibration, benchmark integrity, and pretraining overlap (Aksu et al., 2024; Meyer et al., 2025; Adler et al., 2026). The gap is a coherent, protocol-aware assessment combining accuracy, Regime-Conditional Robustness, Temporal Stability, uncertainty calibration, Auditability / Transparency, and dependence-aware inference.

This proposal develops that assessment across four contrasting domains. Finance and Energy studies are complete and provide preliminary evidence. Scholarship-stage work will extend the framework to Weather and Traffic / Transport before producing a four-domain synthesis.

## 2. Research Aim and Questions

The aim is to determine the conditions under which zero-shot time-series foundation models provide reliable and practically meaningful forecasting evidence relative to strong conventional alternatives.

**Primary research question**

> Under what domain, forecasting horizon, regime, and information-update conditions can zero-shot time-series foundation models be considered trustworthy relative to strong conventional forecasting methods?

**Secondary research questions**

1. When do Chronos and TimesFM improve aggregate point accuracy over protocol-appropriate deterministic, statistical, and supervised neural baselines?
2. How stable is relative performance across difficult domain-specific regimes and across chronological portions of the evaluation period?
3. How closely do supported predictive intervals achieve nominal coverage, and what coverage–width trade-offs arise?
4. How strongly do forecast horizon and the release of new actual observations affect model rankings and failure modes?
5. To what extent can model configuration, forecast vectors, evidence lineage, and downstream analyses be independently audited and reproduced?

## 3. Preliminary Research

### 3.1 Finance - Bitcoin

The completed Finance study evaluates ten models on 1,061 daily Bitcoin Close targets using rolling one-step forecasting. The comparison spans deterministic, statistical, supervised neural, and foundation systems.

Naive persistence ranks first, followed by rolling Simple Exponential Smoothing and rolling ARIMA. TimesFM ranks sixth and Chronos seventh. Large-scale pretraining therefore does not automatically improve this highly persistent series, reinforcing the need for strong protocol-correct baselines.

At nominal 80% coverage, native Chronos intervals cover approximately 84.5% of outcomes, compared with 33.1% for TimesFM. Chronos is closer to nominal marginal coverage, although width and conditional calibration also matter. The leading point forecast and better-calibrated foundation forecast are not the same system.

### 3.2 Energy - South Australian Electricity Demand

The completed Energy study evaluates 13 models on half-hourly South Australian demand. **Protocol A** releases each actual after its 30-minute forecast. **Protocol B** generates all 48 day-ahead values at midnight without within-day updates. Both use the same frozen test series but different information sets.

TimesFM ranks first by MAE under both protocols. SARIMA ranks second under both; DHR-ARIMA changes from third in A to twelfth in B; Chronos ranks fifth and third. These reversals show that operational horizon and update discipline are substantive evaluation choices.

At nominal 80% coverage, Chronos and TimesFM attain approximately 91.1% and 33.6% in A, and 67.6% and 24.6% in B. Chronos is closer to nominal in both, while TimesFM is the stronger point forecaster. This is task-bounded evidence, not universal superiority.

### 3.3 Preliminary Cross-Domain Insight

The completed experiments indicate that foundation-model superiority is conditional rather than uniform. Persistence dominates Bitcoin; TimesFM leads Electricity by MAE; SARIMA remains highly competitive; and the Electricity ranking changes when observations cannot update a forecast within the horizon. Point accuracy and native calibration also disagree consistently for the two evaluated foundation models.

Two datasets cannot isolate a pure domain effect from frequency, target, historical period, horizon, or protocol. The findings should therefore be read as preliminary evidence that motivates a broader test. Weather and Traffic add substantially different physical, seasonal, and behavioral structures and will show whether the observed trade-offs persist beyond Finance and Energy.

## 4. Proposed Research Extension

### 4.1 Weather - Planned

A public Weather benchmark will be selected using predefined chronological, quality, provenance, and forecasting criteria. Environmental measurements add seasonal, event-driven, and physical dynamics distinct from Finance and Energy.

Chronological partitions will precede comparison of strong baselines, a supervised neural model, Chronos, and TimesFM. Forecasts will be frozen before downstream analysis. Dataset, target, sample size, thresholds, and results remain undetermined.

### 4.2 Traffic / Transport - Planned

Traffic adds intraday and weekly periodicity, congestion peaks, behavioral variation, abrupt disruptions, and operational multi-step forecasting.

A public dataset will follow the same provenance and chronological criteria. Model families and evidence freezing will remain consistent, while baselines, regimes, and horizons will be domain-appropriate. The purpose is to test, not assume, stability of earlier conclusions.

## 5. Methodology

### 5.1 Forecasting Models

Four families will be compared: domain-appropriate deterministic baselines; exponential-smoothing and ARIMA-family statistical systems; supervised neural comparators; and zero-shot Chronos-Bolt-Tiny and TimesFM. Optional models such as Moirai will be included only if a reproducible environment is established and will not block completion.

### 5.2 Experimental Protocol

Partitions will remain chronological. Development/validation evidence will support selection, scaling, early stopping, and calibration; the final test will not. Rolling protocols reveal an actual only after prediction, while fixed-origin protocols prohibit within-horizon updates.

Forecast vectors, timestamps, origins, horizons, and targets will be aligned and frozen before downstream analysis, preventing silent changes to forecasts or the comparison set.

### 5.3 Trustworthiness Evaluation

Five dimensions will be evaluated. **Accuracy** measures aggregate error. **Regime-Conditional Robustness** examines predefined difficult conditions. **Temporal Stability** compares chronological test segments. **Uncertainty Calibration** assesses coverage, width, and proper scores where available. **Auditability / Transparency** covers traceable artifacts, protocols, configurations, dependencies, and limitations-not feature-level explanation.

An exploratory composite may support sensitivity analysis, but component evidence will remain primary. Any composite will be identified as researcher-defined, comparison-set-relative, secondary, and not a validated universal trustworthiness instrument.

### 5.4 Statistical Analysis

Pairwise forecast-loss comparisons will account for serial dependence using protocol-appropriate long-run variance estimation. Multiple-comparison correction and practical effect sizes will accompany significance tests. Statistical and practical importance will be interpreted separately, and non-significance will not be treated as equivalence.

### 5.5 Reproducibility and Auditability

Each domain will preserve a validated forecast matrix and evidence lineage. Schemas, keys, timestamps, finiteness, deterministic baselines, metrics, protocol constraints, and recorded hashes will be checked.

This enables artifact-level reproduction without rerunning expensive models. It does not imply independent fresh regeneration of every external checkpoint; relevant limitations will be disclosed.

## 6. Expected Contributions

1. **Cross-domain empirical evidence** on zero-shot foundation forecasters relative to strong deterministic, statistical, and supervised neural systems.
2. **A multidimensional evaluation framework** integrating accuracy, regime behavior, Temporal Stability, uncertainty, and auditability without reducing the research to one leaderboard.
3. **Protocol-aware comparison** that treats forecast horizon and information-update discipline as first-class methodological choices.
4. **Joint interpretation of performance and reliability**, including cases where point accuracy, conditional behavior, and calibration disagree.
5. **A reproducible evidence architecture** based on frozen forecasts, explicit validation boundaries, and a clear distinction between artifact reproduction and full regeneration.

The contribution is primarily empirical and methodological. It does not depend on claiming a new model architecture or a universal Trust Score.

## 7. Expected Outcomes and Significance

The intended outcome is a four-domain evidence base showing where zero-shot models help, where conventional systems remain preferable, and which trustworthiness dimensions qualify those choices.

Chronos or TimesFM need not win every task. Negative or mixed results identify boundaries of transferable forecasting and are scientifically informative.

Scholarship support would enable the two planned domains, stronger calibration and sensitivity analysis, compatible additional models, and a coherent four-domain research output. It would extend an established programme rather than an untested starting concept.

## 8. Research Plan

| Stage | Activity | Status |
|---:|---|---|
| 1 | Multidimensional framework and artifact-validation architecture | Established |
| 2 | Bitcoin / Finance study | Completed |
| 3 | South Australian Electricity / Energy study | Completed |
| 4 | Preliminary two-domain synthesis | Completed |
| 5 | Weather dataset selection, protocol, forecasting, and trustworthiness analysis | Planned |
| 6 | Traffic / Transport dataset selection, protocol, forecasting, and trustworthiness analysis | Planned |
| 7 | Four-domain rank, calibration, robustness, protocol, and sensitivity synthesis | Planned |
| 8 | Final research reporting and reproducibility release | Planned |

## 9. Feasibility

The project begins from a substantial foundation: two domains, four model families, chronological protocols, robustness, Temporal Stability, uncertainty, inference, artifact validation, and cross-domain comparison are implemented.

Chronos and TimesFM inference is feasible in the available CPU environment. Expensive generation is separated from inexpensive artifact analysis, so Weather and Traffic extend a functioning framework.

The scope is bounded to one public series or coherent benchmark per planned domain; optional models will not block a four-domain empirical synthesis.

## 10. Limitations

Completed evidence covers two domains and one primary series per domain. The foundation roster is limited, pretraining overlap is unknown, and uncertainty capabilities differ. The exploratory composite is researcher-defined and comparison-relative. Conclusions remain conditional on datasets, periods, horizons, protocols, checkpoints, and losses; four domains will improve breadth without establishing universal generality.

## 11. Conclusion

The preliminary studies establish both the relevance and feasibility of the proposed research. Bitcoin shows that persistence and classical systems can outperform pretrained complexity. Electricity shows that TimesFM can provide strong zero-shot point forecasts while statistical models remain competitive and rankings respond to operational protocol. Across both domains, Chronos is closer to nominal native interval coverage than TimesFM, illustrating why accuracy and probabilistic reliability require separate evidence.

Weather and Traffic will test whether these patterns persist under environmental dynamics and strongly periodic transport demand. The resulting four-domain synthesis will offer a bounded, reproducible account of where foundation forecasters help, where they do not, and which additional evidence is needed before their forecasts should guide decisions. The central question is therefore not simply whether foundation models can forecast, but under what conditions the available evidence is strong enough to trust their forecasts.

## References

1. Adler, C., Chang, Y., Draxler, F., Abdi, S., & Smyth, P. (2026). Beyond accuracy: Are time series foundation models well-calibrated? *International Conference on Learning Representations*. https://openreview.net/forum?id=nGBN7UjHcy
2. Meyer, M., Kaltenpoth, S., Zalipski, K., & Müller, O. (2025). Time series foundation models: Benchmarking challenges and requirements. *arXiv:2510.13654*. https://arxiv.org/abs/2510.13654
3. Aksu, T., Woo, G., Liu, J., Liu, X., Liu, C., Savarese, S., Xiong, C., & Sahoo, D. (2024). GIFT-Eval: A benchmark for general time series forecasting model evaluation. *NeurIPS Workshop / arXiv:2410.10393*. https://arxiv.org/abs/2410.10393
4. Ansari, A. F., Stella, L., Turkmen, C., Zhang, X., Mercado, P., Shen, H., et al. (2024). Chronos: Learning the language of time series. *Transactions on Machine Learning Research*. https://openreview.net/forum?id=gerNCVqqtR
5. Das, A., Kong, W., Sen, R., & Zhou, Y. (2024). A decoder-only foundation model for time-series forecasting. In *Proceedings of the 41st International Conference on Machine Learning* (PMLR 235). https://proceedings.mlr.press/v235/das24c.html
6. Hewamalage, H., Ackermann, K., & Bergmeir, C. (2023). Forecast evaluation for data scientists: Common pitfalls and best practices. *Data Mining and Knowledge Discovery, 37*, 788–832. https://doi.org/10.1007/s10618-022-00894-5
7. Diebold, F. X., & Mariano, R. S. (1995). Comparing predictive accuracy. *Journal of Business & Economic Statistics, 13*(3), 253–263. https://doi.org/10.1080/07350015.1995.10524599
8. Gneiting, T., Balabdaoui, F., & Raftery, A. E. (2007). Probabilistic forecasts, calibration and sharpness. *Journal of the Royal Statistical Society: Series B, 69*(2), 243–268. https://doi.org/10.1111/j.1467-9868.2007.00587.x
