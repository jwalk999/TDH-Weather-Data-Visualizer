"""
File Name: Hourly_Graph.py

Author: Jonathan W
Date Created: 9/30/2026
Last Update: 10/2/2026
Version: 1.1.2

Scope: Create a nested graph (line and bar) from data collected from Hourly.py
"""

# ============================================================================
# =============================== IMPORTS ====================================
# ============================================================================

# Add the project's parent directory to Python's import search path
# This allows the file to import modules from the Config package
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from Hourly import get_hourly_forecast


# Create function to mark the root directory
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
# Set the project's root folder
sys.path.append(str(_find_project_root()))
PROJECT_ROOT = _find_project_root()



# ============================================================================
# =============================== VARIABLES ==================================
# ============================ DATA COLLECTION ===============================
# ============================================================================

# Run the script and assign the collected data
hourly_dataframe = get_hourly_forecast()

# Label the collected data and point variables to dataframes
x_hourly = hourly_dataframe["Date"]
hourly_temp_real = hourly_dataframe["Temperature"]
hourly_precip_chance = hourly_dataframe["Chance of Precipitation"]
hourly_weather_description = hourly_dataframe["Weather Description"]
hourly_sunrise_time = hourly_dataframe["Sunrise"]
hourly_sunset_time = hourly_dataframe["Sunset"]


# ============================================================================
# ============================ PLOTTING ======================================
# ============================================================================

# Define the graphing section as a callable function
def make_hourly_graphs():

    """
    Use data collected from Hourly.py to create a line graph and bar chart

    Params: x_hourly: the x axis, timestamps
            hourly_temp_real: The real air temperature recorded
            hourly_precip_chance: % Chance of precipitation for each hour
            hourly_weather_description: e.g sunny, cloudy, clear, etc
            hourly_sunrise_time: The timestamp recorded for sunrise
            hourly_sunset_time: The timestamp recorded for sunset

    Returns: Create the graph then save it into memory for the GUI to use
    """

    # Create 1 window (figure) with 2 subplots (temp/precip)
    fig, (ax_temp, ax_precip) = plt.subplots(
        2,
        1,
        figsize=(12, 6),
        sharex=True,  # graphs share the x axis
        facecolor=("#efe3f4"),  # cunty purple-white
    )

# =============================================================================
# ======================= CREATE TEMPERATURE CHART ============================
# =============================================================================
    # Make real air temperature subplot
    ax_temp.plot(
        x_hourly,
        hourly_temp_real,
        marker="o",
        linewidth=1.5,
        color=("#d9534f"),  # pinkish red
        label="Actual Temp",
    )
    for xi, yi in zip(x_hourly, hourly_temp_real):
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
        hourly_sunrise_time.iloc[0],
        0, # y min == all the way to the bottom
        110, # y max == all the way to the top
        color="#f0ad4e", # sunrise orange
        linestyle="dashed",
        lw=1.5,
    )
    ax_temp.vlines(
        hourly_sunset_time.iloc[0],
        0,
        110,
        color="#5bc0de", # sunset blue
        linestyle="dashed",
        lw=1.5,
    )
    # Set temp plot paremeters
    ax_temp.set_ylim(0, 110)
    ax_temp.set(
        ylabel="Temperature (°F)",
        title=f"Hourly Forecast for {x_hourly[1]:%d-%b}",
    )

    # Make the legend top left, outside of the plotting area
    ax_temp.legend(bbox_to_anchor=(0.0, 1.02), loc="lower left", ncols=1, borderaxespad=0.1)


# =============================================================================
# ======================= CREATE PRECIPITATION CHART ==========================
# =============================================================================

    bar_container = ax_precip.bar(
        x_hourly,
        hourly_precip_chance,
        width=0.6,
        color="#4a90d9",  # soft blue
        label="Chance of Precipitation",
    )
    # Put value labels on the bars and format (50%)
    ax_precip.bar_label(bar_container, fmt="{:.0f}%")
    ax_precip.set(ylim=(0, 100), ylabel=("Chance of\nPrecipitation (%)"))
    # Copy the vertical lines from above
    ax_precip.vlines(
        hourly_sunrise_time.iloc[0],
        0,
        110,
        color="#f0ad4e", # sunrise orange
        linestyle="dashed",
        lw=1.5,
        label="Sunrise",
    )
    ax_precip.vlines(
        hourly_sunset_time.iloc[0],
        0,
        110,
        color="#5bc0de", # sunset blue
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
    ax_precip.set_xlim(x_hourly[0] - padding, x_hourly[23] + padding)


    # Save the created chart as a png
    save_path = PROJECT_ROOT / "Data" / "hourly_forecast_chart.png"
    save_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.tight_layout()

    return fig


# Make this file runnable by itself for testing
if __name__ == "__main__":
    make_hourly_graphs()

