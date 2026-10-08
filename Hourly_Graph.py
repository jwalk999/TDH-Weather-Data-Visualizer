"""
File Name: Hourly_Graph.py

Author: Jonathan W
Date Created: 9/30/2026
Last Update: 10/7/2026
Version: 1.3.0

Scope: Builds today's hourly chart (temperature line over precipitation bars, sunrise/sunset marked) from
    Hourly.py's data.
"""

import sys
from pathlib import Path

import matplotlib.dates as mdates
import pandas as pd
from matplotlib.figure import Figure

# Make the Config package importable when this file is run on its own. Skipped in the .exe, where it's bundled.
if not getattr(sys, "frozen", False):
    _root = next((p for p in Path(__file__).resolve().parents if (p / "Config").is_dir()), None)
    if _root is None:
        raise RuntimeError("Could not find the project root (no 'Config' folder above this file)")
    sys.path.append(str(_root))

from Config.global_params import (  # noqa: E402, RUF100
    DATA_DIR,
    f_to_c,
)
from Hourly import get_hourly_forecast  # noqa: E402, RUF100

BACKGROUND_COLOR = "#efe3f4"  # Light purple
TEMP_COLOR = "#d9534f"  # Pinkish red
PRECIP_COLOR = "#4a90d9"  # Soft blue
SUNRISE_COLOR = "#f0ad4e"  # Orange
SUNSET_COLOR = "#5bc0de"  # Light blue


def make_hourly_graphs(
    hourly_df: pd.DataFrame | None = None,
    fig: Figure | None = None,
    celsius: bool = False,
    save: bool = False,
) -> Figure:
    """Builds today's hourly chart: temperature line over precipitation bars, with sunrise and sunset marked.

    Uses matplotlib's Figure directly rather than pyplot, so it embeds cleanly in Qt (FigureCanvasQTAgg) and
    regenerating it doesn't pile up hidden pyplot figures in memory.

    Args:
        hourly_df: Output of get_hourly_forecast(). Fetched fresh if not given; pass it in to avoid a second API call.
        fig: Figure to draw into, such as the one embedded in the GUI. It is cleared first. A new Figure is
            created if not given.
        celsius: Show temperatures in °C instead of °F. The DataFrame itself is left in °F.
        save: Also save the chart to Data/hourly_forecast_chart.png at 300 dpi.

    Returns:
        The finished Figure.
    """
    if hourly_df is None:
        hourly_df = get_hourly_forecast()

    if fig is None:
        fig = Figure(figsize=(12, 6))
    else:
        fig.clear()
    fig.set_facecolor(BACKGROUND_COLOR)
    fig.set_layout_engine("constrained")  # Recomputed on every draw, so the GUI chart adapts when resized

    times = hourly_df["Date"]
    temps = hourly_df["Temperature"]
    if celsius:
        temps = f_to_c(temps)
    unit = "°C" if celsius else "°F"
    pad = 6 if celsius else 10  # Room above and below the data for the point labels
    sunrise = hourly_df["Sunrise"].iloc[0]
    sunset = hourly_df["Sunset"].iloc[0]
    tz = times.dt.tz  # Axis labels default to UTC unless told otherwise

    ax_temp, ax_precip = fig.subplots(2, 1, sharex=True)

    # Full-height sunrise/sunset lines on both charts. Only the temperature chart shows a legend.
    for ax in (ax_temp, ax_precip):
        ax.axvline(sunrise, color=SUNRISE_COLOR, linestyle="--", linewidth=1.5, label="Sunrise")
        ax.axvline(sunset, color=SUNSET_COLOR, linestyle="--", linewidth=1.5, label="Sunset")

    # ===== TEMPERATURE =====
    ax_temp.plot(times, temps, marker="o", linewidth=1.5, color=TEMP_COLOR, label="Actual Temp")
    for x, temp in zip(times, temps):
        ax_temp.annotate(f"{temp:.0f}{unit}", (x, temp), textcoords="offset points", xytext=(0, 8), ha="center",
                         fontsize=8)

    # Scale to the data, with room for the labels, so very hot or below-zero locations aren't cut off
    ax_temp.set_ylim(temps.min() - pad, temps.max() + pad)
    ax_temp.set(ylabel=f"Temperature ({unit})", title=f"Hourly Forecast for {times.iloc[0]:%d-%b}")
    ax_temp.legend(bbox_to_anchor=(0.0, 1.02), loc="lower left", ncols=3, borderaxespad=0.1)

    # ===== PRECIPITATION =====
    # Bar width on a date axis is in days, so 0.6 of an hour is 0.6 / 24
    bars = ax_precip.bar(times, hourly_df["Chance of Precipitation"], width=0.6 / 24, color=PRECIP_COLOR)
    ax_precip.bar_label(bars, fmt="{:.0f}%")
    ax_precip.set(ylim=(0, 110), ylabel="Chance of\nPrecipitation (%)")  # 110 leaves room for the bar labels
    ax_precip.set_yticks(range(0, 101, 20))

    ax_precip.xaxis.set_major_locator(mdates.HourLocator(interval=2, tz=tz))
    ax_precip.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M", tz=tz))

    # First to last hour plus padding. Uses the real last row, since DST days have 23 or 25 hours.
    padding = pd.Timedelta(minutes=30)
    ax_precip.set_xlim(times.iloc[0] - padding, times.iloc[-1] + padding)

    if save:
        save_path = DATA_DIR / "hourly_forecast_chart.png"
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    return fig


if __name__ == "__main__":
    make_hourly_graphs(save=True)
