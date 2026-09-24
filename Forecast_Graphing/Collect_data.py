"""
File Name: Collect_data.py
Author: Jonathan W.
Date: 9/24/2026
Version: 0.5.0
Scope: Collect daily and hourly data for use in graphing
"""

# ===== IMPORT CODE LIBS =====
import sys
from pathlib import Path

import pandas as pd

# make sure file can reference correct file in a different folder
sys.path.append(str(Path(__file__).parent.parent))
# collect parameters from global_params.py
from Config.global_params import (
    OPENMETEO_CLIENT,
    get_daily_params,
    load_descriptions,
)

# direct collection to the api that has the data
url = "https://api.open-meteo.com/v1/forecast"


# ===== COLLECT AND STORE DAILY DATA =====


def main_daily():
    # PARAMETERS AND VARIABLES
    # get parameters from global_params
    params_daily = get_daily_params()
    # set location, weather data types, # of days to forecast, and measurements

    # PROCESS COLLECTED DATA
    # set variables for collected data
    daily = response_daily.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
    daily_weather_code = daily.Variables(2).ValuesAsNumpy()
    daily_precipitation_probability_mean = daily.Variables(3).ValuesAsNumpy()

    # the information collected from global_params.py is written like a library
    # this tells the variables to reference that library
    # allows for data to be callable

    # define the time range for daily data
    daily_data = {
        "Date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left",
        )
    }

    # assign headers for output file using data from set variables
    daily_data["Temperature High"] = daily_temperature_2m_max
    daily_data["Temperature Low"] = daily_temperature_2m_min
    daily_data["WMO Weather Code"] = daily_weather_code
    daily_data["Chance of Precipitation"] = daily_precipitation_probability_mean

    # get descriptions for WMO weather codes from descriptions.json
    def get_weather_description(code, ww_data, period="day"):
        entry = ww_data.get(str(code))
        if entry is None:
            return "Unknown"
        return entry[period]["description"]

    # format caolumns in output file
    daily_dataframe = pd.DataFrame(data=daily_data)
    daily_dataframe["Temperature High"] = daily_dataframe["Temperature High"].map(
        lambda x: f"{x:.0f}°F"
    )
    daily_dataframe["Temperature Low"] = daily_dataframe["Temperature Low"].map(
        lambda x: f"{x:.0f}°F"
    )
    daily_dataframe["Chance of Precipitation"] = daily_dataframe[
        "Chance of Precipitation"
    ].map(lambda x: f"{x:.0f}%")
    # make the dates look cleaner
    daily_data["Date"] = daily_data["Date"].strftime("%Y-%m-%d")

    # print data to text file
    # this function takes all the data, writes it to daily_forecast.txt, then closes it
    # file is saved at directory (%MAIN% / Data / daily_forecast.txt)
    with open("Data/daily_forecast.txt", "w+", encoding="utf-8") as f:
        f.write(
            f"Coordinates: {response_daily.Latitude()}°N , {response_daily.Longitude()}°E"
        )
        f.write(f"\nElevation: {response_daily.Elevation()}m above sea level")
        f.write(f"\nTimezone: {response_daily.Timezone()}")
        f.write("\n~~~Daily Forecast~~~\n")
        f.write(daily_dataframe.to_string())


if __name__ == "__main_daily__":
    main_daily()


# ===== COLLECT AND STORE HOURLY DATA =====


def main_hourly():
    # PARAMETERS AND VARIABLES
    # get parameters from global_params.py
    params_hourly = get_hourly_params()

    # COLLECT DATA FROM API
    # direct open meteo to collect responses from the url using set params
    responses_hourly = OPENMETEO_CLIENT.weather_api(url, params_hourly)
    responses_hourly = responses_hourly(0)

    # PROCESS DATA
    hourly = response_hourly.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Vairables(1).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(3).ValuesAsNumpy()
    # variables point to Current air temperature, "feels like" temperature,
    # chance of precipitaiton, and the weather description (sunny, cloudy, etc.)

    # grab sunrise and sunset from daily data to direct proper weather description
    sunrise = pd.to_datetime(sunrise_unix, unit="s", utc=True).tz_convert(
        responses_hourly.Timezone().decode()
    )[0]
    sunset = pd.to_datetime(sunset_unix, unit="s", utc=True).tz_convert(
        responses_hourly.Timezone().decode()
    )[0]
    # weather codes are time specific
    # example: it cannot be "sunny" at night time, so it is changed to "clear"

    # define time range for hourly data
    hourly_data = {
        "Date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        ).tz_convert(responses_hourly.Timezone().decode())
    }

    # assign headers for output file using data from set variables
    hourly_data["Temperature"] = hourly_temperature_2m
    hourly_data["Feels Like"] = hourly_apparent_temperature
    hourl_data["Chance of Precipitation"] = hourly_precipitation_probability

    # set and retrieve weather descriptions
    hourly_dataframe = pd.DataFrame(data=hourly_data)
    # get descriptions for WMO weather codes from descriptions.json
    ww_data = load_descriptions()
    hourly_dataframe["Weather Description"] = [
        get_weather_description(code, ww_data, period=get_period(ts, sunrise, sunset))
        for code, ts in zip(
            hourly_weather_code,
            hourly_dataframe["Date"],
        )
    ]

    # format columns with its correct unit
    hourly_dataframe["Temperature"] = hourly_dataframe["Temperature"].map(
        lambda x: f"{x:.0f}°F"
    )
    hourly_dataframe["Feels Like"] = hourly_dataframe["Feels Like"].map(
        lambda x: f"{x:.0f}°F"
    )
    hourly_dataframe["Chance of Precipitation"] = hourly_dataframe[
        "Chance of Precipitation"
    ].map(lambda x: f"{x:.0f}%")
    hourly_dataframe["Date"] = hourly_dataframe["Date"].dt.strftime("%Y-%m-%d %H:%M")

    # print data to text file
    # this function takes all the data, writes it to hourly_forecast.txt, then closes it
    # file is saved at directory (%MAIN% / Data / hourly_forecast.txt)
    with open("Data/hourly_forecast.txt", "w+", encoding="utf-8") as f:
        f.write(
            f"Coordinates: {responses_hourly.Latitude()}°N , {response_hourly.Longitude()}°E"
        )
        f.write(f"\nElevation: {response_hourly.Elevation()}m above sea level")
        f.write(f"\nTimezone: {response_hourly.Timezone()}")
        f.write("\n~~~Hourly Forecast~~~\n")
        f.write(hourly_dataframe.to_string())


if __name__ == "__main_hourly__":
    main_hourly()
