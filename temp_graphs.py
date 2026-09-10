"""
File Name: temperature_graphs.py
Author: Jonathan W
Date: 9/9/2026
Version: 0.3.0
Scope: Takes and runs function from weather_script1 to collect temperature data, then puts it in a graph
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from weather_script1 import get_weather_data

#===== CHECK SAVE PATHS AND NAMES=====
# defines the save path and file name
documents_dir = Path.home() / "Documents" / "Too Damn Hot!" / "weather_charts"
documents_dir.mkdir(parents=True, exist_ok=True)
# checks for the save file directory, creates one if it doesn't exist
norm_path = documents_dir / "climate_normals_1990-2026.png"
# this is where the document will save to (c:/user/documents/weather_charts)

need_norms = not norm_path.exists()
# only fetch norms data if chart doesn't exist

#===== DEFINE VARIABLES =====
# as collected from weather_script1
data = get_weather_data(include_norms=need_norms)
df_hour = data["df_hour"]
yesterday = data["yesterday"]
location_name = data["location_name"]


#===== PLOT HOURLY =====
fig_hour, ax = plt.subplots(figsize=(12, 5)) # to fit 24hr labels

# instructions for the chart layout
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

hourly_filename = f"temp_chart_{yesterday.strftime('%m-%d-%Y')}.png"
hourly_path = documents_dir / hourly_filename

# save the files if they don't already exist
if not hourly_path.exists():
    fig_hour.savefig(hourly_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {hourly_path}")
else:
    print(f"Skipped save - file already exists: {hourly_path}")
# prevents saving of multiple charts if the script is ran more than once



#===== PLOT NORMS =====
# only make the climate norms plot if it doesn't exist
# only makes the get_weather_call for norms if the graph hasn't already been made
# cuts down on resource use by limiting unnecessary API calls

if need_norms:
    df_norm = data["df_norm"]
    fig_norm, ax_norm = plt.subplots(figsize=(11, 6))

# instructions for graph
    plt.style.use('seaborn-v0_8-darkgrid') # grid background
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
# monthly labels
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

    fig_norm.savefig(norm_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {norm_path}")

else:
    print(f"Skipped norms - file already exists: {norm_path}")



plt.show()
# displays created graphs in new window using matplot