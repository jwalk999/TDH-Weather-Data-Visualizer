Too Damn Hot is a python-based weather data visualization tool.

In it's current state, it runs a .py file to get the current date, then uses that to connect to the meteostat library to get weather data from a selected weather station or geographical location. The data is then turned into a viewable line graph, it is saved to the user's pc automatically and is named using the date for a unique identifier. The program now creates a temperature normals graph for the specific location between the years 1990 to 2026

v0.3.0 - The script is now separated into two parts for ease of use. The user can now write their own scripts using the function get_weather_data from weather_script1.py v0.4.0 - The future is here! You can now collect forecasts!

:)

To use: Forecasting -

        1. Open 'Too Damn Hot! / Data / global_params.py'
        2. Locate DEFAULT_LOCATION (at the top)
        3. Change the Longitude and Latitude to match the region you want to search
        4. Run 'Too Damn Hot! / Forecast_Graphing / Daily.py and Hourly.py'
        5. Open 'Too Damn Hot! / Data / daily_forecast.txt and hourly_forecast.txt
            - The forecast data is separated into two different text files for easier reading.

Historical -

        1. Open 'Too Damn Hot! / Data / global_params.py'
        2. Locate DEFAULT_LOCATION (at the top)
        3. Change Longitude and Latitude to match the region you want to search
        4. Go to https://meteostat.net/en/ and look up your location using any search term you want (long, lat / zip code / etc.)
        5. On the right side of the screen, under "Station Identifiers," find Meteostat: *****
            - This is the "station_id" that Meteostat uses to find the station you want to get data from
        6. In global_params.py  >  DEFAULT_LOCATION, change 'station_id' to the number you got from Meteostat's website
        7. Run 'Too Damn Hot! / Historical_Graphing / Precip.py and Temp.py
            - Each one will show you 2 graphs of the precipitation and temperature values from YESTERDAY (i.e. 'current date' minus 1 day)
            - One graph shows you the full day for yesterday, measuring precipitation or temperature
            - The second graph shows you the historical mean (norms) for temperature or precipitation between the years 1990 and 2026
                    (This can be used to compare the values for the historical mean and yesterday for a neat comparison)

notes:

- The day is plotted on a line graph and shows points for specific times (hourly increments) only if data for that time exists in meteostat's database.

- The climate norms chart will only run the first time, it will skip itself as long as the climate norms file exists in your documents\Too Damn Hot\weather_charts folder.

- The hourly temperatures chart script will continue to run, but will only save if the file for that day hasn't been saved yet.

Contributions:

- Open Meteo: https://open-meteo.com/

- Meteostat: https://meteostat.net/en/

- descriptions.json: https://gist.github.com/stellasphere/9490c195ed2b53c707087c8c2db4ec0c

Disclosure on AI: Everything written and designed here comes from my own fingers. This project is a test bed for me to learn python and how everything works. I am using Claude Code AI to teach me the ropes. Any code generated is checked by myself for applicability and is only integrated into the code if I think it would work; with personal refinements, as needed. The main files of this program is untouched by AI and none of it is shared that I do not want big-tech to have. If it looks like AI generated code, it's because I'm still a beginner. :)