# Research Data

This directory contains the canonical local inputs for the repository’s two completed empirical case studies: Bitcoin price forecasting and South Australian electricity-demand forecasting. This document records provenance, structure, chronological partitions, data-quality evidence, preprocessing boundaries, and known reproducibility limitations.

The data files are research inputs. Forecasts, metrics, calibration summaries, statistical tests, and trustworthiness evidence are maintained separately under [`results/`](../results/) and documented in the [result artifact guide](../results/README.md).

## Dataset Overview

| Domain | Dataset | Target | Frequency | Coverage | Observations | Final status |
|---|---|---|---|---|---:|---|
| Finance | Local BTC/USD minute OHLCV, aggregated to UTC daily observations | Daily `Close` price | Raw: 1 minute; research target: daily | Raw: 2012-01-01 00:01 UTC to 2026-07-07 01:57 UTC | 7,633,557 raw; 5,302 daily | Completed |
| Energy | Australian Electricity Demand, South Australia T4/SA series | Electricity demand | 30 minutes | 2002-01-01 00:00 to 2015-03-01 23:30 | 230,784 | Completed |

Weather and Transport are planned domain extensions. They are not included in this completed-dataset table because no final dataset, frozen protocol, or authoritative empirical evidence exists for either domain.

# Bitcoin — Financial Time Series

## Dataset Role

Bitcoin provides a non-stationary, high-volatility financial price series with heavy-tailed daily returns and weak weekly seasonality. It is used to test whether complex supervised and zero-shot forecasting systems improve on strong persistence and classical one-step benchmarks under changing market conditions.

These properties motivate the case study; detailed descriptive, stationarity, distributional, seasonal, and structural evidence remains in the [Bitcoin EDA notebook](../notebooks/01_Bitcoin_Data_EDA.ipynb).

## Provenance

| Item | Verified repository record |
|---|---|
| Dataset description | BTC/USD minute-level OHLCV |
| Local file | `data/bitcoin/btcusd_1-min_data.csv` |
| Timestamp representation | Unix seconds, converted to timezone-aware UTC |
| Columns | `Timestamp`, `Open`, `High`, `Low`, `Close`, `Volume` |
| Provider provenance | **Not fully documented in the current repository** |
| Original URL | Not documented |
| Acquisition method/date | Not documented |
| Licence/access terms | **Not documented in the current repository** |
| Local status | Raw local source; excluded from Git tracking |

The filename is insufficient evidence from which to infer an exchange, vendor, publisher, or licence. Provider and redistribution terms require external verification before the raw file is shared or released.

## Canonical Data and Target

The canonical local source is:

```text
data/bitcoin/btcusd_1-min_data.csv
```

The source is sorted chronologically and aggregated into UTC daily OHLCV observations:

- Open: first minute Open
- High: maximum minute High
- Low: minimum minute Low
- Close: last available minute Close
- Volume: sum of minute Volume

Rows missing required daily OHLCV values are excluded by the preprocessing pipeline. No processed daily CSV is stored under `data/`; the daily representation is reconstructed by repository code. The authoritative forecast target is the **daily price-level `Close`**, even when an individual model internally represents changes or log returns.

## Target and Frequency

| Property | Value |
|---|---|
| Raw frequency | One minute |
| Raw start | 2012-01-01 00:01 UTC |
| Raw end | 2026-07-07 01:57 UTC |
| Raw observations | 7,633,557 |
| Research frequency | Daily UTC |
| Daily start | 2012-01-01 |
| Daily end | 2026-07-07 |
| Daily observations | 5,302 |
| Forecast target | Daily `Close` price |
| Frozen test observations | 1,061 |

## Data Quality

The current EDA audit reports:

- zero duplicate raw timestamps;
- monotonically increasing raw timestamps;
- zero malformed timestamps;
- zero nonfinite OHLCV cells;
- zero duplicate daily dates;
- zero missing or nonfinite daily target values;
- zero missing daily calendar dates;
- zero or negative daily Close values: none; and
- one known incomplete endpoint: 2026-07-07 ends at 01:57 UTC rather than 23:59 UTC.

The daily index is continuous across all 5,302 expected UTC calendar days. The audit establishes daily continuity but does not separately report the number of missing individual minute slots within the raw series; daily aggregation may use fewer than 1,440 source rows on a date. The final partial day is retained to preserve the frozen `bitcoin-v1` test definition.

