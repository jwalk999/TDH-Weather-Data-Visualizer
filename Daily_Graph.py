"""
File Name: Daily_Graph.py

Author: Jonathan W
Date Created: 9/25/2026
Last Update: 10/6/2026
Version: 1.2.0

Scope: Builds the 7-day chart (temperature lines over precipitation bars) from Daily.py's data.
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

from Config.global_params import DATA_DIR  # noqa: E402 - must come after the sys.path setup above
from Daily import get_daily_forecast  # noqa: E402

BACKGROUND_COLOR = "#efe3f4"  # Light purple
HIGH_COLOR = "#d9534f"  # Red
LOW_COLOR = "#4a90d9"  # Blue
PRECIP_COLOR = "#4a90d9"  # Soft blue


def make_daily_graphs(daily_df: pd.DataFrame | None = None) -> Figure:
    """Builds the 7-day chart and saves it to Data/daily_forecast_chart.png.

    Uses matplotlib's Figure directly rather than pyplot, so it embeds cleanly in Qt (FigureCanvasQTAgg) and
    regenerating it doesn't pile up hidden pyplot figures in memory.

    Args:
        daily_df: Output of get_daily_forecast(). Fetched fresh if not given; pass it in to avoid a second API call.

    Returns:
        The finished Figure.
    """
    if daily_df is None:
        daily_df = get_daily_forecast()

    dates = daily_df["Date"]
    highs = daily_df["Temperature High"]
    lows = daily_df["Temperature Low"]
    tz = dates.dt.tz  # Axis labels default to UTC, which shifts dates by a day for locations east of UTC

    fig = Figure(figsize=(8, 6), facecolor=BACKGROUND_COLOR)
    ax_temp, ax_precip = fig.subplots(2, 1, sharex=True)

    # ===== TEMPERATURE =====
    ax_temp.plot(dates, highs, marker="o", linewidth=1.5, color=HIGH_COLOR, label="Temp (Hi)")
    ax_temp.plot(dates, lows, marker="o", linewidth=1.5, color=LOW_COLOR, label="Temp (Lo)")
    for x, high, low in zip(dates, highs, lows):
        ax_temp.annotate(f"{high:.0f}°F", (x, high), textcoords="offset points", xytext=(0, 8), ha="center",
                         fontsize=8)
        ax_temp.annotate(f"{low:.0f}°F", (x, low), textcoords="offset points", xytext=(0, -14), ha="center",
                         fontsize=8)

    # Scale to the data, with room for the labels, so very hot or below-zero locations aren't cut off
    ax_temp.set_ylim(lows.min() - 10, highs.max() + 10)
    ax_temp.set(ylabel="Temperature (°F)", title="7-Day Forecast")
    ax_temp.legend(bbox_to_anchor=(0.0, 1.02), loc="lower left", ncols=2, borderaxespad=0.1)

    # ===== PRECIPITATION =====
    bars = ax_precip.bar(dates, daily_df["Chance of Precipitation"], width=0.6, color=PRECIP_COLOR)  # Width in days
    ax_precip.bar_label(bars, fmt="{:.0f}%")
    # 110 leaves room for the bar labels
    ax_precip.set(ylim=(0, 110), ylabel="Chance of\nPrecipitation (%)", xlabel="Date (Month/Day)")
    ax_precip.set_yticks(range(0, 101, 20))

    ax_precip.xaxis.set_major_locator(mdates.DayLocator(tz=tz))
    ax_precip.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d", tz=tz))

    # Lay out before saving so the PNG and the GUI get the same spacing
    fig.tight_layout()
    save_path = DATA_DIR / "daily_forecast_chart.png"
    save_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(save_path, dpi=300, bbox_inches="tight")

    return fig


if __name__ == "__main__":
    make_daily_graphs()
