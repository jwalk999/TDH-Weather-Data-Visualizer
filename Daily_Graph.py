"""
File Name: Daily_Graph.py

Author: Jonathan W
Date Created: 9/25/2026
Last Update: 9/30/2026
Version: 1.1.1

Scope: Create a nested graph (line and bar) from data collected from Daily.py
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


sys.path.append(str(_find_project_root()))

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

# set the project's root folder
PROJECT_ROOT = _find_project_root()

from Daily import get_daily_forecast

# ===== VARIABLES / DATA COLLECTION =====

# Run the script and assign the collected data
daily_dataframe = get_daily_forecast()
# Set variables for collected data
x = daily_dataframe["Date"]
temp_high = daily_dataframe["Temperature High"]
temp_low = daily_dataframe["Temperature Low"]
precip_chance = daily_dataframe["Chance of Precipitation"]


# ===== PLOTTING =====
# Create 1 window (figure) with 2 subplots (temp/precip)
fig, (ax_temp, ax_precip) = plt.subplots(
    2,
    1,  # temp on top, precip on bottom -- rows=2 columns=1
    figsize=(8, 6),
    sharex=True,
    facecolor=("#efe3f4"),  # cunty purple
)

# Create temperature plots on the top panel
# Make hi temp subplot
ax_temp.plot(
    x,
    temp_high,
    marker="o",
    linewidth=1.5,
    color="#d9534f",  # red
    label="Temp (Hi)",
)
for xi, yi in zip(x, temp_high):
    ax_temp.annotate(
        f"{yi:.0f}°F",
        (xi, yi),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center",
        fontsize=8,
    )

# Make lo temp subplot
ax_temp.plot(
    x,
    temp_low,
    marker="o",
    linewidth=1.5,
    color="#4A90D9",  # blue
    label="Temp (Lo)",
)
for xi, yi in zip(x, temp_low):
    ax_temp.annotate(
        f"{yi:.0f}°F",
        (xi, yi),
        textcoords="offset points",
        xytext=(0, -14),
        ha="center",
        fontsize=8,
    )
# Set temp plot parameters
ax_temp.set_ylim(0, 110)
ax_temp.set(
    ylabel="Temperature (°F)",
    title="7-Day Forecast",
)

# Make the legend top left, outside of the plotting area
ax_temp.legend(bbox_to_anchor=(0.0, 1.02), loc="lower left", ncols=1, borderaxespad=0.1)


# Create precip bar chart on the bottom panel
bar_container = ax_precip.bar(
    x,
    precip_chance,
    width=0.6,
    color="#4a90d9",  # soft blue
    label="Chance of Precipitation",
)
# Put value labels on the bars and format (50%)
ax_precip.bar_label(bar_container, fmt="{:.0f}%")
ax_precip.set(ylim=(0, 100), ylabel="Chance of\nPrecipitation(%)")

# Make a shared x axis for the dates
ax_precip.xaxis.set_major_locator(mdates.AutoDateLocator())
ax_precip.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
ax_precip.set_xlabel("Date (Month/Day)")

# Save the file, make one if it does not exist, over-write if it does
save_path = PROJECT_ROOT / "Data" / "daily_forecast_chart.png"
save_path.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(save_path, dpi=300, bbox_inches="tight")

# Show the plots
plt.tight_layout()
plt.show()
