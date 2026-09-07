"""
File Name: weather_data_public.py
Author: Jonathan W
Date: 9/1/2026
Version: 0.2.0
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

# datetime, zoneinfo, matplotlib, meteostat, pathlib



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
location_name = "LaGuardia Airport, NYC"  # to be displayed on the graphs below
ts_norm = ms.normals(ms.Station(id="72503"), 1990, 2026)  # <--- change "id=xxxxx" to the station id you are targeting  https://meteostat.net/en/
# 72503 = LaGuardia Airport, New York City, NY, USA

# collects climatological norms reported between the dates 1990 to 2026 for the your target region
df_norm = ts_norm.fetch(units=ms.UnitSystem.IMPERIAL)
# collect data in Imperial format



#===== GET HOURLY DATA =====
ts_hour = ms.hourly(ms.Station(id="72503"), start_utc, end_utc)  # <---- change "id=xxxxx" to the station id you are targeting    https://meteostat.net/en/
# 72503 = LaGuardia Airport, New York City, NY, USA

# search the meteostat station data
df_hour = ts_hour.fetch(units=ms.UnitSystem.IMPERIAL)
# meteostat uses metric by default, this fetches a time series and converts it to imperial

#===== CONVERT BACK TO EST =====
df_hour.index = df_hour.index.tz_localize('UTC').tz_convert('US/Eastern')








#===== GRAPH SECTION =====

#===== PLOT NORMS =====
plt.style.use('seaborn-v0_8-darkgrid') # grid background

fig_norm, ax_norm = plt.subplots(figsize=(11, 6))

months = df_norm.index
tmin = df_norm['tmin']
tmax = df_norm['tmax']
tavg = (tmin + tmax) / 2

ax_norm.fill_between(
    months, tmin, tmax,
    color='#4a90d9', alpha=0.25, label='Normal Range (Min-Max)'
)       # shades temperature range, blue

ax_norm.plot(
    months, tavg,
    color='#1f5c99', linewidth=2.5, marker='o', markersize=6, label='Average'
)       # shows a bold average line through the middle

ax_norm.plot(months, tmax, color='#d9534f', linewidth=1, linestyle='--', alpha=0.6, label='Max')
ax_norm.plot(months, tmin, color='#5bc0de', linewidth=1, linestyle='--', alpha=0.6, label='Min')
        # min and max lines, red and blue, bold

# only label to average points
for xi, yi in zip(months, tavg):
    ax_norm.annotate(
        f"{yi:.0f}°",
        (xi, yi),
        textcoords="offset points",
        xytext=(0, 10),
        ha='center',
        fontsize=8,
        color='#1f5c99',
        fontweight='bold',
    )


month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# monthlyu lables
ax_norm.set_xticks(range(1, 13))
# only show the intended labels
ax_norm.set_xticklabels(month_labels)

ax_norm.set_ylim(0, 110)
ax_norm.set(
    xlabel="Month",
    ylabel="Temperature (°F)",
    title=f"Monthly Temp Norms - {location_name} (1990-2026)"
)

ax_norm.legend(loc='upper left', frameon=True, fontsize=9)
# show graph legend
ax_norm.grid(True, alpha=0.3)
# show grid

plt.tight_layout()


#===== PLOT HOURLY =====
fig_hour, ax = plt.subplots(figsize=(12, 5)) # to fit 24hr labels

x = df_hour.index
y = df_hour['temp']

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

ax.set_xticks(df_hour.index)
# show only ticks that have associated temp data
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
# force ticks, 24 hours, every hour

ax.set_ylim(30, 110)
ax.set(
    xlabel="Time of Day (EST)",
    ylabel="Temperature (°F)",
    title=f"Temperatures for {yesterday.strftime('%m-%d-%Y')}",
)

fig_hour.autofmt_xdate(rotation=45)  # angle the time stamps to prevent overlap

plt.tight_layout()

#===== SAVE CREATED GRAPHs =====
documents_dir = Path.home() / "Documents" / "Too Damn Hot!" / "weather_charts"
# locates directory documents > weather_charts
documents_dir.mkdir(parents=True, exist_ok=True)
# creates the folder if it does not exist
hourly_filename = f"temp_chart_{yesterday.strftime('%m-%d-%Y')}.png"
norm_filename = "climate_normals_1990-2026.png"
# names the file temp_chart_(yesterday's date, month day year)
hourly_path = documents_dir / hourly_filename
norm_path = documents_dir / norm_filename
# this is where the document will save to (c:/user/documents/weather_charts)


if not hourly_path.exists():
    fig_hour.savefig(hourly_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {hourly_path}")
else:
    print(f"Skipped save - file already exists: {hourly_path}")

if not norm_path.exists():
    fig_norm.savefig(norm_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {norm_path}")
else:
    print(f"Skipped save - file already exists: {norm_path}")
# only save the normals chart if it does not exist, otherwise print a message that says it already exists

# this is the command that saves the file

plt.show()
# displays created graph in new window using matplot

