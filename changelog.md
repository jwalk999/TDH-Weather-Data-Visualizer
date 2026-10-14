# Changelog

All notable changes to **Too Damn Hot!** are documented here.

Version numbers follow `MAJOR.MINOR.PATCH`:
- **MAJOR** (`0.x.x`) stays `0` until the project is stable/feature-complete
- **MINOR** bumps when a new feature or file is added (e.g. a new graph script)
- **PATCH** bumps for bug fixes and small internal cleanups with no new capability

Script-specific version numbers follow `MAJOR.MINOR.PATCH`, scoped to that file alone:
- **MAJOR** stays `0` until that file's scope is considered stable/complete, then becomes `1`
- **MINOR** bumps when new functionality is added to that file
- **PATCH** bumps for bug fixes and small internal cleanups with no new capability

---
## v0.9.0

### Added
- `main.py`
  - A list of functions that acts as the logic behind the User Interface code. 
    - `load_data()` -- the main function, runs `Daily.py` and `Hourly.py`, automatically and organizes all of the collected data into variables for the rest to use
    - `class MainWindow(QMainWindow):` -- builds the window you see when you run the program
    - The setup section adds actions to the buttons and populates the data into 7 individual frames. It also creates the matplotlib graph and uses the settings from `Daily_Graph.py` and `Hourly_Graph.py` to fill in data.
    - The menu bar is also populated:
        - File
            - Refresh
                - Refresh the data to most current
            - Save Graphs
                - Opens a file save box for the graphs
            - Check Connection
                - Pings the Open-Meteo API website to check for connectivity
            - Quit
                - Closes the program
        - View
            - Fahrenheit / Celcius -- pick between °F and °C
            - Show Forecast / Show Graph -- show or hide the forcast or graph sections
            - **Daily Graph / Hourly Graph** -- Pick between the graphs for Daily or Hourly weather forecast
            - ~~Localization~~ -- Coming soon.
            - ~~Themes~~  --  Coming soon.
        - Settings 
            - ~~Set Location~~ -- Not yet implemented, opens a text box for now. 
        - Help
            - About -- Shows the about window
            - Github...  --  opens the Github url
            - **Readme...**  --  Opens the Readme for instructions
- The layout is very simple and rudimentary, I hope to add themes and some kind of localization for international users. 

### Changed
- All .py files have been structured for use in the UI, Ruff used to ensure best practices

---
## v0.8.0

### Added
- Built `main.py`
  - This is where the new main GUI file will live and what will run when launching the program.

### Fixed
- `Hourly_Graph.py` **1.0.1**
  - Fixed a missing required ymin / ymax argument when calling ax_temp.vlines


### Changed
- `Hourly_Graph.py` **1.1.1**
  - Changed all variables to hourly_ to avoid confusing daily variables
  - Turned the main function of the program into a callable script
- `Daily_Graph.py` 
  - Same as above
- Made some fun looking header commends so I can find everything
- Changed imports on all main scripts to be easier to read

---
## v0.7.0

### Added
- Built `Hourly_Graph.py`
  - Essentially the same as `Daily_Graph.py`, but this one shows the forecast for the current date between the hours 00:00 and 23:59. Labels are marked every 2 hours and it uses colors to make it easier to view. It also marks the sunrise and sunset time.
  - **Currently only shows to EST**

### Fixed
- `Daily_Graph.py` **1.1.1**
  - Fixed a double call for the bar graph (ax_precip.bar). Set the container to the actual code I wanted to create the bar graph. 
      - bar_container = ax_precip.bar(x, precip_chance)
      - This draws a second, unneeded bar graph instead of simply assigning the required bar container to the correct graph.
- Ran linting and formatting using [Ruff]

### Changed
- Changed the file headers to mark the version of each .py file. For in-house tracking of specific file versions. v1.0 files are generally untouched and feature-complete. (For now)
  - `Daily_Graph.py` has been set to an arbitrary 1.1.1 due to the change in **v0.6.1**  + the fix from above
- `Daily.py` and `Hourly.py`
  - Added a line to write down the date and time the script was last ran to make sure the data is not stale
  - Added the sunrise and sunset times in `Hourly.py` to the dataframe for graphing
- `.gitignore`
  - added files that do not need to be uploaded to repo
- Minor comment additions

