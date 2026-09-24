'''
File Name: global_params.py
Author: Jonathan W
Date: 9/14/2026
Version: 0.4.0
Scope: Shared constants, API clients, and location settings used across all weather scripts.
        - should be set up to ensure data does not become obselete when running individual scripts
        - should be location agnostic
'''

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import meteostat as ms
import openmeteo_requests
import requests_cache
from retry_requests import retry
import json
from pathlib import Path


# ===== LOCATION =====

DEFAULT_LOCATION = {
    "station_id": "72301",
    "latitude": 35.70,
    "longitude": -81.31,
    "location_name": "Hickory, NC",
}



#===== DATE FORMATTING =====
DATE_FORMAT = '%m-%d-%Y'
DATETIME_FORMAT = '%Y-%m-%d %H:%M'

#===== METEOSTAT SETTINGS =====
UNITS = ms.UnitSystem.IMPERIAL
EASTERN = ZoneInfo('US/Eastern')
UTC = ZoneInfo('UTC')


# set time frames
def get_today():            # current date and time
    return datetime.now(EASTERN)

def get_yesterday():        # yesterday's date and time
    return get_today() - timedelta(days=1)

def get_day_bounds(target_date):
# Returns (start, end) datetimes spanning midnight to 23:59:59 for the given date.
    start = target_date.replace(hour=0, minute=0, second=0, microsecond=0)      
    # yesterday, 00:00:00 am EST
    end = target_date.replace(hour=23, minute=59, second=59, microsecond=0)     
    # yesterday, 11:59:59 pm EST
    return start, end       
    # record full day for yesterday, all hours, data feeds into historical data

def to_utc_naive(dt):
    return dt.astimezone(UTC).replace(tzinfo=None)    
# convert datetime into UTC for use in Meteostat




#===== OPEN-METEO CLIENT =====
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
OPENMETEO_CLIENT = openmeteo_requests.Client(session=retry_session)

# set parameters for forecasting data collection with openmeteo
def get_daily_params():
    location = load_location()
    return {
        'latitude': location['latitude'],
        'longitude': location['longitude'],
        'daily': ['temperature_2m_max', 'temperature_2m_min', 
                  'weather_code', 'precipitation_probability_mean'],
        'models': 'best_match',
        'timezone': 'America/New_York',
        'forecast_days': 7,
        'wind_speed_unit': 'mph',
        'temperature_unit': 'fahrenheit',
        'precipitation_unit': 'inch',
    }

def get_hourly_params():
    location = load_location()
    today = get_today()
    return {
        'latitude': location['latitude'],
        'longitude': location['longitude'],
        'hourly': ['temperature_2m', 'apparent_temperature',
                    'precipitation_probability', 'weather_code'],
        'daily' : ['sunrise', 'sunset'],
        'models': 'best_match',
        'timezone': 'America/New_York',
        'wind_speed_unit': 'mph',
        'temperature_unit': 'fahrenheit',
        'start_date': today.strftime('%Y-%m-%d'),
        'end_date': today.strftime('%Y-%m-%d'),
    }



#===== WEATHER CODE DESCRIPTIONS =====

# tell python where to find the descriptions for weather codes
DESCRIPTIONS_PATH = Path(__file__).parent / 'descriptions.json'
# open and read weather code descriptions
def load_descriptions():
    with open(DESCRIPTIONS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

# set parameters for what counts as day and night
# day = after sunrise and before sunset
# all other values = night
# 'timestamp' is the value we are checking
def get_period(timestamp, sunrise, sunset):
    if sunrise <= timestamp <= sunset:
        return 'day' 
    return 'night'

def get_weather_description(code, ww_data, period='day'):
    entry = ww_data.get(str(int(code)))
    if entry is None:
        return 'Unknown'
    return entry[period]['description']


#===== GLOBAL USE SETTINGS
# use configuration json file to set location and station id info
# set path for config file
CONFIG_PATH = Path(__file__).parent / 'config.json'


#===== SAVING CONFIGS =====

# save new location settings into config.json
# for use with GUI program
def save_location(station_id, latitude, longitude, location_name):
    data = {
        "station_id": station_id,
        "latitude": latitude,
        "longitude": longitude,
        "location_name": location_name,
    }
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


# create config file if it doesn't exist
def load_location():
    if not CONFIG_PATH.exists():
        save_location(**DEFAULT_LOCATION)
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

