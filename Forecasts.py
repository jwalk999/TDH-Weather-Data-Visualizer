"""
File Name: Forecasts.py

Author: Jonathan W
Date Created: 10/15/2026
Last Update: 10/15/2026
Version: 1.0.0

Scope: Fetches the 7-day daily forecast and today's hourly forecast in a single Open-Meteo request.
    Replaces Daily.py and Hourly.py.
"""

import pandas as pd

from Config.global_params import FORECAST_URL, get_openmeteo_client, load_location

# API variable name -> DataFrame column name. Order matters: it sets the Variables(n) index for each column.
DAILY_VARS = {
    "temperature_2m_max": "Temperature High",
    "temperature_2m_min": "Temperature Low",
    "weather_code": "Weather Code",
    "precipitation_probability_mean": "Chance of Precipitation",
    "precipitation_sum": "Precipitation",
    "sunrise": "Sunrise",
    "sunset": "Sunset",
}
HOURLY_VARS = {
    "temperature_2m": "Temperature",
    "apparent_temperature": "Feels Like",
    "precipitation_probability": "Chance of Precipitation",
    "weather_code": "Weather Code",
}
# Sunrise/sunset come back as int64 Unix timestamps, which need ValuesInt64AsNumpy() instead of ValuesAsNumpy()
TIMESTAMP_VARS = {"sunrise", "sunset"}


def _block_to_frame(block, var_map: dict[str, str], tz: str) -> pd.DataFrame:
    """Converts an Open-Meteo daily or hourly block into a DataFrame.

    Args:
        block: The response's Daily() or Hourly() object.
        var_map: API variable names mapped to column names, in the order they were requested.
        tz: IANA timezone name, e.g. "America/New_York".

    Returns:
        A "Date" column of local timestamps followed by one column per variable. Sunrise and sunset are converted
        to timezone-aware timestamps.
    """
    dates = pd.date_range(
        start=pd.to_datetime(block.Time(), unit="s", utc=True),
        end=pd.to_datetime(block.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=block.Interval()),
        inclusive="left",
    ).tz_convert(tz)

    df = pd.DataFrame({"Date": dates})
    for i, (api_name, column) in enumerate(var_map.items()):
        variable = block.Variables(i)
        if api_name in TIMESTAMP_VARS:
            df[column] = pd.to_datetime(variable.ValuesInt64AsNumpy(), unit="s", utc=True).tz_convert(tz)
        else:
            df[column] = variable.ValuesAsNumpy()
    return df


def get_forecast(location: dict | None = None, days: int = 7) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Fetches the daily forecast and today's hourly forecast in one request, in Imperial units.

    Args:
        location: Dict with latitude, longitude and timezone keys. Defaults to the saved location in config.json.
        days: Number of daily forecast days. Defaults to 7.

    Returns:
        The (daily_df, hourly_df) pair. Temperatures are in °F and precipitation in inches. hourly_df covers only
        today in the location's timezone (23 or 25 rows on DST days) and repeats today's sunrise and sunset in
        every row, so the hourly chart can mark them.
    """
    if location is None:
        location = load_location()
    tz = location["timezone"]

    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "daily": list(DAILY_VARS),
        "hourly": list(HOURLY_VARS),
        "models": "best_match",
        "timezone": tz,
        "forecast_days": days,
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
    }
    response = get_openmeteo_client().weather_api(FORECAST_URL, params=params)[0]
    daily_df = _block_to_frame(response.Daily(), DAILY_VARS, tz)
    hourly_df = _block_to_frame(response.Hourly(), HOURLY_VARS, tz)

    # Hourly comes back for every forecast day; the hourly chart only shows today
    today = daily_df["Date"].iloc[0].date()
    hourly_df = hourly_df[hourly_df["Date"].dt.date == today].reset_index(drop=True)
    hourly_df["Sunrise"] = daily_df["Sunrise"].iloc[0]
    hourly_df["Sunset"] = daily_df["Sunset"].iloc[0]

    return daily_df, hourly_df


if __name__ == "__main__":
    daily, hourly = get_forecast()
    print(daily)
    print(hourly)
