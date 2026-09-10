"""
File Name: weather_script1.py
Author: Jonathan W
Date: 9/9/2026
Version: 0.3.0
Scope: Collect live weather data for use in graphs.py
    - Now built as a callable script in it's own file. Easier to run, less resource intensive(?)
    - The data is now collected as a dictionary instead of individual scripts
    - Only runs when the function 'get_weather_data' is imported, this files just defines the function
"""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import meteostat as ms

EASTERN = ZoneInfo('US/Eastern')
UTC = ZoneInfo('UTC')

def get_weather_data(station_id="72503", location_name="LaGuardia Airport, NYC", include_norms=True):
# this is the specific station id for LaGuardia Airport, NYC
# defining it as a function makes it so the file itself does not need to be edited, just change the parameters (station_id and location_name)
#===== DEFINE TIME FRAME =====
# define time frame
    today = datetime.now(EASTERN)
    yesterday = today - timedelta(days=1)
    start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end = yesterday.replace(hour=23, minute=59, second=59, microsecond=0)
# yesterday = current date - 1
# this defines midnight, the yesterday morning, to the last minute before midnight, yesterday evening
# start and end are fuctions used my meteostat to define the timeframe

# meteostat requires the use of UTC time, so we must convert our Eastern Standard Time to UTC
    start_utc = start.astimezone(UTC).replace(tzinfo=None)
    end_utc = end.astimezone(UTC).replace(tzinfo=None)
# this should simply convoert the time zone while keeping time stamps the same

# ensure your time zone corresponds to the station_id above or else the times will be wrong


#====== GET HOURLY DATA =====
    ts_hour = ms.hourly(ms.Station(id=station_id), start_utc, end_utc)
# collects time series data from the specified station id above
    df_hour = ts_hour.fetch(units=ms.UnitSystem.IMPERIAL)
# converts unit system from default metric to imperial
# to keep metric system, delete everything after 'fetch'
    df_hour.index = df_hour.index.tz_localize('UTC').tz_convert('US/Eastern')
# convert back from UTC to EST to plot in graphs


#===== GET CLIMATE NORMALS =====
    df_norm = None
# runs as a boolean, only if the file is not saved on the user's computer
    if include_norms:
        ts_norm = ms.normals(ms.Station(id=station_id), 1990, 2026)
        df_norm = ts_norm.fetch(units=ms.UnitSystem.IMPERIAL)
# collects climate norms, between the dates 1990 to 2026 in imperial format

    return {
        "df_norm" : df_norm,
        "df_hour" : df_hour,
        "yesterday" : yesterday,
        "location_name" : location_name,
        }


def main():
    data = get_weather_data
    print(data["df_hour"])
    print(data["df_norm"])


if __name__ == "__main__":
    main()