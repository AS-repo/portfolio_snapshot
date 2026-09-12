# portfolio-snapshot

Pulls live prices for a list of holdings, prints a markdown table (paste-ready for a Claude chat), and saves a timestamped copy to `snapshots/`.

## Setup

```bash
pip install -r requirements.txt
cp holdings.example.json holdings.json   # fill in your positions; gitignored
```

`holdings.json` is `[{ "ticker", "shares", "avg_price" }, ...]`.

## Run

```bash
python3 portfolio_tracker.py
```

Reports values in GBP by default (converted from the underlying quote via a live USD/GBP rate). Flags: `--holdings <file>` to use a different holdings file, `--no-snapshot` to skip saving, `--usd` to report in USD instead.