---
## v0.6.1

### Changed
- `Daily_Graph.py`: 
  - Changed overall layout of the graphs: temperature chart is now separate from precipitation. Temperature chart now shows low and high temps forecasted for that specific day. There are now fun colors.

**To Do:** Look into integrating matplotlibs into freesimplegui -- !Boost Earth's magnetic field!

---

## v0.6.0

### Added
- Built `Daily_Graph.py`
  - Temperature line chart combined with a ghosted precipitation bar chart on a secondary (`twinx`) axis, in a single figure
  - Chart auto-saves to `Data/daily_forecast_chart.png` on every run, overwrites automatically
  - X-axis dates formatted as `09/30`, `10/1`, etc

### Fixed
- `Daily_Graph.py`: Fixed invalid variable references
- Removed an invalid import statement
- Fixed a misuse that was passing a DataFrame where a timezone was expected

### Changed
- `Daily.py` / `Hourly.py`: Open-Meteo client set to a shared `get_openmeteo_client()` function
- `sys.path` setup replaced with a small upward-searching `_find_project_root()` helper
- Removed unused imports
- Deleted `Collect_data.py`
- Standardized the changelog
- Moved the graph output to stay inside the main folder for portability

**To Do:** Begin integrating freesimplegui and build the user interface -- !Fix global warming!

---

## v0.5.1
- Attempting to ensure low-level coupling
  - Moved API calls to their respective script files
  - Defined a function for the API call to only be run when needed, set up in `\Config\global_params.py`
- Added docstrings to functions
- *!sun cooler failed!*

---

## v0.5.0
- Removed all uses of Meteostat
  - The use case didn't fit how the API works — historical data was consistently 1+ month out of date, and     fetching "yesterday" reliably returned `None`. Empty DataFrames can't be graphed. 🙂
- Changed major layout of the program for easier management
- Formatted primary `.py` files for readability/maintenance
- Weather data storage changed from text file to CSV
- `Daily.py` and `Hourly.py` rebuilt as callable functions for graphing and GUI use
- *!turned down the temperature!*
- *!currently researching physics to install a cooler on the sun!*
**To Do:** Build `Daily_Graph.py` and `Hourly_Graph.py` to make the graphs

---

## v0.4.0 — *The Future Is Here!*
- Cleaned up the program directory, organizing files into folders
- Integrated Open-Meteo to collect forecasting data for current date + 7 days
- Added daily forecast
  - Collects temperatures (hi/low) and precipitation chance
  - Outputs to a text file in an easy-to-read format
- Added hourly forecast
  - Collects average temperature (mean), precipitation chance, sunrise/sunset, and weather description (sunny, cloudy, etc.)
  - Outputs to a text file in an easy-to-read format
- Added `global_params.py` in the Data folder
  - Centralizes parameters used across scripts (location, date)
  - Structured for easy editing once a GUI is implemented
- Added `config.json` as a separate way to alter the user's location, for future use
- Integrated `descriptions.json`, written by GitHub user [stellasphere](https://gist.github.com/stellasphere/9490c195ed2b53c707087c8c2db4ec0c)
  - Interprets weather codes into user-readable phrases (1 = clear, etc.)
- Deleted unnecessary files and tests
- *!turned down the temperature!*

---

## v0.3.0
- Separated the scripts that collect data from the scripts that turn it into graphs
  - Cleaner, runs more efficiently
- Changed the main data collection script into a callable function with station ID and location name as parameters
- Climate normals graph script now only runs if the user hasn't run it before
  - Checks for the norms file in Documents and skips it if it exists
- Added a precipitation graph script with the same parameters as the temperature graph
  - Sometimes it doesn't rain — made sure a blank graph is not generated
- *!turned down the temperature!*

---

## v0.2.0
- Added a graph to plot monthly normal temperatures for comparison
- Changed save command to not run if the files are already present
- Added this changelog file
- Graphs now have color and are more visually appealing
- Changed the minimum temperature for the hourly graph to 30°F
- Added LaGuardia Airport, NYC as a station ID example
- Removed unnecessary files
- Added location name to the graph, changes when `location_name` var is changed
- *!turned down the temperature!*

---

## v0.1.0 — *original alpha release*
- Added a graph to plot yesterday's temperatures in Fahrenheit
