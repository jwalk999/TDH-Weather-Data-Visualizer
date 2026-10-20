"""
File Name: main.py

Author: Jonathan W
Date Created: 10/5/2026
Last Update: 10/20/2026
Version: 0.2.0

Scope: Creates the main GUI environment for the application. Sidebar + stacked pages layout:
    Now, Hourly, 10-Day, Alerts, Radar, Locations and Settings.
"""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#              \     :     /
#       `.      \    :    /      .'         /$$$$$$$$                      /$$$$$$$
#             .-'''''''''''-.              :__  $$__/                     : $$__  $$
#           .'               '.               : $$  /$$$$$$   /$$$$$$     : $$  \ $$  /$$$$$$  /$$$$$$/$$$$  /$$$$$$$
#          /  _______ _______  \              : $$ /$$__  $$ /$$__  $$    : $$  : $$ :____  $$: $$_  $$_  $$: $$__  $$
#  -----  ( ==\#####/-\#####/== )  -----      : $$: $$  \ $$: $$  \ $$    : $$  : $$  /$$$$$$$: $$ \ $$ \ $$: $$  \ $$
#  -----  (                     )  -----      : $$: $$  \ $$: $$  \ $$    : $$  : $$ /$$__  $$: $$ : $$ : $$: $$  : $$
#          \     \_______/     /              : $$:  $$$$$$/:  $$$$$$/    : $$$$$$$/:  $$$$$$$: $$ : $$ : $$: $$  : $$
#           '.               .'               :__/ \______/  \______/     :_______/  \_______/:__/ :__/ :__/:__/  :__/
#             '-._________.-'
#       .'      /    :    \      `.                         /$$   /$$             /$$    /$$
#              /     :     \                               : $$  : $$            : $$   : $$
#                                                          : $$  : $$  /$$$$$$  /$$$$$$ : $$
#                                                          : $$ $$ $$: $$  \ $$  : $$   :__/
#                                                          : $$  : $$: $$  : $$  : $$ /$$
#                                                          : $$  : $$:  $$$$$$/  :  $$$$//$$
#                                                          :__/  :__/ \______/    \___/ :__/
#
#
#   Weather data collection & visualization  | PySide6 + matplotlib + Open-Meteo  |  stay hydrated
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ============================================================================
# =============================== IMPORTS ====================================
# ============================================================================

# Splash screen helpers come first so the bar can update while the heavy imports below load.

import json
import socket
import sys
from pathlib import Path

try:
    import pyi_splash  # Only exists inside the PyInstaller build
except ImportError:
    pyi_splash = None

SPLASH_STEPS = 7


def splash_progress(step: int, label: str) -> None:
    """Show a text progress bar on the PyInstaller splash screen.

    Does nothing when running from source or after the splash has closed.

    Args:
        step: Current step number, 1 to ``SPLASH_STEPS``.
        label: Short description of the current step.
    """
    if pyi_splash and pyi_splash.is_alive():
        filled = round(10 * step / SPLASH_STEPS)
        pyi_splash.update_text(f"{'█' * filled}{'░' * (10 - filled)}  {label}")


def close_splash() -> None:
    """Close the PyInstaller splash screen if it is still open."""
    if pyi_splash and pyi_splash.is_alive():
        pyi_splash.close()


splash_progress(1, "Loading pandas...")
import pandas as pd
import requests

splash_progress(2, "Loading matplotlib...")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

splash_progress(3, "Loading Qt...")
from PySide6.QtCore import QSettings, Qt, QUrl
from PySide6.QtGui import QAction, QActionGroup, QDesktopServices, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QInputDialog,
    QLabel,
    QMainWindow,
    QMenu,
    QMessageBox,
    QSizePolicy,
    QVBoxLayout,
)

splash_progress(4, "Loading app modules...")
import theme
from alerts import get_alerts
from Config.global_params import (
    f_to_c,
    get_weather_description,
    load_descriptions,
    load_location,
    save_location,
)
from Daily_Graph import make_daily_graphs
from Forecasts import get_current_temp, get_forecast_and_current
from geocoding import format_match, geocode, match_to_location
from Hourly_Graph import make_hourly_graphs
from quips import HIGH_F, LOW_F, NORMAL_F, V_HIGH_F, get_quip
from ui_main_window import Ui_MainWindow
from widgets import (
    AlertCard,
    DayRow,
    HourRow,
    clear_layout,
    load_radar,
    make_label,
    make_radar_widget,
    place_row,
)

HERE = Path(__file__).parent
ICON_PATH = HERE / "hot-temperature.png"
README_PATH = HERE / "README.md"
GITHUB_URL = "https://github.com/jwalk999/TDH-Weather-Data-Visualizer"
VERSION = "0.2"
FORECAST_DAYS = 10

# Sidebar rows, in the same order as the pages in the QStackedWidget
PAGE_NOW, PAGE_HOURLY, PAGE_TENDAY, PAGE_ALERTS, PAGE_RADAR, PAGE_LOCATIONS, PAGE_SETTINGS = range(7)

