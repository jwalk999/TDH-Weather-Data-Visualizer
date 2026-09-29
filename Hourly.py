"""
File Name: Hourly.py

Author: Jonathan W
Date: 9/15/2026
Version: 0.5.0

Scope:
    Collects the hourly weather forecast for the next 7 days
    and records temperature, apparent temperature,
    precipitation probability, and weather conditions.
"""


# ===== IMPORTS =====

# Add the project's parent directory to Python's import search path.
# This allows this file to import modules from the Config package.
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd

from Config.global_params import (
    get_hourly_params,
    get_period,
    get_weather_description,
    load_descriptions,
)


# Create a runnable function to collect weather data.
def get_hourly_forecast():
    """
    Make an API call to Openmeteo_Requests to collect hourly forecast data from it.

    Params: url == the open-meteo api url
            cache_session / retry_session: retry the requests if it fails
            responses_hourly: the data that comes back from Openmeteo
            hourly_%parameter%: define the data that comes back
            daily_sunrise(set): Define what sunrise and sunset is and format the dates
            hourly_dataframe: export the data into a Pandas dataframe for displaying to user
            ww_data: convert numeric WMO weather code into condition(sunny, cloudy, etc)
    
    Returns: Collect all of the data [temperature(high)(low)], precip%, WMO weather code
                then spit it out into a csv format file and automatically save it to /Data/ folder
                for the GUI to read
    """

    # ===== API PARAMETERS =====

    # Open-Meteo forecast API endpoint.
    url = "https://api.open-meteo.com/v1/forecast"

    # Load the hourly forecast parameters from global_params.py.
    params_hourly = get_hourly_params()


    # ===== COLLECT WEATHER DATA =====

    # The parameters that allow for data collection from API
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    # Retry the request if it times out // max 5 times // wait 0.2 seconds before next try
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    # Make the API call
    OPENMETEO_CLIENT = openmeteo_requests.Client(session=retry_session)

    # Send the request to Open-Meteo using the configured parameters.
    responses_hourly = OPENMETEO_CLIENT.weather_api(url, params_hourly)

    # The API may return multiple responses. This project uses the first response.
    response_hourly = responses_hourly[0]


    # ===== PROCESS HOURLY DATA =====

    # Access the hourly weather data returned by the API.
    hourly = response_hourly.Hourly()

    # Extract hourly temperature, apparent temperature,
    # precipitation probability, and WMO weather code.
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(3).ValuesAsNumpy()


    # ===== PROCESS SUNRISE AND SUNSET DATA =====

    # Sunrise and sunset are provided as part of the daily forecast data.
    daily = response_hourly.Daily()

    sunrise_unix = daily.Variables(0).ValuesInt64AsNumpy()
    sunset_unix = daily.Variables(1).ValuesInt64AsNumpy()

    # Convert Unix timestamps to the forecast location's local timezone.
    # The first day's sunrise and sunset are used when determining
    # whether an hourly timestamp falls within the day or night period.
    sunrise = pd.to_datetime(
        sunrise_unix,
        unit="s",
        utc=True,
    ).tz_convert(
        response_hourly.Timezone().decode()
    )[0]

    sunset = pd.to_datetime(
        sunset_unix,
        unit="s",
        utc=True,
    ).tz_convert(
        response_hourly.Timezone().decode()
    )[0]


    # ===== CREATE HOURLY DATASET =====

    # Create a date/time range using the start time, end time,
    # and interval supplied by the Open-Meteo response.
    hourly_data = {
        "Date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        ).tz_convert(response_hourly.Timezone().decode())
    }

    # Add the collected weather data to the dataset.
    hourly_data["Temperature"] = hourly_temperature_2m
    hourly_data["Feels Like"] = hourly_apparent_temperature
    hourly_data["Chance of Precipitation"] = hourly_precipitation_probability

    # Convert the collected data into a pandas DataFrame
    # for easier processing and formatting.
    hourly_dataframe = pd.DataFrame(data=hourly_data)

    # Load the WMO weather-code descriptions from descriptions.json.
    ww_data = load_descriptions()

    # Match each WMO weather code with its appropriate description.
    # The period (day/night) is determined using the sunrise and sunset times.
    hourly_dataframe["Weather Description"] = [
        get_weather_description(
            code,
            ww_data,
            period=get_period(ts, sunrise, sunset),
        )
        for code, ts in zip(
            hourly_weather_code,
            hourly_dataframe["Date"],
        )
    ]

    # ===== EXPORT HOURLY FORECAST =====

    # Export the DataFrame as a CSV file.
    # index=False prevents pandas from adding an unnecessary row-number column.
    hourly_dataframe.to_csv(
        "Data/hourly_forecast.csv",
        index=False,
        encoding="utf-8",
    )

    # Collect the same DataFrame so that it can be used in a GUI
    return hourly_dataframe

# Make this file runnable by itself for testing
if __name__ == "__main__":
    get_hourly_forecast()