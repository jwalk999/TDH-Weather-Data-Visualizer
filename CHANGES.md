# Too Damn Hot! v0.2: sidebar layout (design 2a)

## Drop-in steps
1. Copy these files into the repo root, replacing the old ones:
   `main.py`, `main_window.ui`, `theme.py`, `Forecasts.py`, and the new `widgets.py` and `alerts.py`.
2. Regenerate the UI module:
   ```
   pyside6-uic main_window.ui -o ui_main_window.py
   ```
3. Fonts (optional, the app falls back to Calibri without them). Download Archivo from Google Fonts and copy the
   static files into `assets/fonts/`:
   - `Archivo-Regular.ttf`, `Archivo-Bold.ttf`
   - `Archivo_ExtraCondensed-Black.ttf`, `Archivo_ExtraCondensed-ExtraBold.ttf`
4. Radar uses Qt WebEngine. It's included in the `pyside6` package; if it's missing, run `pip install PySide6-Addons`.
5. auto-py-to-exe: add `assets/fonts` → `assets/fonts`, and make sure `widgets.py` and `alerts.py` are picked up.
   QtWebEngine adds about 100 MB to the build.

## What changed
- **Layout:** sidebar (`navList`) plus `QStackedWidget` (`pages`) with Now, Hourly, 10-Day, Alerts, Radar,
  Locations and Settings. The menubar is unchanged.
- **Now page:** a hero card with a big temperature, the quip as a headline under its quips.py bucket, a stat row
  (humidity, wind, UV, precip) and sunrise/sunset. Below that, 7 day cards (`tempFrame1-7`) and the matplotlib
  chart. The separate `precipFrame1-7` cards are merged into the day cards.
- **Hourly and 10-Day pages:** rows built in code (`widgets.HourRow`, `widgets.DayRow`). Colors come from
  `theme.heat_color()`, which stays the same in °C.
- **Forecasts.py:** `get_forecast()` still returns 7 days for the graph scripts. The new
  `get_forecast_and_current()` adds Open-Meteo `current` conditions and 10 days (Open-Meteo allows up to 16).
- **alerts.py:** active NWS alerts from api.weather.gov. Non-US locations return none.
- **Settings page:** units, theme, show forecast/graph and default location. These are kept in sync with the
  View menu. It also adds a heat-alert threshold that shows the banner even when NWS has nothing.
- **Locations page:** saved places are stored in QSettings, each shown with its current temperature, plus
  Make default and Remove buttons.

## Not changed
`quips.py`, `geocoding.py`, `Daily_Graph.py`, `Hourly_Graph.py`, `Config/*`.
