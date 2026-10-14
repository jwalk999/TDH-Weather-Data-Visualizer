"""
File Name: Hourly.py

Author: Jonathan W
Date Created: 9/15/2026
Last Update: 10/6/2026
Version: 1.2.0

Scope: Fetches today's hourly forecast and saves it to Data/hourly_forecast.csv for the graphs and GUI.
"""

import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

# Make the Config package importable when this file is run on its own. Skipped in the .exe, where it's bundled.
if not getattr(sys, "frozen", False):
    _root = next((p for p in Path(__file__).resolve().parents if (p / "Config").is_dir()), None)
    if _root is None:
        raise RuntimeError("Could not find the project root (no 'Config' folder above this file)")
    sys.path.append(str(_root))

from Config.global_params import (  # noqa: E402 - must come after the sys.path setup above
    DATA_DIR,
    DATETIME_FORMAT,
    FORECAST_URL,
    get_hourly_params,
    get_openmeteo_client,
    get_period,
    get_weather_description,
    load_descriptions,
)


def _to_local(unix_times, tz: str) -> pd.DatetimeIndex:
    """Converts Unix timestamps (seconds) to timezone-aware local times."""
    return pd.to_datetime(unix_times, unit="s", utc=True).tz_convert(tz)


def get_hourly_forecast() -> pd.DataFrame:
    """Fetches today's hourly forecast for the saved location and writes it to Data/hourly_forecast.csv.

    The CSV ends with a "# Last Updated: ..." line. Read it back with pd.read_csv(path, comment="#") so that line
    is skipped instead of becoming a junk row.

    Returns:
        One row per hour: Date, Temperature, Feels Like, Chance of Precipitation, Weather Description, Sunrise,
        Sunset. Sunrise and Sunset repeat on every row so the graph can read them from the same DataFrame. All times
        are in the location's timezone.
    """
    response = get_openmeteo_client().weather_api(FORECAST_URL, params=get_hourly_params())[0]
    tz = response.Timezone().decode()
    hourly = response.Hourly()
    daily = response.Daily()

    # Indexes must match the "hourly" and "daily" list orders in get_hourly_params()
    hourly_df = pd.DataFrame({
        "Date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        ).tz_convert(tz),
        "Temperature": hourly.Variables(0).ValuesAsNumpy(),
        "Feels Like": hourly.Variables(1).ValuesAsNumpy(),
        "Chance of Precipitation": hourly.Variables(2).ValuesAsNumpy(),
    })

    # Only today is requested, so the first (only) sunrise/sunset applies to every hour
    sunrise = _to_local(daily.Variables(0).ValuesInt64AsNumpy(), tz)[0]
    sunset = _to_local(daily.Variables(1).ValuesInt64AsNumpy(), tz)[0]

    ww_data = load_descriptions()
    hourly_df["Weather Description"] = [
        get_weather_description(code, ww_data, period=get_period(ts, sunrise, sunset))
        for code, ts in zip(hourly.Variables(3).ValuesAsNumpy(), hourly_df["Date"])
    ]
    hourly_df["Sunrise"] = sunrise
    hourly_df["Sunset"] = sunset

    output_path = DATA_DIR / "hourly_forecast.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    hourly_df.to_csv(output_path, index=False, encoding="utf-8")
    with output_path.open("a", encoding="utf-8") as f:
        f.write(f"# Last Updated: {datetime.now().strftime(DATETIME_FORMAT)}\n")

    return hourly_df


if __name__ == "__main__":
    hourly_df = get_hourly_forecast()
    #print(get_hourly_forecast())
