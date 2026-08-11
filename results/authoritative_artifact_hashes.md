# Authoritative Artifact Hashes

These SHA-256 hashes freeze the authoritative and supporting evidence before the final documentation and figure-organisation pass. All values were recomputed after the pass and matched exactly.

| Artifact | SHA-256 | Role | Authoritative status |
|---|---|---|---|
| `results/validated_forecasts.csv` | `AF8252F0D8965251A9CAEA654D10E6FCDB511CDB547D828A36DAB5DAC0ED0725` | Bitcoin aligned final forecasts | Authoritative |
| `results/baseline_forecasts.csv` | `C25F705512C22A22EBC9B56190A47F651436B3B1A9891997DE598F0BB855D0D5` | Bitcoin baseline evidence | Supporting authoritative evidence |
| `results/persistence_enhanced_lstm_forecast.csv` | `1B198292F339C20E6C0AF611E50205754829ED758653150C90F1704A710B18CF` | Bitcoin PE-LSTM forecasts | Supporting authoritative evidence |
| `results/chronos_bolt_tiny_forecast.csv` | `0057334E226D9CD11439F55F004902AB4EFE88222434732A2E7D908A30BF4DD9` | Bitcoin Chronos forecasts | Supporting authoritative evidence |
| `results/timesfm_forecast.csv` | `3960962297E7296C3ACB31946C47AB1E019A36C6611960EB2091071892695C10` | Bitcoin TimesFM forecasts | Supporting authoritative evidence |
| `results/arima_rolling_forecast.csv` | `ACA63F0202B1B990D80ADA0BC000A67484108F3C6341F0C4C1D8E5D055D79A78` | Bitcoin rolling one-step ARIMA forecasts | Authoritative evidence |
| `results/arima_validation_forecast.csv` | `F3BCCC94BF786549D3DA4A4873A57A8FD4962AF3956F225113ACCCCAC4C3AF5C` | Bitcoin training-only ARIMA validation forecasts | Authoritative evidence |
| `results/prophet_rolling_forecast.csv` | `6F0B505E7290A475B6170B93782D8E9A41CAD3791D50A81517E3E847706FB9B2` | Bitcoin periodic-refit Prophet forecasts | Authoritative evidence |
| `results/simple_exp_smoothing_forecast.csv` | `D11D0FBC368E9F7635E0745D42E325D73EE8D662E14AC82437C5535BDF8F8927` | Bitcoin rolling one-step Simple Exponential Smoothing forecasts | Authoritative evidence |
| `results/holt_winters_forecast.csv` | `C126C6C6BBF4BE1925881B540A53C997B40C61D204954680EF2242E91634016B` | Bitcoin rolling one-step Holt-Winters forecasts | Authoritative evidence |
| `results/simple_exp_smoothing_validation_forecast.csv` | `6AA9D1A9E58D6D4E5A67D16B981C270F4671758DC4859A3805529333373545D0` | Bitcoin training-only Simple Exponential Smoothing validation forecasts | Authoritative evidence |
| `results/holt_winters_validation_forecast.csv` | `91237410D97DC4F9ED9D65121F5DA699091768CFE132B0D8674B52F9E14A970E` | Bitcoin training-only Holt-Winters validation forecasts | Authoritative evidence |
| `results/persistence_enhanced_transformer_forecast.csv` | `7C1A50F53872CA1DB11C520C844340BB25736B58050FEAF4F9079D6AC151F0DE` | Bitcoin deterministic PE-Transformer forecasts | Supporting authoritative evidence |
| `results/persistence_enhanced_transformer_validation_forecast.csv` | `72D32C3F588B79B18C261A2AAC3CBF7E36D41C35CC9998162D99DD51F6A80616` | Bitcoin training-only PE-Transformer validation forecasts | Authoritative evidence |
| `results/foundation_uncertainty_calibration.csv` | `9503CC926176B8BD64B5B785A9AC39A455E9D6D642230BAB5C7173EC0F41CA12` | Bitcoin native and training-calibrated intervals | Authoritative evidence |
| `results/foundation_uncertainty_summary.csv` | `9DA734CB9265E07FE8AE47122F674E098E5395C7CD7EBD74E9E253DFFF8FD654` | Bitcoin uncertainty calibration summary | Authoritative evidence |
| `results/bitcoin_trust_scores_penalised.csv` | `43334D4695AE3DC6E805C9265C1A204E41DD94FD3B492311B525793DDBDEEF3F` | Bitcoin missing-evidence-penalised Trust Scores | Authoritative evidence |
| `results/bitcoin_trust_scores_evidence_available.csv` | `50B17AAE7B67FC67583745D44487C9AF57D5B909E6FB4C0575B09744FC661DD6` | Bitcoin evidence-available Trust Scores | Authoritative evidence |
| `results/bitcoin_dm_pairwise_results.csv` | `DE48D5DC77E591ADE6FBB67D08AE16F8A6961393C23C72801B447B90D3D61B96` | Bitcoin full pairwise Diebold-Mariano results | Authoritative evidence |
| `results/bitcoin_point_forecast_metrics_v2.csv` | `C848334EB888A9C318744D2DF414FDA2D763A849A6D9276E6C56DDB911E706AD` | Bitcoin-v1 artifact-derived metrics | Authoritative rebuilt evidence |
| `results/bitcoin_regime_thresholds_training.csv` | `411E0F1181696FE08C79D8462420710F98971F9059C540571352BFAD956AE31A` | Training-only Bitcoin regime thresholds | Authoritative rebuilt evidence |
| `results/bitcoin_regime_robustness_training_defined.csv` | `5DE17BA988DE4FFA80A83ADA1A27672DB5E27948EE59B460DFFA82807087868E` | Training-defined regime evaluation | Authoritative rebuilt evidence |
| `results/bitcoin_temporal_stability.csv` | `482CFB116D9E3C67AE258B473BB3B98F08876D8ED2AFCAF22E8C7463B4EBFE5E` | Earlier/Middle/Later stability evidence | Authoritative rebuilt evidence |
| `results/bitcoin_uncertainty_evidence_v2.csv` | `847871A6C64ADFB746C2A3EDB936E2D65C01F20E5020D686CA2FC80F8FD262FC` | Method-separated Bitcoin uncertainty evidence | Authoritative rebuilt evidence |
| `results/bitcoin_dm_pairwise_results_hac_holm.csv` | `3C8211FA6E5A35F164A8F7727E078DECBA0ADFF259E904323D6ADD6392783EEB` | HAC DM tests with Holm correction | Authoritative corrected inference |
| `results/bitcoin_transparency_auditability_rubric.csv` | `7161C4F15696187015F37F76FCB6A1B3FCD0A1B6D438643040C2E99CA332312B` | Documented transparency/auditability rubric | Authoritative rebuilt evidence |
| `results/bitcoin_trustworthiness_components_v2.csv` | `43F3D1C769D50EBD9D83C74B0E1257FCDE0AA3077C689C841478F5D08471065B` | Component-first Bitcoin synthesis | Authoritative rebuilt evidence |
| `results/bitcoin_trust_score_sensitivity_v2.csv` | `593E62A809157E8C973A64E57F5E57C7E366420AE926F0812AD125D0CE0F16C5` | Exploratory composite sensitivity | Authoritative rebuilt evidence |
| `results/electricity/protocol_a_validated_forecasts.csv` | `91EFF0A09293B2FC668BCD62CE92A9BCF13C84FC9458B5F60F2F2E08E36A9020` | Electricity rolling one-step forecasts | Authoritative |
| `results/electricity/protocol_b_validated_forecasts.csv` | `F520CBE70763F343F5FB53DBBE2F786A35E5719175330987031877EE7A4970D5` | Electricity 48-step day-ahead forecasts | Authoritative |
| `results/electricity/protocol_b_validated_horizon_metrics.csv` | `22D12E1FBE84EFE55BB3BF15C9136C3BB7CBF1E9A6E524F1F663BA5EB156993C` | Validated horizon metrics | Authoritative |
| `results/electricity/protocol_a_robustness.csv` | `F062D10ECA7B89F37A3CC5BFAFE51FB2DA592BA939B8C0B8A8648ED0F6E2B082` | Protocol A robustness | Authoritative evidence |
| `results/electricity/protocol_b_robustness.csv` | `1CAB0B0F966D5EF93C6BA6548F18597545CD35998720A0B2B627BFD3D5970727` | Protocol B robustness | Authoritative evidence |
| `results/electricity/protocol_a_generalisation.csv` | `6C03D15AF90512BAF1E87B09542F5DC5C70ACF9C57F335A5029E37D346FFF351` | Protocol A temporal generalisation | Authoritative evidence |
| `results/electricity/protocol_b_generalisation.csv` | `5CCDD97774D3041DF6E1DAB8DA05AB29E82B02C5E7B08EF12F8385FE5F5E52F4` | Protocol B temporal generalisation | Authoritative evidence |
| `results/electricity/uncertainty_summary.csv` | `814CC34DF9137DF6C2F33891C1278B0A4AE8746079D9EC0C1B07A4212496A668` | Electricity interval evidence | Authoritative evidence |
| `results/electricity/protocol_a_trust_scores.csv` | `4A9C3D36BB1C96AE82E0B25C92DF3F08FABBA610122592CF191BD9F899D18A6B` | Protocol A Trust Scores | Authoritative evidence |
| `results/electricity/protocol_b_trust_scores.csv` | `C73CA588CF1A8BAAC211D950A6D24E4E49DBCEFEAF1BF30487310D6B4AC0C2F0` | Protocol B Trust Scores | Authoritative evidence |
| `results/electricity/trust_score_sensitivity.csv` | `06277B13923BDA48B1E10BC2F363598223C83F86D7A9EC2E0570768D8B8C6BE6` | Trust-weight sensitivity | Authoritative evidence |
| `results/electricity/protocol_a_dm_tests.csv` | `E457E08B3F5FFE07B8181B3359C6DBA601821AF14D603974021DCF6622A9C57F` | Protocol A DM tests | Authoritative evidence |
| `results/electricity/protocol_b_dm_tests.csv` | `238AC1673B49C7A085E8EE5F8D52A92597FB41CC773D77EEFA0F30FB4970433F` | Protocol B DM tests | Authoritative evidence |
| `results/electricity/protocol_a_effect_sizes.csv` | `50BDEBE26643BF03857C06B16703DF973FA9418982DA3D40950D608E2355062A` | Protocol A effect sizes | Authoritative evidence |
| `results/electricity/protocol_b_effect_sizes.csv` | `7712C38B5BE3AD20A43EB57D6184BD0A665E4219D91D761CA5A8A75523109E72` | Protocol B effect sizes | Authoritative evidence |
| `results/electricity/protocol_b_horizon_significance.csv` | `DF5F71D1E66A8B67E4E95709599A5CE344767E7E0821E1353D118EFF4D86CD16` | Horizon-level significance | Authoritative evidence |
| `results/cross_domain_model_comparison.csv` | `3DE7D10CB9662E63ABF07FD19374D12A371DCBCCB469E142FD5238CB8E1B2D79` | Cross-domain ranks and metrics | Authoritative synthesis |
| `results/cross_domain_foundation_model_comparison.csv` | `EA3C90B5AB7701368EDE6E88EC60453E07D85586749C3704E74A87D49AC5C7B3` | Foundation-model comparison | Authoritative synthesis |
| `results/cross_domain_uncertainty_comparison.csv` | `7487BCFCC87D222BA2F243B0248B0C3DB24D38C9FD14C6DD321BA852888189DB` | Cross-domain calibration comparison | Authoritative synthesis |
| `results/cross_domain_significance_summary.csv` | `61BF9251092246E9B6E69D7FA5FF79E9AF0BED2441F9B60D7B59A006909C179D` | Cross-domain significance summary | Authoritative synthesis |
| `results/cross_domain_rank_stability.csv` | `2A7BDE59F1A501EA048B2CEC45CF656B35013432A82ABFCFB54EFA9BF5A6F069` | Cross-domain model-family rank stability | Authoritative synthesis |
| `results/cross_domain_trust_comparison.csv` | `B54564546C95D47F86B7A3A683D4F891EB55617AD2AD195B479472DD9B496275` | Cross-domain trust-component comparison, 8 comparable families | Authoritative synthesis |
| `results/cross_domain_comparable_families.csv` | `36114632236F71B4AB5DC42F0CF54B2EC46742F1207D8746D24DFBCEB1792723` | Cross-domain model-family comparability map | Authoritative synthesis |
| `results/cross_domain_not_comparable.csv` | `813062D4F4E19B49AE4E6A5E6E13315BB402507B3D08FCA7C51FBDA68ABEB12C` | Cross-domain explicitly non-comparable items | Authoritative synthesis |