## Chronological Split

Bitcoin uses one canonical 80%/20% chronological split rather than the four-part structure used for Electricity.

| Partition | Start | End | N | Purpose |
|---|---|---|---:|---|
| Training / pre-test history | 2012-01-01 | 2023-08-11 | 4,241 | Model fitting, permitted historical transformations, and model-specific validation/calibration windows |
| Frozen final test | 2023-08-12 | 2026-07-07 | 1,061 | Rolling one-step final evaluation only |

Some methods construct training-only validation or calibration subsets inside the 4,241-day pre-test history. Those method-specific windows do not change the canonical final split and must end before the test begins.

## Transformations Used in Modeling

The research target remains daily Close. Model-specific methods may derive log returns, differences, rolling windows, persistence anchors, or train-fitted scaling from permitted historical observations. These representations belong to the forecasting method; they do not replace or mutate the canonical local dataset.

Scalers and fitted statistics must use training/pre-test observations only. A model may reveal the actual at day `t` only after recording its one-step forecast for `t`, after which that observation may enter the next origin.

## Leakage Guardrail

- The split is chronological; no random train/test shuffle is used.
- Every forecast for `t` uses information strictly earlier than `t`.
- Final-test targets do not fit scalers, select model configurations, define corrected robustness thresholds, or calibrate uncertainty intervals.
- Full-series EDA may describe the observed dataset, but any statistic used for fitting, selection, calibration, or conditional evaluation must respect the training/test information boundary.

## Known Limitations

- Provider, original URL, acquisition record, and licence are unresolved.
- The study covers one asset and trading pair only.
- The final UTC day is partial and may not be comparable to a complete daily session.
- Minute-level cadence gaps were not reported as a separate raw-grid count, although the reconstructed daily target has no missing calendar dates.
- Possible foundation-model pretraining overlap is a later model-evaluation limitation, not a defect in the raw Bitcoin observations.

# South Australia Electricity Demand — Energy Time Series

## Dataset Role

South Australian electricity demand complements Bitcoin with strong, operationally relevant temporal structure: short-range persistence, intraday cycles, weekly seasonality, and changing demand variability. The same frozen series supports both frequently updated one-step forecasting and fixed-origin day-ahead forecasting.

## Provenance

The canonical local TSF header states that the Australian Electricity Demand dataset contains five half-hourly state series and was extracted from the R `tsibbledata` package. It records this reference:

> O’Hara-Wild, M., Hyndman, R., and Wang, E. (2021). *tsibbledata: Diverse Datasets for 'tsibble'*. R package version 0.3.0.

The header links to `https://CRAN.R-project.org/package=tsibbledata`. The repository does not preserve an acquisition command, download date, original archive URL, or licence record for the local TSF. Although this filename is commonly associated with forecasting archives, the current local evidence is insufficient to claim a specific Monash Archive acquisition path.

## Canonical Data and Selected Series

```text
data/electricity/australian_electricity_demand_dataset.tsf
```

TSF relation: `Aus_Electricity_Demand`.

The file contains five regional series identified by explicit metadata. The completed study selects only:

| Field | Selected value |
|---|---|
| Series identifier | `T4` |
| State metadata | `SA` |
| Region | South Australia |
| Start timestamp | 2002-01-01 00:00 |
| Target | Half-hourly electricity-demand series values |

The selection is based on series metadata rather than row order. Other Australian states in the TSF are not evaluated in the completed experiments.

## Target, Units, and Frequency

| Property | Value |
|---|---|
| Frequency | Half-hourly / 30 minutes |
| Start | 2002-01-01 00:00 |
| End | 2015-03-01 23:30 |
| Observations | 230,784 |
| Days | 4,808 |
| Selected series | T4 / SA / South Australia |
| Frozen test observations | 46,176 |
| Frozen test days | 962 |
| Unit | Not explicitly encoded in the local TSF metadata |

Repository EDA prose interprets the magnitude as grid demand and sometimes labels plots in MW, but the unit is not an explicit field in the preserved TSF header. Independent unit confirmation therefore remains a provenance task.

## Data Quality

The current Electricity EDA reconstructs a regular 30-minute index and reports:

- 230,784 observations;
- monotonic chronological ordering;
- inferred frequency `30min`;
- zero duplicate timestamps;
- zero missing timestamps;
- zero missing or nonfinite demand values;
- zero demand values: none;
- negative demand values: none; and
- complete daily and weekly cadence identities.

