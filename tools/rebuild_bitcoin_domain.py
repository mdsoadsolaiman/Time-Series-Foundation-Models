"""Artifact-only final rebuild of the Bitcoin notebook domain.

This script never trains a model and never writes the protected point-forecast
CSVs.  It produces derived evidence, final figures, and lightweight notebooks.
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nbformat as nbf
import numpy as np
import pandas as pd
from nbclient import NotebookClient

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT))

from src.bitcoin_pipeline import (
    CONTEXT_POLICY, FINAL_MODEL_ORDER, MODEL_COLUMNS, canonical_split,
    find_project_root, forecast_series, hac_dm, holm_adjust, load_bitcoin_target,
    load_validated_forecasts, metric_table, robustness_table, temporal_stability_table,
    test_regime_masks, training_regime_thresholds,
)

ROOT = find_project_root(Path(__file__))
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
NOTEBOOKS = ROOT / "notebooks"
PYTHON = "python"


def build_derived_evidence() -> dict[str, pd.DataFrame]:
    _, target = load_bitcoin_target(ROOT)
    train, test = canonical_split(target)
    validated = load_validated_forecasts(ROOT)
    forecasts = forecast_series(validated, target)
    metrics = metric_table(validated["Actual"], forecasts, train).reset_index()

    thresholds = training_regime_thresholds(train)
    threshold_frame = pd.DataFrame([
        {"Threshold": key, "Value": value, "Source": "Training data only",
         "Training_Start": train.index.min(), "Training_End": train.index.max()}
        for key, value in thresholds.items()
    ])
    masks = test_regime_masks(target, test.index, thresholds)
    robustness = robustness_table(validated["Actual"], forecasts, train, masks)
    stability = temporal_stability_table(validated["Actual"], forecasts, train)

    validation_actual = train.tail(len(test)).rename("Actual")
    validation = {
        "Naive": target.shift(1).reindex(validation_actual.index),
        "7-Day Moving Average": target.shift(1).rolling(7).mean().reindex(validation_actual.index),
        "ARIMA Rolling One-Step": pd.read_csv(RESULTS / "arima_validation_forecast.csv", parse_dates=["Timestamp"]).set_index("Timestamp")["ARIMA_Rolling_Validation"],
        "Simple Exponential Smoothing — Rolling One-Step": pd.read_csv(RESULTS / "simple_exp_smoothing_validation_forecast.csv", parse_dates=["Timestamp"]).set_index("Timestamp")["Simple_Exp_Smoothing_Validation"],
        "Additive-Trend Exponential Smoothing": pd.read_csv(RESULTS / "holt_winters_validation_forecast.csv", parse_dates=["Timestamp"]).set_index("Timestamp")["Holt_Winters_Validation"],
        "Persistence-Enhanced Log-Return Transformer": pd.read_csv(RESULTS / "persistence_enhanced_transformer_validation_forecast.csv", parse_dates=["Timestamp"]).set_index("Timestamp")["Persistence_Enhanced_Transformer"],
    }
    uncertainty_rows = []
    for model, vector in validation.items():
        vector.index = pd.to_datetime(vector.index, utc=True)
        residual = (validation_actual - vector.reindex(validation_actual.index)).abs().dropna()
        for nominal in (0.80, 0.95):
            radius = float(residual.quantile(nominal))
            coverage = float(((validated["Actual"] - forecasts[model]).abs() <= radius).mean())
            uncertainty_rows.append({"Model": model, "Uncertainty Evidence Type": "Validation-Residual Empirical Interval",
                                     "Native": False, "Calibrated": True, "Calibration Source": "Final 1,061 training dates",
                                     "Nominal Level": nominal, "Coverage": coverage, "Average Width": 2 * radius,
                                     "Coverage Error": abs(coverage - nominal), "Evidence Status": "Available"})
    calibration = pd.read_csv(RESULTS / "foundation_uncertainty_summary.csv")
    for row in calibration.to_dict("records"):
        model = "Chronos-Bolt-Tiny" if row["Model"] == "Chronos_Bolt_Tiny" else row["Model"]
        uncertainty_rows.extend([
            {"Model": model, "Uncertainty Evidence Type": "Native Foundation Quantiles", "Native": True,
             "Calibrated": False, "Calibration Source": "None", "Nominal Level": 0.80,
             "Coverage": row["Native_Test_Coverage_80"], "Average Width": row["Native_Average_Width_80"],
             "Coverage Error": abs(row["Native_Test_Coverage_80"] - 0.80), "Evidence Status": "Available"},
            {"Model": model, "Uncertainty Evidence Type": "Training-Only CQR-Adjusted Foundation Quantiles", "Native": False,
             "Calibrated": True, "Calibration Source": f"180 training rows ending {row['Calibration_End']}", "Nominal Level": 0.80,
             "Coverage": row["Calibrated_Test_Coverage_80"], "Average Width": row["Calibrated_Average_Width_80"],
             "Coverage Error": abs(row["Calibrated_Test_Coverage_80"] - 0.80), "Evidence Status": "Available"},
        ])
    for model in ["Persistence-Enhanced Log-Return LSTM", "Prophet — 30-Day Periodic Refit"]:
        uncertainty_rows.append({"Model": model, "Uncertainty Evidence Type": "Unavailable", "Native": False,
                                 "Calibrated": False, "Calibration Source": "None", "Nominal Level": 0.80,
                                 "Coverage": np.nan, "Average Width": np.nan, "Coverage Error": np.nan,
                                 "Evidence Status": "Unavailable"})
    uncertainty = pd.DataFrame(uncertainty_rows)

    dm_rows = []
    for model_a, model_b in itertools.combinations(FINAL_MODEL_ORDER, 2):
        result = hac_dm(validated["Actual"], forecasts[model_a], forecasts[model_b])
        rmse_a = float(metrics.set_index("Model").loc[model_a, "RMSE"])
        rmse_b = float(metrics.set_index("Model").loc[model_b, "RMSE"])
        difference = abs(rmse_a - rmse_b)
        dm_rows.append({"Model A": model_a, "Model B": model_b, **result,
                        "Lower-RMSE model": model_a if rmse_a < rmse_b else model_b,
                        "Absolute RMSE difference": difference,
                        "Relative RMSE difference": difference / min(rmse_a, rmse_b),
                        "Practical interpretation": "Small" if difference / validated["Actual"].mean() < 0.01 else "Moderate/Large"})
    dm = pd.DataFrame(dm_rows)
    dm["Holm-adjusted p-value"] = holm_adjust(dm["Raw p-value"])
    dm["Significant raw?"] = dm["Raw p-value"] < 0.05
    dm["Significant Holm?"] = dm["Holm-adjusted p-value"] < 0.05

    rubric = pd.DataFrame([
        ["Naive", 100, 100, 100, 100, 100, 100],
        ["Simple Exponential Smoothing — Rolling One-Step", 95, 100, 100, 90, 95, 100],
        ["Additive-Trend Exponential Smoothing", 92, 100, 100, 88, 92, 100],
        ["ARIMA Rolling One-Step", 85, 100, 100, 82, 90, 100],
        ["7-Day Moving Average", 98, 100, 100, 98, 98, 100],
        ["Prophet — 30-Day Periodic Refit", 75, 100, 90, 72, 82, 100],
        ["Persistence-Enhanced Log-Return LSTM", 50, 100, 90, 55, 70, 100],
        ["Persistence-Enhanced Log-Return Transformer", 45, 100, 100, 45, 75, 100],
        ["Chronos-Bolt-Tiny", 35, 100, 90, 60, 82, 45],
        ["TimesFM", 30, 100, 90, 50, 78, 45],
    ], columns=["Model", "Mechanism Transparency", "Artifact Reproducibility", "Deterministic Behaviour",
                "Implementation Simplicity", "Failure Detectability", "External Independence"])
    rubric["Transparency and Auditability Score"] = rubric.drop(columns="Model").mean(axis=1)

    metric_index = metrics.set_index("Model")
    accuracy = 100 * metric_index["RMSE"].min() / metric_index["RMSE"]
    robust_penalty = robustness.pivot(index="Model", columns="Regime", values="RMSE")
    robust_penalty = robust_penalty.mean(axis=1) + robust_penalty.std(axis=1)
    robust_score = 100 * robust_penalty.min() / robust_penalty
    stability_penalty = stability.pivot(index="Model", columns="Segment", values="RMSE")
    stability_penalty = stability_penalty.mean(axis=1) + stability_penalty.std(axis=1)
    stability_score = 100 * stability_penalty.min() / stability_penalty
    preferred_uncertainty = uncertainty[(uncertainty["Nominal Level"] == 0.80) &
        (~uncertainty["Uncertainty Evidence Type"].eq("Native Foundation Quantiles"))].drop_duplicates("Model")
    uncertainty_score = preferred_uncertainty.set_index("Model")["Coverage Error"].map(
        lambda x: max(0.0, 100 * (1 - x / 0.8)) if pd.notna(x) else np.nan
    )
    components = pd.DataFrame({"Point Forecast Accuracy": accuracy,
                               "Regime-Conditional Robustness": robust_score,
                               "Temporal Stability": stability_score,
                               "Uncertainty Calibration": uncertainty_score,
                               "Transparency and Auditability": rubric.set_index("Model")["Transparency and Auditability Score"]})
    components["Uncertainty Evidence Type"] = preferred_uncertainty.set_index("Model")["Uncertainty Evidence Type"]
    weights = {"Point Forecast Accuracy": .35, "Regime-Conditional Robustness": .20,
               "Temporal Stability": .20, "Uncertainty Calibration": .15,
               "Transparency and Auditability": .10}
    trust = components.copy()
    trust["Exploratory Composite — Missing Evidence Penalised"] = sum(
        trust[column].fillna(0) * weight for column, weight in weights.items())
    available_scores = []
    for model, row in components.iterrows():
        available = [column for column in weights if pd.notna(row[column])]
        available_scores.append(sum(row[column] * weights[column] for column in available) /
                                sum(weights[column] for column in available))
    trust["Exploratory Composite — Evidence Available"] = available_scores
    trust = trust.reset_index(names="Model")

    sensitivity_rows = []
    scenarios = {"Base": weights, "Lower transparency": {**weights, "Transparency and Auditability": .05,
                  "Point Forecast Accuracy": .40}, "Higher transparency": {**weights,
                  "Transparency and Auditability": .15, "Point Forecast Accuracy": .30}}
    for scenario, scenario_weights in scenarios.items():
        scores = sum(components[column].fillna(0) * weight for column, weight in scenario_weights.items())
        for rank, (model, score) in enumerate(scores.sort_values(ascending=False).items(), 1):
            sensitivity_rows.append({"Scenario": scenario, "Model": model, "Rank": rank, "Score": score})
    sensitivity = pd.DataFrame(sensitivity_rows)

    outputs = {
        "bitcoin_point_forecast_metrics_v2.csv": metrics,
        "bitcoin_regime_thresholds_training.csv": threshold_frame,
        "bitcoin_regime_robustness_training_defined.csv": robustness,
        "bitcoin_temporal_stability.csv": stability,
        "bitcoin_uncertainty_evidence_v2.csv": uncertainty,
        "bitcoin_dm_pairwise_results_hac_holm.csv": dm,
        "bitcoin_transparency_auditability_rubric.csv": rubric,
        "bitcoin_trustworthiness_components_v2.csv": trust,
        "bitcoin_trust_score_sensitivity_v2.csv": sensitivity,
    }
    for filename, frame in outputs.items():
        frame.to_csv(RESULTS / filename, index=False)
    return outputs


def make_figures(outputs: dict[str, pd.DataFrame]) -> None:
    FIGURES.mkdir(exist_ok=True)
    metrics = outputs["bitcoin_point_forecast_metrics_v2.csv"].sort_values("RMSE")
    colors = ["#c44e52" if "Prophet" in name else "#4c72b0" for name in metrics["Model"]]
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.barh(metrics["Model"], metrics["RMSE"], color=colors)
    ax.invert_yaxis(); ax.set_xscale("log"); ax.set_xlabel("RMSE (log scale)")
    ax.set_title("Bitcoin Final Ten-Model Accuracy — Frozen Forecasts")
    fig.tight_layout(); fig.savefig(FIGURES / "bitcoin_fair_protocol_rmse.png", dpi=180); plt.close(fig)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.barh(metrics["Model"], metrics["MAE"], color=colors); ax.invert_yaxis(); ax.set_xscale("log")
    ax.set_xlabel("MAE (log scale)"); ax.set_title("Bitcoin Model Accuracy — All Final Analytical Models")
    fig.tight_layout(); fig.savefig(FIGURES / "bitcoin_model_accuracy.png", dpi=180); plt.close(fig)
    trust = outputs["bitcoin_trustworthiness_components_v2.csv"].sort_values("Exploratory Composite — Missing Evidence Penalised")
    fig, ax = plt.subplots(figsize=(12, 6)); ax.barh(trust["Model"], trust["Exploratory Composite — Missing Evidence Penalised"])
    ax.set_xlabel("Exploratory composite score"); ax.set_title("Bitcoin Exploratory Trustworthiness Summary — Secondary Evidence")
    fig.tight_layout(); fig.savefig(FIGURES / "bitcoin_trust_score_rankings.png", dpi=180); plt.close(fig)
    validated = load_validated_forecasts(ROOT)
    fig, ax = plt.subplots(figsize=(13, 6)); validated["Actual"].plot(ax=ax, label="Actual", linewidth=2)
    for column, label in [("Naive", "Naive"), ("ARIMA_Rolling", "ARIMA"),
                          ("Persistence_Enhanced_LSTM", "PE-LSTM"), ("TimesFM", "TimesFM"),
                          ("Prophet_Periodic_Refit", "Prophet")]:
        validated[column].plot(ax=ax, label=label, alpha=.75)
    ax.set_title("Bitcoin Forecast Comparison — Selected Models"); ax.legend(ncol=3)
    fig.tight_layout(); fig.savefig(FIGURES / "bitcoin_forecast_comparison.png", dpi=180); plt.close(fig)
    misleading = FIGURES / "bitcoin_pe_lstm_determinism.png"
    if misleading.exists():
        misleading.unlink()


def role_block(title: str, role: str, inputs: str, outputs: str, depends: str,
               status: str, does_not: str) -> str:
    return f"""# {title}

