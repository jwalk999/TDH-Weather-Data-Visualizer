"""
File Name: global_params.py

Author: Jonathan W
Date Created: 9/14/2026
Last Update: 10/6/2026
Version: 1.2.0

Scope: Shared paths, location settings and Open-Meteo helpers for every weather script.
    Anything that can go stale (dates, location) is read through a function, never stored at import time.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import openmeteo_requests
import requests_cache
from retry_requests import retry

# ===== PATHS =====
# In the .exe, user files live next to the executable. PyInstaller's unpack folder is deleted on exit, so anything
# written there (config, CSVs, charts) would vanish. From source, config.json is in Config/ and Data/ is in the root.
if getattr(sys, "frozen", False):
    CONFIG_PATH = Path(sys.executable).parent / "config.json"
    DATA_DIR = Path(sys.executable).parent / "Data"
else:
    CONFIG_PATH = Path(__file__).parent / "config.json"
    DATA_DIR = Path(__file__).parent.parent / "Data"

# Read-only, so it can stay bundled. Add it in auto-py-to-exe as: Config/descriptions.json -> Config
DESCRIPTIONS_PATH = Path(__file__).parent / "descriptions.json"


# ===== LOCATION =====
# Used when config.json is missing or corrupt, and to fill keys an older config.json lacks
DEFAULT_LOCATION = {
    "location_name": "Hickory, NC",
    "latitude": 35.7411,
    "longitude": -81.3895,
    "elevation": None,  # Metres. None lets Meteostat estimate it; geocoding results fill it in.
    "timezone": "America/New_York",
}


def save_location(location: dict) -> None:
    """Saves a location to config.json via a temp file, so a crash mid-write can't corrupt it.

    Args:
        location: Dict with location_name, latitude, longitude, elevation and timezone keys.
    """
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = CONFIG_PATH.with_suffix(".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(location, f, indent=4)
    tmp_path.replace(CONFIG_PATH)


def load_location() -> dict:
    """Loads the saved location, recreating config.json from the default if it's missing or corrupt.

    Returns:
        Location dict. Keys missing from the file are filled from DEFAULT_LOCATION.
    """
    try:
        with CONFIG_PATH.open(encoding="utf-8") as f:
            saved = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        save_location(DEFAULT_LOCATION)
        return DEFAULT_LOCATION.copy()
    return {**DEFAULT_LOCATION, **saved}


def get_timezone() -> ZoneInfo:
    """Returns the saved location's timezone."""
    return ZoneInfo(load_location()["timezone"])


# ===== DATE FORMATTING =====
DATE_FORMAT = "%m-%d-%Y"  # 12-25-2026
DATETIME_FORMAT = "%Y-%m-%d %H:%M"  # 2026-12-25 23:59


# ===== OPEN-METEO =====
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
_openmeteo_client = None


def get_openmeteo_client() -> openmeteo_requests.Client:
    """Returns the shared Open-Meteo client, creating it on first use.

    Responses are cached for an hour in Data/ and failed requests are retried up to 5 times. The cache path is
    absolute so it doesn't depend on which folder the script or .exe was launched from.
    """
    global _openmeteo_client
    if _openmeteo_client is None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        cache_session = requests_cache.CachedSession(str(DATA_DIR / ".cache"), expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        _openmeteo_client = openmeteo_requests.Client(session=retry_session)
    return _openmeteo_client


def get_daily_params() -> dict:
    """Builds request params for the 7-day daily forecast at the saved location.

    The "daily" list order sets the Variables(n) indexes in Daily.py. Change one, change the other.
    """
    location = load_location()
    return {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "daily": [
            "temperature_2m_max",  # 0
            "temperature_2m_min",  # 1
            "weather_code",  # 2
            "precipitation_probability_mean",  # 3
            "sunrise",  # 4
            "sunset",  # 5
        ],
        "models": "best_match",
        "timezone": location["timezone"],
        "forecast_days": 7,
        "wind_speed_unit": "mph",
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
    }


def get_hourly_params() -> dict:
    """Builds request params for today's hourly forecast at the saved location.

    "Today" is taken in the location's timezone, not the computer's. The "hourly" and "daily" list orders set the
    Variables(n) indexes in Hourly.py.
    """
    location = load_location()
    today = datetime.now(tz=ZoneInfo(location["timezone"])).strftime("%Y-%m-%d")
    return {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "hourly": [
            "temperature_2m",  # 0
            "apparent_temperature",  # 1
            "precipitation_probability",  # 2
            "weather_code",  # 3
        ],
        "daily": ["sunrise", "sunset"],  # 0, 1
        "models": "best_match",
        "timezone": location["timezone"],
        "wind_speed_unit": "mph",
        "temperature_unit": "fahrenheit",
        "start_date": today,
        "end_date": today,
    }


# ===== WEATHER CODE DESCRIPTIONS =====
def load_descriptions() -> dict:
    """Loads WMO weather code descriptions, keyed by code as a string, each with "day" and "night" entries."""
    with DESCRIPTIONS_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def get_period(timestamp: datetime, sunrise: datetime, sunset: datetime) -> str:
    """Returns "day" if the timestamp is between sunrise and sunset (inclusive), otherwise "night".

    All three must be timezone-aware, or the comparison raises a TypeError.
    """
    if sunrise <= timestamp <= sunset:
        return "day"
    return "night"


def get_weather_description(code: float, ww_data: dict, period: str = "day") -> str:
    """Translates a WMO weather code into a description, e.g. 0 -> "Sunny" (day) or "Clear" (night).

    Args:
        code: WMO code. Open-Meteo returns floats, so it's converted to int for the lookup.
        ww_data: Descriptions from load_descriptions().
        period: "day" or "night".

    Returns:
        The description, or "Unknown" if the code isn't in descriptions.json.
    """
    entry = ww_data.get(str(int(code)))
    if entry is None:
        return "Unknown"
    return entry[period]["description"]
