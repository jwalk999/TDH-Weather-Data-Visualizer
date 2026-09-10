"""
File Name: precip_graphs.py
Author: Jonathan W
Date: 9/10/2026
Version: 0.3.0
Scope: Takes and runs function from weather_script1 to collect precipitation data, then puts it in a graph
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from weather_script1 import get_weather_data


#===== DEFINE VARIABLES =====
# as collected from weather_script1
data = get_weather_data(include_norms=False)
df_hour = data["df_hour"]
yesterday = data["yesterday"]
location_name = data["location_name"]


#===== PLOT HOURLY =====

valid = df_hour['prcp'].notna()
x_valid = df_hour.index[valid]
y_valid = df_hour['prcp'][valid]


# only create the precipitation graph if there is precipitation data for the date range
if valid.any():

    fig_hour, ax = plt.subplots(figsize=(12, 5)) # to fit 24hr labels
# instructions for the chart layout
    ax.plot(x_valid, y_valid, marker='o', linewidth=1.5)


    for xi, yi in zip(x_valid, y_valid):
        ax.annotate(
            f"{yi}in.",
            (xi, yi),
            textcoords="offset points",
            xytext=(0, 8),
            ha='center',
            fontsize=8,
        )
    ax.set_xticks(x_valid)
# show only ticks that have associated data
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
# force ticks, 24 hours, every hour

    ax.set_ylim(0, 2)
    ax.set(
        xlabel="Time of Day (EST)",
        ylabel="Precipitation (inches)",
        title=f"Precipitation Values for {yesterday.strftime('%m-%d-%Y')}",
    )

    fig_hour.autofmt_xdate(rotation=45)  # angle the time stamps to prevent overlap

    plt.tight_layout()


#===== SAVE GRAPH=====
# only save the hourly chart if it does not already exist in the user's documents
# prevents saving of multiple charts if the script is ran more than once
    documents_dir = Path.home() / "Documents" / "Too Damn Hot!" / "weather_charts"
    documents_dir.mkdir(parents=True, exist_ok=True)
    hourly_filename = f"precip_chart_{yesterday.strftime('%m-%d-%Y')}.png"
    hourly_path = documents_dir / hourly_filename
    if not hourly_path.exists():
        fig_hour.savefig(hourly_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {hourly_path}")

    else:
        print(f"Skipped save - file already exists: {hourly_path}")
    plt.show()
# tell the user they can't make a chart that doesn't exist
else:
    print("No Precipition Data exists, skipping chart.")

