# Trustworthy Foundation Models for Time-Series Forecasting: Evaluating Generalisation, Robustness, Uncertainty, and Explainability

## Abstract

Time-series foundation models promise transferable forecasting capability with little or no task-specific training. Their practical value, however, cannot be established from average point accuracy alone. A model may perform well overall while failing under extremes, deteriorating across time, producing poorly calibrated uncertainty, or offering limited explanation of its forecasts. This research proposes a protocol-aware evaluation of trustworthy time-series foundation models across structurally different domains.

Preliminary work has completed two case studies: daily Bitcoin price forecasting and half-hourly South Australian electricity-demand forecasting. Deterministic baselines, statistical models, domain-adapted LSTMs, Chronos-Bolt-Tiny, and TimesFM were evaluated using chronological partitions and saved forecast vectors. The evidence is deliberately mixed. Naive persistence is the strongest Bitcoin model, while zero-shot TimesFM ranks first under both rolling one-step and true 48-step electricity protocols. Chronos is less accurate in several comparisons but provides substantially better 80% interval calibration than TimesFM in both domains. These results motivate a framework that examines accuracy, robustness, temporal generalisation, uncertainty, explainability, aggregate Trust Scores, and protocol-appropriate Diebold–Mariano tests.

The proposed research will extend the framework to Weather, Transport, additional electricity regions, and further model families where environments permit. Expected outcomes include a reproducible artifact-based evaluation process, clearer evidence about when zero-shot foundation models outperform strong baselines, and practical guidance for assessing calibration and trustworthiness independently of point accuracy. Claims will remain bounded by the evaluated domains, protocols, and available model implementations.

## Background

Foundation-model approaches have expanded from language and vision into time-series forecasting, offering pretrained models that can generate zero-shot forecasts across datasets. This raises the possibility of reducing per-domain training and engineering. Time-series deployment nevertheless involves temporal dependence, horizon-specific information constraints, distribution change, extreme events, and decisions that depend on calibrated uncertainty. Evaluation therefore needs to connect model comparisons to realistic forecast protocols and multiple dimensions of trust.

## Research Problem

Strong zero-shot point accuracy does not guarantee robustness, stable temporal generalisation, calibrated uncertainty, interpretability, or consistent behaviour across domains. Comparisons can also be misleading when rolling one-step forecasts are mixed with true multi-step forecasts or weak baselines are used. The problem is to evaluate foundation models under fair information sets while preserving evidence needed to audit each conclusion.

## Research Gap

The project addresses the practical gap between point-metric leaderboards and multidimensional, protocol-aware evaluation. It does not claim that trustworthiness frameworks or cross-domain forecasting comparisons are unprecedented. Its contribution is to combine frozen protocols, strong baselines, exact saved vectors, calibration evidence, robustness/generalisation analysis, and statistical testing in a reproducible case-study programme.

## Research Questions

1. Do foundation models generalise consistently across domains?
2. Does the strongest model depend on temporal structure?
3. Can zero-shot foundation models outperform strong domain-specific baselines?
4. Is uncertainty calibration consistent across domains?
5. Does model complexity imply greater trustworthiness?
6. How does forecast horizon change relative model performance?

## Methodology

Finance and Energy are complete; Weather and Transport are planned. Comparisons include naive and seasonal baselines, moving averages, DHR-ARIMA where appropriate, deterministic LSTMs, Chronos, and TimesFM. Foundation models remain zero-shot.

Protocols include daily or half-hourly rolling one-step forecasts and a true electricity 48-step day-ahead protocol with no within-horizon updates. Partitions are chronological; selection is validation-only; scalers and calibration cannot use final-test outcomes. Exact forecast vectors are saved before downstream analysis.

Evaluation reports MAE, RMSE, MAPE, sMAPE, and MASE where applicable; regime robustness; chronological generalisation; empirical coverage and interval width; explainability evidence; Penalised and Evidence-Available Trust Scores; and protocol-appropriate Diebold–Mariano tests with serial-dependence and multiple-comparison handling. Cross-domain comparisons use scale-independent measures, ranks, and baseline-relative changes rather than raw error units.

## Preliminary Results

For Bitcoin, Naive is best (MAE 1290.353242; sMAPE 1.744142), followed by Persistence-Enhanced LSTM, TimesFM, and Chronos. TimesFM trails Naive by about 4.6% in MAE. For electricity, TimesFM ranks first under rolling one-step (MASE-48 0.1400) and 48-step day-ahead forecasting (0.6892), improving on the strongest protocol-specific baselines by about 38%.

Uncertainty evidence separates point performance from calibration. Chronos obtains approximately 84.5% Bitcoin coverage, 91.1% Electricity A coverage, and 67.6% Electricity B coverage for nominal 80% intervals. TimesFM obtains approximately 33.1%, 33.6%, and 24.6%. Preliminary results therefore support domain dependence, horizon dependence, and independent calibration evaluation.

## Expected Contributions

1. A protocol-aware comparison design that separates one-step and operational multi-step tasks.
2. Cross-domain evidence about zero-shot foundation-model effectiveness relative to strong baselines.
3. A transparent multidimensional trustworthiness framework with explicit missing-evidence treatment.
4. Empirical analysis of point accuracy versus uncertainty calibration.
5. A reproducible artifact-based workflow for downstream audit and statistical testing.

## Research Significance

The research is relevant to trustworthy AI because forecasts increasingly support financial, energy, transport, and environmental decisions. Demonstrating when a model is accurate is not enough; practitioners also need to know when it fails, whether intervals are meaningful, whether conclusions survive protocol changes, and which evidence is missing. The proposed framework aims to make those distinctions visible.

## Limitations

Preliminary evidence covers only two domains and one electricity region. Domain frequencies, targets, and horizons differ. LSTM formulations are not identical. Trust weights and explainability scores are researcher-defined. Available quantiles are limited, no foundation model is fine-tuned, and Moirai, PatchTST, and iTransformer remain unavailable in the completed environment. These constraints limit generalisation and will be reported rather than concealed.

## Future Work

The next stages will add Weather and Transport, evaluate additional electricity regions, study model scaling, develop leakage-free calibration and conformal prediction, and add foundation-model families in a compatible environment. Protocols and selection rules will be frozen before final-test inspection.

## References

Exact bibliographic references have not yet been verified in the repository. Before submission, this section will be populated with checked primary references for Chronos, TimesFM, time-series foundation models, Diebold–Mariano testing, probabilistic forecast calibration, conformal prediction, and trustworthy AI. No placeholder entry should be treated as a citation.