HEAT_TIPS = [
    "Drink water before you feel thirsty.",
    "Check on neighbors, older relatives and pets.",
    "Never leave anyone in a parked car. Not even for a minute.",
    "Do outdoor work before 10 AM or after 7 PM.",
]


# =============================================================================
# ============================== FORMATTING ===================================
# =============================================================================

def _num(value, default: float = 0.0) -> float:
    """Returns ``value`` as a float, or ``default`` if it's missing or NaN (Open-Meteo leaves gaps far out)."""
    return default if value is None or pd.isna(value) else float(value)


def compass(degrees: float) -> str:
    """Turns a wind direction in degrees into an 8-point compass label, e.g. 225 -> "SW"."""
    return ["N", "NE", "E", "SE", "S", "SW", "W", "NW"][round(degrees / 45) % 8]


def uv_label(uv: float) -> str:
    """Turns a UV index into the WHO category name."""
    for limit, name in ((3, "low"), (6, "moderate"), (8, "high"), (11, "very high")):
        if uv < limit:
            return name
    return "extreme"


def bucket_name(temp_f: float) -> str:
    """Names the quips.py temperature bucket a reading falls in."""
    for limit, name in ((V_HIGH_F, "Too damn hot"), (HIGH_F, "Hot"), (NORMAL_F, "Normal"), (LOW_F, "Chilly")):
        if temp_f >= limit:
            return name
    return "Freezing"


def bucket_kicker(temp_f: float) -> str:
    """The small caption above the quip headline, e.g. "TOO DAMN HOT BUCKET · 95°F+"."""
    for limit, name in ((V_HIGH_F, "TOO DAMN HOT"), (HIGH_F, "HOT"), (NORMAL_F, "NORMAL"), (LOW_F, "CHILLY")):
        if temp_f >= limit:
            return f"{name} BUCKET · {limit}°F+"
    return f"FREEZING BUCKET · UNDER {LOW_F}°F"


def fmt_hour(stamp: pd.Timestamp) -> str:
    """Formats a timestamp as a short hour, e.g. "2 PM"."""
    return stamp.strftime("%I %p").lstrip("0")


# =============================================================================
# ============================== DATA FETCH ===================================
# ==============================AND LOADING ===================================
# =============================================================================

# Pass the scroll function through the figure canvas so scrolling works on the graphs
class ScrollPassthroughCanvas(FigureCanvasQTAgg):
    """A matplotlib canvas that lets the mouse wheel scroll the page instead of the chart"""

    def wheelEvent(self, event):  # noqa: N802 - Qt override
        """Pass the wheel event to the parent widget.

        Args:
            event (QWheelEvent): The mouse wheel event.
        """
        event.ignore()