## Role
{role}

## Inputs
{inputs}

## Outputs
{outputs}

## Depends On
{depends}

## Authoritative Status
{status}

## What This Notebook Does Not Do
{does_not}
"""


COMMON_SETUP = """from pathlib import Path
import sys
import pandas as pd
import numpy as np
ROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()
sys.path.insert(0, str(ROOT))
from src.bitcoin_pipeline import *
RUN_GENERATION = False
PROMOTE_TO_AUTHORITATIVE = False
"""


def notebook(title: str, role: str, inputs: str, outputs: str, depends: str,
             status: str, does_not: str, sections: list[tuple[str, str]]) -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.metadata["language_info"] = {"name": "python", "version": "3"}
    nb.cells = [nbf.v4.new_markdown_cell(role_block(title, role, inputs, outputs, depends, status, does_not)),
                nbf.v4.new_code_cell(COMMON_SETUP)]
    for kind, source in sections:
        nb.cells.append(nbf.v4.new_markdown_cell(source) if kind == "md" else nbf.v4.new_code_cell(source))
    return nb


def build_notebooks() -> None:
    specs = {}
    specs["01_Bitcoin_Data_EDA.ipynb"] = notebook("Bitcoin Data and Exploratory Analysis", "Canonical UTC data preparation and split definition.",
        "`data/bitcoin/btcusd_1-min_data.csv`", "Executed dataset, missingness, aggregation, return, volatility, and split summaries.", "Raw Bitcoin source data.",
        "AUTHORITATIVE DATA PREPARATION", "It does not train models or write forecast artifacts.", [
        ("code", "daily, target = load_bitcoin_target(ROOT)\ntrain, test = canonical_split(target)\nraw = load_bitcoin_data(ROOT/'data'/'bitcoin'/'btcusd_1-min_data.csv')\nsummary = pd.DataFrame({'Value':[len(raw), raw.Timestamp.min(), raw.Timestamp.max(), len(daily), target.index.min(), target.index.max(), target.isna().sum(), target.index.duplicated().sum()]}, index=['Raw rows','Raw start','Raw end','Daily rows','Daily start','Daily end','Missing Close','Duplicate daily dates'])\nsummary"),
        ("md", "## Daily aggregation\nOpen=first, High=max, Low=min, Close=last, Volume=sum in UTC calendar days. The target is the last available Close in each UTC date."),
        ("code", "pd.DataFrame({'Start':[train.index.min(),test.index.min()],'End':[train.index.max(),test.index.max()],'Rows':[len(train),len(test)]}, index=['Train','Test'])"),
        ("code", "eda = pd.DataFrame({'Close':target,'Log Return':np.log(target/target.shift(1))}); eda['30-Day Volatility']=eda['Log Return'].rolling(30).std(); eda.tail()"),
        ("md", "## Limitation\nThe final UTC date contains only the available observations through 01:57 UTC and therefore represents a partial daily observation rather than a completed 24-hour UTC trading day.")])

    specs["02_Bitcoin_Classical_Baselines.ipynb"] = notebook("Bitcoin Classical Baselines", "Artifact-only comparison of final past-only classical systems.",
        "Frozen validated forecasts and canonical target.", "Final classical metrics and seasonality evidence.", "01 Bitcoin Data/EDA.", "AUTHORITATIVE ANALYSIS",
        "It does not fit or overwrite classical model vectors. Earlier static multi-step implementations are excluded.", [
        ("code", "_, target=load_bitcoin_target(ROOT); train,test=canonical_split(target); v=load_validated_forecasts(ROOT); f=forecast_series(v,target); names=['Naive','7-Day Moving Average','Simple Exponential Smoothing — Rolling One-Step','Additive-Trend Exponential Smoothing','ARIMA Rolling One-Step']; metric_table(v.Actual,{n:f[n] for n in names},train).sort_values('RMSE')"),
        ("md", "## Seasonality decision\nLag-7 ACF = -0.023409; approximate 95% bound = ±0.026920; weekly STL strength = 0.069923. Weekly SARIMA was not retained."),
        ("md", "## Protocol note\nSES and additive-trend smoothing refit daily on 128 prior prices. ARIMA starts with 128 returns and appends each newly observed return without refitting parameters.")])

    specs["03_Bitcoin_PE_LSTM.ipynb"] = notebook("Bitcoin Persistence-Enhanced Log-Return LSTM", "Final supervised recurrent-model evidence.",
        "Frozen PE-LSTM and validated forecast artifacts.", "Artifact-derived PE-LSTM metrics and reproducibility record.", "01 Bitcoin Data/EDA.", "AUTHORITATIVE MODEL ANALYSIS",
        "Safe Run All does not train TensorFlow or overwrite the frozen vector.", [
        ("md", "## Authoritative design\nA 30-return input window predicts a scaled log return. A train-only scaler is used; the predicted return is reconstructed from the previous observed price. Generation used seed 42, deterministic TensorFlow, `shuffle=False`, and chronological validation."),
        ("code", "_,target=load_bitcoin_target(ROOT); train,test=canonical_split(target); v=load_validated_forecasts(ROOT); metric_table(v.Actual,{'Persistence-Enhanced Log-Return LSTM':v.Persistence_Enhanced_LSTM},train)"),
        ("md", "## Determinism evidence\nExternal fresh-kernel regression checks previously produced bit-identical forecasts; the independent run vectors were not preserved as separate authoritative artifacts. No three-run plot is presented."),
        ("md", "## Historical provenance\nRaw-price LSTM variants were development experiments and are excluded from every final table, figure, Trust Score, and inference test.")])

    specs["04_Bitcoin_PE_Transformer.ipynb"] = notebook("Bitcoin Persistence-Enhanced Log-Return Transformer", "Final supervised Transformer evidence.",
        "Frozen validated, PE-Transformer, PE-LSTM, and ARIMA vectors.", "Artifact-derived final comparison.", "01 and 03.", "AUTHORITATIVE MODEL ANALYSIS",
        "Safe Run All does not train TensorFlow; raw-price Transformer variants are not ranked.", [
        ("md", "## Final design\nThe model uses 128 prior log returns, train-only scaling, deterministic seed controls, and persistence-anchored price reconstruction."),
        ("code", "_,target=load_bitcoin_target(ROOT); train,test=canonical_split(target); v=load_validated_forecasts(ROOT); f=forecast_series(v,target); names=['Naive','ARIMA Rolling One-Step','Persistence-Enhanced Log-Return LSTM','Persistence-Enhanced Log-Return Transformer']; metric_table(v.Actual,{n:f[n] for n in names},train).sort_values('RMSE')"),
        ("md", "## Development appendix\nTransformer v1, corrected raw-price Transformer, and positional raw-price Transformer are historical diagnostics only.")])

    specs["05_Bitcoin_Prophet_and_Deferred_Models.ipynb"] = notebook("Bitcoin Prophet and Deferred Models", "Describe and evaluate the periodic-refit Prophet comparator; record deferred models.",
        "Frozen Prophet and validated vectors.", "Artifact-derived Prophet metrics and model-status table.", "01.", "SUPPORTING VALIDATED COMPARATOR",
        "It does not refit Prophet, install packages, or execute deferred models.", [
        ("md", "## Prophet protocol\nProphet uses 128 historical prices at each refit origin and refits every 30 forecast dates. It is past-only but does not update daily, so it is not operationally identical to daily-updated rolling one-step systems."),
        ("code", "_,target=load_bitcoin_target(ROOT); train,test=canonical_split(target); v=load_validated_forecasts(ROOT); metric_table(v.Actual,{'Prophet — 30-Day Periodic Refit':v.Prophet_Periodic_Refit},train)"),
        ("code", "pd.DataFrame({'Model':['Moirai','PatchTST','iTransformer','Informer','Autoformer'],'Status':['Unavailable','Deferred','Deferred','Unavailable / unexecuted','Unavailable / unexecuted']})")])

    specs["06_Bitcoin_Foundation_Models.ipynb"] = notebook("Bitcoin Foundation Models", "Artifact-only analysis of the two completed zero-shot systems.",
        "Frozen Chronos, TimesFM, and validated vectors.", "Artifact-derived foundation-model comparison.", "01.", "AUTHORITATIVE MODEL ANALYSIS",
        "It does not download checkpoints, load models, fine-tune, or regenerate forecasts.", [
        ("code", "pd.DataFrame({'Model':['Chronos-Bolt-Tiny','TimesFM'],'Checkpoint':['amazon/chronos-bolt-tiny','google/timesfm-2.5-200m-pytorch'],'Zero-shot':[True,True],'Context':[128,128],'Context end':['t-1','t-1'],'Horizon':[1,1],'Targets':[1061,1061]})"),
        ("code", "_,target=load_bitcoin_target(ROOT); train,test=canonical_split(target); v=load_validated_forecasts(ROOT); metric_table(v.Actual,{'Chronos-Bolt-Tiny':v.Chronos_Bolt_Tiny,'TimesFM':v.TimesFM},train).sort_values('RMSE')"),
        ("md", "## Limitation\nFoundation-model pretraining overlap with this Bitcoin period cannot be ruled out from local evidence. No contamination is asserted.")])

    specs["07_Bitcoin_Forecast_Freeze_and_Validation.ipynb"] = notebook("Bitcoin Forecast Freeze and Validation", "Formal boundary between expensive generation and inexpensive analysis.",
        "All frozen Bitcoin point vectors and the canonical target.", "Validation PASS table; no forecast writes.", "01–06.", "AUTHORITATIVE VALIDATION GATE",
        "It does not train, regenerate, promote, or overwrite forecasts.", [
        ("code", "_,target=load_bitcoin_target(ROOT); train,test=canonical_split(target); v=load_validated_forecasts(ROOT); checks={'1,061 rows and 10 data columns after Timestamp index':v.shape==(1061,10),'Exact timestamps':v.index.equals(test.index),'Actual identity':np.allclose(v.Actual,test),'Complete':not v.isna().any().any(),'Finite':np.isfinite(v).all().all(),'Unique timestamps':v.index.is_unique,'No duplicate vectors':not v.drop(columns='Actual').T.duplicated().any(),'PE-Transformer exists':'Persistence_Enhanced_Transformer' in v}; pd.DataFrame({'Check':checks.keys(),'PASS':checks.values()})"),
        ("code", "import subprocess,sys; run=subprocess.run([sys.executable,str(ROOT/'src'/'verify_research_artifacts.py')],capture_output=True,text=True); print(run.stdout.splitlines()[-1]); assert run.returncode==0"),
        ("md", "## Promotion controls\nGeneration must target `results/staging/bitcoin/<run-id>/`. `promote_staged_forecast` requires schema, timestamp, row-count, finite-value, optional hash checks, and `explicit_opt_in=True`.")])

    specs["08_Bitcoin_Naive_Audit.ipynb"] = notebook("Bitcoin Naive Forecast Audit", "Final proof of the rolling persistence implementation.",
        "Canonical target and frozen validated forecasts.", "Executed row audit, manual metrics, and PASS table.", "01 and 07.", "AUTHORITATIVE VALIDATION",
        "It does not compare historical models or write forecasts.", [
        ("code", "_,target=load_bitcoin_target(ROOT); train,test=canonical_split(target); v=load_validated_forecasts(ROOT); naive=target.shift(1).reindex(test.index); rows=pd.DataFrame({'Forecast date':test.index,'Previous actual':[train.iloc[-1],*test.iloc[:-1]],'Forecast':naive,'Actual':test}); display(rows.head(10)); display(rows.tail(10))"),
        ("code", "error=test-naive; manual={'MAE':np.abs(error).mean(),'RMSE':np.sqrt(np.mean(error**2)),'MAPE':100*np.mean(np.abs(error/test)),'sMAPE':100*np.mean(2*np.abs(error)/(np.abs(test)+np.abs(naive)))}; manual"),
        ("code", "checks={'First forecast uses final training observation':np.isclose(naive.iloc[0],train.iloc[-1]),'Later forecasts use previous revealed actual':np.allclose(naive.iloc[1:],test.iloc[:-1]),'Frozen vector identity':np.allclose(naive,v.Naive),'No same-day target use':not np.allclose(naive,test),'Exact error identity':np.allclose(error,target.diff().reindex(test.index)),'No index shift':naive.index.equals(test.index)}; result=pd.DataFrame({'Check':checks.keys(),'PASS':checks.values()}); assert result.PASS.all(); result")])

    specs["09_Bitcoin_Robustness_and_Temporal_Stability.ipynb"] = notebook("Bitcoin Robustness and Temporal Stability", "Apply training-defined regimes and balanced temporal segments to all ten models.",
        "Frozen forecasts and derived robustness/stability CSVs.", "Training-only thresholds, regime metrics, temporal metrics.", "07 and 08.", "AUTHORITATIVE DOWNSTREAM ANALYSIS",
        "It does not derive thresholds from test quantiles or fit models.", [
        ("code", "thresholds=pd.read_csv(ROOT/'results'/'bitcoin_regime_thresholds_training.csv'); assert thresholds.Source.eq('Training data only').all(); thresholds"),
        ("code", "robust=pd.read_csv(ROOT/'results'/'bitcoin_regime_robustness_training_defined.csv'); assert robust.Model.nunique()==10; robust.groupby('Regime').N.first()"),
        ("code", "stability=pd.read_csv(ROOT/'results'/'bitcoin_temporal_stability.csv'); assert stability.Model.nunique()==10; stability.groupby('Segment').N.first()"),
        ("md", "These are Regime-Conditional Robustness and Temporal Stability diagnostics, not comprehensive robustness or broad generalisation claims.")])

    specs["10_Bitcoin_Uncertainty.ipynb"] = notebook("Bitcoin Uncertainty Evidence", "Separate native, training-calibrated, empirical, and unavailable uncertainty evidence.",
        "Foundation uncertainty and validation residual artifacts.", "Unified evidence table with method labels.", "07 and 09.", "AUTHORITATIVE DOWNSTREAM ANALYSIS",
        "It does not calibrate on test residuals or treat heterogeneous widths as directly comparable.", [
        ("code", "u=pd.read_csv(ROOT/'results'/'bitcoin_uncertainty_evidence_v2.csv'); u"),
        ("code", "u[u['Model'].isin(['Chronos-Bolt-Tiny','TimesFM'])][['Model','Uncertainty Evidence Type','Nominal Level','Coverage','Average Width','Coverage Error']]") ,
        ("md", "Chronos has a negative CQR adjustment because its native calibration intervals over-covered on the training calibration window; finite-sample CQR therefore narrows rather than widens them. Widths are interpreted only within methodologically comparable evidence types.")])

    specs["11_Bitcoin_Statistical_Inference.ipynb"] = notebook("Bitcoin Statistical Inference", "HAC Diebold–Mariano inference with Holm family-wise correction.",
        "Ten frozen/reconstructed forecast vectors.", "`bitcoin_dm_pairwise_results_hac_holm.csv`.", "07–10.", "AUTHORITATIVE CORRECTED INFERENCE",
        "It does not rerun models or silently replace the historical DM artifact.", [
        ("code", "dm=pd.read_csv(ROOT/'results'/'bitcoin_dm_pairwise_results_hac_holm.csv'); assert dm.shape[0]==45 and len(set(dm['Model A'])|set(dm['Model B']))==10; dm"),
        ("md", "Squared-error loss is used. The Newey–West/Bartlett HAC lag is `floor(4*(N/100)^(2/9))` (6 at N=1,061). Raw and Holm-adjusted p-values are both preserved; Holm significance is the primary family-wise conclusion.")])

    specs["12_Bitcoin_Trustworthiness_Synthesis.ipynb"] = notebook("Bitcoin Trustworthiness Synthesis", "Component-first synthesis of already-computed Bitcoin evidence.",
        "Metrics, robustness, stability, uncertainty, inference, and rubric CSVs.", "Dimension table, exploratory composites, sensitivity analysis.", "07–11.", "AUTHORITATIVE SYNTHESIS; COMPOSITE IS SECONDARY",
        "It does not calculate regimes, calibrate uncertainty, perform DM tests, or train models.", [
        ("code", "trust=pd.read_csv(ROOT/'results'/'bitcoin_trustworthiness_components_v2.csv'); trust"),
        ("code", "rubric=pd.read_csv(ROOT/'results'/'bitcoin_transparency_auditability_rubric.csv'); rubric"),
        ("code", "sensitivity=pd.read_csv(ROOT/'results'/'bitcoin_trust_score_sensitivity_v2.csv'); sensitivity.pivot(index='Model',columns='Scenario',values='Rank').sort_values('Base')"),
        ("md", "## Interpretation guardrails\nDimensions are correlated; weights are researcher-defined; scores depend on the comparison set; missing-evidence penalties measure evidence completeness rather than observed poor uncertainty; and uncertainty methods are heterogeneous. Dimension-level evidence is primary. The composite is an exploratory secondary summary.")])

    specs["Bitcoin_Master.ipynb"] = notebook("Bitcoin Master — Final Artifact-Driven Workflow", "Safe-mode interface to the final ten-model Bitcoin experiment.",
        "Frozen point vectors and corrected derived Bitcoin evidence.", "Complete final synthesis without generation.", "01–12.", "MASTER / ORCHESTRATION",
        "Default Run All does not train, load external checkpoints, regenerate forecasts, or modify artifacts.", [
        ("code", "daily,target=load_bitcoin_target(ROOT); train,test=canonical_split(target); v=load_validated_forecasts(ROOT); forecasts=forecast_series(v,target); pd.DataFrame({'Daily rows':[len(target)],'Train':[len(train)],'Test':[len(test)],'Test start':[test.index.min()],'Test end':[test.index.max()]})"),
        ("md", "## Rolling one-step protocol\nAt target date t, only observations strictly before t are available. Actual t is revealed only after the forecast is recorded."),
        ("code", "pd.DataFrame({'Model':FINAL_MODEL_ORDER,'Context / update policy':[CONTEXT_POLICY[m] for m in FINAL_MODEL_ORDER]})"),
        ("code", "metrics=pd.read_csv(ROOT/'results'/'bitcoin_point_forecast_metrics_v2.csv'); metrics.sort_values('RMSE')"),
        ("code", "pd.read_csv(ROOT/'results'/'bitcoin_regime_robustness_training_defined.csv').groupby(['Regime','Model']).RMSE.first().unstack(0)"),
        ("code", "pd.read_csv(ROOT/'results'/'bitcoin_temporal_stability.csv').groupby(['Segment','Model']).RMSE.first().unstack(0)"),
        ("code", "pd.read_csv(ROOT/'results'/'bitcoin_uncertainty_evidence_v2.csv')"),
        ("code", "dm=pd.read_csv(ROOT/'results'/'bitcoin_dm_pairwise_results_hac_holm.csv'); dm[['Model A','Model B','Raw p-value','Holm-adjusted p-value','Significant Holm?','Lower-RMSE model']]"),
        ("code", "pd.read_csv(ROOT/'results'/'bitcoin_transparency_auditability_rubric.csv')"),
        ("code", "pd.read_csv(ROOT/'results'/'bitcoin_trustworthiness_components_v2.csv').sort_values('Exploratory Composite — Missing Evidence Penalised',ascending=False)"),
        ("md", "## Limitations and findings\nThe last UTC date is partial through 01:57; model contexts and update policies differ; Prophet updates only every 30 targets; foundation pretraining overlap is unresolved; uncertainty methods are heterogeneous; and composite weights are subjective. Under the frozen rolling one-day protocol, simple persistence remains exceptionally strong and complexity does not guarantee improved point accuracy.")])

    old = ["01_EDA.ipynb", "02_Classical_Models.ipynb", "03_Deep_Learning_LSTM.ipynb", "04_Transformers.ipynb",
           "05_Advanced_Forecasting_Models.ipynb", "05_Foundation_Models.ipynb", "06_Trustworthiness.ipynb",
           "07_Model_Validation_Audit.ipynb", "08_Naive_Forecast_Audit.ipynb", "09_Statistical_Significance_Test.ipynb"]
    for name in old:
        path = NOTEBOOKS / name
        if path.exists():
            path.unlink()
    for name, nb in specs.items():
        nbf.write(nb, NOTEBOOKS / name)


def execute_notebooks() -> None:
    for path in sorted(NOTEBOOKS.glob("*_Bitcoin_*.ipynb")) + [NOTEBOOKS / "Bitcoin_Master.ipynb"]:
        nb = nbf.read(path, as_version=4)
        client = NotebookClient(nb, timeout=180, kernel_name="python3", resources={"metadata": {"path": str(NOTEBOOKS)}})
        client.execute()
        nbf.write(nb, path)


def main() -> None:
    outputs = build_derived_evidence()
    make_figures(outputs)
    build_notebooks()
    execute_notebooks()
    print(json.dumps({"derived_artifacts": len(outputs), "notebooks": 13, "models": 10, "dm_pairs": 45}, indent=2))


if __name__ == "__main__":
    main()
