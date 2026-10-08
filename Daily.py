"""
File Name: Daily.py

Author: Jonathan W
Date Created: 9/15/2026
Last Update: 10/6/2026
Version: 1.2.0

Scope: Fetches the 7-day daily forecast and saves it to Data/daily_forecast.csv for the graphs and GUI.
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
    get_daily_params,
    get_openmeteo_client,
    get_weather_description,
    load_descriptions,
)


def _to_local(unix_times, tz: str) -> pd.DatetimeIndex:
    """Converts Unix timestamps (seconds) to timezone-aware local times."""
    return pd.to_datetime(unix_times, unit="s", utc=True).tz_convert(tz)


def get_daily_forecast() -> pd.DataFrame:
    """Fetches the 7-day forecast for the saved location and writes it to Data/daily_forecast.csv.

    The CSV ends with a "# Last Updated: ..." line. Read it back with pd.read_csv(path, comment="#") so that line
    is skipped instead of becoming a junk row.

    Returns:
        One row per day: Date, Temperature High, Temperature Low, Chance of Precipitation, Weather Description,
        Sunrise, Sunset. All times are in the location's timezone.
    """
    response = get_openmeteo_client().weather_api(FORECAST_URL, params=get_daily_params())[0]
    tz = response.Timezone().decode()
    daily = response.Daily()

    # Indexes must match the "daily" list order in get_daily_params()
    daily_df = pd.DataFrame({
        "Date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left",
        ).tz_convert(tz),
        "Temperature High": daily.Variables(0).ValuesAsNumpy(),
        "Temperature Low": daily.Variables(1).ValuesAsNumpy(),
        "Chance of Precipitation": daily.Variables(3).ValuesAsNumpy(),
    })

    # A daily code describes the whole day, so always use the daytime wording ("Sunny", not "Clear").
    ww_data = load_descriptions()
    daily_df["Weather Description"] = [
        get_weather_description(code, ww_data, period="day") for code in daily.Variables(2).ValuesAsNumpy()
    ]
    daily_df["Sunrise"] = _to_local(daily.Variables(4).ValuesInt64AsNumpy(), tz)
    daily_df["Sunset"] = _to_local(daily.Variables(5).ValuesInt64AsNumpy(), tz)

    output_path = DATA_DIR / "daily_forecast.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    daily_df.to_csv(output_path, index=False, encoding="utf-8")
    with output_path.open("a", encoding="utf-8") as f:
        f.write(f"# Last Updated: {datetime.now().strftime(DATETIME_FORMAT)}\n")

    return daily_df


if __name__ == "__main__":
    daily_df = get_daily_forecast()
    #print(get_daily_forecast())
