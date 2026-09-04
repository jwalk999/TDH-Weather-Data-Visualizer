"""
File Name: weather_data.py
Author: Jonathan W
Date: 9/1/2026
Version: 0.1.0
Scope: Collect live weather data and post them into easy to read graphs and images
        - uses plugins from Meteostat (https://dev.meteostat.net/python)
        - for practicing Pyton techniques
        - future usage may include implementation of a Raspberry Pi to create a weather "station" 
        - historical weather data for today's date minus 1 (yesterday)
        - make the program callable to be ran on a daily basis

"""

#===== IMPORT CODE LIBRARIES =====
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import meteostat as ms
from pathlib import Path


#===== SET TIME FRAME =====
EASTERN = ZoneInfo('US/Eastern')
# defines Eastern Standard Time / USA
UTC = ZoneInfo('UTC')
# defines UTC time

today = datetime.now(EASTERN)
# current date and time
yesterday = today - timedelta(days=1)
# yesterday's date and time
start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
# yesterday, 00:00:00 am EST
end = yesterday.replace(hour=23, minute=59, second=59, microsecond=0)
# yesterday, 11:59:59 pm EST
# recording all hours of the day for current date -1
# used to record temperatures from each hour
# meteostat does not record futuristic data

#===== CONVERT EST TO UTC =====
# meteostat does not interact with ZoneInfo
# replace EST with UTC and delete tzinfo label
start_utc = start.astimezone(UTC).replace(tzinfo=None)
end_utc = end.astimezone(UTC).replace(tzinfo=None)
# this should simply convert the time zone while keeping timestamps


#===== GET HOURLY DATA =====
ts = ms.hourly(ms.Station(id="*****"), start_utc, end_utc)
# search the meteostat station data, replace ***** with the unique identifier for your chosen weather station
# find weather station id's at https://meteostat.com/en/
df = ts.fetch(units=ms.UnitSystem.IMPERIAL)
# meteostat uses metric by default, this fetches a time series and converts it to imperial

#===== CONVERT BACK TO EST TO PLOT =====
df.index = df.index.tz_localize('UTC').tz_convert('US/Eastern')

#===== PLOT =====
fig, ax = plt.subplots(figsize=(12, 5)) # to fit 24hr labels

x = df.index
y = df['temp']

ax.plot(x, y, marker='o', linewidth=1.5)

for xi, yi, in zip(x, y):
    ax.annotate(
        f"{yi:.0f}°",
        (xi, yi),
        textcoords="offset points",
        xytext=(0, 8),
        ha='center',
        fontsize=8,
    )

ax.set_xticks(df.index)
# show only ticks that have associated temp data
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
# force ticks, 24 hours, every hour

ax.set_ylim(0, 110)
ax.set(
    xlabel="Time of Day (EST)",
    ylabel="Temperature (°F)",
    title=f"Temperatures for {yesterday.strftime('%m-%d-%Y')}",
)

fig.autofmt_xdate(rotation=45)  # angle the time stamps to prevent overlap

#===== SAVE CREATED GRAPH =====
documents_dir = Path.home() / "Documents" / "weather_charts"
# locates directory documents > weather_charts
documents_dir.mkdir(parents=True, exist_ok=True)
# creates the folder if it does not exist
filename = f"temp_chart_{yesterday.strftime('%m-%d-%Y')}.png"
# names the file temp_chart_(yesterday's date, month day year)
save_path = documents_dir / filename
# names the file the filename variable and saves it to path documents_dir variable


fig.savefig(save_path, dpi=300, bbox_inches='tight')
# this is the command that saves the file

plt.tight_layout()
plt.show()
# displays created graph in new window using matplot

