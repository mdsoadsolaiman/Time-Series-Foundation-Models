"""Rebuild the four cross-domain comparison CSVs from frozen per-domain artifacts.

Reads only already-frozen results from both domains (Bitcoin root results/*.csv,
Electricity results/electricity/*.csv). Never fits, retrains, or regenerates a
per-domain forecast, and never writes to a per-domain results file. Raw MAE/RMSE are
never pooled numerically across domains -- only within-domain ranks and each domain's
own relative/percentage metrics are compared side by side.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

BITCOIN_PROTOCOL = "Rolling one-step daily"
ELEC_A_PROTOCOL = "Protocol A: rolling one-step 30-minute"
ELEC_B_PROTOCOL = "Protocol B: 48-step day-ahead"

ELEC_DISPLAY_NAME = {
    "Daily_Seasonal_Naive": "Daily Seasonal Naive", "Weekly_Seasonal_Naive": "Weekly Seasonal Naive",
    "Moving_Average": "Moving Average", "DHR_ARIMA": "DHR-ARIMA",
    "Simple_Exponential_Smoothing": "Simple Exponential Smoothing", "Holt_Winters": "Holt-Winters",
    "Chronos_Bolt_Tiny": "Chronos-Bolt-Tiny",
}


def elec_name(model: str) -> str:
    return ELEC_DISPLAY_NAME.get(model, model)


# ---------------------------------------------------------------------------
# Task 1 inputs / Task 2 comparability map
# ---------------------------------------------------------------------------

FAMILY_MAP = {
    "Naive": {"Bitcoin": "Naive", "Electricity_A": "Naive", "Electricity_B": "Naive",
              "Note": "Directly comparable: lag-1 persistence in both domains."},
    "Chronos-Bolt-Tiny": {"Bitcoin": "Chronos-Bolt-Tiny", "Electricity_A": "Chronos_Bolt_Tiny",
                           "Electricity_B": "Chronos_Bolt_Tiny",
                           "Note": "Directly comparable: identical zero-shot model, matching protocol in both domains."},
    "TimesFM": {"Bitcoin": "TimesFM", "Electricity_A": "TimesFM", "Electricity_B": "TimesFM",
                "Note": "Directly comparable: identical zero-shot model, matching protocol in both domains."},
    "ARIMA-family (best)": {"Bitcoin": "ARIMA Rolling One-Step", "Electricity_A": "SARIMA", "Electricity_B": "SARIMA",
                             "Note": "NOT the same model. Bitcoin has only plain ARIMA; Electricity's best-performing "
                                     "ARIMA-family model is compared (of ARIMA/SARIMA/DHR-ARIMA per protocol). "
                                     "Bitcoin has no DHR-ARIMA (harmonic-regression) equivalent."},
    "Prophet": {"Bitcoin": "Prophet — 30-Day Periodic Refit", "Electricity_A": "Prophet", "Electricity_B": "Prophet",
                "Note": "Both periodic-refit. Bitcoin refits every 30 days; Electricity refits every 14 days "
                        "(validation-selected per domain) -- cadences are not the same and are not pooled."},
    "Simple Exponential Smoothing": {"Bitcoin": "Simple Exponential Smoothing — Rolling One-Step",
                                      "Electricity_A": "Simple_Exponential_Smoothing", "Electricity_B": "Simple_Exponential_Smoothing",
                                      "Note": "Both periodic-refit (methodology comparable), but Bitcoin's is true rolling "
                                              "one-step refit while Electricity's uses a 1-day validation-selected cadence -- "
                                              "not numerically pooled, only methodology is compared."},
    "Holt-Winters": {"Bitcoin": "Additive-Trend Exponential Smoothing", "Electricity_A": "Holt_Winters", "Electricity_B": "Holt_Winters",
                     "Note": "Genuine domain difference, not an inconsistency: Bitcoin's version has NO seasonal "
                             "component (seasonality tested and found absent in Bitcoin price returns), so it is "
                             "additive-trend-only (\"Holt's method\"). Electricity's version uses daily (period-48) "
                             "seasonality (seasonality tested and found strongly present, ACF ~0.8 at lag 48)."},
    "LSTM-family": {"Bitcoin": "Persistence-Enhanced Log-Return LSTM", "Electricity_A": "LSTM", "Electricity_B": "LSTM",
                    "Note": "NOT the same model. Compared as a model CLASS (recurrent neural network), not as identical "
                            "architectures: Bitcoin's is a persistence-enhanced log-return LSTM (different target "
                            "transform, different design) vs Electricity's direct-demand LSTM."},
}

NOT_COMPARABLE = pd.DataFrame([
    {"Item": "Electricity Daily/Weekly Seasonal Naive", "Reason": "No Bitcoin equivalent: Bitcoin's own seasonality "
     "testing (notebook 01) found no exploitable daily/weekly seasonality in price returns, so no seasonal-naive "
     "baseline was built for Bitcoin."},
    {"Item": "Electricity DHR-ARIMA", "Reason": "No Bitcoin equivalent: this harmonic-regression ARIMA variant exists "
     "only because Electricity has strong daily+weekly seasonality to model; it is folded into the ARIMA-family "
     "comparison as Electricity's non-representative alternative, not compared 1:1 with any Bitcoin model."},
    {"Item": "Bitcoin 7-Day Moving Average vs Electricity Moving_Average", "Reason": "Different wall-clock windows: "
     "Bitcoin's is a 7-observation (1-week) trailing average of daily prices; Electricity's is a 48-observation "
     "(1-day) trailing average of half-hourly demand. Both are \"moving average\" in name only -- not treated as a "
     "comparable family."},
    {"Item": "Bitcoin Persistence-Enhanced Log-Return Transformer", "Reason": "No Electricity equivalent: Electricity "
     "has no transformer-architecture comparator in its current model set."},
])


def main() -> None:
    # ---- Bitcoin ----
    bitcoin = pd.read_csv(RESULTS / "bitcoin_point_forecast_metrics_v2.csv")
    assert len(bitcoin) == 10, f"expected 10 Bitcoin models, found {len(bitcoin)}"
    bitcoin_comp = bitcoin[["Model", "MAE", "RMSE", "MAPE", "sMAPE"]].copy()
    bitcoin_comp.insert(0, "Protocol", BITCOIN_PROTOCOL)
    bitcoin_comp.insert(0, "Domain", "Bitcoin")
    bitcoin_comp["Within_Domain_Rank"] = bitcoin_comp["MAE"].rank(method="min").astype(int)
    bitcoin_comp["MASE_48"] = np.nan

    # ---- Electricity ----
    elec_frames = []
    for protocol_label, path in [(ELEC_A_PROTOCOL, "protocol_a_trust_scores.csv"), (ELEC_B_PROTOCOL, "protocol_b_trust_scores.csv")]:
        t = pd.read_csv(RESULTS / "electricity" / path)
        assert len(t) == 13, f"expected 13 Electricity models in {path}, found {len(t)}"
        frame = t[["Model", "MAE", "RMSE", "MAPE", "sMAPE", "MASE_48"]].copy()
        frame["Model"] = frame["Model"].map(elec_name)
        frame.insert(0, "Protocol", protocol_label)
        frame.insert(0, "Domain", "Electricity")
        frame["Within_Domain_Rank"] = frame["MASE_48"].rank(method="min").astype(int)
        elec_frames.append(frame)

    comparison = pd.concat([bitcoin_comp, *elec_frames], ignore_index=True)
    comparison = comparison[["Domain", "Protocol", "Model", "MAE", "RMSE", "MAPE", "sMAPE", "Within_Domain_Rank", "MASE_48"]]
    comparison.to_csv(RESULTS / "cross_domain_model_comparison.csv", index=False)
    print("cross_domain_model_comparison.csv:", comparison.shape)

    # ---- Task 3: rank stability across the 8 comparable families ----
    def lookup_rank(domain, protocol, model):
        row = comparison[(comparison.Domain == domain) & (comparison.Protocol == protocol) & (comparison.Model == model)]
        assert len(row) == 1, (domain, protocol, model, len(row))
        return int(row.Within_Domain_Rank.iloc[0])

    rank_rows = []
    for family, spec in FAMILY_MAP.items():
        br = lookup_rank("Bitcoin", BITCOIN_PROTOCOL, spec["Bitcoin"])
        ar = lookup_rank("Electricity", ELEC_A_PROTOCOL, elec_name(spec["Electricity_A"]))
        brr = lookup_rank("Electricity", ELEC_B_PROTOCOL, elec_name(spec["Electricity_B"]))
        ranks = [br, ar, brr]
        rank_rows.append({
            "Model_Family": family, "Bitcoin_Representative": spec["Bitcoin"],
            "Electricity_A_Representative": spec["Electricity_A"], "Electricity_B_Representative": spec["Electricity_B"],
            "Bitcoin_Rank": br, "Electricity_Protocol_A_Rank": ar, "Electricity_Protocol_B_Rank": brr,
            "Mean_Rank": float(np.mean(ranks)), "Rank_Std": float(np.std(ranks, ddof=1)),
            "Best_Rank": min(ranks), "Worst_Rank": max(ranks),
        })
    rank_stability = pd.DataFrame(rank_rows).sort_values("Mean_Rank").reset_index(drop=True)
    rank_stability.to_csv(RESULTS / "cross_domain_rank_stability.csv", index=False)
    print("cross_domain_rank_stability.csv:", rank_stability.shape)

    # ---- Task 4: uncertainty comparison (native + calibrated, kept separate) ----
    fus = pd.read_csv(RESULTS / "foundation_uncertainty_summary.csv")
    unc_rows = []
    for _, r in fus.iterrows():
        model = "Chronos-Bolt-Tiny" if r.Model == "Chronos_Bolt_Tiny" else r.Model
        unc_rows.append({"Domain": "Bitcoin", "Protocol": BITCOIN_PROTOCOL, "Model": model, "Calibration_Type": "Native",
                          "Nominal_Coverage": 0.8, "Empirical_Coverage": r.Native_Test_Coverage_80,
                          "Coverage_Error": abs(r.Native_Test_Coverage_80 - 0.8), "Average_Width": r.Native_Average_Width_80,
                          "Width_Units": "Bitcoin price units (USD)"})
        unc_rows.append({"Domain": "Bitcoin", "Protocol": BITCOIN_PROTOCOL, "Model": model, "Calibration_Type": "Calibrated",
                          "Nominal_Coverage": 0.8, "Empirical_Coverage": r.Calibrated_Test_Coverage_80,
                          "Coverage_Error": abs(r.Calibrated_Test_Coverage_80 - 0.8), "Average_Width": r.Calibrated_Average_Width_80,
                          "Width_Units": "Bitcoin price units (USD)"})
    elec_unc = pd.read_csv(RESULTS / "electricity" / "uncertainty_summary.csv")
    elec_unc = elec_unc[elec_unc.Available]
    protocol_label = {"A": ELEC_A_PROTOCOL, "B": ELEC_B_PROTOCOL}
    for _, r in elec_unc.iterrows():
        unc_rows.append({"Domain": "Electricity", "Protocol": protocol_label[r.Protocol], "Model": elec_name(r.Model),
                          "Calibration_Type": "Native", "Nominal_Coverage": r.Nominal_Coverage,
                          "Empirical_Coverage": r.Empirical_Coverage, "Coverage_Error": abs(r.Empirical_Coverage - r.Nominal_Coverage),
                          "Average_Width": r.Average_Width, "Width_Units": "Electricity demand units (MW)"})
    uncertainty = pd.DataFrame(unc_rows)
    uncertainty.to_csv(RESULTS / "cross_domain_uncertainty_comparison.csv", index=False)
    print("cross_domain_uncertainty_comparison.csv:", uncertainty.shape,
          "(Electricity has no post-hoc calibrated variant -- not fabricated, simply absent)")

    # ---- Task 6: foundation-model comparison against CURRENT strongest baseline ----
    def strongest_baseline(domain, protocol, exclude):
        sub = comparison[(comparison.Domain == domain) & (comparison.Protocol == protocol) & (~comparison.Model.isin(exclude))]
        metric = "MASE_48" if domain == "Electricity" else "MAE"
        return sub.sort_values(metric).iloc[0]

    # bitcoin_point_forecast_metrics_v2.csv and bitcoin_trust_scores_penalised.csv name
    # the same three models differently; this maps the former's names (used everywhere
    # else in this script) to the latter's for trust-score lookups only.
    BITCOIN_TRUST_ALIAS = {
        "Additive-Trend Exponential Smoothing": "Holt-Winters Rolling One-Step",
        "Prophet — 30-Day Periodic Refit": "Prophet 30-Day Periodic Refit",
        "Simple Exponential Smoothing — Rolling One-Step": "Simple Exponential Smoothing Rolling One-Step",
    }

    def trust_lookup(domain, protocol, model):
        if domain == "Bitcoin":
            t = pd.read_csv(RESULTS / "bitcoin_trust_scores_penalised.csv")
            model = BITCOIN_TRUST_ALIAS.get(model, model)
        else:
            path = "protocol_a_trust_scores.csv" if protocol == ELEC_A_PROTOCOL else "protocol_b_trust_scores.csv"
            t = pd.read_csv(RESULTS / "electricity" / path)
            t["Model"] = t["Model"].map(elec_name)
        row = t[t.Model == model].iloc[0]
        return row

    exclude_zero_shot = ["TimesFM", "Chronos-Bolt-Tiny", "Chronos_Bolt_Tiny"]
    fm_rows = []
    for domain, protocol in [("Bitcoin", BITCOIN_PROTOCOL), ("Electricity", ELEC_A_PROTOCOL), ("Electricity", ELEC_B_PROTOCOL)]:
        base = strongest_baseline(domain, protocol, exclude_zero_shot)
        for model in ["TimesFM", "Chronos-Bolt-Tiny"]:
            row = comparison[(comparison.Domain == domain) & (comparison.Protocol == protocol) & (comparison.Model == model)].iloc[0]
            trust = trust_lookup(domain, protocol, model)
            unc = uncertainty[(uncertainty.Domain == domain) & (uncertainty.Protocol == protocol) & (uncertainty.Model == model) & (uncertainty.Calibration_Type == "Native")]
            fm_rows.append({
                "Domain": domain, "Protocol": protocol, "Model": model, "Point_Rank": int(row.Within_Domain_Rank),
                "sMAPE": row.sMAPE, "Strongest_Baseline": base.Model, "Strongest_Baseline_Family":
                    next((fam for fam, spec in FAMILY_MAP.items() if spec.get("Electricity_A" if domain == "Electricity" else "Bitcoin") == base.Model or spec.get("Bitcoin") == base.Model), "n/a"),
                "Relative_MAE_Difference_Percent": float(100 * (row.MAE - base.MAE) / base.MAE),
                "Beat_Baseline": bool(row.MAE < base.MAE),
                "Relative_Robustness_Score": float(trust["Relative Robustness Score"]),
                "Relative_Generalisation_Score": float(trust["Relative Generalisation Score"]),
                "Empirical_80_Coverage": float(unc.Empirical_Coverage.iloc[0]) if len(unc) else np.nan,
                "Coverage_Error": float(unc.Coverage_Error.iloc[0]) if len(unc) else np.nan,
                "Penalised_Trust_Score": float(trust["Overall Trust Score - Missing Evidence Penalised"]),
                "Zero_Shot": True, "Inference_Cost": "Recorded in domain notebook; units/protocol differ",
            })
    foundation = pd.DataFrame(fm_rows)
    foundation.to_csv(RESULTS / "cross_domain_foundation_model_comparison.csv", index=False)
    print("cross_domain_foundation_model_comparison.csv:", foundation.shape)
    print(foundation[["Domain", "Protocol", "Model", "Strongest_Baseline", "Relative_MAE_Difference_Percent", "Beat_Baseline"]].to_string())

    # ---- Task 5: significance summary, Holm for Bitcoin, BH for Electricity, never pooled ----
    holm = pd.read_csv(RESULTS / "bitcoin_dm_pairwise_results_hac_holm.csv")

    def holm_row(a, b, note):
        r = holm[((holm["Model A"] == a) & (holm["Model B"] == b)) | ((holm["Model A"] == b) & (holm["Model B"] == a))].iloc[0]
        return {"Domain": "Bitcoin", "Protocol": BITCOIN_PROTOCOL, "Comparison": f"{a} vs {b}",
                "Lower_Loss_Model": r["Lower-RMSE model"], "p_value": float(r["Holm-adjusted p-value"]),
                "Correction_Method": "Holm (family-wise error control)", "Significant": bool(r["Significant Holm?"]),
                "Practical_Interpretation": note}

    dm_a = pd.read_csv(RESULTS / "electricity" / "protocol_a_dm_tests.csv")
    dm_b = pd.read_csv(RESULTS / "electricity" / "protocol_b_dm_tests.csv")

    def bh_row(dm, protocol, m1, m2, note):
        r = dm[((dm.Model_1 == m1) & (dm.Model_2 == m2)) | ((dm.Model_1 == m2) & (dm.Model_2 == m1))].iloc[0]
        return {"Domain": "Electricity", "Protocol": protocol, "Comparison": f"{elec_name(m1)} vs {elec_name(m2)}",
                "Lower_Loss_Model": elec_name(r.Lower_Error_Winner), "p_value": float(r.p_value_BH),
                "Correction_Method": "Benjamini-Hochberg (false discovery rate control)", "Significant": bool(r["Significant_BH_0.05"]),
                "Practical_Interpretation": note}

    significance = pd.DataFrame([
        holm_row("Naive", "TimesFM", "TimesFM does not beat persistence; Naive has lower squared loss."),
        holm_row("Naive", "Chronos-Bolt-Tiny", "Naive has lower squared loss."),
        holm_row("TimesFM", "Chronos-Bolt-Tiny", "TimesFM improves on Chronos but not on Naive."),
        holm_row("Persistence-Enhanced Log-Return LSTM", "TimesFM", "No statistically significant difference was detected."),
        holm_row("ARIMA Rolling One-Step", "TimesFM", "ARIMA-family comparison: TimesFM vs Bitcoin's only ARIMA-family model."),
        bh_row(dm_a, ELEC_A_PROTOCOL, "TimesFM", "SARIMA", "ARIMA-family comparison: TimesFM vs Electricity's strongest ARIMA-family model."),
        bh_row(dm_a, ELEC_A_PROTOCOL, "TimesFM", "Chronos_Bolt_Tiny", "TimesFM significantly beats Chronos."),
        bh_row(dm_a, ELEC_A_PROTOCOL, "Chronos_Bolt_Tiny", "Naive", "Chronos significantly beats Naive on squared loss."),
        bh_row(dm_b, ELEC_B_PROTOCOL, "TimesFM", "SARIMA", "ARIMA-family comparison: TimesFM vs Electricity's strongest ARIMA-family model (Protocol B)."),
        bh_row(dm_b, ELEC_B_PROTOCOL, "TimesFM", "Chronos_Bolt_Tiny", "TimesFM significantly beats Chronos."),
        bh_row(dm_b, ELEC_B_PROTOCOL, "TimesFM", "Daily_Seasonal_Naive", "TimesFM significantly beats the strongest day-ahead seasonal-naive baseline."),
        bh_row(dm_b, ELEC_B_PROTOCOL, "Chronos_Bolt_Tiny", "Daily_Seasonal_Naive", "Chronos has significantly lower daily squared loss."),
    ])
    significance.to_csv(RESULTS / "cross_domain_significance_summary.csv", index=False)
    print("cross_domain_significance_summary.csv:", significance.shape)

    # ---- Trust-component comparison for the 8 comparable families (replaces old hardcoded 4-model dict) ----
    trust_rows = []
    for family, spec in FAMILY_MAP.items():
        for domain, protocol, model in [
            ("Bitcoin", BITCOIN_PROTOCOL, spec["Bitcoin"]),
            ("Electricity", ELEC_A_PROTOCOL, elec_name(spec["Electricity_A"])),
            ("Electricity", ELEC_B_PROTOCOL, elec_name(spec["Electricity_B"])),
        ]:
            t = trust_lookup(domain, protocol, model)
            basis = "Bitcoin frozen RMSE-relative framework" if domain == "Bitcoin" else "Electricity frozen MASE-48-relative framework"
            if domain == "Bitcoin":
                ea = pd.read_csv(RESULTS / "bitcoin_trust_scores_evidence_available.csv")
                ea_model = BITCOIN_TRUST_ALIAS.get(model, model)
                ea_score = float(ea[ea.Model == ea_model]["Evidence-Available Trust Score"].iloc[0])
            else:
                ea_score = float(t["Evidence-Available Trust Score"])
            trust_rows.append({
                "Model_Family": family, "Domain": domain, "Protocol": protocol, "Model": model,
                "Relative_Accuracy_Score": float(t["Relative Accuracy Score"]),
                "Relative_Robustness_Score": float(t["Relative Robustness Score"]),
                "Relative_Generalisation_Score": float(t["Relative Generalisation Score"]),
                "Uncertainty_Score": None if pd.isna(t.get("Uncertainty Score", np.nan)) else float(t["Uncertainty Score"]),
                "Explainability_Score": float(t["Explainability Score"]),
                "Penalised_Trust_Score": float(t["Overall Trust Score - Missing Evidence Penalised"]),
                "Evidence_Available_Trust_Score": ea_score,
                "Component_Basis": basis,
            })
    trust_comparison = pd.DataFrame(trust_rows)
    trust_comparison.to_csv(RESULTS / "cross_domain_trust_comparison.csv", index=False)
    print("cross_domain_trust_comparison.csv:", trust_comparison.shape)

    # ---- comparability map + non-comparable items, saved for the notebook to load ----
    fam_rows = [{"Model_Family": k, "Bitcoin_Representative": v["Bitcoin"], "Electricity_A_Representative": elec_name(v["Electricity_A"]),
                 "Electricity_B_Representative": elec_name(v["Electricity_B"]), "Note": v["Note"]} for k, v in FAMILY_MAP.items()]
    pd.DataFrame(fam_rows).to_csv(RESULTS / "cross_domain_comparable_families.csv", index=False)
    NOT_COMPARABLE.to_csv(RESULTS / "cross_domain_not_comparable.csv", index=False)
    print("cross_domain_comparable_families.csv:", len(fam_rows), "rows")
    print("cross_domain_not_comparable.csv:", len(NOT_COMPARABLE), "rows")


if __name__ == "__main__":
    main()
