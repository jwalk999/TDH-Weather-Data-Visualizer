# TDH-Weather-Data-Visualizer
Too Damn Hot is a python-based weather data visualization tool.

In it's current state, it runs a .py file to get the current date, then uses that to connect to the meteostat library to get weather data from a selected weather station or geographical location.
The data is then turned into a viewable line graph, it is saved to the user's pc automatically and is named using the date for a unique identifier.

To use:
1. Open weather_data.py in a text editor
2. Go to lines 25, 30, 58
    - change US/EASTERN and EASTERN identifiers to your specific Time Zone (https://docs.python.org/3/library/datetime.html#timezone-objects)
4. Find line 51, and edit id="*****" to the specific weather station you want to target
    - info available on https://meteostat.net/en/
    - search for your target city and pick a weather station
5. Run weather_data.py
6. The created graph will open in a separate window, you can find the saved version at C:\Users\*USERNAME*\Documents\weather_charts\temp_chart_*date*

info:
The day is plotted on a line graph and shows points for specific times (hourly increments) only if data for that time exists in meteostat's database.
