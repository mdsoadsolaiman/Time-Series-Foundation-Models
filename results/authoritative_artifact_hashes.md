# Authoritative Artifact Hashes

These SHA-256 hashes freeze the authoritative and supporting evidence before the final documentation and figure-organisation pass. All values were recomputed after the pass and matched exactly.

| Artifact | SHA-256 | Role | Authoritative status |
|---|---|---|---|
| `results/validated_forecasts.csv` | `A84D09F24CE9549EF30D84E958738DB9C2FC68B37342267978697009493820A0` | Bitcoin aligned final forecasts | Authoritative |
| `results/baseline_forecasts.csv` | `D3140C5B0278D9A2D3A12FC812B72A4487DEFA622B915C6465BBD0610210BAF9` | Bitcoin baseline evidence | Supporting authoritative evidence |
| `results/persistence_enhanced_lstm_forecast.csv` | `3D3EE249A63560CF8C7E0BE7375F23F783DB670C857FCE4FC7AF663123405BE2` | Bitcoin PE-LSTM forecasts | Supporting authoritative evidence |
| `results/chronos_bolt_tiny_forecast.csv` | `AD075664AA9F1330086016B118E8164298A2135D50191725336AE02C3BAAE802` | Bitcoin Chronos forecasts | Supporting authoritative evidence |
| `results/timesfm_forecast.csv` | `6FB06E487BDB7DA7410651AD418F4B1F8D02B72E5380D471A1984765395F9CC3` | Bitcoin TimesFM forecasts | Supporting authoritative evidence |
| `results/arima_rolling_forecast.csv` | `74E3B7BE81552A8FBB4E24FD8479E9FD35C84C2F3DA28F7776452768DAFFC856` | Bitcoin rolling one-step ARIMA forecasts | Authoritative evidence |
| `results/arima_validation_forecast.csv` | `610BDFE07039C581CE9971E2E277F405F0412AB8ACF0637AFEB9FB31143B378D` | Bitcoin training-only ARIMA validation forecasts | Authoritative evidence |
| `results/prophet_rolling_forecast.csv` | `16B4CC848D0A34A8BA5BA5C235720DC31F2C41A5EAA99EDC0DD00DD001470616` | Bitcoin periodic-refit Prophet forecasts | Authoritative evidence |
| `results/simple_exp_smoothing_forecast.csv` | `12D79C344528BB3DBC97698B7A519436DDDD8ED4D7984E218AD61FC887DA0B03` | Bitcoin rolling one-step Simple Exponential Smoothing forecasts | Authoritative evidence |
| `results/holt_winters_forecast.csv` | `8D2A1AA275E67BF87FE90298D24B0961F2D3BE759FF4FC1A795B638C43BAB4BF` | Bitcoin rolling one-step Holt-Winters forecasts | Authoritative evidence |
| `results/simple_exp_smoothing_validation_forecast.csv` | `0B682C0AEB929E048875AEEDD18EFDACE312CD3B6776406BA1B556C3BD04579D` | Bitcoin training-only Simple Exponential Smoothing validation forecasts | Authoritative evidence |
| `results/holt_winters_validation_forecast.csv` | `6D524D6705F7F8765F36ED5457FC05025911A4F7D36D3D2252BA48C4BA799AA8` | Bitcoin training-only Holt-Winters validation forecasts | Authoritative evidence |
| `results/persistence_enhanced_transformer_forecast.csv` | `8F7DADAB20DFFA7DDB51362675F4C2E6E4A4FCEA3AD6412C94EC911B4E96CAEF` | Bitcoin deterministic PE-Transformer forecasts | Supporting authoritative evidence |
| `results/persistence_enhanced_transformer_validation_forecast.csv` | `B4382E20696C4F7D675324085EFBDBA6A8E5DD0EBBA6984E1DF0AF539C7653A9` | Bitcoin training-only PE-Transformer validation forecasts | Authoritative evidence |
| `results/foundation_uncertainty_calibration.csv` | `F4054321A7C56177E7452ECBCC9F08A262F5FACAAF0DC39DD8E1E8E0A1832AAA` | Bitcoin native and training-calibrated intervals | Authoritative evidence |
| `results/foundation_uncertainty_summary.csv` | `F83D7C6E73CBAB24936470712900269EBEBC90F418177303218E10BD03CFE0F0` | Bitcoin uncertainty calibration summary | Authoritative evidence |
| `results/bitcoin_trust_scores_penalised.csv` | `F803AF494C1E9C9BA165AF64B8EDD5126E8CF3476BD1DEE801E5A32AA51B2155` | Bitcoin missing-evidence-penalised Trust Scores | Authoritative evidence |
| `results/bitcoin_trust_scores_evidence_available.csv` | `030D6BBA1CF4ACDC09CD4B8266471002F9C1154ED53A96AFEA75478EE76C3FD5` | Bitcoin evidence-available Trust Scores | Authoritative evidence |
| `results/bitcoin_dm_pairwise_results.csv` | `294B74D2E4282C9D3FF55665BBDCEAD5BFA2E1188D11EBABE53F56D0B90653C0` | Bitcoin full pairwise Diebold-Mariano results | Authoritative evidence |
| `results/bitcoin_point_forecast_metrics_v2.csv` | `DF01DC83C1C1BAD16610C5ADAA8F3B8513D88E440FA1CCFF67A03048DA30B3D8` | Bitcoin-v1 artifact-derived metrics | Authoritative rebuilt evidence |
| `results/bitcoin_regime_thresholds_training.csv` | `40A3276296ED9C40A92D64F736E3FDE93BC3C3AD9FFEA48585473A168E265F15` | Training-only Bitcoin regime thresholds | Authoritative rebuilt evidence |
| `results/bitcoin_regime_robustness_training_defined.csv` | `B5F60B0A1AF1D46364743E882F2EED2AF08CBB83B5390DB299A9AC45F0B743D7` | Training-defined regime evaluation | Authoritative rebuilt evidence |
| `results/bitcoin_temporal_stability.csv` | `19C21B51B2B10EAD05FC9B0EF11DBD192F34088E7D2085CEF3FBBDBA50FD1E76` | Earlier/Middle/Later stability evidence | Authoritative rebuilt evidence |
| `results/bitcoin_uncertainty_evidence_v2.csv` | `FE082169F2F9A865CDA66A4A7E03309D187C0C7E1D14046476BA06063BBD7441` | Method-separated Bitcoin uncertainty evidence | Authoritative rebuilt evidence |
| `results/bitcoin_dm_pairwise_results_hac_holm.csv` | `5ABE3500960BD89BB5EB580B7A82F62319E6167B9304AC4AF84EE03494BD9F47` | HAC DM tests with Holm correction | Authoritative corrected inference |
| `results/bitcoin_transparency_auditability_rubric.csv` | `320B40E4621CD75EC807640F689F7CD914A8F17C0188F5774B66C5E0EEFF4B6D` | Documented transparency/auditability rubric | Authoritative rebuilt evidence |
| `results/bitcoin_trustworthiness_components_v2.csv` | `77877D13EDF53F18BB101CD79369325967980EA92E5C6454048EDB6E87DA0E53` | Component-first Bitcoin synthesis | Authoritative rebuilt evidence |
| `results/bitcoin_trust_score_sensitivity_v2.csv` | `71FAC64AB5A03D2156CEB33DCB98FBAE229632537FEC86B52BC44C6A093D4EEE` | Exploratory composite sensitivity | Authoritative rebuilt evidence |
| `results/electricity/protocol_a_validated_forecasts.csv` | `CC362BACCBB7B612C7499832792C07769FF2D098222116C13B8D9BF3E46A601C` | Electricity rolling one-step forecasts | Authoritative |
| `results/electricity/protocol_b_validated_forecasts.csv` | `AEA1D57D987BBC89CC8C9D6AEFE95AFEF2A46AAB77FEBA6649EE85B78B0533CE` | Electricity 48-step day-ahead forecasts | Authoritative |
| `results/electricity/protocol_b_validated_horizon_metrics.csv` | `58DBEBD52C62AF3C90B7656DC487863A510A78AE01661DB6777F709C475658E3` | Validated horizon metrics | Authoritative |
| `results/electricity/protocol_a_robustness.csv` | `C412142321D0A55AB8B59EA24BEB9EA6B907B9FDFB8CE48ADA1C69B633A5216D` | Protocol A robustness | Authoritative evidence |
| `results/electricity/protocol_b_robustness.csv` | `174ECFF8CD873524B747AB57E76337ADB9525B9D9C582C4D4D16CFCB7F2C019E` | Protocol B robustness | Authoritative evidence |
| `results/electricity/protocol_a_generalisation.csv` | `0083D0F64C26B539292561CF6CBAF6E58A5242E66F95A405E95AFD4A5274E483` | Protocol A temporal generalisation | Authoritative evidence |
| `results/electricity/protocol_b_generalisation.csv` | `CBEF19FB6CB5FB3EE00F6989EA3018E528310A4CB59D6C035154FBF2971B0302` | Protocol B temporal generalisation | Authoritative evidence |
| `results/electricity/uncertainty_summary.csv` | `2CC86B36F102052936C4894C8B86279048E1F946AA394D10849AC26E19E46D97` | Electricity interval evidence | Authoritative evidence |
| `results/electricity/protocol_a_trust_scores.csv` | `A2CDCEECD39457AE4C90C912D6AC35540231F2E9F2300C666076EF35042309E7` | Protocol A Trust Scores | Authoritative evidence |
| `results/electricity/protocol_b_trust_scores.csv` | `E5705845BF6CAF3F1BF3A7CE79E365265A16F5BB58C7319984351D1247DA0B23` | Protocol B Trust Scores | Authoritative evidence |
| `results/electricity/trust_score_sensitivity.csv` | `D0A2EBF81380ED60A8BB0124CB5F291E5A8D5D7E6CC44B54EC31D517148988D1` | Trust-weight sensitivity | Authoritative evidence |
| `results/electricity/protocol_a_dm_tests.csv` | `B41FBEB7D7C6E1E6E3966A47E9187CD901DC697916BEC7FBD0E5DD2372475D76` | Protocol A DM tests | Authoritative evidence |
| `results/electricity/protocol_b_dm_tests.csv` | `68885BCA93E9D25194230EE39D856F98BCBB9D022DCAEA78A3688C1A8DAF4550` | Protocol B DM tests | Authoritative evidence |
| `results/electricity/protocol_a_effect_sizes.csv` | `97F5BF1F0A6CD3851D07676C8649D7F0744C5DD18E2472E9E785B8F6947C535A` | Protocol A effect sizes | Authoritative evidence |
| `results/electricity/protocol_b_effect_sizes.csv` | `3AEFB912598BB60AFFDF59EDECA8F42F208AE01C853D08A1BDEBBC155C8BADB3` | Protocol B effect sizes | Authoritative evidence |
| `results/electricity/protocol_b_horizon_significance.csv` | `9E109EC114CCB61C54D26BF0C1EA958DCAE145DD795282A0F6A2AAF42BDA42A5` | Horizon-level significance | Authoritative evidence |
| `results/cross_domain_model_comparison.csv` | `E521C4F93A605FD11241622C7F479205D067044FDB3D89CB19941E050393601C` | Cross-domain ranks and metrics | Authoritative synthesis |
| `results/cross_domain_foundation_model_comparison.csv` | `7453C25FD6F014934C4240BD2598C9FD990CACBB576418D669FC418DB5D0DEC2` | Foundation-model comparison | Authoritative synthesis |
| `results/cross_domain_uncertainty_comparison.csv` | `32FECE2416050BDEEB2A8965C701B34D8BB5747869693B2D062854F87AD4FA9F` | Cross-domain calibration comparison | Authoritative synthesis |
| `results/cross_domain_significance_summary.csv` | `5109E88D0C4D1F538539691404CD36AB9FEA9B55EDCD6A04C5E68DB9FF937BB0` | Cross-domain significance summary | Authoritative synthesis |
| `results/cross_domain_rank_stability.csv` | `785B22B6B6D3B833D8EB2B2103C615E45622A62C174FAD834331E6CFF7FA316C` | Cross-domain model-family rank stability | Authoritative synthesis |
| `results/cross_domain_trust_comparison.csv` | `C2CE17DA6277C3B3F8C4FC940606DF6F5431A15BD4D4E69005B5462871330C9A` | Cross-domain trust-component comparison, 8 comparable families | Authoritative synthesis |
| `results/cross_domain_comparable_families.csv` | `00732C7B2891BCF355A46DA297615B72E677F4246AA9ADEC73FAFA9491FEBDC1` | Cross-domain model-family comparability map | Authoritative synthesis |
| `results/cross_domain_not_comparable.csv` | `0C08B30C451466F55977C5DB4A22F0375821D4C184C74EE33E4239B67A93E13E` | Cross-domain explicitly non-comparable items | Authoritative synthesis |

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
