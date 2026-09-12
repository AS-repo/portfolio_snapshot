#!/usr/bin/env python3
"""
Portfolio tracker: pulls live prices for a list of holdings and prints a
Claude-paste-ready markdown summary. Also saves a timestamped .md snapshot
of each run to snapshots/.

Usage:
    python3 portfolio_tracker.py [--holdings holdings.json] [--no-snapshot]
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import yfinance as yf

SCRIPT_DIR = Path(__file__).resolve().parent
SNAPSHOT_DIR = SCRIPT_DIR / "snapshots"


def load_holdings(path: Path):
    with open(path) as f:
        data = json.load(f)
    for row in data:
        if "ticker" not in row or "shares" not in row or "avg_price" not in row:
            raise ValueError(f"Holding entry missing required fields: {row}")
    return data


def fetch_quote(ticker: str):
    t = yf.Ticker(ticker)
    fast = t.fast_info
    try:
        price = fast.last_price
        prev_close = fast.previous_close
    except Exception:
        price = None
        prev_close = None
    if price is None or prev_close is None or price != price or prev_close != prev_close:
        hist = t.history(period="2d")
        if hist.empty:
            raise ValueError(f"No price data returned for {ticker}")
        price = hist["Close"].iloc[-1]
        prev_close = hist["Close"].iloc[-2] if len(hist) > 1 else price
    day_change = price - prev_close
    day_change_pct = (day_change / prev_close * 100) if prev_close else 0.0
    return {
        "price": float(price),
        "prev_close": float(prev_close),
        "day_change": float(day_change),
        "day_change_pct": float(day_change_pct),
    }


def build_rows(holdings):
    rows = []
    for h in holdings:
        ticker = h["ticker"].upper()
        shares = float(h["shares"])
        avg_price = float(h["avg_price"])
        try:
            q = fetch_quote(ticker)
        except Exception as e:
            print(f"  ! warning: failed to fetch {ticker}: {e}", file=sys.stderr)
            continue

        market_value = shares * q["price"]
        cost_basis = shares * avg_price
        total_gain = market_value - cost_basis
        total_gain_pct = (total_gain / cost_basis * 100) if cost_basis else 0.0
        day_pl = shares * q["day_change"]

        rows.append({
            "ticker": ticker,
            "shares": shares,
            "avg_price": avg_price,
            "price": q["price"],
            "day_change": q["day_change"],
            "day_change_pct": q["day_change_pct"],
            "day_pl": day_pl,
            "market_value": market_value,
            "cost_basis": cost_basis,
            "total_gain": total_gain,
            "total_gain_pct": total_gain_pct,
        })
    return rows


def fmt_money(x):
    sign = "-" if x < 0 else ""
    return f"{sign}${abs(x):,.2f}"


def fmt_pct(x):
    sign = "+" if x >= 0 else ""
    return f"{sign}{x:.2f}%"


def render_markdown(rows, timestamp):
    total_value = sum(r["market_value"] for r in rows)
    total_cost = sum(r["cost_basis"] for r in rows)
    total_day_pl = sum(r["day_pl"] for r in rows)
    total_gain = total_value - total_cost
    total_gain_pct = (total_gain / total_cost * 100) if total_cost else 0.0
    total_day_pct = (total_day_pl / (total_value - total_day_pl) * 100) if (total_value - total_day_pl) else 0.0

    lines = []
    lines.append(f"# Portfolio Snapshot — {timestamp}")
    lines.append("")
    lines.append("| Ticker | Shares | Avg Cost | Price | Day Chg | Day % | Mkt Value | Total G/L | Total % |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for r in sorted(rows, key=lambda x: -x["market_value"]):
        lines.append(
            f"| {r['ticker']} | {r['shares']:g} | {fmt_money(r['avg_price'])} | "
            f"{fmt_money(r['price'])} | {fmt_money(r['day_change'])} | {fmt_pct(r['day_change_pct'])} | "
            f"{fmt_money(r['market_value'])} | {fmt_money(r['total_gain'])} | {fmt_pct(r['total_gain_pct'])} |"
        )
    lines.append("")
    lines.append(
        f"**Total value:** {fmt_money(total_value)}  |  "
        f"**Day P/L:** {fmt_money(total_day_pl)} ({fmt_pct(total_day_pct)})  |  "
        f"**Total G/L:** {fmt_money(total_gain)} ({fmt_pct(total_gain_pct)})"
    )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Track a stock portfolio with live prices.")
    parser.add_argument("--holdings", default=str(SCRIPT_DIR / "holdings.json"), help="Path to holdings JSON file")
    parser.add_argument("--no-snapshot", action="store_true", help="Skip saving a markdown snapshot file")
    args = parser.parse_args()

    holdings_path = Path(args.holdings)
    if not holdings_path.exists():
        print(f"Holdings file not found: {holdings_path}", file=sys.stderr)
        sys.exit(1)

    holdings = load_holdings(holdings_path)
    print(f"Fetching live prices for {len(holdings)} holdings...", file=sys.stderr)
    rows = build_rows(holdings)
    if not rows:
        print("No prices could be fetched. Exiting.", file=sys.stderr)
        sys.exit(1)

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    markdown = render_markdown(rows, timestamp)
    print()
    print(markdown)
    print()

    if not args.no_snapshot:
        SNAPSHOT_DIR.mkdir(exist_ok=True)
        file_stamp = now.strftime("%Y%m%d_%H%M%S")
        out_path = SNAPSHOT_DIR / f"portfolio_{file_stamp}.md"
        out_path.write_text(markdown + "\n")
        print(f"Snapshot saved: {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