def load_data():
    """
    Load current conditions, today's hours, the 10-day forecast and active alerts.
    All units are held in Imperial format; the window formats them according to user settings.

    Returns:
        tuple: ``(current, days, hours, alerts, daily_df, hourly_df)``. daily_df and hourly_df are the raw
        dataframes, used for graphing.

    ``current`` keys: location, temp_f, feels_f, high_f, low_f, humidity, wind_mph, wind_dir, uv, precip_chance,
        condition, sunrise, sunset, quip, date, updated, latitude, longitude.
    ``days`` is a list of dicts (one per day) with day, date, high_f, low_f, precip_chance, precip_in,
        condition and quip.
    ``hours`` is a list of dicts with stamp, temp_f, feels_f, precip_chance and is_now.
    ``alerts`` is the list from alerts.get_alerts(), or empty if NWS couldn't be reached.

    Raises:
        requests.exceptions.ConnectionError: If Open-Meteo cannot be reached
    """
    location = load_location()
    tz = location["timezone"]
    daily_df, hourly_df, now = get_forecast_and_current(location, days=FORECAST_DAYS)
    descriptions = load_descriptions()
    now_ts = pd.Timestamp.now(tz=tz)
    today = daily_df.iloc[0]

    past = hourly_df[hourly_df["Date"] <= now_ts]
    now_row = past.iloc[-1] if len(past) else hourly_df.iloc[0]

    temp_f = now["Temperature"]
    condition = get_weather_description(now["Weather Code"], descriptions, "day" if now["Is Day"] else "night")

    current = {
        "location": location["location_name"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "temp_f": temp_f,
        "feels_f": now["Feels Like"],
        "high_f": _num(today["Temperature High"], temp_f),
        "low_f": _num(today["Temperature Low"], temp_f),
        "humidity": now["Humidity"],
        "wind_mph": now["Wind Speed"],
        "wind_dir": compass(now["Wind Direction"]),
        "uv": now["UV Index"],
        "precip_chance": int(_num(now_row["Chance of Precipitation"])),
        "condition": condition,
        "sunrise": today["Sunrise"].strftime("%I:%M %p").lstrip("0"),
        "sunset": today["Sunset"].strftime("%I:%M %p").lstrip("0"),
        "quip": get_quip(temp_f, condition),
        "date": f"{now_ts:%A, %B} {now_ts.day}",  # %-d isn't supported on Windows
        "updated": now_ts.strftime("%I:%M %p").lstrip("0"),
    }

    days = []
    for i, row in enumerate(daily_df.to_dict("records")):
        high_f = _num(row["Temperature High"])
        day_condition = get_weather_description(_num(row["Weather Code"]), descriptions, "day")
        days.append({
            "day": "Today" if i == 0 else row["Date"].strftime("%a"),
            "date": f"{row['Date'].month}/{row['Date'].day}",
            "high_f": high_f,
            "low_f": _num(row["Temperature Low"]),
            "precip_chance": int(_num(row["Chance of Precipitation"])),
            "precip_in": _num(row["Precipitation"]),
            "condition": day_condition,
            "quip": get_quip(high_f, day_condition),
        })

    hours = [
        {
            "stamp": row["Date"],
            "temp_f": _num(row["Temperature"]),
            "feels_f": _num(row["Feels Like"]),
            "precip_chance": int(_num(row["Chance of Precipitation"])),
            "is_now": row["Date"].hour == now_ts.hour,
        }
        for row in hourly_df.to_dict("records")
    ]

    # Alerts are a bonus; a failed NWS call shouldn't block the forecast
    try:
        alerts = get_alerts(location["latitude"], location["longitude"])
    except requests.RequestException:
        alerts = []

    return current, days, hours, alerts, daily_df, hourly_df


class MainWindow(QMainWindow):
    """The Too Damn Hot! main window.

    Wraps the Qt Designer-generated layout (sidebar + stacked pages), populates it with ``load_data()``,
    and handles every menu action and settings control.

    Attributes:
        ui (Ui_MainWindow):     Generated UI, every Designer widget is an attribute.
        settings (QSettings):   Saved preferences (theme, units, heat threshold, saved places).
        current (dict | None):  Current conditions from the last refresh, or None before the first load.
        days (list[dict]):      Daily forecast dicts from the last refresh.
        hours (list[dict]):     Today's hourly dicts from the last refresh.
        alerts (list[dict]):    Active NWS alerts from the last refresh.
        use_celsius (bool):     True when the user picks Celsius.
        heat_threshold_f (int): Feels-like temperature (°F) that triggers the in-app heat banner.
        day_cells (list[dict[str, QLabel]]): Label sets for the 7 day cards on the Now page.
        figure (Figure):        The matplotlib figure shown in ``plotArea``.
        canvas (FigureCanvasQTAgg): The Qt widget that displays ``figure``.
        radar_view (QWidget | None): The radar map, built the first time the Radar page opens.
    """

    def __init__(self):
        """Build the window, set up widgets and menus, and load data."""
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        if ICON_PATH.exists():
            self.setWindowIcon(QIcon(str(ICON_PATH)))

        self.settings = QSettings("TooDamnHot", "TooDamnHot")
        self.current = None
        self.days = []
        self.hours = []
        self.alerts = []
        self.daily_df = None
        self.hourly_df = None
        self.graph_mode = "daily"
        self.use_celsius = self.settings.value("celsius", False, type=bool)
        self.heat_threshold_f = self.settings.value("heat_threshold_f", 105, type=int)
        self.radar_view = None
        self.theme_actions: dict[str, QAction] = {}

        self._setup_nav()
        self._setup_forecast_frames()
        self._setup_plot()
        self._setup_menus()
        self._build_theme_menu()
        self._setup_settings_page()
        self.ui.addLocationButton.clicked.connect(self.add_place)
        self.ui.alertBanner.hide()
        self.change_theme(self.settings.value("theme", theme.DEFAULT_THEME))
        self.statusBar().showMessage("Ready")
        splash_progress(6, "Fetching forecast...")
        self.refresh()

    # ====================================================================
    # ====================================================================
    # ============================== SETUP ===============================
    # ====================================================================
    # ====================================================================

    def _setup_nav(self):
        """Connect the sidebar to the stacked pages and start on the Now page."""
        self.ui.navList.currentRowChanged.connect(self._on_page_changed)
        self.ui.navList.setCurrentRow(PAGE_NOW)
        self.ui.alertLinkLabel.linkActivated.connect(lambda _link: self.ui.navList.setCurrentRow(PAGE_ALERTS))

    def _on_page_changed(self, row: int):
        """
        Show the page for a sidebar row. The Radar and Locations pages load lazily the first time they're needed.

        Args:
            row: Sidebar row, one of the PAGE_* constants.
        """
        self.ui.pages.setCurrentIndex(row)
        if row == PAGE_RADAR:
            self._ensure_radar()
        elif row == PAGE_LOCATIONS:
            self._refresh_places()

    def _setup_forecast_frames(self):
        """
        Give each empty Designer day frame (``tempFrame1`` - ``tempFrame7``) a card layout with four labels.

        Stores the labels for each in ``self.day_cells``, in day order.
        """
        self.day_cells = [self._build_cell(getattr(self.ui, f"tempFrame{i}")) for i in range(1, 8)]

    @staticmethod
    def _build_cell(frame):
        """
        Add a vertical layout with day, high, low and precip labels to a frame.

        Args:
            frame (QFrame): An empty frame with no layout.

        Returns:
            dict[str, QLabel]: The labels keyed by ``"day"``, ``"main"``, ``"low"`` and ``"precip"``, top to bottom.
        """
        frame.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        frame.setMinimumWidth(70)
        frame.setProperty("card", True)  # Picks up the rounded card style from theme.build_stylesheet()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(2)
        cell = {}
        for key in ("day", "main", "low", "precip"):
            label = QLabel("-", frame)
            label.setProperty("role", key)  # Lets the stylesheet color each line
            layout.addWidget(label)
            cell[key] = label
        return cell

    def _setup_plot(self):
        """
        Create the matplotlib figure and embed its canvas in ``plotArea``.

        Uses the layout set in Designer, or creates one if ``plotArea`` has lost it.
        """
        self.figure = Figure()
        self.canvas = ScrollPassthroughCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout = self.ui.plotArea.layout() or QVBoxLayout(self.ui.plotArea)
        layout.addWidget(self.canvas)

    def _setup_menus(self):
        """
        Connect every menu action to its handler.

        Also groups Fahrenheit/Celsius so only one can be checked, and makes the Show Graph and Show Forecast
        actions checkable toggles.
        """
        ui = self.ui

        # File
        ui.action_Reload_Data.triggered.connect(self.refresh)
        ui.actionSave.triggered.connect(self.save_graph)
        ui.action_Check_Connection.triggered.connect(self.check_connection)
        ui.action_Quit.triggered.connect(self.close)

        # View
        units = QActionGroup(self)
        units.addAction(ui.action_Units)
        units.addAction(ui.actionCelcius)
        ui.action_Units.setChecked(True)
        ui.actionCelcius.toggled.connect(self.set_celsius)
        if self.use_celsius:
            ui.actionCelcius.setChecked(True)

        for action, widget in ((ui.actionShow_Forecast, ui.forecastBox), (ui.actionShow_Graph, ui.plotArea)):
            action.setCheckable(True)
            action.setChecked(True)
            action.toggled.connect(widget.setVisible)

        ui.action_Localization.triggered.connect(lambda: self.not_ready("Localization"))

        # Graphs
        graphs = QActionGroup(self)
        for mode, text in (("daily", "&Daily Graph"), ("hourly", "&Hourly Graph")):
            action = QAction(text, self)
            action.setCheckable(True)
            action.setChecked(mode == "daily")
            graphs.addAction(action)
            ui.menu_View.insertAction(ui.action_Localization, action)
            action.triggered.connect(lambda _checked, m=mode: self.set_graph_mode(m))
        ui.menu_View.insertSeparator(ui.action_Localization)

        # Settings
        ui.actionSet_Location.triggered.connect(self.set_location)

        # Help
        ui.actionAbout.triggered.connect(self.show_about)
        ui.actionReadme.triggered.connect(self.open_readme)
        ui.actionGithub.triggered.connect(lambda: QDesktopServices.openUrl(QUrl(GITHUB_URL)))

    def _build_theme_menu(self):
        """
        Replace Designer's View > Themes placeholder with a submenu of checkable themes.

        Entries come from ``theme.THEMES`` in order, with the active theme checked. The submenu is inserted
        where the placeholder sat and the placeholder is hidden, so regenerating the .ui file doesn't break it.
        """
        menu = QMenu(self.ui.action_Themes.text(), self)
        group = QActionGroup(self)  # Exclusive by default, so only one theme is checked
        for name in theme.THEMES:
            action = QAction(name, self)
            action.setCheckable(True)
            action.setChecked(name == theme.current().name)
            action.triggered.connect(lambda _checked, n=name: self.change_theme(n))
            group.addAction(action)
            menu.addAction(action)
            self.theme_actions[name] = action
        self.ui.menu_View.insertMenu(self.ui.action_Themes, menu)
        self.ui.action_Themes.setVisible(False)

    def _setup_settings_page(self):
        """Fill the Settings page controls and keep them in sync with the View menu."""
        ui = self.ui
        ui.unitsCombo.setCurrentIndex(1 if self.use_celsius else 0)
        ui.unitsCombo.currentIndexChanged.connect(
            lambda i: (ui.actionCelcius if i == 1 else ui.action_Units).setChecked(True)
        )

        ui.themeCombo.addItems(list(theme.THEMES))
        ui.themeCombo.setCurrentText(theme.current().name)
        ui.themeCombo.currentTextChanged.connect(self.change_theme)

        # setChecked() only emits toggled when the value changes, so these two-way links don't loop
        for check, action in ((ui.showForecastCheck, ui.actionShow_Forecast), (ui.showGraphCheck, ui.actionShow_Graph)):
            check.toggled.connect(action.setChecked)
            action.toggled.connect(check.setChecked)

        ui.heatThresholdSpin.setValue(self.heat_threshold_f)
        ui.heatThresholdSpin.valueChanged.connect(self.set_heat_threshold)
        ui.changeLocationButton.clicked.connect(self.set_location)

    # ====================================================================
    # ====================================================================
    # ============================== DATA ================================
    # ====================================================================
    # ====================================================================

    def refresh(self):
        """
        Reload weather data and update the window.

        Any exception from ``load_data()`` is caught and shown in a warning dialog.
        A failed fetch leaves the previous data on screen.
        Runs on the main thread, so the window is unresponsive while loading.
        """
        self.statusBar().showMessage("Loading Data...")
        QApplication.processEvents()  # show message before fetching
        try:
            (self.current, self.days, self.hours, self.alerts,
             self.daily_df, self.hourly_df) = load_data()
        except Exception as err:  # throw an error without crashing  # noqa: BLE001
            close_splash()  # The splash stays on top and would hide the dialog
            QMessageBox.warning(self, "Refresh Failed", f"Couldn't load weather data:\n{err}")
            self.statusBar().showMessage("Refresh failed")
            return
        self.update_display()
        if self.radar_view is not None:
            load_radar(self.radar_view, self.current["latitude"], self.current["longitude"])
        self.statusBar().showMessage(f"Open-Meteo · updated {self.current['updated']} · F5 to refresh")

    def fmt_temp(self, temp_f: float) -> str:
        """
        Format a temperature with its unit, e.g. "99°F" or "37°C".

        Args:
            temp_f: Temperature in degrees Fahrenheit.

        Returns:
            str: The temperature rounded to a whole number with the selected unit.
        """
        if self.use_celsius:
            return f"{f_to_c(temp_f):.0f}°C"
        return f"{temp_f:.0f}°F"

    def fmt_deg(self, temp_f: float) -> str:
        """Format a temperature with just a degree sign, e.g. "99°", for tight spots like the day cards."""
        value = f_to_c(temp_f) if self.use_celsius else temp_f
        return f"{value:.0f}°"

    def fmt_precip(self, precip_in: float) -> str:
        """
        Format a precipitation amount for display in the user's selected unit.

        Args:
            precip_in: Precipitation in inches.

        Returns:
            str: Millimetres rounded to a whole number when Celsius is selected, otherwise inches to two decimals.
        """
        if self.use_celsius:
            return f"{precip_in * 25.4:.0f} mm"
        return f"{precip_in:.2f} in"

    def fmt_wind(self, mph: float, direction: str) -> str:
        """Format wind speed and direction in the user's unit system, e.g. "SW 6 mph" or "SW 10 km/h"."""
        if self.use_celsius:
            return f"{direction} {mph * 1.609:.0f} km/h"
        return f"{direction} {mph:.0f} mph"

    @staticmethod
    def _stat_html(name: str, value: str) -> str:
        """Two-line rich text for the stat row: a small muted caption over the value."""
        muted = theme.current().muted
        return (f"<span style='color:{muted};font-size:11px'>{name.upper()}</span><br>"
                f"<span style='font-size:19px'>{value}</span>")

    def update_display(self):
        """
        Write the cached data into every page and redraw the graph.

        Does nothing if no data has loaded yet. Called after each refresh and whenever units or theme change.
        """
        if self.current is None:
            return

        ui, cur, colors = self.ui, self.current, theme.current()
        unit = "°C" if self.use_celsius else "°F"
        number = f"{f_to_c(cur['temp_f']) if self.use_celsius else cur['temp_f']:.0f}"

        # ===== NOW =====
        ui.locationLabel.setText(cur["location"])
        ui.dateLabel.setText(f"{cur['date']} · updated {cur['updated']}")
        ui.bigtempLabel.setText(f"{number}<span style='font-size:36px;color:{colors.hot}'>{unit}</span>")
        ui.bigprecLabel.setText(
            f"{cur['condition']} · Feels like <b style='color:{colors.hot}'>{self.fmt_deg(cur['feels_f'])}</b>"
        )
        ui.hiloLabel.setText(
            f"H <span style='color:{colors.hot}'>{self.fmt_deg(cur['high_f'])}</span> · "
            f"L <span style='color:{colors.cool}'>{self.fmt_deg(cur['low_f'])}</span>"
        )
        ui.quipKickerLabel.setText(bucket_kicker(cur["temp_f"]))
        ui.quipLabel.setText(cur["quip"])
        ui.humidityLabel.setText(self._stat_html("Humidity", f"{cur['humidity']:.0f}%"))
        ui.windLabel.setText(self._stat_html("Wind", self.fmt_wind(cur["wind_mph"], cur["wind_dir"])))
        ui.uvLabel.setText(self._stat_html("UV index", f"{cur['uv']:.0f} · {uv_label(cur['uv'])}"))
        ui.precipNowLabel.setText(self._stat_html("Precip", f"{cur['precip_chance']}%"))
        ui.sunriseLabel.setText(f"● Sunrise {cur['sunrise']}")
        ui.sunsetLabel.setText(f"● Sunset {cur['sunset']}")

        ui.tempsLabel.setText("Next 7 days")
        for day, cell in zip(self.days[:7], self.day_cells):
            cell["day"].setText(day["day"])
            cell["main"].setText(self.fmt_deg(day["high_f"]))
            cell["low"].setText(self.fmt_deg(day["low_f"]))
            cell["precip"].setText(f"{day['precip_chance']}% · {self.fmt_precip(day['precip_in'])}")

        self._update_alert_banner()
        self._render_hourly()
        self._render_ten_day()
        self._render_alerts()

        alerts_item = ui.navList.item(PAGE_ALERTS)
        alerts_item.setText(f"Alerts  ({len(self.alerts)})" if self.alerts else "Alerts")
        ui.locationValueLabel.setText(cur["location"])
        self.draw_graph()

    def _peak_feels(self) -> float | None:
        """Today's highest feels-like temperature in °F, or None before the first load."""
        return max((h["feels_f"] for h in self.hours), default=None)

    def _update_alert_banner(self):
        """
        Show the banner on the Now page for the most severe NWS alert, or for the user's own heat threshold
        when NWS has nothing. Hidden otherwise.
        """
        ui = self.ui
        peak = self._peak_feels()
        if self.alerts:
            first = self.alerts[0]
            more = f" · +{len(self.alerts) - 1} more" if len(self.alerts) > 1 else ""
            until = f"Until {first['ends']}" if first["ends"] else "In effect"
            ui.alertTitleLabel.setText(first["event"])
            ui.alertDetailLabel.setText(f"{until}{more}")
        elif peak is not None and peak >= self.heat_threshold_f:
            ui.alertTitleLabel.setText("Heat index alert")
            ui.alertDetailLabel.setText(
                f"Feels like up to {self.fmt_temp(peak)} today (your limit is {self.fmt_temp(self.heat_threshold_f)})"
            )
        else:
            ui.alertBanner.hide()
            return
        ink = theme.current().highlighted_text
        ui.alertLinkLabel.setText(f"<a href='#alerts' style='color:{ink};text-decoration:none'><b>Details →</b></a>")
        ui.alertBanner.show()

    def _render_hourly(self):
        """Rebuild the Hourly page rows and its one-line summary."""
        layout = self.ui.hourlyList.layout()
        clear_layout(layout)
        if not self.hours:
            return

        hottest = max(self.hours, key=lambda h: h["temp_f"])
        wettest = max(self.hours, key=lambda h: h["precip_chance"])
        summary = f"Peaks at {self.fmt_deg(hottest['temp_f'])} around {fmt_hour(hottest['stamp'])}."
        if wettest["precip_chance"] > 0:
            summary += f" Rain chance tops out at {wettest['precip_chance']}% near {fmt_hour(wettest['stamp'])}."
        else:
            summary += " No rain in sight. Not even a little."
        self.ui.hourlySubtitle.setText(summary)

        for hour in self.hours:
            layout.addWidget(HourRow(
                fmt_hour(hour["stamp"]),
                self.fmt_deg(hour["temp_f"]),
                self.fmt_deg(hour["feels_f"]),
                hour["precip_chance"],
                hour["temp_f"],
                hour["feels_f"],
                is_now=hour["is_now"],
            ))

    def _render_ten_day(self):
        """Rebuild the 10-Day page rows and its summary."""
        layout = self.ui.tenDayList.layout()
        clear_layout(layout)
        too_hot = sum(day["high_f"] >= V_HIGH_F for day in self.days)
        if too_hot:
            self.ui.tenDaySubtitle.setText(
                f"{too_hot} of {len(self.days)} days are in the too hot. Congratulations."
            )
        else:
            self.ui.tenDaySubtitle.setText("Not one day above 95 degrees. Suspicious.")

        for day in self.days:
            layout.addWidget(DayRow(
                day["day"],
                day["date"],
                self.fmt_deg(day["high_f"]),
                self.fmt_deg(day["low_f"]),
                day["high_f"],
                day["quip"],
                day["condition"],
                day["precip_chance"],
            ))

    def _render_alerts(self):
        """Rebuild the Alerts page: NWS alert cards (or an all-clear), heat tips, and the user's threshold."""
        layout = self.ui.alertsList.layout()
        clear_layout(layout)
        count = len(self.alerts)
        self.ui.alertsSubtitle.setText(
            f"{count} active for {self.current['location']}" if count else f"Nothing active for {self.current['location']}"
        )

        for alert in self.alerts:
            layout.addWidget(AlertCard(alert, get_quip(self.current["temp_f"], self.current["condition"])))
        if not count:
            layout.addWidget(make_label(
                "No alerts. The atmosphere has temporarily suspended hostilities.", "subtitle", wrap=True
            ))

        peak = self._peak_feels()
        if count or (peak is not None and peak >= self.heat_threshold_f):
            layout.addWidget(make_label("Don't die out there", "section"))
            for tip in HEAT_TIPS:
                layout.addWidget(make_label(f"•  {tip}", "body", wrap=True))

        layout.addWidget(make_label(
            f"Your own heat alert: feels-like ≥ {self.fmt_temp(self.heat_threshold_f)}. Change it in Settings.",
            "sub",
        ))

    def draw_graph(self):
        """
        Draw the selected forecast chart onto the embedded figure.

        Draws the daily (first 7 days) or hourly chart depending on ``self.graph_mode``, in the user's selected
        unit. Does nothing if no data has loaded yet.
        """
        if self.daily_df is None:
            return
        if self.graph_mode == "hourly":
            make_hourly_graphs(self.hourly_df, fig=self.figure, celsius=self.use_celsius)
        else:
            make_daily_graphs(self.daily_df.head(7), fig=self.figure, celsius=self.use_celsius)
        self.canvas.draw_idle()

    def set_graph_mode(self, mode: str):
        """
        Switch which chart is shown and redraw it. Connected to the Daily/Hourly Graph menu actions.

        Args:
            mode: ``"daily"`` or ``"hourly"``.
        """
        self.graph_mode = mode
        self.draw_graph()

    # ====================================================================
    # ====================================================================
    # ============================ RADAR =================================
    # ====================================================================
    # ====================================================================

    def _ensure_radar(self):
        """Build the radar map the first time the Radar page is opened."""
        if self.radar_view is not None:
            return
        self.statusBar().showMessage("Loading radar...", 3000)
        QApplication.processEvents()
        self.radar_view = make_radar_widget(self.ui.radarHost)
        self.ui.radarHost.layout().addWidget(self.radar_view)
        location = load_location()
        load_radar(self.radar_view, location["latitude"], location["longitude"])

    # ====================================================================
    # ====================================================================
    # =========================== LOCATIONS ==============================
    # ====================================================================
    # ====================================================================

    def _load_places(self) -> list[dict]:
        """Returns the saved places (location dicts) from QSettings."""
        try:
            return json.loads(self.settings.value("places", "[]"))
        except (TypeError, json.JSONDecodeError):
            return []

    def _save_places(self, places: list[dict]):
        """Saves the list of places to QSettings as JSON."""
        self.settings.setValue("places", json.dumps(places))

    def _refresh_places(self):
        """
        Rebuild the Locations page: the default location first, then saved places, each with its current
        temperature. Temperatures go through the hour-long cache, so reopening the page is quick.
        """
        layout = self.ui.locationsList.layout()
        clear_layout(layout)
        self.statusBar().showMessage("Checking your places...")
        QApplication.processEvents()

        default = load_location()
        entries = [(default, True)] + [(p, False) for p in self._load_places()
                                       if p["location_name"] != default["location_name"]]
        for loc, is_default in entries:
            try:
                temp_f = get_current_temp(loc)
            except Exception:  # noqa: BLE001 - one bad place shouldn't break the page
                temp_f = None
            if temp_f is None:
                detail, temp_text = "Couldn't reach Open-Meteo", "--"
            else:
                detail, temp_text = f"{bucket_name(temp_f)} · “{get_quip(temp_f)}”", self.fmt_deg(temp_f)
            layout.addWidget(place_row(
                loc["location_name"],
                temp_text,
                temp_f,
                detail,
                is_default,
                None if is_default else (lambda loc=loc: self.make_default(loc)),
                None if is_default else (lambda loc=loc: self.remove_place(loc)),
            ))
        self.statusBar().showMessage("Places updated", 3000)

    def _pick_location(self, title: str) -> dict | None:
        """
        Prompt for a place name, geocode it, and let the user pick a match.

        Network errors and empty results are shown in a warning dialog.

        Args:
            title: Dialog title.

        Returns:
            A location dict for config.json, or None if cancelled or nothing was found.
        """
        current = self.current["location"] if self.current else ""
        text, ok = QInputDialog.getText(self, title, "City or postal code:", text=current)
        if not ok or not text.strip():
            return None

        try:
            matches = geocode(text.strip(), limit=5)
        except requests.RequestException as err:
            QMessageBox.warning(self, "Location Lookup Failed", f"Couldn't search for that location:\n{err}")
            return None
        if not matches:
            QMessageBox.warning(self, "Location Not Found", f'No places found for "{text.strip()}".')
            return None

        match = matches[0]
        if len(matches) > 1:
            names = [format_match(m) for m in matches]
            choice, ok = QInputDialog.getItem(self, "Choose Location", "Which one?", names, 0, False)
            if not ok:
                return None
            match = matches[names.index(choice)]
        return match_to_location(match)

    def add_place(self):
        """Geocode a new place and add it to the saved list on the Locations page."""
        location = self._pick_location("Add Place")
        if location is None:
            return
        places = [p for p in self._load_places() if p["location_name"] != location["location_name"]]
        self._save_places(places + [location])
        self._refresh_places()

    def remove_place(self, location: dict):
        """Remove a place from the saved list."""
        self._save_places([p for p in self._load_places() if p["location_name"] != location["location_name"]])
        self._refresh_places()

    def make_default(self, location: dict):
        """
        Make a saved place the default location. The old default joins the saved list so it isn't lost.

        Args:
            location: The place to make default.
        """
        old = load_location()
        places = [p for p in self._load_places() if p["location_name"] != location["location_name"]]
        self._save_places(places + [{k: old[k] for k in ("location_name", "latitude", "longitude",
                                                          "elevation", "timezone") if k in old}])
        # Merge so keys this page doesn't set (like station_id) survive the save
        save_location({**old, **location})
        self.refresh()
        self._refresh_places()

    # ====================================================================
    # ====================================================================
    # ======================= MENU HANDLERS ==============================
    # ====================================================================
    # ====================================================================

    def set_celsius(self, checked: bool):
        """
        Switch display units, save the choice and refresh the window. Connected to the Celsius action's
        ``toggled`` signal.

        Args:
            checked: True when Celsius is selected, False when Fahrenheit is checked.
        """
        self.use_celsius = checked
        self.settings.setValue("celsius", checked)
        combo = self.ui.unitsCombo
        combo.blockSignals(True)
        combo.setCurrentIndex(1 if checked else 0)
        combo.blockSignals(False)
        self.update_display()

    def set_heat_threshold(self, value_f: int):
        """
        Save the user's heat-alert threshold and update the banner and Alerts page.

        Args:
            value_f: Feels-like temperature in °F.
        """
        self.heat_threshold_f = value_f
        self.settings.setValue("heat_threshold_f", value_f)
        if self.current is not None:
            self._update_alert_banner()
            self._render_alerts()

    def change_theme(self, name: str):
        """
        Switch the app to a theme, save the choice, and redraw everything in the new colors.

        Args:
            name: Key from ``theme.THEMES``.
        """
        if name not in theme.THEMES:
            return
        theme.apply_theme(QApplication.instance(), name)
        self.settings.setValue("theme", name)
        for theme_name, action in self.theme_actions.items():
            action.setChecked(theme_name == name)
        combo = self.ui.themeCombo
        combo.blockSignals(True)
        combo.setCurrentText(name)
        combo.blockSignals(False)
        self.update_display()  # Rebuilds rows with inline colors and redraws the chart
        if self.radar_view is not None:
            location = load_location()
            load_radar(self.radar_view, location["latitude"], location["longitude"])
        self.statusBar().showMessage(f"Theme: {name}", 3000)

    def save_graph(self):
        """
        Ask for a file name and save the current graph.

        Format follows the file extension shown in the dialog. Does nothing if cancelled.
        """
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Graph", str(HERE / "forecast.png"), "PNG Image (*.png);; PDF (*.pdf);; SVG(*.svg)"
        )
        if path:
            self.figure.savefig(path, dpi=150)
            self.statusBar().showMessage(f"Saved {Path(path).name}", 5000)

    def check_connection(self):
        """
        Test whether the Open-Meteo API server is reachable.

        Opens a TCP connection to api.open-meteo.com on port 443 with a 3-second timeout.
        Reports success in the status bar and failure in a warning dialog. Blocks the window for
        up to 3 seconds.
        """
        try:
            with socket.create_connection(("api.open-meteo.com", 443), timeout=3):
                pass
            self.statusBar().showMessage("Connection successful", 5000)
        except OSError:
            QMessageBox.warning(self, "No connection", "Could not reach api.open-meteo.com.")

    def set_location(self):
        """Prompt for a new default location, save it to config.json and refresh."""
        location = self._pick_location("Set Location")
        if location is None:
            return
        # Merge so keys this dialog doesn't set (like station_id) survive the save
        save_location({**load_location(), **location})
        self.refresh()

    def open_readme(self):
        """
        Open the local README.md in the default app, or the GitHub README if file is missing
        """
        if README_PATH.exists():
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(README_PATH)))
        else:
            QDesktopServices.openUrl(QUrl(f"{GITHUB_URL}#readme"))

    def show_about(self):
        """
        Show the About dialog with the version number and a link to GitHub
        """
        QMessageBox.about(
            self,
            "About Too Damn Hot!",
            f"<b>Too Damn Hot!</b> v{VERSION}<br>"
            "Weather forecasting from Open-Meteo. Alerts from the National Weather Service.<br>"
            "Radar from RainViewer.<br>"
            f'<a href="{GITHUB_URL}">GitHub</a>',
        )

    def not_ready(self, feature):
        """
        Show a temporary "coming soon" message for an unfinished menu feature

        Args:
            feature (str): Name of the feature, shown in the status bar message.
        """
        self.statusBar().showMessage(f"{feature} is coming soon", 4000)


if __name__ == "__main__":
    splash_progress(5, "Building window...")
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # The native Windows style ignores most palette colors
    theme.load_fonts()  # Before apply_theme(), because the stylesheet names the font families
    theme.apply_theme(app, QSettings("TooDamnHot", "TooDamnHot").value("theme", theme.DEFAULT_THEME))
    window = MainWindow()
    splash_progress(7, "Ready")
    window.show()
    close_splash()
    sys.exit(app.exec())
