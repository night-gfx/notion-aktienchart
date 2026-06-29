"""
Transform time series data by extracting metadata for dynamic indexing.

For each series, computes and stores:
- first_price: The first price (base for indexing)
- base_dates: Key reference dates (1y, 3y, 5y, 10y, 20y before latest)

The browser then computes indexed and log-return values dynamically
based on the user's selected basis point.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "commodities.json"
OUTPUT = ROOT / "data" / "commodities_transformed.json"


def subtract_years(date_str: str, years: int) -> str:
    """Subtract years from a YYYY-MM-DD date string."""
    parts = date_str.split("-")
    year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
    year -= years
    return f"{year:04d}-{month:02d}-{day:02d}"


def find_closest_date(date_target: str, available_dates: list[str]) -> str | None:
    """Find the closest date in available_dates that is <= date_target."""
    matching = [d for d in available_dates if d <= date_target]
    return matching[-1] if matching else None


def transform_series(series: dict[str, Any], latest_date: str) -> dict[str, Any]:
    """
    Transform a single series to include metadata for dynamic indexing.
    
    Args:
        series: Dict with "ticker", "name", "group", "data" (list of [date, price])
        latest_date: The latest date across all series
    
    Returns:
        Enhanced dict with first_price and base_dates for dynamic calculations.
    """
    ticker = series.get("ticker", "unknown")
    data = series.get("data", [])
    
    if not data:
        return {
            **series,
            "first_price": None,
            "base_dates": {},
        }
    
    # Extract dates
    available_dates = [date_str for date_str, price in data if float(price) > 0]
    
    if not available_dates:
        print(f"  {ticker}: No valid dates found")
        return {
            **series,
            "first_price": None,
            "base_dates": {},
        }
    
    # Find first valid price
    first_price = None
    for date_str, price in data:
        price_float = float(price)
        if price_float > 0:
            first_price = price_float
            break
    
    if first_price is None:
        print(f"  {ticker}: No valid first price found")
        return {
            **series,
            "first_price": None,
            "base_dates": {},
        }
    
    # Compute target dates for common basis points
    base_dates = {}
    for years in [1, 3, 5, 10, 20]:
        target_date = subtract_years(latest_date, years)
        closest = find_closest_date(target_date, available_dates)
        if closest:
            base_dates[f"{years}y"] = closest
    
    return {
        **series,
        "first_price": round(first_price, 8),
        "base_dates": base_dates,
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
        
        transformed = transform_series(series, latest_date)
        transformed_series.append(transformed)
    
    # Build output payload
    output_payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "frequency": "daily",
        "source": "Yahoo Finance via yfinance (with dynamic indexing metadata)",
        "latest_date": latest_date,
        "indexing_info": {
            "description": "Browser computes indexed and log_return dynamically",
            "indexed": "100 × (price / base_price)",
            "log_return": "100 × ln(price / base_price)",
            "available_bases": ["display-start", "1y", "3y", "5y", "10y", "20y", "first-common", "custom"]
        },
        "series": transformed_series,
        "errors": payload.get("errors", []),
    }
    
    # Write output
    OUTPUT.write_text(
        json.dumps(output_payload, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    
    print(f"\nWrote {OUTPUT}")
    print(f"  {len(transformed_series)} series with dynamic indexing metadata")


if __name__ == "__main__":
    main()
