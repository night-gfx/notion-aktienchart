"""
Transform time series data by computing indexed and log-return versions.

For each series:
- Stores original prices
- Computes "indexed": (price / first_price) × 100
- Computes "log_return": 100 × ln(price / first_price)

All computed once at data preparation time, not in the browser.
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "commodities.json"
OUTPUT = ROOT / "data" / "commodities_transformed.json"


def transform_series(series: dict[str, Any]) -> dict[str, Any]:
    """
    Transform a single series to include price, indexed, and log-return data.
    
    Args:
        series: Dict with "ticker", "name", "group", "data" (list of [date, price])
    
    Returns:
        Enhanced dict with indexed and log_return computed for all observations.
    """
    ticker = series.get("ticker", "unknown")
    data = series.get("data", [])
    
    if not data:
        return {
            **series,
            "indexed": [],
            "log_return": [],
        }
    
    # Extract first valid price (base for indexing)
    base_price = None
    for date_str, price in data:
        price_float = float(price)
        if price_float > 0:
            base_price = price_float
            break
    
    if base_price is None:
        print(f"  {ticker}: No valid base price found")
        return {
            **series,
            "indexed": [],
            "log_return": [],
        }
    
    indexed_data = []
    log_return_data = []
    
    for date_str, price in data:
        price_float = float(price)
        
        if price_float > 0:
            # Index: (P_t / P_base) × 100
            indexed_value = (price_float / base_price) * 100
            indexed_data.append([date_str, round(indexed_value, 8)])
            
            # Log-return: 100 × ln(P_t / P_base)
            try:
                log_return_value = 100 * math.log(price_float / base_price)
                log_return_data.append([date_str, round(log_return_value, 8)])
            except (ValueError, ZeroDivisionError):
                print(f"  {ticker} at {date_str}: Math error in log calculation")
                log_return_data.append([date_str, None])
        else:
            # Invalid prices
            indexed_data.append([date_str, None])
            log_return_data.append([date_str, None])
    
    return {
        **series,
        "indexed": indexed_data,
        "log_return": log_return_data,
    }


def main() -> None:
    """Load raw commodity data and compute all transformations."""
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
        "source": "Yahoo Finance via yfinance (transformed)",
        "transformations": {
            "indexed": "100 × (price / first_price)",
            "log_return": "100 × ln(price / first_price)",
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
    print(f"  {len(transformed_series)} series with indexed and log-return data")


if __name__ == "__main__":
    main()
