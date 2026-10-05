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
- Forecast data exported to CSV for easy reading or GUI use
- Combined temperature + precipitation-chance graph, auto-saved as a PNG

---

## Project Structure

```
Too Damn Hot!/
├── Config/
│   ├── global_params.py     # shared constants, location config, API params
│   ├── config.json          # current location (edit here, or via GUI later)
│   └── descriptions.json    # WMO weather code → readable description
├── Data/                    # generated output (CSV + chart PNGs)
├── Daily.py                 # collects the daily forecast
├── Hourly.py                # collects the hourly forecast
├── Daily_Graph.py           # graphs the daily forecast
└── requirements.txt
```

---

## Usage: Forecasting

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

## Disclosure on AI

Everything written and designed here comes from my own fingers. This project
is a test bed for me to learn Python and how everything works. I am using
Claude AI to teach me the ropes. Any code generated is checked by myself for
applicability and is only integrated into the code if I think it would work,
with personal refinements as needed. The main files of this program are
untouched by AI, and none of it is shared that I do not want big-tech to
have. If it looks like AI-generated code, it's because I'm still a beginner. :)
