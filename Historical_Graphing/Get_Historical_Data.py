'''
File Name: weather_data_public.py
Author: Jonathan W
Date: 9/1/2026
Version: 0.2.0
Scope: Collect live weather data and post them into easy to read graphs and images
        - uses plugins from Meteostat (https://dev.meteostat.net/python)
        - for practicing Pyton techniques
        - future usage may include implementation of a Raspberry Pi to create a weather 'station' 
        - historical weather data for today's date minus 1 (yesterday)
        - make the program callable to be ran on a daily basis

'''

#===== IMPORT CODE LIBRARIES =====
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import meteostat as ms


# datetime, zoneinfo, matplotlib, meteostat, pathlib


#===== SET TIME FRAME =====
EASTERN = ZoneInfo('US/Eastern')
# defines Eastern Standard Time / USA
UTC = ZoneInfo('UTC')
# defines UTC time

def main():




    today = datetime.now(EASTERN)
# current date and time
    yesterday = today - timedelta(days=1)
# yesterday's date and time
    start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
# yesterday, 00:00:00 am EST
    end = yesterday.replace(hour=23, minute=59, second=59, microsecond=0)
# yesterday, 11:59:59 pm EST
# recording all hours of the day for yesterday (today -1)
# used to record temperatures from each hour
# meteostat does not record futuristic data

#===== CONVERT EST TO UTC =====
# meteostat does not interact with ZoneInfo
# replace EST with UTC and delete tzinfo label
    start_utc = start.astimezone(UTC).replace(tzinfo=None)
    end_utc = end.astimezone(UTC).replace(tzinfo=None)
# this should simply convert the time zone while keeping timestamps

# user must ensure that the timezone is accurate to the weather station's location, or else the time stamps will be incorrect


#===== DATA COLLECTION SECTION =====

#===== GET CLIMATE NORMALS =====
    location_name = 'LaGuardia Airport, NYC'  # to be displayed on the graphs below
    ts_norm = ms.normals(ms.Station(id='72503'), 1990, 2026)  # <--- change 'id=xxxxx' to the station id you are targeting  https://meteostat.net/en/
# 72503 = LaGuardia Airport, New York City, NY, USA

# collects climatological norms reported between the dates 1990 to 2026 for the your target region
    df_norm = ts_norm.fetch(units=ms.UnitSystem.IMPERIAL)
# collect data in Imperial format



#===== GET HOURLY DATA =====
    ts_hour = ms.hourly(ms.Station(id='72503'), start_utc, end_utc)  # <---- change 'id=xxxxx' to the station id you are targeting    https://meteostat.net/en/
# 72503 = LaGuardia Airport, New York City, NY, USA

# search the meteostat station data
    df_hour = ts_hour.fetch(units=ms.UnitSystem.IMPERIAL)
# meteostat uses metric by default, this fetches a time series and converts it to imperial

#===== CONVERT BACK TO EST =====
    df_hour.index = df_hour.index.tz_localize('UTC').tz_convert('US/Eastern')

if __name__ == '__main__':
    main()
