'''
File Name: Hourly.py
Author: Jonathan W
Date: 9/15/2026
Version: 0.4.0
Scope: Collects hourly forecast for the next 7 days
        - logs temperature highs and lows, precipitation probability, and weather type
        - settings found in global_param.py
'''


import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
import sys
from pathlib import Path
# tell python to search entire folder structure for imports
sys.path.append(str(Path(__file__).parent.parent))
# import data from global params as needed for openmeteo
from Config.global_params import (
    get_hourly_params, 
    OPENMETEO_CLIENT, 
    load_descriptions, 
    get_period, 
    get_weather_description
)

#===== COLLECT PARAMETERS =====
url = 'https://api.open-meteo.com/v1/forecast'  # tells api where to get the weather data from
params_hourly = get_hourly_params() # tells api what to get from url, referencing script built in global_params.py

#===== COLLECT DATA FROM API =====

# direct open meteo to collect responses from the url using set parameters
responses_hourly = OPENMETEO_CLIENT.weather_api(url, params_hourly)
response_hourly = responses_hourly[0]



#===== PROCESS DATA =====

# process hourly data
hourly = response_hourly.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()
hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()
hourly_weather_code = hourly.Variables(3).ValuesAsNumpy()

# process daily data for sunrise and sunset variables
daily = response_hourly.Daily()
sunrise_unix = daily.Variables(0).ValuesInt64AsNumpy()
sunset_unix = daily.Variables(1).ValuesInt64AsNumpy()

# convert unix timestamps to readable format using correct timezone
sunrise = pd.to_datetime(sunrise_unix, unit = 's', utc=True).tz_convert(response_hourly.Timezone().decode())[0]
sunset = pd.to_datetime(sunset_unix, unit = 's', utc=True).tz_convert(response_hourly.Timezone().decode())[0]

# define time range for hourly data
hourly_data = {
    'Date': pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = 's', utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = 's', utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = 'left'
    ).tz_convert(response_hourly.Timezone().decode())
}

# set headers for output file using data from above variables
hourly_data['Temperature'] = hourly_temperature_2m
hourly_data['Feels Like'] = hourly_apparent_temperature
hourly_data['Chance of Precipitation'] = hourly_precipitation_probability

# set time frame as variable to check against when getting weather description
hourly_dataframe = pd.DataFrame(data = hourly_data)

# retrieve descriptions for WMO weather codes from descriptions.json
ww_data = load_descriptions()
hourly_dataframe['Weather Description'] = [
    get_weather_description(code, ww_data, period=get_period(ts, sunrise, sunset))
    for code, ts in zip(hourly_weather_code, hourly_dataframe['Date'])
]
# assign proper descriptions according to 'wmo weather code' and sunrise/sunset

# format each column with its correct unit before exporting
hourly_dataframe['Temperature'] = hourly_dataframe['Temperature'].map(lambda x: f'{x:.0f}°F')
hourly_dataframe['Feels Like'] = hourly_dataframe['Feels Like'].map(lambda x: f'{x:.0f}°F')
hourly_dataframe['Chance of Precipitation'] = hourly_dataframe['Chance of Precipitation'].map(lambda x: f'{x:.0f}%')
hourly_dataframe['Date'] = hourly_dataframe['Date'].dt.strftime('%Y-%m-%d %H:%M')

# export data to external file
with open('Data/hourly_forecast.txt', 'w+', encoding='utf-8') as f:
    f.write(f'Coordinates: {response_hourly.Latitude()}°N , {response_hourly.Longitude()}°E')
    f.write(f'\nElevation: {response_hourly.Elevation()}m above sea level')
    f.write(f'\nTimezone: {response_hourly.Timezone()}')
    f.write('\n~~~Hourly Data~~~\n')
    f.write(hourly_dataframe.to_string())