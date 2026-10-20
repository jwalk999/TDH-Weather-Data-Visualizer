"""
File Name: Forecasts.py

Author: Jonathan W
Date Created: 10/15/2026
Last Update: 10/20/2026
Version: 1.1.0

Scope: Fetches the daily forecast, today's hourly forecast and (optionally) current conditions in a single
    Open-Meteo request. get_forecast() keeps its old 7-day behaviour for the graph scripts; the window uses
    get_forecast_and_current() for 10 days plus the current-conditions stat row.
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
# Current conditions. Same order rule: it sets the Variables(n) index.
CURRENT_VARS = {
    "temperature_2m": "Temperature",
    "apparent_temperature": "Feels Like",
    "relative_humidity_2m": "Humidity",
    "wind_speed_10m": "Wind Speed",
    "wind_direction_10m": "Wind Direction",
    "uv_index": "UV Index",
    "weather_code": "Weather Code",
    "is_day": "Is Day",
}
# Sunrise/sunset come back as int64 Unix timestamps, which need ValuesInt64AsNumpy() instead of ValuesAsNumpy()
TIMESTAMP_VARS = {"sunrise", "sunset"}
MAX_FORECAST_DAYS = 16  # Open-Meteo's limit for forecast_days


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


def _request(location: dict, days: int, with_current: bool):
    """Sends one forecast request in Imperial units.

    Args:
        location: Dict with latitude, longitude and timezone keys.
        days: Number of daily forecast days, capped at MAX_FORECAST_DAYS.
        with_current: Also ask for current conditions.

    Returns:
        The first Open-Meteo response object.
    """
    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "daily": list(DAILY_VARS),
        "hourly": list(HOURLY_VARS),
        "models": "best_match",
        "timezone": location["timezone"],
        "forecast_days": min(days, MAX_FORECAST_DAYS),
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
        "wind_speed_unit": "mph",
    }
    if with_current:
        params["current"] = list(CURRENT_VARS)
    return get_openmeteo_client().weather_api(FORECAST_URL, params=params)[0]


def _split_frames(response, tz: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Builds the daily frame and today's hourly frame from a response.

    Args:
        response: An Open-Meteo response from _request().
        tz: IANA timezone name.

    Returns:
        The (daily_df, hourly_df) pair. hourly_df covers only today and repeats today's sunrise and sunset in
        every row, so the hourly chart can mark them.
    """
    daily_df = _block_to_frame(response.Daily(), DAILY_VARS, tz)
    hourly_df = _block_to_frame(response.Hourly(), HOURLY_VARS, tz)

    # Hourly comes back for every forecast day; the hourly chart and page only show today
    today = daily_df["Date"].iloc[0].date()
    hourly_df = hourly_df[hourly_df["Date"].dt.date == today].reset_index(drop=True)
    hourly_df["Sunrise"] = daily_df["Sunrise"].iloc[0]
    hourly_df["Sunset"] = daily_df["Sunset"].iloc[0]
    return daily_df, hourly_df


def get_forecast(location: dict | None = None, days: int = 7) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Fetches the daily forecast and today's hourly forecast in one request, in Imperial units.

    Args:
        location: Dict with latitude, longitude and timezone keys. Defaults to the saved location in config.json.
        days: Number of daily forecast days. Defaults to 7.

    Returns:
        The (daily_df, hourly_df) pair. Temperatures are in °F and precipitation in inches. hourly_df covers only
        today in the location's timezone (23 or 25 rows on DST days).
    """
    if location is None:
        location = load_location()
    response = _request(location, days, with_current=False)
    return _split_frames(response, location["timezone"])


def get_forecast_and_current(
    location: dict | None = None, days: int = 10
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, float]]:
    """Fetches the daily forecast, today's hourly forecast and current conditions in one request.

    Args:
        location: Dict with latitude, longitude and timezone keys. Defaults to the saved location in config.json.
        days: Number of daily forecast days. Defaults to 10.

    Returns:
        ``(daily_df, hourly_df, current)``. ``current`` maps the CURRENT_VARS column names to floats: °F, %, mph,
        degrees, UV index, WMO code, and Is Day (1.0 or 0.0).
    """
    if location is None:
        location = load_location()
    response = _request(location, days, with_current=True)
    daily_df, hourly_df = _split_frames(response, location["timezone"])

    block = response.Current()
    current = {column: float(block.Variables(i).Value()) for i, column in enumerate(CURRENT_VARS.values())}
    return daily_df, hourly_df, current


def get_current_temp(location: dict) -> float:
    """Fetches just the current temperature for a location, for the Locations page.

    Responses go through the shared hour-long cache, so reopening the page doesn't hit the API again.

    Args:
        location: Dict with latitude, longitude and timezone keys.

    Returns:
        The current temperature in °F.
    """
    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "current": ["temperature_2m", "weather_code", "is_day"],
        "timezone": location["timezone"],
        "temperature_unit": "fahrenheit",
    }
    response = get_openmeteo_client().weather_api(FORECAST_URL, params=params)[0]
    return float(response.Current().Variables(0).Value())


if __name__ == "__main__":
    daily, hourly, now = get_forecast_and_current()
    print(daily)
    print(hourly)
    print(now)
