# portfolio-snapshot

Pulls live prices for a list of holdings, prints a markdown table (paste-ready for a Claude chat), and saves a timestamped copy to `snapshots/`.

## Setup

```bash
pip install -r requirements.txt
cp holdings.example.json holdings.json   # fill in your positions; gitignored
```

`holdings.json` is `[{ "ticker", "shares", "avg_price", "currency" }, ...]`.

- `ticker` must be the exact yfinance symbol, including exchange suffix for non-US listings (e.g. `VUKG.L` on the LSE).
- `currency` is the currency `avg_price` was paid in (`"USD"` or `"GBP"`); defaults to `"USD"` if omitted.

## Run

```bash
python3 portfolio_tracker.py
```

Reports values in GBP by default. Each holding's live quote and cost basis are converted to GBP independently based on their own currencies (handling USD, GBP, and GBX/pence-denominated LSE tickers), via a live USD/GBP rate. Flags: `--holdings <file>` to use a different holdings file, `--no-snapshot` to skip saving, `--usd` to report in USD instead.
