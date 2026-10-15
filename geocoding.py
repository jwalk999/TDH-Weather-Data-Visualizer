"""
File Name: geocoding.py

Author: Jonathan W
Date Created: 10/15/2026
Last Update: 10/15/2026
Version: 1.0.0

Scope: Looks up place names with the Open-Meteo Geocoding API and turns results into config.json locations.
"""

import json

import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def geocode(name: str, limit: int = 3) -> list[dict] | None:
    """Looks up a place name and returns the top matches.

    Args:
        name: Place name or postal code to search for, e.g. "Hickory".
        limit: Maximum number of matches to return. Defaults to 3.

    Returns:
        Up to ``limit`` match dicts with keys like name, admin1, country, latitude, longitude, elevation and
        timezone, or None if nothing matched.

    Raises:
        requests.HTTPError: If the API request fails.
    """
    r = requests.get(
        GEOCODING_URL,
        params={"name": name, "count": limit, "language": "en", "format": "json"},
        timeout=10,
    )
    r.raise_for_status()
    results = r.json().get("results")
    if not results:
        return None
    return results[:limit]


def format_match(match: dict) -> str:
    """Builds a display name from a geocoding match, e.g. "Hickory, North Carolina, United States".

    Args:
        match: One result from geocode().

    Returns:
        The place name followed by its state/province and country, skipping any that are missing.
    """
    parts = (match.get("name"), match.get("admin1"), match.get("country"))
    return ", ".join(part for part in parts if part)


def match_to_location(match: dict) -> dict:
    """Converts a geocoding match into the location dict saved in config.json.

    Args:
        match: One result from geocode().

    Returns:
        Dict with location_name, latitude, longitude, elevation and timezone keys.
    """
    return {
        "location_name": format_match(match),
        "latitude": match["latitude"],
        "longitude": match["longitude"],
        "elevation": match.get("elevation"),
        "timezone": match["timezone"],
    }


if __name__ == "__main__":
    matches = geocode("Hickory")
    if matches:
        with open("location.json", "w", encoding="utf-8") as f:
            json.dump(matches, f, indent=2, ensure_ascii=False)
        for m in matches:
            print(match_to_location(m))
