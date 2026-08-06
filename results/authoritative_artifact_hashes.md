# Authoritative Artifact Hashes

These SHA-256 hashes freeze the authoritative and supporting evidence before the final documentation and figure-organisation pass. All values were recomputed after the pass and matched exactly.

| Artifact | SHA-256 | Role | Authoritative status |
|---|---|---|---|
| `results/validated_forecasts.csv` | `0F2E6A028102A9FD4D5788A18E80CFC71D694BC28E4E72F36778122A25D25A4F` | Bitcoin aligned final forecasts | Authoritative |
| `results/baseline_forecasts.csv` | `C25F705512C22A22EBC9B56190A47F651436B3B1A9891997DE598F0BB855D0D5` | Bitcoin baseline evidence | Supporting authoritative evidence |
| `results/persistence_enhanced_lstm_forecast.csv` | `3AC102B0E89E184948D14799BAB4078E90293DFDCC6E513E3417038FE71AD93F` | Bitcoin PE-LSTM forecasts | Supporting authoritative evidence |
| `results/chronos_bolt_tiny_forecast.csv` | `0057334E226D9CD11439F55F004902AB4EFE88222434732A2E7D908A30BF4DD9` | Bitcoin Chronos forecasts | Supporting authoritative evidence |
| `results/timesfm_forecast.csv` | `3960962297E7296C3ACB31946C47AB1E019A36C6611960EB2091071892695C10` | Bitcoin TimesFM forecasts | Supporting authoritative evidence |
| `results/electricity/protocol_a_validated_forecasts.csv` | `E48D3E53BE01F2365E782CEB192B000044A4964BF7FA7EAAA104C8F640732C95` | Electricity rolling one-step forecasts | Authoritative |
| `results/electricity/protocol_b_validated_forecasts.csv` | `064D0D63688126B53033C18DE94B9232173E94CC595920DF9C45AB3442DCB19E` | Electricity 48-step day-ahead forecasts | Authoritative |
| `results/electricity/protocol_b_validated_horizon_metrics.csv` | `868E03ACEDBB444B25B4F43E4670CBDE2A7A8BE9E93C5447ECF79F56E32CA8E3` | Validated horizon metrics | Authoritative |
| `results/electricity/protocol_a_robustness.csv` | `19D7DAECA346194F740B997D6B898D0C4A2CF48F5EED7D43CB6D874C486A30B6` | Protocol A robustness | Authoritative evidence |
| `results/electricity/protocol_b_robustness.csv` | `788F88F21A7C1138F74AA0C674A137A8344B97B1228F8464C42D02DB3EDFCFDA` | Protocol B robustness | Authoritative evidence |
| `results/electricity/protocol_a_generalisation.csv` | `E6A5098EC8C09E047746407D38D0EE203368501FF32FBB2CF23A2FB16A4CE23C` | Protocol A temporal generalisation | Authoritative evidence |
| `results/electricity/protocol_b_generalisation.csv` | `7423A61DFE8A769C8B2D4D878A9DA58FC23398C537EFA1C1DB5940CDE877EC3B` | Protocol B temporal generalisation | Authoritative evidence |
| `results/electricity/uncertainty_summary.csv` | `170D1E63207300A4EA4279630DBB3949A17CABD700E8F418869A980346F4376B` | Electricity interval evidence | Authoritative evidence |
| `results/electricity/protocol_a_trust_scores.csv` | `964D8175B085DCC8F3B15B1BECDD21AA25746E1080A33110BBCF64FF7892CA3F` | Protocol A Trust Scores | Authoritative evidence |
| `results/electricity/protocol_b_trust_scores.csv` | `C6202DE846AD3001BD2861A8489E7132D1458328D834DDDFC6D4A009EA03AF76` | Protocol B Trust Scores | Authoritative evidence |
| `results/electricity/trust_score_sensitivity.csv` | `E84D212349F90953ECDCBB162F2826A9EE1EDDE5CDB8CC84EA98687118751EC2` | Trust-weight sensitivity | Authoritative evidence |
| `results/electricity/protocol_a_dm_tests.csv` | `D913B8A3C6BD2EF4392A030045AA3E2F50CA7BC53D99D0CC81A33CBF1454D2F3` | Protocol A DM tests | Authoritative evidence |
| `results/electricity/protocol_b_dm_tests.csv` | `79C7B5A1C058AB7F5E4904ED0168D2DFCCDC73D68E05A84B933713FE410C16DE` | Protocol B DM tests | Authoritative evidence |
| `results/electricity/protocol_a_effect_sizes.csv` | `AA689049399834A8B6B9588646B551915C7E93FF7C7F150CC25831701D79A126` | Protocol A effect sizes | Authoritative evidence |
| `results/electricity/protocol_b_effect_sizes.csv` | `D4F1F10B502AADCD482A50DDE128A8DFE63754EF8B106583C15D2CC1EAEE30E2` | Protocol B effect sizes | Authoritative evidence |
| `results/electricity/protocol_b_horizon_significance.csv` | `DF5F71D1E66A8B67E4E95709599A5CE344767E7E0821E1353D118EFF4D86CD16` | Horizon-level significance | Authoritative evidence |
| `results/cross_domain_model_comparison.csv` | `E24C650C9383D98CD18300C827B94F2CA29DBF41FB0BE8F8E0C1DA986B51DF0A` | Cross-domain ranks and metrics | Authoritative synthesis |
| `results/cross_domain_foundation_model_comparison.csv` | `3BEAEAEB2BA9C0493CC1E96FF0F44B9B7EEBA49184ACF4ACB839C634F62ECFB4` | Foundation-model comparison | Authoritative synthesis |
| `results/cross_domain_uncertainty_comparison.csv` | `591637120FAB3C49A6D3130DBE3243B6A616FB1C0F095679B2CD58D877B57BA2` | Cross-domain calibration comparison | Authoritative synthesis |
| `results/cross_domain_significance_summary.csv` | `AB16CBB3CD382C11B6F8B0A7FD39D890684F6C03E9A4DBBEFFDFE330F4D19379` | Cross-domain significance summary | Authoritative synthesis |

Hash equality establishes byte-level preservation; it does not replace methodological validation documented in the case studies.
