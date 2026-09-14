# TDH-Weather-Data-Visualizer
Too Damn Hot is a python-based weather data visualization tool.


In it's current state, it runs a .py file to get the current date, then uses that to connect to the meteostat library to get weather data from a selected weather station or geographical location. 
The data is then turned into a viewable line graph, it is saved to the user's pc automatically and is named using the date for a unique identifier.
The program now creates a temperature normals graph for the specific location between the years 1990 to 2026


v0.3.0 - The script is now separated into two parts for ease of use. The user can now write their own scripts using the function get_weather_data from weather_script1.py

:)

To use:

    1. Open weather_script1.py
    2. Line 19: change 'station_id' to the id corresponding to your selected location's id
        - info found on https://meteostat.net
    3. Change 'location_name' to the name of the city you are searching
    4. Run graphs.py


notes: 
    - The day is plotted on a line graph and shows points for specific times (hourly increments) only if data for that time exists in meteostat's database.

    - The climate norms chart will only run the first time, it will skip itself as long as the climate norms file exists in your documents\Too Damn Hot\weather_charts folder.

    - The hourly temperatures chart script will continue to run, but will only save if the file for that day hasn't been saved yet.


Contributions:
    - Open Meteo: 
    - Meteostat: 
    - descriptions.json: https://gist.github.com/stellasphere/9490c195ed2b53c707087c8c2db4ec0c



Disclosure on AI:
    Everything written and designed here comes from my own fingers. This project is a test bed for me to learn python and how everything works. I am using Claude Code AI to teach me the ropes. Any code generated is checked by myself for applicability and is only integrated into the code if I think it would work; with personal refinements, as needed. The main files of this program is untouched by AI and none of it is shared that I do not want *big-tech* to have. If it looks like AI generated code, it's because I'm still a beginner.  :)
