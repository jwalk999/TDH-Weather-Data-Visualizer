"""
File Name: Daily_Graph.py

Author: Jonathan W
Date: 9/25/2026
Version: 0.5.0

Scope: Create a nested graph (line and bar) from data collected from Daily.py
        - Calls on daily.py to get the forecast data
        - Puts it into a graph
"""

#===== IMPORTS =====
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
            raise RuntimeError(f"Could not find project root (looking for '{marker}' folder)")
        path = path.parent
    return path


sys.path.append(str(_find_project_root()))

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

# set the project's root folder
PROJECT_ROOT = _find_project_root()

from Daily import get_daily_forecast

# ===== GET DATA =====
daily_dataframe = get_daily_forecast()
x = daily_dataframe["Date"]
temp_high = daily_dataframe["Temperature High"]
precip_chance = daily_dataframe["Chance of Precipitation"]


# ===== COMBINED CHART =====
fig, ax_temp = plt.subplots(figsize=(12, 6))

# --- ghosted precipitation bars, drawn first so the line sits on top ---
ax_precip = ax_temp.twinx()
ax_precip.bar(
    x, precip_chance,
    width=0.6,
    color="#4a90d9",
    alpha=0.25,
    zorder=1,
    label="Chance of Precipitation",
)
ax_precip.set_ylim(0, 100)
ax_precip.set_ylabel("Chance of Precipitation (%)")
ax_precip.grid(False)  # avoid a second grid fighting with the primary axis

# --- temperature line, drawn on top ---
ax_temp.plot(
    x, temp_high,
    marker="o", linewidth=1.5, color="#d9534f",
    zorder=2, label="Temperature High",
)

for xi, yi in zip(x, temp_high):
    ax_temp.annotate(
        f"{yi:.0f}°F",
        (xi, yi),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center",
        fontsize=8,
        zorder=3,
    )

ax_temp.set_zorder(ax_precip.get_zorder() + 1)  # ensures the line's background stays transparent
ax_temp.patch.set_visible(False)

ax_temp.set_xticks(x)
ax_temp.xaxis.set_major_locator(mdates.AutoDateLocator())
ax_temp.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
ax_temp.set_ylim(0, 110)
ax_temp.set(
    xlabel="Date (Month/Day)",
    ylabel="Temperature (°F)",
    title="7-Day Forecast: Temperature & Chance of Precipitation",
)


# combined legend from both axes
lines_temp, labels_temp = ax_temp.get_legend_handles_labels()
lines_precip, labels_precip = ax_precip.get_legend_handles_labels()
ax_temp.legend(lines_temp + lines_precip, labels_temp + labels_precip, loc="upper left")

save_path = PROJECT_ROOT / "Data" / "daily_forecast_chart.png"
save_path.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(save_path, dpi=300, bbox_inches="tight")

plt.tight_layout()
plt.show()