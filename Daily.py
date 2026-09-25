"""
File Name: Daily_Graph.py
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
    OPENMETEO_CLIENT,
    get_daily_params,
    load_descriptions,
    get_weather_description,
    get_period,
)


# ===== API PARAMETERS =====
# Open-Meteo forecast API endpoint
url = "https://api.open-meteo.com/v1/forecast"

# Load the daily forcast parameters from global_params.py
params_daily = get_daily_params()



# ===== COLLECT WEATHER DATA =====

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


# ===== FORMAT OUTPUT DATA =====

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

# Format temperatures as whole numbers with Fahrenheit units.
daily_dataframe["Temperature High"] = daily_dataframe[
    "Temperature High"
].map(lambda x: f"{x:.0f}°F")

daily_dataframe["Temperature Low"] = daily_dataframe[
    "Temperature Low"
].map(lambda x: f"{x:.0f}°F")

# Format precipitation probability as a whole-number percentage.
daily_dataframe["Chance of Precipitation"] = daily_dataframe[
    "Chance of Precipitation"
].map(lambda x: f"{x:.0f}%")

# Format dates as YYYY-MM-DD for easier reading in the output file.
daily_dataframe["Date"] = daily_dataframe["Date"].dt.strftime("%Y-%m-%d")


# ===== EXPORT DAILY FORECAST =====

# Export the formatted DataFrame as a CSV file.
# index=False prevents pandas from adding an unnecessary row-number column.
daily_dataframe.to_csv(
    "Data/daily_forecast.csv",
    index=False,
    encoding="utf-8",
)

