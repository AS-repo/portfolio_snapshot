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

Flags: `--holdings <file>` to use a different holdings file, `--no-snapshot` to skip saving.
