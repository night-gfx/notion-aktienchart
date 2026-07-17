"""Add weekly closing prices used by the browser-side analysis charts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "commodities.json"
OUTPUT = ROOT / "data" / "commodities_transformed.json"


def weekly_closes(data: list[list[object]]) -> list[list[object]]:
    """Return the last available close in every ISO calendar week."""
    weeks: dict[tuple[int, int], list[object]] = {}
    for date_str, price in data:
        value = float(price)
        if value <= 0:
            continue
        date = datetime.strptime(str(date_str), "%Y-%m-%d")
        iso_year, iso_week, _ = date.isocalendar()
        weeks[(iso_year, iso_week)] = [str(date_str), round(value, 8)]
    return list(weeks.values())


def transform_series(series: dict[str, Any]) -> dict[str, Any]:
    """Add weekly closes to one daily time series."""
    data = series.get("data", [])

    if not data:
        return {**series, "weekly_data": []}

    return {
        **series,
        "weekly_data": weekly_closes(data),
    }


def main() -> None:
    """Load raw commodity data and compute transformation metadata."""
    if not INPUT.exists():
        print(f"Input file not found: {INPUT}")
        return
    
    # Load input
    try:
        payload = json.loads(INPUT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error reading {INPUT}: {e}")
        return
    
    original_series = payload.get("series", [])
    print(f"Processing {len(original_series)} series...")
    
    # Find latest date across all series
    all_dates = []
    for series in original_series:
        if isinstance(series, dict) and series.get("data"):
            for date_str, price in series["data"]:
                try:
                    if float(price) > 0:
                        all_dates.append(date_str)
                except (ValueError, TypeError):
                    pass
    
    all_dates.sort()
    latest_date = all_dates[-1] if all_dates else None
    
    if not latest_date:
        print("No valid dates found in any series")
        return
    
    print(f"Latest date across all series: {latest_date}")
    
    # Transform each series
    transformed_series = []
    for series in original_series:
        if not isinstance(series, dict) or not series.get("ticker"):
            continue
        
        ticker = series.get("ticker")
        print(f"  Transforming {ticker}...")
        
        transformed = transform_series(series)
        transformed_series.append(transformed)
    
    # Build output payload
    output_payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "frequency": "daily",
        "source": "Yahoo Finance via yfinance",
        "latest_date": latest_date,
        "series": transformed_series,
        "errors": payload.get("errors", []),
    }
    
    # Write output
    OUTPUT.write_text(
        json.dumps(output_payload, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    
    print(f"\nWrote {OUTPUT}")
    print(f"  {len(transformed_series)} series with weekly closes")


if __name__ == "__main__":
    main()
