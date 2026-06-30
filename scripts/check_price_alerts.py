#!/usr/bin/env python3
"""Check open GitHub price-alert issues against the latest commodity prices."""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "commodities_transformed.json"
ALERT_MARKER = "<!-- commodity-price-alert -->"
FIELD_PATTERN = re.compile(
    r"^(Ticker|Zielpreis|Richtung):\s*(.+?)\s*$",
    re.MULTILINE,
)


def parse_alert(body: str) -> dict[str, str] | None:
    if ALERT_MARKER not in body:
        return None
    fields = {key: value for key, value in FIELD_PATTERN.findall(body)}
    if not {"Ticker", "Zielpreis", "Richtung"} <= fields.keys():
        return None
    if fields["Richtung"] not in {"above", "below"}:
        return None
    try:
        price = float(fields["Zielpreis"])
    except ValueError:
        return None
    if price <= 0:
        return None
    return {
        "ticker": fields["Ticker"],
        "price": price,
        "direction": fields["Richtung"],
    }


def latest_prices(path: Path = DATA_FILE) -> dict[str, tuple[str, float]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    prices: dict[str, tuple[str, float]] = {}
    for series in payload.get("series", []):
        data = series.get("data") or []
        if not data:
            continue
        date, value = data[-1]
        prices[series["ticker"]] = (date, float(value))
    return prices


def is_reached(alert: dict[str, object], current_price: float) -> bool:
    target = float(alert["price"])
    return (
        current_price >= target
        if alert["direction"] == "above"
        else current_price <= target
    )


class GitHubApi:
    def __init__(self, repository: str, token: str) -> None:
        self.repository = repository
        self.base_url = f"https://api.github.com/repos/{repository}"
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "commodity-price-alert-checker",
        }

    def request(self, method: str, path: str, payload: dict | None = None):
        data = json.dumps(payload).encode() if payload is not None else None
        request = urllib.request.Request(
            f"{self.base_url}{path}",
            data=data,
            headers=self.headers,
            method=method,
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)

    def open_issues(self) -> list[dict]:
        issues = self.request("GET", "/issues?state=open&per_page=100")
        return [issue for issue in issues if "pull_request" not in issue]

    def comment(self, issue_number: int, body: str) -> None:
        self.request(
            "POST",
            f"/issues/{issue_number}/comments",
            {"body": body},
        )

    def close(self, issue_number: int) -> None:
        self.request("PATCH", f"/issues/{issue_number}", {"state": "closed"})


def main() -> int:
    now = datetime.now(ZoneInfo("Europe/Berlin"))
    if not 8 <= now.hour < 24 and os.getenv("GITHUB_EVENT_NAME") != "workflow_dispatch":
        print(f"Outside alert window: {now:%H:%M} Europe/Berlin")
        return 0

    repository = os.environ.get("GITHUB_REPOSITORY")
    token = os.environ.get("GITHUB_TOKEN")
    if not repository or not token:
        print("GITHUB_REPOSITORY and GITHUB_TOKEN are required.", file=sys.stderr)
        return 2

    prices = latest_prices()
    api = GitHubApi(repository, token)
    checked = 0
    triggered = 0

    try:
        issues = api.open_issues()
        for issue in issues:
            alert = parse_alert(issue.get("body") or "")
            if alert is None:
                continue
            checked += 1
            quote = prices.get(alert["ticker"])
            if quote is None:
                print(f"No price data for {alert['ticker']}")
                continue
            quote_date, current_price = quote
            if not is_reached(alert, current_price):
                continue

            relation = "≥" if alert["direction"] == "above" else "≤"
            message = (
                f"🔔 **Preisalarm erreicht**\n\n"
                f"- Ticker: `{alert['ticker']}`\n"
                f"- Aktueller Kurs: **{current_price:g}**\n"
                f"- Bedingung: {relation} **{alert['price']:g}**\n"
                f"- Kursdatum: {quote_date}\n\n"
                "Der Alarm wird nach dieser Benachrichtigung automatisch geschlossen."
            )
            api.comment(issue["number"], message)
            api.close(issue["number"])
            triggered += 1
            print(f"Triggered issue #{issue['number']} for {alert['ticker']}")
    except (urllib.error.HTTPError, urllib.error.URLError) as error:
        print(f"GitHub API error: {error}", file=sys.stderr)
        return 1

    print(f"Checked {checked} active price alerts; triggered {triggered}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
