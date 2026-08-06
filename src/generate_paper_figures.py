"""Generate manuscript figures exclusively from frozen CSV artifacts.

Inputs:
  results/validated_forecasts.csv
  results/cross_domain_model_comparison.csv
  results/cross_domain_foundation_model_comparison.csv
  results/cross_domain_uncertainty_comparison.csv
  results/electricity/protocol_a_validated_forecasts.csv
  results/electricity/protocol_b_validated_forecasts.csv
  results/electricity/protocol_b_validated_horizon_metrics.csv

This module does not import, load, train, or call any forecasting model.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
COLORS = {"Actual": "#222222", "Naive": "#0072B2", "Persistence-Enhanced LSTM": "#009E73",
          "LSTM": "#009E73", "TimesFM": "#D55E00", "Chronos-Bolt-Tiny": "#CC79A7",
          "DHR-ARIMA": "#56B4E9", "Daily Seasonal Naive": "#E69F00"}
NAME = {"Persistence_Enhanced_LSTM": "Persistence-Enhanced LSTM", "Chronos_Bolt_Tiny": "Chronos-Bolt-Tiny",
        "DHR_ARIMA": "DHR-ARIMA", "Daily_Seasonal_Naive": "Daily Seasonal Naive"}

def save(fig, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=240, bbox_inches="tight")
    plt.close(fig)

def line_plot(df, cols, title, ylabel, path):
    fig, ax = plt.subplots(figsize=(11, 5.2))
    x = pd.to_datetime(df["Timestamp"])
    for col in cols:
        label = NAME.get(col, col)
        ax.plot(x, df[col], label=label, lw=2.1 if col == "Actual" else 1.35,
                color=COLORS.get(label), alpha=0.95)
    ax.set(title=title, xlabel="Date", ylabel=ylabel)
    ax.legend(ncol=3, frameon=False)
    ax.grid(axis="y", alpha=.2)
    save(fig, path)

def cross_domain_revision_figures():
    """Regenerate only the revised cross-domain evidence figures from frozen CSVs."""
    plt.rcParams.update({"font.size": 10, "axes.titlesize": 13, "axes.labelsize": 11, "figure.facecolor": "white"})
    unc = pd.read_csv(RESULTS / "cross_domain_uncertainty_comparison.csv")
    fm = pd.read_csv(RESULTS / "cross_domain_foundation_model_comparison.csv")
    task_map = {
        "Rolling one-step daily": "Bitcoin",
        "Protocol A: rolling one-step 30-minute": "Electricity A",
        "Protocol B: 48-step day-ahead": "Electricity B",
    }
    unc["Task"] = unc["Protocol"].map(task_map)
    tasks = ["Bitcoin", "Electricity A", "Electricity B"]
    models = ["Chronos-Bolt-Tiny", "TimesFM"]

    fig, ax = plt.subplots(figsize=(8.8, 4.9))
    x = np.arange(len(tasks)); width = 0.34
    for i, model in enumerate(models):
        q = unc[unc.Model.eq(model)].set_index("Task").reindex(tasks)
        ax.bar(x + (i - .5) * width, 100 * q.Empirical_Coverage, width,
               label=model, color=COLORS[model])
    ax.axhline(80, color="#222222", ls="--", lw=1.5, label="Nominal 80%")
    ax.set_xticks(x, tasks)
    ax.set(ylim=(0, 100), ylabel="Empirical marginal coverage (%)",
           title="Native 80% interval coverage across completed tasks")
    ax.legend(frameon=False, ncol=3, loc="upper center")
    ax.grid(axis="y", alpha=.2)
    save(fig, FIGURES / "cross_domain" / "uncertainty_calibration_across_domains.png")

    fm["Task"] = fm["Protocol"].map(task_map)
    rows = pd.MultiIndex.from_product([tasks, ["TimesFM", "Chronos-Bolt-Tiny"]], names=["Task", "Model"])
    q = fm.set_index(["Task", "Model"]).reindex(rows).reset_index()
    columns = ["Point rank", "Beats strongest\nbaseline", "80% coverage\nerror", "Robustness\nscore", "Temporal stability\nscore", "Evidence"]
    values = []
    colours = []
    for _, r in q.iterrows():
        coverage_error = 100 * r.Coverage_Error
        values.append([
            f"{int(r.Point_Rank)}",
            "Yes" if bool(r.Beat_Baseline) else "No",
            f"{coverage_error:.1f} pp",
            f"{r.Relative_Robustness_Score:.1f}",
            f"{r.Relative_Generalisation_Score:.1f}",
            "5/5",
        ])
        colours.append([
            max(0, min(1, (r.Point_Rank - 1) / 7)),
            0 if bool(r.Beat_Baseline) else 1,
            max(0, min(1, coverage_error / 60)),
            1 - r.Relative_Robustness_Score / 100,
            1 - r.Relative_Generalisation_Score / 100,
            0,
        ])
    cmap = LinearSegmentedColormap.from_list("evidence", ["#D9F0D3", "#FFF2CC", "#F4CCCC"])
    fig, ax = plt.subplots(figsize=(11.8, 5.4))
    ax.imshow(np.asarray(colours), cmap=cmap, vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(np.arange(len(columns)), columns)
    ax.set_yticks(np.arange(len(q)), [f"{t} — {m}" for t, m in zip(q.Task, q.Model)])
    for i, row in enumerate(values):
        for j, value in enumerate(row): ax.text(j, i, value, ha="center", va="center", fontsize=9)
    ax.set_title("Trustworthiness evidence matrix (components are not aggregated)")
    ax.tick_params(length=0)
    for spine in ax.spines.values(): spine.set_visible(False)
    fig.text(.5, .01, "Ranks and relative scores are within-task; coverage error is absolute distance from nominal 80%. Green indicates stronger task-specific evidence.", ha="center", fontsize=8.5)
    save(fig, FIGURES / "cross_domain" / "trustworthiness_evidence_matrix.png")

def main():
    plt.rcParams.update({"font.size": 10, "axes.titlesize": 13, "axes.labelsize": 11, "figure.facecolor": "white"})
    btc = pd.read_csv(RESULTS / "validated_forecasts.csv")
    mid = max(0, len(btc)//2 - 60)
    line_plot(btc.iloc[mid:mid+120], ["Actual", "Naive", "Persistence_Enhanced_LSTM", "TimesFM", "Chronos_Bolt_Tiny"],
              "Bitcoin forecasts: representative 120-day window", "Daily close (USD)", FIGURES/"bitcoin"/"bitcoin_forecast_comparison.png")

    comp = pd.read_csv(RESULTS / "cross_domain_model_comparison.csv")
    b = comp[comp.Domain.eq("Bitcoin")].sort_values("Within_Domain_Rank")
    fig, ax = plt.subplots(figsize=(8.8, 4.8)); labels=[NAME.get(x,x) for x in b.Model]
    ax.bar(labels, b.sMAPE, color=[COLORS.get(x,"#999999") for x in labels]); ax.set(ylabel="sMAPE (%)", title="Bitcoin point accuracy (lower is better)")
    ax.tick_params(axis="x", rotation=18); ax.grid(axis="y", alpha=.2); save(fig, FIGURES/"bitcoin"/"bitcoin_model_accuracy.png")

    unc = pd.read_csv(RESULTS / "cross_domain_uncertainty_comparison.csv")
    def coverage_plot(d, title, path):
        fig, ax=plt.subplots(figsize=(8.8,4.8)); labels=[f"{NAME.get(m,m)}\n{p.replace('Protocol ','Elec ')}" for m,p in zip(d.Model,d.Protocol)]
        ax.bar(labels,100*d.Empirical_Coverage,color=[COLORS.get(NAME.get(m,m),"#999") for m in d.Model]); ax.axhline(80,color="#222",ls="--",lw=1.5,label="Nominal 80%")
        ax.set(ylim=(0,100),ylabel="Empirical coverage (%)",title=title); ax.legend(frameon=False); ax.grid(axis="y",alpha=.2); save(fig,path)
    coverage_plot(unc[unc.Domain.eq("Bitcoin")], "Bitcoin native interval calibration", FIGURES/"bitcoin"/"bitcoin_uncertainty_calibration.png")

    a=pd.read_csv(RESULTS/"electricity"/"protocol_a_validated_forecasts.csv")
    a["Timestamp"]=pd.to_datetime(a.Timestamp)
    profile=a.assign(slot=a.Timestamp.dt.hour*2+a.Timestamp.dt.minute//30).groupby("slot").Actual.mean()
    fig,ax=plt.subplots(figsize=(9,4.8)); ax.plot(np.arange(48)/2,profile.values,color="#0072B2",lw=2.2); ax.set(xlabel="Hour of day",ylabel="Mean demand",title="South Australian average half-hour demand profile"); ax.grid(alpha=.2); save(fig,FIGURES/"electricity"/"electricity_weekly_pattern.png")
    line_plot(a.iloc[:336], ["Actual","TimesFM","DHR_ARIMA","Chronos_Bolt_Tiny","Naive","LSTM"], "Electricity Protocol A: first seven test days", "Demand", FIGURES/"electricity"/"protocol_a_forecast_comparison.png")

    pb=pd.read_csv(RESULTS/"electricity"/"protocol_b_validated_forecasts.csv"); pb["Origin"]=pd.to_datetime(pb.Origin); pb["Timestamp"]=pd.to_datetime(pb.Timestamp)
    daily=pb.groupby("Origin").Actual.mean(); target=(daily-daily.median()).abs().idxmin(); day=pb[pb.Origin.eq(target)]
    line_plot(day,["Actual","TimesFM","Chronos_Bolt_Tiny","Daily_Seasonal_Naive","LSTM"],f"Electricity Protocol B: median-demand day ({target.date()})","Demand",FIGURES/"electricity"/"protocol_b_day_ahead_example.png")

    hm=pd.read_csv(RESULTS/"electricity"/"protocol_b_validated_horizon_metrics.csv")
    fig,ax=plt.subplots(figsize=(10,5.2))
    for m in ["TimesFM","Chronos_Bolt_Tiny","Daily_Seasonal_Naive","LSTM","DHR_ARIMA"]:
        q=hm[hm.Model.eq(m)]; label=NAME.get(m,m); ax.plot(q.Horizon,q.MASE_48,label=label,color=COLORS.get(label),lw=1.8)
    ax.set(xlabel="Forecast horizon (half-hours)",ylabel="MASE-48",title="Electricity day-ahead error by horizon"); ax.legend(ncol=3,frameon=False); ax.grid(alpha=.2); save(fig,FIGURES/"electricity"/"protocol_b_horizon_mase.png")

    e=comp[comp.Domain.eq("Electricity")]
    fig,axs=plt.subplots(1,2,figsize=(12,4.8),sharey=True)
    for ax,(protocol,q) in zip(axs,e.groupby("Protocol",sort=False)):
        q=q.sort_values("Within_Domain_Rank"); labels=[NAME.get(x,x) for x in q.Model]; ax.barh(labels,q.MASE_48,color="#56B4E9"); ax.invert_yaxis(); ax.set(title=protocol.replace("Protocol ",""),xlabel="MASE-48")
    axs[0].set_ylabel("Model"); fig.suptitle("Electricity accuracy rankings by protocol"); save(fig,FIGURES/"electricity"/"electricity_model_accuracy.png")
    coverage_plot(unc[unc.Domain.eq("Electricity")],"Electricity native interval calibration",FIGURES/"electricity"/"electricity_uncertainty_calibration.png")

    common=comp[comp.Model.isin(["Naive","LSTM","Chronos-Bolt-Tiny","TimesFM"])].copy(); common["Task"]=common.Domain.where(common.Domain.eq("Bitcoin"),common.Protocol.str.extract(r"(Protocol [AB])")[0].str.replace("Protocol ","Electricity "))
    piv=common.pivot(index="Model",columns="Task",values="Within_Domain_Rank").reindex(["Naive","LSTM","Chronos-Bolt-Tiny","TimesFM"])
    fig,ax=plt.subplots(figsize=(9,5)); x=np.arange(len(piv.columns));
    for m,row in piv.iterrows(): ax.plot(x,row,marker="o",lw=2,label=m,color=COLORS.get(m))
    ax.set_xticks(x,piv.columns); ax.set_yticks(range(1,9)); ax.invert_yaxis(); ax.set(ylabel="Within-domain rank (1 = best)",title="Model rank across completed domain–protocol tasks"); ax.legend(frameon=False,ncol=2); ax.grid(alpha=.2); save(fig,FIGURES/"cross_domain"/"model_rank_across_domains.png")

    fm=pd.read_csv(RESULTS/"cross_domain_foundation_model_comparison.csv"); fm["Task"]=fm.Domain.where(fm.Domain.eq("Bitcoin"),fm.Protocol.str.extract(r"(Protocol [AB])")[0].str.replace("Protocol ","Electricity "))
    fig,ax=plt.subplots(figsize=(9,5)); tasks=list(fm.Task.drop_duplicates()); x=np.arange(len(tasks)); width=.36
    for i,m in enumerate(["TimesFM","Chronos-Bolt-Tiny"]):
        q=fm[fm.Model.eq(m)].set_index("Task").reindex(tasks); ax.bar(x+(i-.5)*width,q.Relative_MAE_Difference_Percent,width,label=m,color=COLORS[m])
    ax.axhline(0,color="#222",lw=1); ax.set_xticks(x,tasks); ax.set(ylabel="MAE difference versus strongest baseline (%)",title="Foundation models relative to protocol-specific baselines"); ax.legend(frameon=False); ax.grid(axis="y",alpha=.2); save(fig,FIGURES/"cross_domain"/"foundation_model_relative_baseline.png")
    coverage_plot(unc,"Native 80% interval coverage across completed tasks",FIGURES/"cross_domain"/"uncertainty_calibration_across_domains.png")

if __name__ == "__main__":
    import sys
    if "--cross-domain-revision-only" in sys.argv:
        cross_domain_revision_figures()
    else:
        main()
