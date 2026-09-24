"""
File Name: Daily_graph.py
Author: Jonathan W.
Date: 9/24/2026
Version: 0.5.0
Scope: Collects data from Daily.py to put it into a graph
"""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from Daily import daily_data

# ===== DEFINE VARIABLES =====
data = daily_data
daily_data["Temperature High"] = daily_temperature_2m_max
daily_data["Temperature Low"] = daily_temperature_2m_min
daily_data["WMO Weather Code"] = daily_weather_code
daily_data["Chance of Precipitation"] = daily_precipitation_probability_mean


# ===== PLOT DATA ======
# set axis data
x = daily_temperature_2m_max
y = daily_data["Date"]

# setting layout of chart
fig_date, ax = plt.subplots(figsize=(12, 5))
ax.plot(x, y, marker="o", linewidth=1.5)
for xi, yi in zip(x, y):
    ax.annotate(
        f"{yi:.0f}°F"(xi, yi),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center",
        fontsize=8,
    )
# show only x ticks (markers) that have data
# the x axis tick markers will be dates
ax.set_xticks(daily_temperature_2m_max)
ax.axis.set_major_formatter(mdates.DateFormatter("%m-%d-%Y"))
# set the range for the y axis as 30°F to 110°F
# this should represent the data more accurately
ax.set_ylim(30, 110)
# label the axes and put a title at the top
ax.set(
    xlabel="Date (m-d-Y)",
    ylabel="Temperature (°F)",
    title=f"Daily Forecast ({pd.date_range})",  # should be the next 7 days
)

# angle the dates 45 degrees to make sure they fit
fig_date.autofmt_xdate(rotation=45)

plt.tight_layout()
plt.show()
