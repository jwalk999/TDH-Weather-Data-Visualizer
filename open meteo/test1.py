import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

# setup API client with cache and retry on error

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

#===== WEATHER VARIABLES =====
url = "https://api.open-meteo.com/v1/forecast"

# get parameters for the daily data set
params_daily = {
    "latitude": 35.72,
    "longitude": -81.33,
    "daily": ["temperature_2m_max", "temperature_2m_min", "weather_code", "precipitation_probability_max"],
    "models": "ncep_gfs_seamless",
    "timezone": "America/New_York",
    "forecast_days": 7,
    "wind_speed_unit": "mph",
    "temperature_unit": "fahrenheit",
    "precipitation_unit": "inch",
}


# get parameters for the hourly data set
# if "hourly" is included in the default params list, then it will print 160+ lines of hourly data
# this helps to reduce this as hourly data is only needed for the current day
# by default, this makes another API call, which is limited, but running a different program would do the same thing
params_hourly = {
    "latitude": 35.72,
    "longitude": -81.33,
    "hourly": ["temperature_2m", "apparent_temperature", "precipitation_probability"],
    "models": "ncep_gfs_seamless",
    "timezone": "America/New_York",
    "wind_speed_unit": "mph",
    "temperature_unit": "fahrenheit",
    "precipitation_unit": "inch",
    "start_date": "2026-09-13",
    "end_date": "2026-09-13",
}

# (35.72, -81.33) = gps coordinates for Hickory, NC
# defined on NOAA database as Hickory, NC (Catawba County)
# https://forecast.weather.gov/MapClick.php?textField1=35.73&textField2=-81.33


#===== COLLECT DATA FROM API =====


# direct open meteo to collect responses from the url using the parameters above
responses_daily = openmeteo.weather_api(url, params = params_daily)
responses_hourly = openmeteo.weather_api(url, params = params_hourly)

# process first location, add a for-loop for multiple locations or weather models
response_daily = responses_daily[0]
response_hourly = responses_hourly[0]

# export data to external file named exports.txt
with open("open meteo/exports.txt", "w+", encoding="utf-8") as exports:
    exports.write("\n")
    exports.write(f"Coordinates: {response_daily.Latitude()}°N {response_daily.Longitude()}°E")
    exports.write("\n")
    exports.write(f"Elevation: {response_daily.Elevation()} m above sea level")
    exports.write("\n")
    exports.write(f"Timezone: {response_daily.Timezone()}")

#===== HOURLY =====

# process hourly data, the order of variables must be the same as requested
hourly = response_hourly.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()
hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()

# define time range for hourly data
hourly_data = {
    "date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    ).tz_convert(response_hourly.Timezone().decode())
}

# direct hourly data into proper variable values
hourly_data["Temperature"] = hourly_temperature_2m
hourly_data["Feels Like"] = hourly_apparent_temperature
hourly_data["Chance of Precipitation"] = hourly_precipitation_probability

hourly_data["date"] = hourly_data["date"].strftime("%Y-%m-%d %H:%M")
hourly_dataframe = pd.DataFrame(data=hourly_data)

# format each column with its correct unit before exporting
hourly_dataframe["Temperature"] = hourly_dataframe["Temperature"].map(lambda x: f"{x:.0f}°F")
hourly_dataframe["Feels Like"] = hourly_dataframe["Feels Like"].map(lambda x: f"{x:.0f}°F")
hourly_dataframe["Chance of Precipitation"] = hourly_dataframe["Chance of Precipitation"].map(lambda x: f"{x:.2f}%")


# export data to external file named exports.txt
with open("open meteo/exports.txt", "a", encoding="utf-8") as exports:
    exports.write("\n\nHourly Data\n")
    exports.write(hourly_dataframe.to_string())



#===== DAILY =====

# process daily data, order of variables must be the same as requested
daily = response_daily.Daily()
daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
daily_weather_code = daily.Variables(2).ValuesAsNumpy()
daily_precipitation_probability_mean = daily.Variables(3).ValuesAsNumpy()

# define time range for daily data
daily_data = {
    "date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    ).tz_convert(response_daily.Timezone().decode())
}

# direct daily data into proper variable values
daily_data["Temperature High"] = daily_temperature_2m_max
daily_data["Temperature Low"] = daily_temperature_2m_min
daily_data["WMO Weather Code"] = daily_weather_code
daily_data["Chance of Precipitation"] = daily_precipitation_probability_mean


# classify the weather codes into readable format, WMO Weather interpretation coes (WW) 
WEATHER_CODES = {
    # Clear / Cloudy
    # Clear / Cloudy
    0: "Clear",                 # Clear sky
    1: "Clear",                 # Mainly clear
    2: "Partly Cloudy",
    3: "Overcast",

    # Fog
    45: "Fog",
    48: "Fog",                  # Depositing rime fog

    # Drizzle (continuous, not freezing)
    51: "Drizzle",              # Slight
    53: "Drizzle",              # Moderate
    55: "Drizzle",              # Dense/heavy
    56: "Freezing Drizzle",     # Slight
    57: "Freezing Drizzle",     # Moderate/heavy

    # Rain (continuous, not freezing)
    61: "Light Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    66: "Freezing Rain",        # Slight
    67: "Freezing Rain",        # Moderate/heavy

    # Snow (continuous fall of snowflakes)
    71: "Light Snow",
    73: "Moderate Snow",
    75: "Heavy Snow",
    77: "Light Snow",           # Snow grains

    # Showers (convective, distinct from steady precipitation)
    80: "Rain Showers",         # Slight
    81: "Rain Showers",         # Moderate/heavy
    82: "Rain Showers",         # Violent
    85: "Snow Showers",         # Slight
    86: "Snow Showers",         # Moderate/heavy

    # Thunderstorms
    95: "Thunderstorm",         # Slight/moderate, no hail
    96: "Thunderstorm w/ Hail", # Slight/moderate, with hail / only available for EU data sets
    99: "Thunderstorm w/ Hail", # Heavy, with hail / only available for EU data sets
}

def get_weather_description(code):
    return WEATHER_CODES.get(code, "Unknown")


daily_weather_type = [get_weather_description(code) for code in daily_weather_code]
daily_data["weather_type"] = daily_weather_type
# make the output date look cleaner
daily_data["date"] = daily_data["date"].strftime("%Y-%m-%d")
daily_dataframe = pd.DataFrame(data = daily_data)

# format each column with its correct unit before exporting
daily_dataframe["Temperature High"] = daily_dataframe["Temperature High"].map(lambda x: f"{x:.0f}°F")
daily_dataframe["Temperature Low"] = daily_dataframe["Temperature Low"].map(lambda x: f"{x:.0f}°F")
daily_dataframe["Chance of Precipitation"] = daily_dataframe["Chance of Precipitation"].map(lambda x: f"{x:.0f}%")

# export data to external file named exports.txt
with open("open meteo/exports.txt", "a", encoding="utf-8") as exports:
    exports.write("\n\nDaily Data\n")
    exports.write(daily_dataframe.to_string())