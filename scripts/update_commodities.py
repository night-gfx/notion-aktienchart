"""
Download historical commodity futures data via yfinance and save daily
closing prices as a JSON file for GitHub Pages.
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "commodities.json"

COMMODITIES: dict[str, list[dict[str, str]]] = {
    "Energy": [
        {"ticker": "CL=F", "name": "WTI Crude"},
        {"ticker": "BZ=F", "name": "Brent Crude"},
        {"ticker": "NG=F", "name": "Natural Gas"},
        {"ticker": "RB=F", "name": "RBOB Gasoline"},
        {"ticker": "HO=F", "name": "Heating Oil"},
    ],
    "Metals": [
        {"ticker": "GC=F", "name": "Gold"},
        {"ticker": "SI=F", "name": "Silver"},
        {"ticker": "HG=F", "name": "Copper"},
        {"ticker": "PL=F", "name": "Platinum"},
        {"ticker": "PA=F", "name": "Palladium"},
        {"ticker": "ALI=F", "name": "Aluminum"},
    ],
    "Grains / Oilseeds": [
        {"ticker": "ZC=F", "name": "Corn"},
        {"ticker": "ZW=F", "name": "Wheat"},
        {"ticker": "KE=F", "name": "KC HRW Wheat"},
        {"ticker": "ZS=F", "name": "Soybeans"},
        {"ticker": "ZL=F", "name": "Soybean Oil"},
        {"ticker": "ZM=F", "name": "Soybean Meal"},
        {"ticker": "ZO=F", "name": "Oats"},
        {"ticker": "ZR=F", "name": "Rough Rice"},
    ],
    "Softs": [
        {"ticker": "KC=F", "name": "Coffee"},
        {"ticker": "SB=F", "name": "Sugar"},
        {"ticker": "CC=F", "name": "Cocoa"},
        {"ticker": "CT=F", "name": "Cotton"},
        {"ticker": "OJ=F", "name": "Orange Juice"},
    ],
    "Livestock": [
        {"ticker": "LE=F", "name": "Live Cattle"},
        {"ticker": "HE=F", "name": "Lean Hogs"},
        {"ticker": "GF=F", "name": "Feeder Cattle"},
    ],
}


def existing_series() -> dict[str, dict[str, Any]]:
    """Keep historical data after a temporary data-provider failure."""
    if not OUTPUT.exists():
        return {}

    try:
        payload = json.loads(OUTPUT.read_text(encoding="utf-8"))
        return {
            item["ticker"]: item
            for item in payload.get("series", [])
            if isinstance(item, dict) and item.get("ticker")
        }
    except (OSError, json.JSONDecodeError):
        return {}


def daily_points(history: pd.DataFrame) -> list[list[object]]:
    """Return one closing price for every available trading day."""
    if history.empty:
        return []

    close = pd.to_numeric(history["Close"], errors="coerce").dropna()
    if close.empty:
        return []

    index = pd.to_datetime(close.index)
    if getattr(index, "tz", None) is not None:
        index = index.tz_localize(None)

    close.index = index.normalize()
    close = close[~close.index.duplicated(keep="last")].sort_index()

    return [
        [date.strftime("%Y-%m-%d"), round(float(value), 8)]
        for date, value in close.items()
        if pd.notna(value) and float(value) > 0
    ]

def download(ticker: str, attempts: int = 3) -> list[list[object]]:
    last_error: Exception | None = None

    for attempt in range(1, attempts + 1):
        try:
            history = yf.Ticker(ticker).history(
                period="max",
                interval="1d",
                auto_adjust=False,
                actions=False,
            )

            values = daily_points(history)
            if values:
                return values

            raise RuntimeError("No usable close prices returned.")

        except Exception as error:
            last_error = error
            if attempt < attempts:
                time.sleep(attempt * 3)

    raise RuntimeError(f"{ticker}: {last_error}")


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    old = existing_series()
    series: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []

    for group, instruments in COMMODITIES.items():
        for instrument in instruments:
            ticker = instrument["ticker"]

            try:
                data = download(ticker)
                series.append({
                    "ticker": ticker,
                    "name": instrument["name"],
                    "group": group,
                    "data": data,
                })
                print(f"Downloaded {ticker}: {len(data)} observations")

            except Exception as error:
                if ticker in old:
                    kept = old[ticker].copy()
                    kept["name"] = instrument["name"]
                    kept["group"] = group
                    series.append(kept)
                    print(f"Kept previous {ticker}: {error}")
                else:
                    errors.append({"ticker": ticker, "error": str(error)})
                    print(f"Failed {ticker}: {error}")

            time.sleep(0.7)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "frequency": "daily",
        "source": "Yahoo Finance via yfinance",
        "series": series,
        "errors": errors,
    }

    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    print(f"Wrote {OUTPUT} — daily data for {len(series)} series, {len(errors)} errors.")


if __name__ == "__main__":
    main()
