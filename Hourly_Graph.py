"""
File Name: Hourly_Graph.py

Author: Jonathan W
Date Created: 9/30/2026
Last Update: 10/1/2026
Version: 1.0.0

Scope: Create a nested graph (line and bar) from data collected from Hourly.py
"""

# ===== IMPORTS =====
# Add the project's parent directory to Python's import search path
# This allows the file to import modules from the Config package
import sys
from pathlib import Path


def _find_project_root(marker="Config"):
    """
    Set the folder directory for all scripts to append their search queries

    Returns: the full folder path of the program
    Errors: Raise a runtime error if it cannot find the Config file
    """

    path = Path(__file__).resolve().parent
    while not (path / marker).is_dir():
        if path.parent == path:
            raise RuntimeError(
                f"Could not find project root (looking for '{marker}' folder)"
            )
        path = path.parent
    return path


# set system file path to project root
sys.path.append(str(_find_project_root()))

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

# set the project's root folder
PROJECT_ROOT = _find_project_root()

from zoneinfo import ZoneInfo

import pandas as pd

from Hourly import get_hourly_forecast

# ===== VARIABLES / DATA COLLECTION =====

# Run the script and assign the collected data
hourly_dataframe = get_hourly_forecast()

# Label the collected data and point variables to dataframes
x = hourly_dataframe["Date"]
temp_real = hourly_dataframe["Temperature"]
precip_chance = hourly_dataframe["Chance of Precipitation"]
weather_description = hourly_dataframe["Weather Description"]
sunrise_time = hourly_dataframe["Sunrise"]
sunset_time = hourly_dataframe["Sunset"]

# ===== PLOTTING =====
# Create 1 window (figure) with 2 subplots (temp/precip)
fig, (ax_temp, ax_precip) = plt.subplots(
    2,
    1,
    figsize=(12, 6),
    sharex=True,  # graphs share the x axis
    facecolor=("#efe3f4"),  # cunty purple
)

# Create Temperature chart
# Make real air temperature subplot
ax_temp.plot(
    x,
    temp_real,
    marker="o",
    linewidth=1.5,
    color=("#d9534f"),  # red (placeholder)
    label="Actual Temp",
)
for xi, yi in zip(x, temp_real):
    ax_temp.annotate(
        f"{yi:.0f}°F",
        (xi, yi),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center",
        fontsize=8,
    )

# Create 2 vertical lines and label them for sunrise and sunset
ax_temp.vlines(
    sunrise_time.iloc[0],
    color="#f0ad4e",
    linestyle="dashed",
    lw=1.5,
)
ax_temp.vlines(
    sunset_time.iloc[0],
    0,
    110,
    color="#5bc0de",
    linestyle="dashed",
    lw=1.5,
)
# Set temp plot paremeters
ax_temp.set_ylim(0, 110)
ax_temp.set(
    ylabel="Temperature (°F)",
    title=f"Hourly Forecast for {x[1]:%d-%b}",
)

# Make the legend top left, outside of the plotting area
ax_temp.legend(bbox_to_anchor=(0.0, 1.02), loc="lower left", ncols=1, borderaxespad=0.1)


# ===== PRECIPITATION CHART =====
bar_container = ax_precip.bar(
    x,
    precip_chance,
    width=0.6,
    color="#4a90d9",  # soft blue
    label="Chance of Precipitation",
)
# Put value labels on the bars and format (50%)
ax_precip.bar_label(bar_container, fmt="{:.0f}%")
ax_precip.set(ylim=(0, 100), ylabel=("Chance of\nPrecipitation (%)"))
# Copy the vertical lines from above
ax_precip.vlines(
    sunrise_time.iloc[0],
    0,
    110,
    color="#f0ad4e",
    linestyle="dashed",
    lw=1.5,
    label="Sunrise",
)
ax_precip.vlines(
    sunset_time.iloc[0],
    0,
    110,
    color="#5bc0de",
    linestyle="dashed",
    lw=1.5,
    label="Sunset",
)

# Make shared x axis for the times
# X axis labels as hours across the day
ax_precip.xaxis.set_major_locator(mdates.HourLocator(interval=2))
# Make sure the date format is in the correct timezone
ax_precip.xaxis.set_major_formatter(
    mdates.DateFormatter("%H:%M", tz=ZoneInfo("America/New_York"))
)
# Add a little blank space for a cleaner graph
padding = pd.Timedelta(minutes=30)
ax_precip.set_xlim(x[0] - padding, x[23] + padding)


# Save the created chart as a png
save_path = PROJECT_ROOT / "Data" / "hourly_forecast_chart.png"
save_path.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(save_path, dpi=300, bbox_inches="tight")

plt.tight_layout()
plt.show()