Hash equality establishes byte-level preservation; it does not replace methodological validation documented in the case studies.

## Changelog

- `results/persistence_enhanced_lstm_forecast.csv`: replaced the prior nondeterministic vector with the Step 1 bit-identical TensorFlow result.
- `results/validated_forecasts.csv`: refreshed in Steps 3 and 5 with the deterministic PE-LSTM vector plus ARIMA and Prophet forecasts.
- `results/arima_rolling_forecast.csv`: added the Step 5 rolling one-step ARIMA vector.
- `results/prophet_rolling_forecast.csv`: added the Step 5 strictly past-only 30-day periodic-refit Prophet vector.
- `results/foundation_uncertainty_calibration.csv`: added Step 6 native and training-only conformalized 80% intervals.
- `results/foundation_uncertainty_summary.csv`: added Step 6 native-versus-calibrated coverage and width evidence.
- `results/bitcoin_trust_scores_penalised.csv`: added the Step 6 complete missing-evidence-penalised ranking.
- `results/bitcoin_trust_scores_evidence_available.csv`: added the Step 6 complete evidence-available ranking.
- `results/bitcoin_dm_pairwise_results.csv`: added all 15 Step 7 pairwise significance comparisons.
- Step B — Notebook 08 diff resolution: no artifact hash changed; the rerun-only notebook diff was discarded after all saved audit values reproduced exactly.
- `results/arima_validation_forecast.csv`: added in Step C to preserve the 1,061 training-only ARIMA forecasts used for empirical residual intervals; no test date is present.
- `results/bitcoin_trust_scores_penalised.csv`: changed in Step C because ARIMA now has an 80%/95% empirical uncertainty score instead of a missing-evidence penalty; ARIMA rose from 83.559942 to 96.552205 while Naive remained first at 97.810622.
- `results/bitcoin_trust_scores_evidence_available.csv`: changed in Step C because ARIMA's uncertainty dimension is now included rather than excluded and renormalised; ARIMA fell from 98.305814 to 96.552205, so Naive now leads at 97.810622.
- Fair exponential-smoothing rebuild: added true rolling one-step test and training-only validation vectors for Simple Exponential Smoothing and additive-trend non-seasonal Holt-Winters, each using a strict 128-day prior-only context.
- `results/validated_forecasts.csv`: expanded from eight to ten columns by merging the two new 1,061-row vectors.
- `results/bitcoin_trust_scores_penalised.csv` and `results/bitcoin_trust_scores_evidence_available.csv`: recomputed for nine models with validation-residual empirical uncertainty evidence for both smoothing models; Naive remains first.
- `results/bitcoin_dm_pairwise_results.csv`: expanded from 15 to 28 comparisons so both smoothing models are tested against every previously saved Bitcoin forecast vector.
- Classical-notebook consolidation: moved the authoritative ARIMA, Simple Exponential Smoothing, and Holt-Winters rolling displays from Notebook 05 into their original Notebook 02 home beside the unchanged historical static sections. Notebook 05 now retains Prophet and deferred PatchTST/iTransformer content only. All 37 protected artifacts remained byte-identical, so no SHA-256 value changed.
- Bitcoin presentation alignment: refreshed only the derived `results/cross_domain_model_comparison.csv` Bitcoin neural row from the frozen PE Log-Return LSTM vector, replacing stale metrics and the ambiguous display name. Electricity rows and all forecast artifacts remained byte-identical.
- Persistence-Enhanced Transformer freeze: added byte-identical test and training-only validation vectors, expanded `validated_forecasts.csv` to eleven columns, recomputed both Trust Score variants for ten models, and expanded Bitcoin DM evidence to all 45 pairs. No electricity or cross-domain artifact changed.
- Electricity classical-comparator expansion: added ARIMA, SARIMA, Prophet, Simple Exponential Smoothing, and Holt-Winters (13 models total, up from 8). `protocol_a/b_validated_forecasts.csv` expanded to 15/17 columns; `protocol_b_validated_horizon_metrics.csv` to 624 rows; `protocol_a/b_robustness.csv` to 52 rows; `protocol_a/b_generalisation.csv` to 39 rows; `uncertainty_summary.csv` to 26 rows (5 new models marked unavailable, same as the 6 existing models without saved residual evidence); `protocol_a/b_trust_scores.csv` and `trust_score_sensitivity.csv` recomputed for 13 models; `protocol_a/b_dm_tests.csv` and `protocol_a/b_effect_sizes.csv` expanded from 28 to 78 pairs (C(13,2)). All raw per-model metrics, DM statistics, and effect sizes for the original 8 models and 28 pairs reproduced byte-identically; only set-relative quantities (relative scores, BH-adjusted p-values, ranks) changed, as expected when the comparison set grows. `protocol_b_horizon_significance.csv` (a curated 4-model subset) was not touched.
- Cross-domain comparison rebuild: expanded from a reduced 4-common-model Bitcoin set to 8 genuinely comparable model families (Naive, Chronos-Bolt-Tiny, TimesFM, best ARIMA-family, Prophet, Simple Exponential Smoothing, Holt-Winters, LSTM-family), each explicitly labelled where domains use best-in-family or model-class representatives rather than identical models. `cross_domain_model_comparison.csv` now reports the full roster (10 Bitcoin, 13 Electricity per protocol, up from 4+8+8). `cross_domain_foundation_model_comparison.csv` and the new `cross_domain_significance_summary.csv` now compare Chronos/TimesFM against each task's CURRENT strongest baseline (SARIMA for both Electricity protocols, up from DHR-ARIMA/Daily-Seasonal-Naive) -- notably, SARIMA now has significantly lower squared-error loss than TimesFM in Electricity Protocol A (BH-corrected p=9.6e-05) despite TimesFM's lower MAE/MASE-48. `cross_domain_significance_summary.csv` now correctly uses Holm-corrected p-values for Bitcoin (was previously raw p-values, an inconsistency versus Bitcoin's own frozen `bitcoin_dm_pairwise_results_hac_holm.csv`) alongside Benjamini-Hochberg-corrected p-values for Electricity, with an explicit methodology-reconciliation note added to the notebook. `cross_domain_uncertainty_comparison.csv` now includes Bitcoin's native AND post-hoc-calibrated coverage (previously native only), kept in separate rows. Added four new authoritative synthesis artifacts: `cross_domain_rank_stability.csv`, `cross_domain_trust_comparison.csv`, `cross_domain_comparable_families.csv`, `cross_domain_not_comparable.csv`. Zero Bitcoin or Electricity per-domain result files were read differently or modified -- all four rebuilt/new files are pure downstream synthesis of already-frozen per-domain artifacts.
