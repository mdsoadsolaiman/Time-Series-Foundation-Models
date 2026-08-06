# Proposal Literature Integration Plan

This plan maps evidence into a future proposal revision; it does not edit the proposal. “Literature” means externally published evidence. “Preliminary evidence” means frozen repository results and must remain labelled as such.

| Proposal section | Recent sources to cite (2022–2026) | Foundational source, only where necessary | Project preliminary evidence | Claim supported / integration instruction |
|---|---|---|---|---|
| Abstract | Chronos; TimesFM; Moirai; Adler et al. (2026) | None | Two-domain ranks and coverage | Pretrained zero-shot forecasting is established; motivate integrated accuracy/calibration analysis without claiming universality. |
| Background | PatchTST; iTransformer; Chronos; TimesFM; Moirai; Liang et al. (2024) | None | None | Present the 2022–2026 evolution. Classify PatchTST/iTransformer as modern supervised architectures, not foundation models. |
| Research problem | Toner et al. (2025); Guibert et al. (2026); QuitoBench (2026); Hewamalage et al. (2023) | Gneiting et al. (2007) for calibration/sharpness | TimesFM rank and coverage changes | Accuracy, uncertainty, regime, horizon, and efficiency can disagree. |
| Research gap | Meyer et al. (2025); GIFT-Eval; fev-bench; Adler et al.; Wiliński et al.; Guibert et al. | None | Artifact-auditable Bitcoin/electricity synthesis | Cross-domain benchmarking exists; the defensible gap is integrated, protocol-aware trustworthiness evaluation. |
| RQ1: rank stability | GIFT-Eval; Toner et al.; fev-bench; QuitoBench | None | TimesFM ranks 3/1/1 | Test stability across declared domains; call existing results convergent preliminary evidence. |
| RQ2: temporal structure | RevIN; QuitoBench; Hewamalage et al. | None | Bespoke regime slices | Ask how temporal structures affect relative performance; state that project regimes are researcher-defined. |
| RQ3: baseline superiority | Zeng et al.; Toner et al.; fev-bench | None | Bitcoin Naive; Electricity Seasonal Naive; DHR-ARIMA A/B contrast | Require strong, protocol-appropriate baselines and both statistical and practical significance. |
| RQ4: calibration | Adler et al. (2026) | Gneiting et al. (2007); Stankevičiūtė et al. (2021) for future conformal work | Coverage: Bitcoin 84.5/33.1; Elec A 91.1/33.7; Elec B 67.6/24.6 | Compare coverage, sharpness, width, and proper interval scores; avoid model-wide claims. |
| RQ5: complexity/trust | Guibert et al.; NIST AI RMF; Wiliński et al.; Boileau et al. | None | Component rubric and sensitivity analysis | Call the score a researcher-defined composite; report components and measured efficiency where feasible. |
| RQ6: horizon | GIFT-Eval; QuitoBench; Adler et al.; Hewamalage et al. | None | Electricity Protocol A versus B | Treat horizon and information set as design variables, not interchangeable protocols. |
| Method: splits/protocols | Hewamalage et al.; Meyer et al.; GIFT-Eval | None | Frozen origins, vectors, hashes | Support chronological splits, overlap disclosure, no lookahead, and artifact auditability. |
| Method: models | Chronos; TimesFM; Moirai; Time-MoE | None | Chronos-Bolt-Tiny and TimesFM versions | Distinguish original Chronos from Bolt; explain absent models as scope/environment limits. |
| Method: robustness | RevIN; QuitoBench; Toner et al. | None | Volatility, seasonality, trend, demand-level regimes | Cite related shift work but label the project framework bespoke. |
| Method: adaptation | In-context fine-tuning; TS-RAG | Stankevičiūtė et al. for conformal wrapper | No adapted final-test result yet | Present retrieval/in-context/conformal methods as future preregistered extensions, not completed evidence. |
| Method: explainability | Wiliński et al.; Boileau et al.; TS-RAG | None | Transparency, interpretation, complexity, reproducibility, failure detectability | Explain that the rubric is broader than attribution XAI; add probing/faithfulness evidence in future work. |
| Method: statistics | fev-bench; Hewamalage et al. | Diebold & Mariano (1995); Harvey et al. (1997) | HAC, daily grouping, BH correction, effect sizes | DM is foundational, not recent; explain dependence and multiplicity safeguards. |
| Preliminary results | Recent sources only for contextual comparison | None | Frozen CSVs and case-study reports | Cite repository artifacts for every number; external literature must not be presented as replication. |
| Expected contributions | Meyer et al.; Adler et al.; Guibert et al.; Wiliński et al. | None | Auditable component synthesis | Promise integrated application and sensitivity testing, not a first-ever benchmark or universal metric. |
| Limitations | Model papers; Toner et al.; Adler et al. | None | Two domains, one electricity region, two completed TSFMs | Declare version, domain, horizon, environment, and native-interval limits. |
| Future work | Moirai; Time-MoE; in-context FT; TS-RAG; QuitoBench | Stankevičiūtė et al. | Weather/traffic/regions and recalibration are unfinished | Pre-register additional domains, adaptation, calibration data, regime definitions, and resource measurements. |

## Required wording controls

- Use **“convergent preliminary evidence”** for the TimesFM rank change across Bitcoin and electricity.
- Use **“researcher-defined composite evaluation framework”** for the Trust Score.
- State explicitly that the Explainability Score is broader than standard feature-attribution XAI.
- Do not say foundation models have not been evaluated across domains.
- Do not call PatchTST or iTransformer foundation models unless a cited source and the exact configuration support that claim.
- Do not attach literature citations to repository numbers; cite the frozen artifact or case-study file.
- Avoid “first,” “unprecedented,” and universal superiority or calibration claims.

## Access action before proposal revision

Retrieve the publisher full text of Diebold and Mariano (1995) through university access and verify assumptions, long-run variance details, overlapping-horizon treatment, and limitations. Recent central sources are accessible; no other university-access item currently blocks proposal integration.
