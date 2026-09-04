from datetime import dt
import matplotlib.pyplot as plt
import meteostat as ms

# Specify location and time range
POINT = ms.Point(35.7332, -81.3412)  # looks up gps coords
START = dt.date('US/Eastern')
END = dt.time.now(2026, 9, 1, 23, 59)


# Get hourly data for specified range
ts = ms.hourly(
    '72301',
    START,
    END
)

df = ts.fetch(units=ms.UnitSystem.IMPERIAL)

# Plot line chart for hourly temperature
df.plot(y=[ms.Parameter.TEMP])
plt.show()