No imputation, gap filling, automatic cleaning, or timestamp correction is required by the audited T4 series.

## Seasonal Structure

At half-hourly frequency:

- 48 observations represent one day;
- 336 observations represent one week.

These periods motivate lag-48 and lag-336 baselines, daily/weekly Fourier terms, model context windows, and horizon-specific diagnostics. Detailed ACF, profile, distributional, extreme-event, and stationarity evidence remains in the [Electricity EDA notebook](../notebooks/electricity/10_Electricity_EDA.ipynb).

## Chronological Partitions

All boundaries are aligned to complete days and loaded from the shared Electricity partition utility.

| Partition | Start | End | N | Purpose |
|---|---|---|---:|---|
| Development | 2002-01-01 00:00 | 2011-06-23 23:30 | 166,128 | Model development and candidate fitting |
| Validation | 2011-06-24 00:00 | 2012-07-12 23:30 | 18,480 | Configuration, cadence, context, and epoch selection |
| Pre-test (Development + Validation) | 2002-01-01 00:00 | 2012-07-12 23:30 | 184,608 | Final permitted fitting/calibration history after selection |
| Frozen final test | 2012-07-13 00:00 | 2015-03-01 23:30 | 46,176 | Evaluation-only evidence under both protocols |

## Evaluation Protocols

Protocol A and Protocol B are different uses of the **same frozen test dataset**, not separate datasets.

- **Protocol A — rolling one-step:** predict the next 30-minute target; release the actual only after its forecast is recorded; permit that actual to update the next origin.
- **Protocol B — fixed-origin day-ahead:** at each of 962 midnight origins, generate all 48 half-hour predictions for the next 24 hours; reveal no actual within the target block.

The shared target and dates allow protocol comparisons while preserving distinct information sets.

## Leakage Guardrail

- All partitions remain chronological.
- Model and hyperparameter selection uses pre-test validation evidence rather than final-test results.
- Final fitting and permitted scaling use development plus validation history only.
- Robustness thresholds are intended to be derived from training/pre-test information; full-series EDA thresholds are descriptive and are not substituted for them.
- Uncertainty calibration must not use final-test residuals.
- Protocol B contexts remain fixed across all 48 horizons and cannot incorporate within-day actuals.

## Known Limitations

- Only one of the five regional series is evaluated.
- The completed models use the univariate demand history; no weather, holiday, price, generation-mix, or other exogenous covariates are included.
- The fixed 2002–2015 historical period may not represent current grid structure or consumption behavior.
- Unit metadata is not explicitly encoded in the preserved TSF header.
- The repository does not document the exact TSF acquisition procedure, download date, or local-file licence/access terms.

# Chronological Evaluation Design

Forecast evaluation uses time order because future observations cannot be available to a model trained for an earlier origin. Random train/test allocation would permit future information to influence past forecasts and would not represent deployment.

The domain split designs are related but not identical:

- Bitcoin uses a canonical training/pre-test history followed by one frozen test. Model-specific validation and calibration windows are drawn from the pre-test history.
- Electricity explicitly separates Development and Validation, combines them into Pre-test after selection, and preserves a final Test partition aligned to complete days.

In both domains, the final test is evaluation-only. Descriptive analysis of an already-observed full series is kept conceptually separate from statistics used to fit, tune, calibrate, or define evaluation conditions.

# Preprocessing and Model Representations

Raw local files remain unchanged. Reproducible preparation creates in-memory canonical targets and model-specific representations:

| Operation | Domain/use | Information rule |
|---|---|---|
| UTC conversion and daily OHLCV aggregation | Bitcoin canonical daily data | Deterministic source transformation |
| Log returns and differencing | Bitcoin neural/ARIMA representations; Electricity statistical diagnostics/models | Computed from permitted historical observations |
| Scaling | Supervised neural models | Fit on training/pre-test data only |
| Rolling windows and persistence anchors | Both domains | End strictly before the forecast target |
| Seasonal lags 48 and 336 | Electricity | Use legally available prior demand |
| Fourier features | Electricity DHR-ARIMA | Configuration selected from pre-test evidence |

Model transformations do not replace the canonical target. Final Bitcoin metrics remain on price-level Close, and final Electricity metrics remain on demand values.

# Data Quality and Validation

