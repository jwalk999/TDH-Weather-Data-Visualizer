"""
File Name: Daily_Graph.py

Author: Jonathan W
Date Created: 9/25/2026
Last Update: 10/7/2026
Version: 1.3.0

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

from Config.global_params import DATA_DIR, f_to_c  # noqa: E402 - must come after the sys.path setup above
from Daily import get_daily_forecast  # noqa: E402

BACKGROUND_COLOR = "#efe3f4"  # Light purple
HIGH_COLOR = "#d9534f"  # Red
LOW_COLOR = "#4a90d9"  # Blue
PRECIP_COLOR = "#4a90d9"  # Soft blue


def make_daily_graphs(
    daily_df: pd.DataFrame | None = None,
    fig: Figure | None = None,
    celsius: bool = False,
    save: bool = False,
) -> Figure:
    """Builds the 7-day chart: temperature lines over precipitation bars.

    Uses matplotlib's Figure directly rather than pyplot, so it embeds cleanly in Qt (FigureCanvasQTAgg) and
    regenerating it doesn't pile up hidden pyplot figures in memory.

    Args:
        daily_df: Output of get_daily_forecast(). Fetched fresh if not given; pass it in to avoid a second API call.
        fig: Figure to draw into, such as the one embedded in the GUI. It is cleared first. A new Figure is
            created if not given.
        celsius: Show temperatures in °C instead of °F. The DataFrame itself is left in °F.
        save: Also save the chart to Data/daily_forecast_chart.png at 300 dpi.

    Returns:
        The finished Figure.
    """
    if daily_df is None:
        daily_df = get_daily_forecast()

    if fig is None:
        fig = Figure(figsize=(8, 6))
    else:
        fig.clear()
    fig.set_facecolor(BACKGROUND_COLOR)
    fig.set_layout_engine("constrained")  # Recomputed on every draw, so the GUI chart adapts when resized

    dates = daily_df["Date"]
    highs = daily_df["Temperature High"]
    lows = daily_df["Temperature Low"]
    if celsius:
        highs, lows = f_to_c(highs), f_to_c(lows)
    unit = "°C" if celsius else "°F"
    pad = 6 if celsius else 10  # Room above and below the data for the point labels
    tz = dates.dt.tz  # Axis labels default to UTC, which shifts dates by a day for locations east of UTC

    ax_temp, ax_precip = fig.subplots(2, 1, sharex=True)

    # ===== TEMPERATURE =====
    ax_temp.plot(dates, highs, marker="o", linewidth=1.5, color=HIGH_COLOR, label="Temp (Hi)")
    ax_temp.plot(dates, lows, marker="o", linewidth=1.5, color=LOW_COLOR, label="Temp (Lo)")
    for x, high, low in zip(dates, highs, lows):
        ax_temp.annotate(f"{high:.0f}{unit}", (x, high), textcoords="offset points", xytext=(0, 8), ha="center",
                         fontsize=8)
        ax_temp.annotate(f"{low:.0f}{unit}", (x, low), textcoords="offset points", xytext=(0, -14), ha="center",
                         fontsize=8)

    # Scale to the data, with room for the labels, so very hot or below-zero locations aren't cut off
    ax_temp.set_ylim(lows.min() - pad, highs.max() + pad)
    ax_temp.set(ylabel=f"Temperature ({unit})", title="7-Day Forecast")
    ax_temp.legend(bbox_to_anchor=(0.0, 1.02), loc="lower left", ncols=2, borderaxespad=0.1)

    # ===== PRECIPITATION =====
    bars = ax_precip.bar(dates, daily_df["Chance of Precipitation"], width=0.6, color=PRECIP_COLOR)  # Width in days
    ax_precip.bar_label(bars, fmt="{:.0f}%")
    # 110 leaves room for the bar labels
    ax_precip.set(ylim=(0, 110), ylabel="Chance of\nPrecipitation (%)", xlabel="Date (Month/Day)")
    ax_precip.set_yticks(range(0, 101, 20))

    ax_precip.xaxis.set_major_locator(mdates.DayLocator(tz=tz))
    ax_precip.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d", tz=tz))

    if save:
        save_path = DATA_DIR / "daily_forecast_chart.png"
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    return fig


if __name__ == "__main__":
    make_daily_graphs(save=True)
