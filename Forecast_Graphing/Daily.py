'''
File Name: Daily.py
Author: Jonathan W
Date: 9/15/2026
Version: 0.4.0
Scope: Collects daily forecast for the next 7 days
        - logs temperature highs and lows, precipitation probability, and weather type
        - settings found in global_param.py
'''
# tell python to search grandparent directory for required import files
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd

from Config.global_params import (
    OPENMETEO_CLIENT,
    get_daily_params,
)

#===== COLLECT PARAMETERS AND VARIABLES =====
url = 'https://api.open-meteo.com/v1/forecast'

# get parameters from global_params
params_daily = get_daily_params()
# sets location, weather data types, # of days to forecast, and measurement units


#===== COLLECT DATA FROM API =====

# direct open meteo to collect responses from the url using set parameters
responses_daily = OPENMETEO_CLIENT.weather_api(url, params_daily)
response_daily = responses_daily[0]

#===== PROCESS DATA =====

# set variables for the data collected using the parameters set in global_params.py
daily = response_daily.Daily()
daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
daily_weather_code = daily.Variables(2).ValuesAsNumpy()
daily_precipitation_probability_mean = daily.Variables(3).ValuesAsNumpy()

# define time range for daily data
daily_data = {
    'Date': pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = 's', utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = 's', utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = 'left'
    ).tz_convert(response_daily.Timezone().decode())
}

# direct data into values for set variables
daily_data['Temperature High'] = daily_temperature_2m_max
daily_data['Temperature Low'] = daily_temperature_2m_min
daily_data['WMO Weather Code'] = daily_weather_code
daily_data['Chance of Precipitation'] = daily_precipitation_probability_mean

# retrieve descriptions for WMO weather codes from descriptions.json
def get_weather_description(code, ww_data, period='day'):
    entry = ww_data.get(str(code))
    if entry is None:
        return 'Unknown'
    return entry[period]['description']


# format each column with its correct unit before exporting
daily_dataframe = pd.DataFrame(data = daily_data)
daily_dataframe['Temperature High'] = daily_dataframe['Temperature High'].map(lambda x: f'{x:.0f}°F')
daily_dataframe['Temperature Low'] = daily_dataframe['Temperature Low'].map(lambda x: f'{x:.0f}°F')
daily_dataframe['Chance of Precipitation'] = daily_dataframe['Chance of Precipitation'].map(lambda x: f'{x:.0f}%')

# make output date look cleaner
daily_data['Date'] = daily_data['Date'].strftime('%Y-%m-%d')

# export data to external file
with open('Data/daily_forecast.txt', 'w+', encoding='utf-8') as f:
    f.write(f'Coordinates: {response_daily.Latitude()}°N , {response_daily.Longitude()}°E')
    f.write(f'\nElevation: {response_daily.Elevation()}m above sea level')
    f.write(f'\nTimezone: {response_daily.Timezone()}')
    f.write('\n~~~Daily Data~~~\n')
    f.write(daily_dataframe.to_string())