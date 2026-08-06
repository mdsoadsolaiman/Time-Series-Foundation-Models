# Bitcoin Data

## Verified local source record

The completed Finance study uses the local file `btcusd_1-min_data.csv`. Repository code and notebooks identify it as BTC/USD minute-level OHLCV data with columns `Timestamp`, `Open`, `High`, `Low`, `Close`, and `Volume`. `Timestamp` is stored as Unix seconds and converted to a UTC datetime.

The repository does **not** contain a verified original download URL, provider attribution, or licence record. The filename is not sufficient evidence from which to infer a publisher. The original source must therefore be confirmed by the researcher before redistribution or external release; this document deliberately does not guess it.

## Data characteristics and target

- Raw frequency: one minute.
- Verified local date range: 2012-01-01 00:01 UTC to 2026-07-07 01:57 UTC.
- Verified local row count: 7,633,557.
- Forecast target: daily Bitcoin `Close`.
- Daily preparation: sort chronologically; resample in UTC; aggregate Open=first, High=max, Low=min, Close=last, Volume=sum; drop incomplete daily rows as implemented in `src/preprocessing.py`.
- Chronological split: 80%/20%; train through 2023-08-11 and test from 2023-08-12 through 2026-07-07 (1,061 days).

## Reproduction and tracking policy

Place an independently and lawfully obtained source file at:

```text
data/bitcoin/btcusd_1-min_data.csv
```

Then run the data audit in `notebooks/01_EDA.ipynb`. The raw file is approximately 386 MB and is excluded by `.gitignore`; it is not tracked in Git. No processed daily CSV is created here because the raw provenance and redistribution terms have not yet been verified, and the daily series is reproducibly derived by repository code.
