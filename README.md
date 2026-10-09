# Too Damn Hot! 🌡️

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

              \     :     /
       `.      \    :    /      .'         /$$$$$$$$                      /$$$$$$$
             .-'''''''''''-.              :__  $$__/                     : $$__  $$
           .'               '.               : $$  /$$$$$$   /$$$$$$     : $$  \ $$  /$$$$$$  /$$$$$$/$$$$  /$$$$$$$
          /  _______ _______  \              : $$ /$$__  $$ /$$__  $$    : $$  : $$ :____  $$: $$_  $$_  $$: $$__  $$
  -----  ( ==\#####/-\#####/== )  -----      : $$: $$  \ $$: $$  \ $$    : $$  : $$  /$$$$$$$: $$ \ $$ \ $$: $$  \ $$
  -----  (                     )  -----      : $$: $$  \ $$: $$  \ $$    : $$  : $$ /$$__  $$: $$ : $$ : $$: $$  : $$
          \     \_______/     /              : $$:  $$$$$$/:  $$$$$$/    : $$$$$$$/:  $$$$$$$: $$ : $$ : $$: $$  : $$
           '.               .'               :__/ \______/  \______/     :_______/  \_______/:__/ :__/ :__/:__/  :__/
             '-._________.-'
       .'      /    :    \      `.                         /$$   /$$             /$$    /$$
              /     :     \                               : $$  : $$            : $$   : $$
                                                          : $$  : $$  /$$$$$$  /$$$$$$ : $$
                                                          : $$__  $$: $$  \ $$  : $$   :__/
                                                          : $$  : $$: $$  : $$  : $$ /$$
                                                          : $$  : $$:  $$$$$$/  :  $$$$//$$
                                                          :__/  :__/ \______/    \___/ :__/


   Weather data collection & visualization  |  freesimplegui + matplotlib + Open-Meteo  |  stay hydrated
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


A Python-based weather data visualization tool. Collects a 7-day forecast for
a chosen location and turns it into readable data files and graphs.

See [`changelog.md`](./changelog.md) for full version history.

---

## Features

- 7-day daily and single-day hourly forecasts via [Open-Meteo](https://open-meteo.com/)
- Weather codes translated into plain-language descriptions
- Forecast data exported to CSV for easy reading and GUI use
- Combined temperature + precipitation-chance graph, can be saved as a PNG
- Only allows for 7-day forecasting due to Open-Meteo's API limitations

---

## How To:

1. Run TooDamnHot.exe
   - It will take a minute to load
   - A Command Line window will open, do not be alarmed: it is so python can be ran
2. Enjoy!

To Change Views:
1. Click on View
2. Pick the option you want
   - Fahrenheit  -- Temperatures in °F, auto checked ON
   - Celcius --  Temperatures in °C
   - Show Forecast -- show or hide the forecast section, auto checked ON
   - Show Graph -- show or hid the graph section, auto checked ON
   - Daily Graph -- show the 7 day forecast graph, auto checked ON
            - Temperature - the red line is the **High Temp**, the blue line is the **Low Temp**
            - Chance of Precipitation  - bar graph showing % chance of precipitation
   - Hourly Graph -- show the current day's hourly graph, 00:00am to 11:59pm
            - Temperature - red line showing the actual air temperature for each specific hour
            - Precipitation - % chance of precipitation for each specific hour
            - Orange Dotted Line - shows sunrise time
            - Blue Dotted Line - shows sunset time

Refresh the app by clicking `View / Refresh` or press *F5*
Save the graphs to your PC by clicking `View / Save Graphs` or press *Ctrl + S*
Exit by clicking the red X, `View / Quit`, or press *Ctrl + Q*


## Usage // *Deprecated*

1. Open `Too Damn Hot! / Config / global_params.py`
2. Find `DEFAULT_LOCATION` near the top
3. Change the latitude/longitude to your target region
   (after the first run, you can change location in config.json)
4. Run `Daily.py` and `Hourly.py` - makes the API call and generates a .csv file for exporting
5. Run `Daily_Graph.py` - collects data from `Daily.py` and creates a graph
   (graphs will automatically be displayed)
6. Check the `Data/` folder for:
   - `daily_forecast.csv` / `hourly_forecast.csv` — the raw forecast data
   - `daily_forecast_chart.png` — temperature + precipitation chance, combined
---

## Contributions

- **Open-Meteo** — forecast data: https://open-meteo.com/
- **descriptions.json** — weather code → description mapping, by GitHub user
  [stellasphere](https://gist.github.com/stellasphere/9490c195ed2b53c707087c8c2db4ec0c)

---

## Responsible Disclosures

Everything written and designed here comes from my own fingers. This project
is a test bed for me to learn Python and how everything works. I am using
Claude AI to teach me the ropes. Any code generated is checked by myself for
applicability and is only integrated into the code if I think it would work,
with personal refinements as needed. The main files of this program are
untouched by AI. 

This app does not collect any data on your system, it may generate a `Cache` folder, this is only used by the python 
environment used within the app. Nothing is collected or saved and you can uninstall the app by just deleting the 
`TooDamnHot` folder. API calls made to Open-Meteo are only used to retrieve data from their servers. Nothing is sent
to them.


---

## License
This project is built under the GNU GENERAL PUBLIC LICENSE, but all that mumbo jumbo basically means you can use 
the code and project in any way you want. I just ask that any changes be made on a separate Git repository and all forks 
link back to the original Main repo. Also, please keep all versions of this software free for public use.