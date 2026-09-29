"""
File Name: Daily.py

Author: Jonathan W
Date: 9/15/2026
Version: 0.5.0

Scope: 
        - Collects the daily weather forecast for the next 7 days
        - prepares the data for graphing.
"""


#===== IMPORTS =====
# Add the project's parent directory to Python's import search path
# This allows the file to import modules from the Config package
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
from matplotlib import pyplot

from Config.global_params import(
    get_daily_params,
    load_descriptions,
    get_weather_description,
    get_period,
)


# Create a runnable function to collect weather data.
def get_daily_forecast():
    """
    Make an API call to Openmeteo_Requests to collect daily forecast data from it.

    Params: url == the open-meteo api url
            cache_session / retry_session: retry the requests if it fails
            responses_daily: the data that comes back from Openmeteo
            daily_%parameter% AND sunrise(set)_unix: define the data that comes back
            Define what sunrise and sunset is and format the dates
            daily_dataframe: export the data into a Pandas dataframe for displaying to user
            ww_data: convert numeric WMO weather code into condition(sunny, cloudy, etc)
    
    Returns: Collect all of the data [temperature(high)(low)], precip%, WMO weather code
                then spit it out into a csv format file and automatically save it to /Data/ folder
                for the GUI to read
    """
    # ===== API PARAMETERS =====
    # Open-Meteo forecast API endpoint
    url = "https://api.open-meteo.com/v1/forecast"

    # Load the daily forcast parameters from global_params.py
    params_daily = get_daily_params()



    # ===== COLLECT WEATHER DATA =====
    # The parameters that allow for data collection from API
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    # Retry the request if it times out // max 5 times // wait 0.2 seconds before next try
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    # Make the API call
    OPENMETEO_CLIENT = openmeteo_requests.Client(session=retry_session)

    # Send the request to Open-Meteo using the configured parameters
    responses_daily = OPENMETEO_CLIENT.weather_api(url, params_daily)

    # The API may return multiple responses, we will use only the first response
    response_daily = responses_daily[0]


    # ===== PROCESS WEATHER DATA =====

    # Access the daily weather data returned by the API
    daily = response_daily.Daily()

    # Extract the daily high and low temperatures
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()

    # Extract the WMO weather code and precipitation probability
    daily_weather_code = daily.Variables(2).ValuesAsNumpy()
    daily_precipitation_probability_mean = daily.Variables(3).ValuesAsNumpy()

    # Extract sunrise and sunset times as Unix timestamps
    sunrise_unix = daily.Variables(4).ValuesInt64AsNumpy()
    sunset_unix = daily.Variables(5).ValuesInt64AsNumpy()

    # Convert sunrise and sunset timestamps to the forecast location's
    # local timezone. Only the first day's sunrise and sunset are needed
    # for determining the day/night period.
    sunrise = pd.to_datetime(
        sunrise_unix,
        unit="s",
        utc=True
    ).tz_convert(
        response_daily.Timezone().decode()
    )[0]


    sunset = pd.to_datetime(
        sunset_unix,
        unit="s",
        utc=True,
    ).tz_convert(
        response_daily.Timezone().decode()
    )[0]


    # ===== CREATE DAILY DATASET =====

    # Create a date/time range using the start time, end time, and interval
    # supplied by the Open-Meteo response.
    daily_data = {
        "Date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left",
        ).tz_convert(response_daily.Timezone().decode())
    }

    # Add the weather data to the dataset.
    daily_data["Temperature High"] = daily_temperature_2m_max
    daily_data["Temperature Low"] = daily_temperature_2m_min
    daily_data["Chance of Precipitation"] = daily_precipitation_probability_mean

    # Convert the collected data into a pandas DataFrame for 
    # easier processing and formatting.
    daily_dataframe = pd.DataFrame(data=daily_data)

    # Load the WMO weather-code descriptions from descriptions.json
    ww_data = load_descriptions()

    # Match each WMO weather-code description with its appropriate description.
    # The period (day/night) is determined using the sunrise and sunset times.
    daily_dataframe["Weather Description"] = [
        get_weather_description(
            code, ww_data,
            period=get_period(ts, sunrise, sunset),
        )
        for code, ts in zip(
            daily_weather_code,
            daily_dataframe["Date"],
        )
    ]

    # ===== EXPORT DAILY FORECAST =====

    # Export the DataFrame as a CSV file.
    # index=False prevents pandas from adding an unnecessary row-number column.
    daily_dataframe.to_csv(
        "Data/daily_forecast.csv",
        index=False,
        encoding="utf-8",
    )

    # Collect the same DataFrame so that it can be used in a GUI
    return daily_dataframe

# Make this file runnable by itself for testing
if __name__ == "__main__":
    get_daily_forecast()