| Check | Bitcoin | Electricity |
|---|---|---|
| Missing values | 0 nonfinite raw OHLCV cells; 0 missing daily targets | 0 missing and 0 nonfinite T4 values |
| Duplicate timestamps | 0 raw; 0 daily | 0 |
| Frequency/gap validation | Daily calendar: 5,302 expected and observed dates; raw minute-slot gap count not separately reported | Regular 30-minute grid; 0 missing timestamps |
| Invalid target values | 0 zero or negative daily Close values | 0 zero or negative demand values |
| Chronological ordering | Raw timestamps monotonic; daily target sorted and unique | Monotonic, sorted, unique |
| Partial end observation | Final UTC day ends at 01:57 and is retained | None; final test ends at 23:30 on a complete day |

These checks establish the reported structural properties. They do not prove that upstream measurements are free from vendor, exchange, sensor, or collection error.

# Data Lineage

```text
raw/local dataset
  → EDA and structural quality checks
  → canonical chronological target and split
  → model-specific historical transformations
  → frozen final-test target
  → forecast artifacts under results/
  → validation and downstream analysis
```

The `data/` directory contains research inputs and their documentation. Predictions, forecast metrics, DM tests, uncertainty evidence, and trust scores belong under `results/`, where their authority and hash protection are documented.

# Data Reproducibility

Two reproducibility questions must be separated:

- **Local analysis reproducibility:** given the preserved local files, repository code can reconstruct the canonical targets, quality audits, and chronological partitions.
- **Source-acquisition reproducibility:** independently obtaining the exact original files requires provider, version, URL, access, licence, and acquisition metadata.

Bitcoin local analysis is reproducible from the present CSV, but exact independent reacquisition is not currently documented. Electricity local analysis is reproducible from the TSF; its header records `tsibbledata` extraction and a package reference, but the exact local acquisition route and licence remain incomplete.

# Planned Domain Extensions

| Domain | Proposed research role | Status |
|---|---|---|
| Weather | Extend evaluation to meteorological structure and domain-specific horizons | **PLANNED — NOT PART OF CURRENT FINAL EMPIRICAL EVIDENCE** |
| Transport | Extend evaluation to mobility/traffic demand and operational forecasting | **PLANNED — NOT PART OF CURRENT FINAL EMPIRICAL EVIDENCE** |

No Weather or Transport dataset file currently exists under `data/`. A directory or future local file alone would not establish a completed evaluation; completion requires a frozen protocol, validated forecasts, and authoritative evidence.

# Dataset Citation and Licence Status

| Dataset | Citation / source status | Licence / access status |
|---|---|---|
| Bitcoin BTC/USD minute OHLCV | Provider, URL, acquisition method, and date need external verification | Not documented; redistribution status unresolved |
| Australian Electricity Demand | Local TSF states extraction from O’Hara-Wild, Hyndman, and Wang (2021), `tsibbledata` 0.3.0; exact acquisition route needs verification | Not documented in the local artifact; needs external verification |

The project bibliography is maintained in [`paper/references.md`](../paper/references.md). Citation presence does not substitute for a verified dataset licence.

# Directory Structure

```text
data/
├── README.md
├── bitcoin/
│   ├── README.md
│   └── btcusd_1-min_data.csv
└── electricity/
    └── australian_electricity_demand_dataset.tsf
```

There are no stored processed/split datasets, Weather/Transport files, or historical unused datasets in the current data tree. Canonical prepared series and partitions are reconstructed in memory.

# Detailed Data Analysis

This README documents provenance, structure, governance, and information boundaries. Detailed analysis remains in:

- [Bitcoin Data EDA](../notebooks/01_Bitcoin_Data_EDA.ipynb): descriptive statistics, stationarity, returns, distributions, seasonality, extremes, and regime preview.
- [South Australia Electricity EDA](../notebooks/electricity/10_Electricity_EDA.ipynb): regional selection, quality audit, seasonal profiles, autocorrelation, extremes, variability, stationarity, and frozen partition context.

# Related Documentation

- [Research overview](../README.md)
- [Notebook workflow guide](../notebooks/README.md)
- [Result artifact guide](../results/README.md)
- [Bitcoin domain data note](bitcoin/README.md)
- [Bitcoin reproducibility record](../docs/bitcoin_reproducibility.md)
- [Research manuscript and references](../paper/README.md)
