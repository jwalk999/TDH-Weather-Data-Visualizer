"""
File Name: alerts.py

Author: Jonathan W
Date Created: 10/20/2026
Last Update: 10/20/2026
Version: 1.0.0

Scope: Fetches active weather alerts for a point from the US National Weather Service (api.weather.gov).
    Open-Meteo has no alerts, so this is a separate, free, keyless call. Locations outside the US simply
    return no alerts.
"""

from datetime import datetime

import requests

NWS_ALERTS_URL = "https://api.weather.gov/alerts/active"
# NWS asks every client to identify itself; requests without a User-Agent can be blocked
HEADERS = {
    "User-Agent": "TooDamnHot (https://github.com/jwalk999/TDH-Weather-Data-Visualizer)",
    "Accept": "application/geo+json",
}
SEVERITY_ORDER = {"Extreme": 0, "Severe": 1, "Moderate": 2, "Minor": 3}
MAX_TEXT = 600  # NWS descriptions can run for pages; the card only needs the gist


def _tidy(text: str | None) -> str:
    """Collapses NWS's hard-wrapped text into one paragraph and trims it to MAX_TEXT characters."""
    if not text:
        return ""
    text = " ".join(text.split())
    return text if len(text) <= MAX_TEXT else text[: MAX_TEXT - 1].rstrip() + "…"


def _format_time(iso: str | None) -> str:
    """Turns an ISO timestamp like "2026-07-14T21:00:00-04:00" into "9:00 PM Tue". Empty string if missing."""
    if not iso:
        return ""
    stamp = datetime.fromisoformat(iso)
    return stamp.strftime("%I:%M %p %a").lstrip("0")


def get_alerts(latitude: float, longitude: float) -> list[dict]:
    """Returns the active alerts for a point, most severe first.

    Args:
        latitude: Decimal degrees.
        longitude: Decimal degrees.

    Returns:
        A list of dicts with event, severity, headline, description, instruction, sender and ends keys.
        Empty when there are no alerts or the point is outside NWS coverage.

    Raises:
        requests.RequestException: On network errors or unexpected HTTP errors.
    """
    r = requests.get(
        NWS_ALERTS_URL,
        params={"point": f"{latitude:.4f},{longitude:.4f}"},
        headers=HEADERS,
        timeout=10,
    )
    if r.status_code in (400, 404):  # Outside the US or an invalid point
        return []
    r.raise_for_status()

    alerts = []
    for feature in r.json().get("features", []):
        props = feature.get("properties", {})
        alerts.append({
            "event": props.get("event", "Weather Alert"),
            "severity": props.get("severity", "Unknown"),
            "headline": props.get("headline", ""),
            "description": _tidy(props.get("description")),
            "instruction": _tidy(props.get("instruction")),
            "sender": props.get("senderName", "National Weather Service"),
            "ends": _format_time(props.get("ends") or props.get("expires")),
        })
    alerts.sort(key=lambda a: SEVERITY_ORDER.get(a["severity"], 9))
    return alerts


if __name__ == "__main__":
    for alert in get_alerts(35.73319, -81.3412):
        print(alert["severity"], "-", alert["event"], "until", alert["ends"])
