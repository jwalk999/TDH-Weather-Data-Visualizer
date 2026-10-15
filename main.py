"""
File Name: main.py

Author: Jonathan W
Date Created: 10/5/2026
Last Update: 10/15/2026
Version: 0.0.2

Scope: Creates the main GUI environment for the application
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

import socket
import sys
from pathlib import Path

import pandas as pd
import requests
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
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

import theme
from Config.global_params import (
    f_to_c,
    get_period,
    get_weather_description,
    load_descriptions,
    load_location,
    save_location,
)
from Daily_Graph import make_daily_graphs
from Forecasts import get_forecast
from geocoding import format_match, geocode, match_to_location
from Hourly_Graph import make_hourly_graphs
from quips import get_quip
from ui_main_window import Ui_MainWindow

HERE = Path(__file__).parent
ICON_PATH = HERE / "hot-temperature.png"
README_PATH = HERE / "README.md"
GITHUB_URL = "https://github.com/jwalk999/TDH-Weather-Data-Visualizer"
VERSION = "0.1"

# =============================================================================
# ============================== DATA FETCH ===================================
# ==============================AND LOADING ===================================
# =============================================================================

# Pass the scroll function through the figure canvas so scrolling works on the graphs
class ScrollPassthroughCanvas(FigureCanvasQTAgg):
    """A matplotlib canvas that lets the mosue wheel scroll the page instead of the chart"""

    def wheelEvent(self, event):
        """ Pass the wheel event to the parent widget.

        Args:
            event (QWheelEvent): The mouse wheel event.
        """
        event.ignore()


def load_data():
    """
    Load current and 7-day forecast conditions for display.
    All units are held in Imperial format, the window will format them according to
    user settings.

    Returns:
        tuple[dict, list[dict], pd.DataFrame, pd.DataFrame]: A ``(current, forecast, daily_df, hourly_df)``
        tuple. daily_df and hourly_df are the raw dataframes, used for graphing.

    ``current`` has keys:
        location (str):     Display location name and info.
        temp_f (float):     Current temperature in °F.
        condition (str):    Current weather description. e.g. "Clear".
        sunrise (str):      Formatted sunrise time, e.g. "6:52 AM".
        sunset (str):       Formatted sunset time, e.g. "8:45 PM".
        quip (str):         Quip shown next to location.

    ``forecast`` is a list of 7 dicts, one per day, each with keys:
        day (str):          Short day name, e.g. "Mon".
        high_f (float):     Daily high in °F.
        low_f (float):      Daily low in °F.
        precip_chance (int): Chance of precipitation, 0-100%.
        precip_in (float):  Expected precipitation in inches.

    Raises:
        requests.exceptions.ConnectionError: If Open-Meteo cannot be reached
    """
    location = load_location()
    tz = location["timezone"]
    daily_df, hourly_df = get_forecast(location)

    # Latest hourly row at or before now (hourly data starts at midnight, so row 0 is wrong)
    now_row = hourly_df[hourly_df["Date"] <= pd.Timestamp.now(tz=tz)].iloc[-1]
    today = daily_df.iloc[0]

    temp_f = float(now_row["Temperature"])
    period = get_period(now_row["Date"], today["Sunrise"], today["Sunset"])
    condition = get_weather_description(now_row["Weather Code"], load_descriptions(), period)

    current = {
        "location": location["location_name"],
        "temp_f": temp_f,
        "condition": condition,
        "sunrise": today["Sunrise"].strftime("%I:%M %p").lstrip("0"),
        "sunset": today["Sunset"].strftime("%I:%M %p").lstrip("0"),
        "quip": get_quip(temp_f, condition),
    }

    forecast = [
        {
            "day": row["Date"].strftime("%a"),
            "high_f": float(row["Temperature High"]),
            "low_f": float(row["Temperature Low"]),
            "precip_chance": int(row["Chance of Precipitation"]),
            "precip_in": float(row["Precipitation"]),
        }
        for row in daily_df.head(7).to_dict("records")
    ]

    return current, forecast, daily_df, hourly_df

class MainWindow(QMainWindow):
    """The Too Damn Hot! main window.

    Wraps the QT Designer-generated layout, populates with ``load_data()``,
    and handles every menu action.

    Attributes:
        ui (Ui_MainWindow):     Generated UI, every Designer widget is an attribute.
        current (dict | None):  Current conditions saved from previous refresh, 
                                or None from first load.
        forecast (list[dict]): The 7 daily forecast dicts from last refresh
        use_celsius (bool):     True when user picks Celsius from the View menu
        temp_cells (list[dict[str, QLabel]]): Label sets for the 7 temp frames.
        precip_cells (list[dict[str, QLabel]]): Label sets for the 7 precip frames.
        figure (Figure):        The matplotlib figure shown in ``plotArea``.
        canvas (FigureCanvasQTAgg): The Qt widget that displays ``figure``.
    
    """


    def __init__(self):
        """Build the window, set up widgets and menus, and load data."""
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Resolve the path to the app icon
        if ICON_PATH.exists():
            self.setWindowIcon(QIcon(str(ICON_PATH)))

        self.current = None
        self.forecast = []        
        self.daily_df = None
        self.hourly_df = None
        self.graph_mode = "daily"
        self.use_celsius = False

        self._setup_forecast_frames()
        self._setup_plot()
        self._setup_menus()

        self._build_theme_menu()

        self.statusBar().showMessage("Ready")
        self.refresh()

    # ====================================================================
    # ====================================================================
    # ============================== SETUP ===============================
    # ====================================================================
    # ====================================================================

    def _setup_forecast_frames(self):
        """
        Give each empty Designer forecast frame a layout with three labels.

        Collects the frames by name:
                (``tempFrame1`` - ``tempFrame7``)
                (``precipFrame1`` - ``precipFrame7``)
        Stores the labels for each in 
                ``self.temp_cells``
                ``self.precip_cells``
            all in day order.
        """
        self.temp_cells = [self._build_cell(getattr(self.ui, f"tempFrame{i}")) for i in range (1, 8)]
        self.precip_cells = [self._build_cell(getattr(self.ui, f"precipFrame{i}")) for i in range (1, 8)]

    @staticmethod
    def _build_cell(frame):
        """
        Add a vertical layout with day, main and sub levels to a frame.

        Args:
            frame (QFrame): An empty frame with no layout.

        Returns:
            dict[str, QLabel]: The labels keyed by ``"day"``, ``"main"``, and ``"sub"``,
                    top to bottom.
        """
        frame.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        frame.setMinimumWidth(70)
        frame.setProperty("card", True)  # Picks up the rounded card style from theme.build_stylesheet()
        layout = QVBoxLayout(frame)
        cell = {}
        for key in ("day", "main", "sub"):
            label = QLabel("-", frame)
            label.setProperty("role", key)  # Lets the stylesheet dim the day and sub labels
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        self.ui.plotArea.setMinimumHeight(560)  # Designer sets 300, which squeezes the two charts together
        layout = self.ui.plotArea.layout() or QVBoxLayout(self.ui.plotArea)
        layout.addWidget(self.canvas)

    def _setup_menus(self):
        """
        Connect every menu action to its handler.

        Also groups Fahrenheit/Celsius so only one can be checked, 
            makes the Show Graph and Show Forecast actions checkable toggles.
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
        self.ui.menu_View.insertMenu(self.ui.action_Themes, menu)
        self.ui.action_Themes.setVisible(False)

    # ====================================================================
    # ====================================================================
    # ============================== DATA ================================
    # ====================================================================
    # ====================================================================

    # Refresh page function
    def refresh(self):
        """
        Reload weather data and update the window.

        Any exception from ``load_data()`` is caught and shown in a warning dialogue.
        A failed fetch leaves the previous data on screen. 
        Runs on the main thread, so the window is unreponsive while loading.
        """
        self.statusBar().showMessage("Loading Data...")
        QApplication.processEvents() # show message before fetching
        try:
            self.current, self.forecast, self.daily_df, self.hourly_df = load_data()
        except Exception as err: # throw an error without crashing  # noqa: BLE001
            QMessageBox.warning(self, "Refresh Failed", f"Couldn't load weather data:\n{err}")
            self.statusBar().showMessage("Refresh failed")
            return
        self.update_display()
        self.statusBar().showMessage("Data updated", 5000)


    # Format temperatures function
    def fmt_temp(self, temp_f: float) -> str:
        """
        Format a temperature for display in user's slected unit.

        Args:
            temp_f: Temperature in degrees Fahrenheit.
        
        Returns:
            str: The temperature rounded to a whole number with selcted unit.
        """
        if self.use_celsius:
            return f"{f_to_c(temp_f):.0f}°C"
        return f"{temp_f:.0f}°F"


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


    # Update function
    def update_display(self):
        """
        Write the cached data into every label and redraw the graph.

        Does nothing if no data has loaded yet. Called after each refresh and whenever
                units change.
        """
        if self.current is None:
            return
        
        ui, cur = self.ui, self.current
        ui.locationLabel.setText(cur["location"])
        ui.quipLabel.setText(cur["quip"])
        ui.bigtempLabel.setText(self.fmt_temp(cur["temp_f"]))
        ui.bigprecLabel.setText(cur["condition"])
        ui.sunriseLabel.setText(f"Sunrise {cur['sunrise']}")
        ui.sunsetLabel.setText(f"Sunset {cur['sunset']}")

        ui.tempsLabel.setText("Temperature")
        ui.precipsLabel.setText("Precipitation")
        for day, t_cell, p_cell in zip(self.forecast, self.temp_cells, self.precip_cells):
            t_cell["day"].setText(day["day"])
            t_cell["main"].setText(self.fmt_temp(day["high_f"]))
            t_cell["sub"].setText(self.fmt_temp(day["low_f"]))
            p_cell["day"].setText(day["day"])
            p_cell["main"].setText(f"{day['precip_chance']}%")
            p_cell["sub"].setText(self.fmt_precip(day["precip_in"]))

        self.draw_graph()

    def draw_graph(self):
        """
        Draw the selected forecast chart onto the embedded figure.

        Draws the daily or hourly chart depending on ``self.graph_mode``, in the user's selected unit.
        Does nothing if no data has loaded yet.
        """
        if self.daily_df is None:
            return
        if self.graph_mode == "hourly":
            make_hourly_graphs(self.hourly_df, fig=self.figure, celsius=self.use_celsius)
        else:
            make_daily_graphs(self.daily_df, fig=self.figure, celsius=self.use_celsius)
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
    # ======================= MENU HANDLERS ==============================
    # ====================================================================
    # ====================================================================

    def set_celsius(self, checked: bool):
        """
        Switch display units and refresh the window. Connected to Celsius action's
                ``toggled`` signal.
        
        Args:
            checked: True when Celsius is selected, False when Fahrenheit is checked.
        """
        self.use_celsius = checked
        self.update_display()

    def change_theme(self, name: str):
        """
        Switch the app to a theme, save the choice, and redraw the graph in the new colors.

        Args:
            name: Key from ``theme.THEMES``.
        """
        theme.apply_theme(QApplication.instance(), name)
        QSettings("TooDamnHot", "TooDamnHot").setValue("theme", name)
        self.draw_graph()  # The chart keeps its old colors until it's redrawn
        self.statusBar().showMessage(f"Theme: {name}", 3000)

    def save_graph(self):
        """
        Ask for a file name and save the current graph.

        Format follows the file extension shown in the dialog. Does nothing if cancelled
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
        Reports success if the status bar and failure in a warning dialog. Blocks the window for
        up to 3 seconds.
        """
        try:
            with socket.create_connection(("api.open-meteo.com", 443), timeout=3):
                pass
            self.statusBar().showMessage("Connection successful", 5000)
        except OSError:
            QMessageBox.warning(self, "No connection", "Could not reach api.open_meteo.com.")

    def set_location(self):
        """
        Prompt for a place name, geocode it, save the chosen match to config.json and refresh.

        If the search returns more than one match, the user picks from a list. Network errors and empty
        results are shown in a warning dialog, and the saved location is left unchanged.
        """
        current = self.current["location"] if self.current else ""
        text, ok = QInputDialog.getText(self, "Set Location", "City or postal code:", text=current)
        if not ok or not text.strip():
            return

        try:
            matches = geocode(text.strip(), limit=5)
        except requests.RequestException as err:
            QMessageBox.warning(self, "Location Lookup Failed", f"Couldn't search for that location:\n{err}")
            return
        if not matches:
            QMessageBox.warning(self, "Location Not Found", f'No places found for "{text.strip()}".')
            return

        match = matches[0]
        if len(matches) > 1:
            names = [format_match(m) for m in matches]
            choice, ok = QInputDialog.getItem(self, "Choose Location", "Which one?", names, 0, False)
            if not ok:
                return
            match = matches[names.index(choice)]

        # Merge so keys this dialog doesn't set (like station_id) survive the save
        save_location({**load_location(), **match_to_location(match)})
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
            "Weather forecasting from Open-Meteo.<br>"
            f'<a href="{GITHUB_URL}">GitHub</a>',
        )

    def not_ready(self, feature):
        """
        Show a temporary "coming soon" message for an unfinished menu feature"
        
        Args:
            feature (str): Name of the feature, shown in the status bar message.
        """
        self.statusBar().showMessage(f"{feature} is coming soon", 4000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # The native Windows style ignores most palette colors
    theme.apply_theme(app, QSettings("TooDamnHot", "TooDamnHot").value("theme", theme.DEFAULT_THEME))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())