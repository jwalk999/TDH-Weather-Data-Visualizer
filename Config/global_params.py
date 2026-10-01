"""
File Name: global_params.py

Author: Jonathan W
Date: 9/14/2026
Version: 0.6.0

Scope: Shared constants, API clients, and location settings used across all weather scripts.
        - should be set up to ensure data does not become obselete when running individual scripts
        - should be location agnostic
"""

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import openmeteo_requests
import requests_cache
from retry_requests import retry

# ===== LOCATION =====
# set default location as a baseline
DEFAULT_LOCATION = {
    "latitude": 35.7411,
    "longitude": -81.3895,
    "location_name": "Hickory, NC",
}


# ===== TIME FRAMES=====
# set Eastern Standard Time - must match DEFAULT_LOCATION's coordinates
EASTERN = ZoneInfo("US/Eastern")


# ===== DATE FORMATTING =====
# set the date and time formats
DATE_FORMAT = "%m-%d-%Y"  # Month-Day-Year // 12/25/202X == Christmas
DATETIME_FORMAT = "%Y-%m-%d %H:%M" # Month-Day-Year // 12/25/202X 11:59 (pm)


# ===== OPEN-METEO CLIENT =====
_openmeteo_client = None
def get_openmeteo_client():
    """
    Sets the parameters needed to make the API call to OpenMeteo

    Params: _openmeteo_client = Object that tells if there is data collected
            cache_session: creates a cache for the api call
            retry_session: retry the API call 5 times in case of failure
            openmeteo_requests: the API call, copies data to cache

    Returns: The weather data as collected from the API call
    """
    global _openmeteo_client
    if _openmeteo_client is None:
        cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        _openmeteo_client = openmeteo_requests.Client(session=retry_session)
    return _openmeteo_client

# set parameters for forecasting data collection with openmeteo
def get_daily_params():
    """
    Set parameters for the weather collection function
    Params: longitude, latitude - as set by object 'location'
            daily: *weather_output_type* <- what weather data do you want?
                    temperature_2m - temperature with 2 meter resolution
                    temperature_2m_max - the highest temperature recorded
                    temperature_2m_min - lowest temperature recorded
                    weather_code - WMO weather code (translates to conditions)
                    precipitation_probability_mean - average precip % reported
                    sunrise - checks to see if a specific time is after sunrise
                    sunset - checks to see if a specific time is after sunset
            models: best_match (picks the weather model that has the most informaiton
                                for a given location)
            timezone: pick your timezone
            forecast_days: the amount of days the API will collect data for
            wind_speed_unit: miles per hour / kilometers per hour
            temperature_unit: fahrenheit / celcius
            precipitation_unit: inch / centimeter

    Returns: Only sets the specific parameters needed for openmeteo_requests responses
    """
    location = load_location()
    return {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "weather_code",
            "precipitation_probability_mean",
            "sunrise",
            "sunset",
        ],
        "models": "best_match",
        "timezone": "America/New_York",
        "forecast_days": 7,
        "wind_speed_unit": "mph",
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
    }


def get_hourly_params():
    """
    Set parameters for the weather collection function
    Params: longitude, latitude - as set by object 'location'
            daily: *weather_output_type* <- what weather data do you want?
                temperature_2m - temperature with 2 meter resolution
                apparent_temperature - "feels like" temp
                weather_code - WMO weather code (translates to conditions)
                precipitation_probability_mean - average precip % reported
            models: best_match (picks the weather model that has the most informaiton
                                for a given location)
            timezone: pick your timezone
            forecast_days: the amount of days the API will collect data for
            wind_speed_unit: miles per hour / kilometers per hour
            temperature_unit: fahrenheit / celcius
            start_date AND end_date: set the time frame needed from the API

    Returns: Only sets the specific parameters needed for openmeteo_requests responses
    """
    location = load_location()
    today = datetime.now(tz=EASTERN)
    return {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "hourly": [
            "temperature_2m",
            "apparent_temperature",
            "precipitation_probability",
            "weather_code",
        ],
        "daily": ["sunrise", "sunset"],
        "models": "best_match",
        "timezone": "America/New_York",
        "wind_speed_unit": "mph",
        "temperature_unit": "fahrenheit",
        "start_date": today.strftime("%Y-%m-%d"),
        "end_date": today.strftime("%Y-%m-%d"),
    }


# ===== WEATHER CODE DESCRIPTIONS =====

# tell python where to find the descriptions for weather codes
DESCRIPTIONS_PATH = Path(__file__).parent / "descriptions.json"


# open and read weather code descriptions
def load_descriptions():
    """
    Open the descriptions.json file and read its contents
    
    Returns: Weather descriptions to translate WMO weather codes into weather condition
            types. Encodes the data unto utf-8 for readability.

    """
    with open(DESCRIPTIONS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# set parameters for what counts as day and night
# day = after sunrise and before sunset
# all other values = night
# "timestamp" is the value we are checking
def get_period(timestamp, sunrise, sunset):
    """
    Define when day and night is according to sunrise and sunset time stamps

    Returns: if %TIME% is before sunset and after sunrise = day
             if %TIME% is outside of this time range = night
    """
    if sunrise <= timestamp <= sunset:
        return "day"
    return "night"


def get_weather_description(code, ww_data, period="day"):
    """
    Use the get_period functions return (day/night) to define which weather code
        description is returned: day = sunny // night = clear
    """
    entry = ww_data.get(str(int(code)))
    if entry is None:
        return "Unknown"
    return entry[period]["description"]


# ===== GLOBAL USE SETTINGS
# use configuration json file to set location and station id info
# set path for config file
CONFIG_PATH = Path(__file__).parent / "config.json"


# ===== SAVING CONFIGS =====
def save_location(latitude, longitude, location_name):
    """
    Set the location and location name as defined from above and paste them into a json
    file for easily reading where the user is so a GUI can read it. User can change the json file 
    to point to their chosen location.
    """
    data = {
        "latitude": latitude,
        "longitude": longitude,
        "location_name": location_name,
    }
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# create config file if it doesn"t exist
def load_location():
    """
    Set the save location of the config.json file if it does not exist

    """
    if not CONFIG_PATH.exists():
        save_location(**DEFAULT_LOCATION)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
