"""Regenerate figures/cross_domain/*.png from the rebuilt cross-domain CSVs only.

Deliberately standalone from src/generate_paper_figures.py's main(), which also
regenerates Bitcoin and Electricity per-domain figures -- this script touches nothing
outside figures/cross_domain/. Reads only results/cross_domain_*.csv.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures" / "cross_domain"

TASK_MAP = {
    "Rolling one-step daily": "Bitcoin",
    "Protocol A: rolling one-step 30-minute": "Electricity A",
    "Protocol B: 48-step day-ahead": "Electricity B",
}
TASKS = ["Bitcoin", "Electricity A", "Electricity B"]
FAMILY_COLORS = {
    "Naive": "#0072B2", "Chronos-Bolt-Tiny": "#CC79A7", "TimesFM": "#D55E00",
    "ARIMA-family (best)": "#56B4E9", "Prophet": "#E69F00", "Simple Exponential Smoothing": "#009E73",
    "Holt-Winters": "#9467BD", "LSTM-family": "#F0E442",
}


def save(fig, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=240, bbox_inches="tight")
    plt.close(fig)


def model_rank_figure():
    rank = pd.read_csv(RESULTS / "cross_domain_rank_stability.csv")
    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    x = np.arange(3)
    for _, row in rank.iterrows():
        y = [row.Bitcoin_Rank, row.Electricity_Protocol_A_Rank, row.Electricity_Protocol_B_Rank]
        ax.plot(x, y, marker="o", lw=2, label=row.Model_Family, color=FAMILY_COLORS.get(row.Model_Family))
    ax.set_xticks(x, TASKS)
    ax.set_yticks(range(1, 14))
    ax.invert_yaxis()
    ax.set(ylabel="Within-domain rank (1 = best; Bitcoin out of 10, Electricity out of 13)",
           title="Model-family rank across domains and protocols")
    ax.legend(frameon=False, ncol=2, fontsize=8, loc="lower center", bbox_to_anchor=(0.5, -0.32))
    ax.grid(alpha=.2)
    save(fig, FIGURES / "model_rank_across_domains.png")


def foundation_baseline_figure():
    fm = pd.read_csv(RESULTS / "cross_domain_foundation_model_comparison.csv")
    fm["Task"] = fm["Protocol"].map(TASK_MAP)
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(TASKS))
    width = 0.36
    for i, model in enumerate(["TimesFM", "Chronos-Bolt-Tiny"]):
        q = fm[fm.Model.eq(model)].set_index("Task").reindex(TASKS)
        bars = ax.bar(x + (i - .5) * width, q.Relative_MAE_Difference_Percent, width,
                       label=model, color=FAMILY_COLORS.get(model))
        for xi, (_, r) in zip(x + (i - .5) * width, q.iterrows()):
            ax.annotate(r.Strongest_Baseline, (xi, r.Relative_MAE_Difference_Percent),
                        textcoords="offset points", xytext=(0, 6 if r.Relative_MAE_Difference_Percent >= 0 else -14),
                        ha="center", fontsize=7, rotation=0)
    ax.axhline(0, color="#222", lw=1)
    ax.set_xticks(x, TASKS)
    ax.set(ylabel="MAE difference vs. current strongest same-task baseline (%)",
           title="Foundation models relative to each task's current strongest baseline\n(baseline model annotated above/below each bar)")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=.2)
    save(fig, FIGURES / "foundation_model_relative_baseline.png")


def uncertainty_figure():
    unc = pd.read_csv(RESULTS / "cross_domain_uncertainty_comparison.csv")
    native = unc[unc.Calibration_Type == "Native"].copy()
    native["Task"] = native["Protocol"].map(TASK_MAP)
    fig, ax = plt.subplots(figsize=(8.8, 4.9))
    x = np.arange(len(TASKS))
    width = 0.34
    for i, model in enumerate(["Chronos-Bolt-Tiny", "TimesFM"]):
        q = native[native.Model.eq(model)].set_index("Task").reindex(TASKS)
        ax.bar(x + (i - .5) * width, 100 * q.Empirical_Coverage, width, label=model, color=FAMILY_COLORS.get(model))
    ax.axhline(80, color="#222222", ls="--", lw=1.5, label="Nominal 80%")
    ax.set_xticks(x, TASKS)
    ax.set(ylim=(0, 100), ylabel="Empirical marginal coverage (%)",
           title="Native 80% interval coverage across completed tasks")
    ax.legend(frameon=False, ncol=3, loc="upper center")
    ax.grid(axis="y", alpha=.2)
    save(fig, FIGURES / "uncertainty_calibration_across_domains.png")


def trustworthiness_matrix_figure():
    trust = pd.read_csv(RESULTS / "cross_domain_trust_comparison.csv")
    trust = trust[trust.Model_Family.isin(["Chronos-Bolt-Tiny", "TimesFM"])].copy()
    trust["Task"] = trust["Protocol"].map(TASK_MAP)
    rows = pd.MultiIndex.from_product([TASKS, ["TimesFM", "Chronos-Bolt-Tiny"]], names=["Task", "Model_Family"])
    q = trust.set_index(["Task", "Model_Family"]).reindex(rows).reset_index()
    columns = ["Relative\naccuracy", "Robustness\nscore", "Generalisation\nscore", "Uncertainty\nscore", "Explainability\nscore", "Penalised\ntrust score"]
    values, colours = [], []
    for _, r in q.iterrows():
        unc = r.Uncertainty_Score
        values.append([f"{r.Relative_Accuracy_Score:.1f}", f"{r.Relative_Robustness_Score:.1f}",
                        f"{r.Relative_Generalisation_Score:.1f}", "n/a" if pd.isna(unc) else f"{unc:.1f}",
                        f"{r.Explainability_Score:.1f}", f"{r.Penalised_Trust_Score:.1f}"])
        colours.append([1 - r.Relative_Accuracy_Score / 100, 1 - r.Relative_Robustness_Score / 100,
                         1 - r.Relative_Generalisation_Score / 100, .5 if pd.isna(unc) else 1 - unc / 100,
                         1 - r.Explainability_Score / 100, 1 - r.Penalised_Trust_Score / 100])
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("evidence", ["#D9F0D3", "#FFF2CC", "#F4CCCC"])
    fig, ax = plt.subplots(figsize=(10.5, 5.4))
    ax.imshow(np.asarray(colours, dtype=float), cmap=cmap, vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(np.arange(len(columns)), columns)
    ax.set_yticks(np.arange(len(q)), [f"{t} — {m}" for t, m in zip(q.Task, q.Model_Family)])
    for i, row in enumerate(values):
        for j, value in enumerate(row):
            ax.text(j, i, value, ha="center", va="center", fontsize=9)
    ax.set_title("Trustworthiness evidence matrix, Chronos vs TimesFM (components are not aggregated)")
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.text(.5, .01, "Scores are within-task and within-domain, never pooled across domains. \"n/a\" = no saved uncertainty evidence for that task.", ha="center", fontsize=8.5)
    save(fig, FIGURES / "trustworthiness_evidence_matrix.png")


def main():
    plt.rcParams.update({"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 11, "figure.facecolor": "white"})
    model_rank_figure()
    foundation_baseline_figure()
    uncertainty_figure()
    trustworthiness_matrix_figure()
    print("Regenerated 4 figures in", FIGURES)


if __name__ == "__main__":
    main()
