# Portfolio Tracker

Pulls live prices for your holdings and prints a paste-ready markdown
summary for a Claude chat. Each run also saves a timestamped `.md`
snapshot of the table to `snapshots/`.

## Setup

```bash
pip install -r requirements.txt
```

## Configure holdings

Copy the example file and fill in your real positions:

```bash
cp holdings.example.json holdings.json
```

`holdings.json` is gitignored so your actual positions never get pushed.

```json
[
  { "ticker": "AAPL", "shares": 10, "avg_price": 150.00 },
  { "ticker": "MSFT", "shares": 5, "avg_price": 300.00 }
]
```

- `ticker`: any symbol Yahoo Finance recognizes (US and most international exchanges)
- `shares`: number of shares held (fractional shares OK)
- `avg_price`: your average cost basis per share

## Run

```bash
python3 portfolio_tracker.py
```

This prints a markdown table (total value, day change, total gain/loss)
to your terminal — copy/paste it straight into a Claude chat — and saves
a timestamped copy to `snapshots/portfolio_YYYYMMDD_HHMMSS.md`.

Use `--holdings path/to/file.json` to point at a different holdings file,
or `--no-snapshot` to skip saving the snapshot file.
