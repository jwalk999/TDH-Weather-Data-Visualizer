"""
File Name: widgets.py

Author: Jonathan W
Date Created: 10/20/2026
Last Update: 10/20/2026
Version: 1.0.0

Scope: Small custom widgets for the sidebar pages: hourly heat bars, 10-day rows, alert cards, saved-place rows
    and the radar map. Colors come from theme.current() when a widget is built or painted, so a theme switch only
    needs the pages rebuilt.
"""

from collections.abc import Callable

from PySide6.QtCore import QPointF, QRectF, Qt, QUrl
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

import theme

# Range the hourly bars are scaled across, in °F. Hotter or colder values are clamped to the ends.
BAR_MIN_F = 60
BAR_MAX_F = 115
ALIGN_RIGHT = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter


# ===== HELPERS =====
def clear_layout(layout: QLayout) -> None:
    """Removes and deletes every widget and sub-layout in a layout, so a page can be rebuilt.

    Args:
        layout: The layout to empty.
    """
    while layout.count():
        item = layout.takeAt(0)
        if item.widget() is not None:
            item.widget().deleteLater()
        elif item.layout() is not None:
            clear_layout(item.layout())


def make_label(text: str, role: str | None = None, wrap: bool = False, align=None) -> QLabel:
    """Creates a QLabel that picks up a style from theme.build_stylesheet() through its ``role`` property.

    Args:
        text: Label text. Rich text is allowed.
        role: Stylesheet role, e.g. "title", "sub", "precip".
        wrap: Turn on word wrap.
        align: Optional Qt alignment flags.

    Returns:
        The new label.
    """
    label = QLabel(text)
    if role:
        label.setProperty("role", role)
    label.setWordWrap(wrap)
    if align is not None:
        label.setAlignment(align)
    return label


def _fraction(temp_f: float) -> float:
    """Position of a temperature along the hourly bar scale, 0.0 to 1.0."""
    return max(0.0, min(1.0, (temp_f - BAR_MIN_F) / (BAR_MAX_F - BAR_MIN_F)))


# ===== HOURLY =====
class HeatBar(QWidget):
    """A horizontal bar for one hour: the length and color show the temperature, a thin line marks feels-like.

    Attributes:
        temp_f: Air temperature in °F.
        feels_f: Apparent temperature in °F.
    """

    def __init__(self, temp_f: float, feels_f: float, parent: QWidget | None = None):
        super().__init__(parent)
        self.temp_f = temp_f
        self.feels_f = feels_f
        self.setMinimumHeight(18)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def paintEvent(self, event):  # noqa: N802 - Qt override
        """Draws the bar and the feels-like marker."""
        width, height = self.width(), self.height()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        bar = QPainterPath()
        bar.addRoundedRect(QRectF(0, 3, max(6.0, width * _fraction(self.temp_f)), height - 6), 5, 5)
        painter.fillPath(bar, theme.heat_color(self.temp_f))

        marker = QColor(theme.current().text)
        marker.setAlphaF(0.4)
        painter.setPen(QPen(marker, 2))
        x = width * _fraction(self.feels_f)
        painter.drawLine(QPointF(x, 0), QPointF(x, height))
        painter.end()


class HourRow(QFrame):
    """One row of the Hourly page: hour, heat bar, temperature, feels-like and precipitation chance."""

    def __init__(
        self,
        hour_text: str,
        temp_text: str,
        feels_text: str,
        precip_chance: int,
        temp_f: float,
        feels_f: float,
        is_now: bool = False,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.setProperty("now", is_now)  # Highlighted by the stylesheet
        grid = QGridLayout(self)
        grid.setContentsMargins(8, 3, 8, 3)
        grid.setHorizontalSpacing(14)
        grid.addWidget(make_label(hour_text, "mono"), 0, 0)
        grid.addWidget(HeatBar(temp_f, feels_f), 0, 1)
        grid.addWidget(make_label(temp_text, "strong", align=ALIGN_RIGHT), 0, 2)
        grid.addWidget(make_label(f"feels {feels_text}", "sub"), 0, 3)
        grid.addWidget(make_label(f"{precip_chance}%", "precip", align=ALIGN_RIGHT), 0, 4)
        for column, width in ((0, 52), (2, 44), (3, 84), (4, 44)):
            grid.setColumnMinimumWidth(column, width)
        grid.setColumnStretch(1, 1)


# ===== 10-DAY =====
class DayRow(QFrame):
    """One row of the 10-Day page: day and date, big high, low, a quip, and conditions with precip chance."""

    def __init__(
        self,
        day: str,
        date: str,
        high_text: str,
        low_text: str,
        high_f: float,
        quip: str,
        condition: str,
        precip_chance: int,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.setProperty("row", True)
        grid = QGridLayout(self)
        grid.setContentsMargins(0, 10, 0, 10)
        grid.setHorizontalSpacing(18)

        day_box = QVBoxLayout()
        day_box.setSpacing(0)
        day_box.addWidget(make_label(day, "dayname"))
        day_box.addWidget(make_label(date, "mono"))
        grid.addLayout(day_box, 0, 0)

        temps = QHBoxLayout()
        temps.setSpacing(6)
        high = make_label(high_text, "dayhi")
        high.setStyleSheet(f"color: {theme.heat_color(high_f).name()};")
        temps.addWidget(high, alignment=Qt.AlignmentFlag.AlignBottom)
        temps.addWidget(make_label(low_text, "cool"), alignment=Qt.AlignmentFlag.AlignBottom)
        temps.addStretch()
        grid.addLayout(temps, 0, 1)

        grid.addWidget(make_label(quip, "body", wrap=True), 0, 2)

        right = QVBoxLayout()
        right.setSpacing(0)
        right.addWidget(make_label(condition, "small", align=ALIGN_RIGHT))
        right.addWidget(make_label(f"{precip_chance}% precip", "precip", align=ALIGN_RIGHT))
        grid.addLayout(right, 0, 3)

        grid.setColumnMinimumWidth(0, 84)
        grid.setColumnMinimumWidth(1, 130)
        grid.setColumnMinimumWidth(3, 130)
        grid.setColumnStretch(2, 1)


# ===== ALERTS =====
SEVERITY_COLORS = {"Extreme": "hot", "Severe": "hot", "Moderate": "sunrise", "Minor": "sunrise"}


class AlertCard(QFrame):
    """A card for one NWS alert: severity pill, event name, issuer and end time, description, and a quip."""

    def __init__(self, alert: dict, quip: str, parent: QWidget | None = None):
        super().__init__(parent)
        colors = theme.current()
        self.setProperty("card", True)
        box = QVBoxLayout(self)
        box.setContentsMargins(18, 16, 18, 16)
        box.setSpacing(8)

        head = QHBoxLayout()
        head.setSpacing(10)
        pill = make_label(alert["severity"].upper(), "pill")
        pill_color = getattr(colors, SEVERITY_COLORS.get(alert["severity"], "muted"))
        pill.setStyleSheet(f"background: {pill_color}; color: {colors.highlighted_text};")
        head.addWidget(pill)
        head.addWidget(make_label(alert["event"], "h3"))
        head.addStretch()
        until = f" · until {alert['ends']}" if alert["ends"] else ""
        head.addWidget(make_label(f"{alert['sender']}{until}", "sub"))
        box.addLayout(head)

        if alert["description"]:
            box.addWidget(make_label(alert["description"], "body", wrap=True))
        if alert["instruction"]:
            box.addWidget(make_label(alert["instruction"], "sub", wrap=True))
        box.addWidget(make_label(f"“{quip}”", "accent", wrap=True))


# ===== LOCATIONS =====
def place_row(
    name: str,
    temp_text: str,
    temp_f: float | None,
    detail: str,
    is_default: bool,
    on_default: Callable[[], None] | None,
    on_remove: Callable[[], None] | None,
) -> QFrame:
    """Builds one row of the Locations page.

    Args:
        name: Display name.
        temp_text: Formatted current temperature, or "--" while unknown.
        temp_f: Current temperature in °F for the heat color, or None.
        detail: Second line, e.g. the bucket and a quip.
        is_default: Show the DEFAULT tag.
        on_default: Called by the "Make default" button. None hides the button.
        on_remove: Called by the "Remove" button. None hides the button.

    Returns:
        The row frame.
    """
    row = QFrame()
    row.setProperty("row", True)
    grid = QGridLayout(row)
    grid.setContentsMargins(0, 12, 0, 12)
    grid.setHorizontalSpacing(16)

    left = QVBoxLayout()
    left.setSpacing(2)
    title = QHBoxLayout()
    title.setSpacing(8)
    title.addWidget(make_label(name, "h3"))
    if is_default:
        title.addWidget(make_label("DEFAULT", "tag"))
    title.addStretch()
    left.addLayout(title)
    left.addWidget(make_label(detail, "sub", wrap=True))
    grid.addLayout(left, 0, 0)
    grid.setColumnStretch(0, 1)

    temp = make_label(temp_text, "placetemp", align=ALIGN_RIGHT)
    if temp_f is not None:
        temp.setStyleSheet(f"color: {theme.heat_color(temp_f).name()};")
    grid.addWidget(temp, 0, 1)

    buttons = QHBoxLayout()
    buttons.setSpacing(6)
    if on_default:
        button = QPushButton("Make default")
        button.clicked.connect(lambda _checked=False: on_default())
        buttons.addWidget(button)
    if on_remove:
        button = QPushButton("Remove")
        button.clicked.connect(lambda _checked=False: on_remove())
        buttons.addWidget(button)
    grid.addLayout(buttons, 0, 2)
    grid.setColumnMinimumWidth(2, 220)
    return row


# ===== RADAR =====
# Leaflet in a QWebEngineView. No API keys needed:
#   - US: NEXRAD composite from the Iowa Environmental Mesonet (IEM) tile cache, free, 5-minute frames, the last
#     50 minutes looped. Full zoom.
#   - Everywhere else: RainViewer's keyless public tiles (max zoom 7, last ~2 hours, 100 requests/min per IP).
#   - Basemap: Esri Light/Dark Gray Canvas (free, keyless, attribution required). It's split into a plain base
#     layer under the radar and a labels-only layer on top, so city names stay readable through the rain.
# Placeholders are swapped with str.replace so the JS braces don't need escaping.
RADAR_HTML = """<!doctype html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
html,body,#map{height:100%;margin:0;background:%BG%}
#stamp{position:absolute;left:12px;bottom:12px;z-index:1000;padding:6px 10px;border-radius:6px;
  background:%BG%;color:%TEXT%;font:13px sans-serif;opacity:.92}
</style>
</head><body><div id="map"></div><div id="stamp">Loading radar…</div><script>
const LAT = %LAT%, LON = %LON%;
const map = L.map('map').setView([LAT, LON], 7);
const ESRI = 'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_%CANVAS%_Gray_';
L.tileLayer(ESRI + 'Base/MapServer/tile/{z}/{y}/{x}', {
  maxZoom: 16, attribution: 'Basemap &copy; Esri'
}).addTo(map);
// Labels get their own pane above the radar so they're never buried
map.createPane('labels');
map.getPane('labels').style.zIndex = 650;
map.getPane('labels').style.pointerEvents = 'none';
L.tileLayer(ESRI + 'Reference/MapServer/tile/{z}/{y}/{x}', {maxZoom: 16, pane: 'labels'}).addTo(map);
L.circleMarker([LAT, LON], {radius: 7, color: '%ACCENT%', fillColor: '%ACCENT%', fillOpacity: 1}).addTo(map);
const stamp = document.getElementById('stamp');

function animate(layers, labels) {
  let i = layers.length - 1;
  layers[i].setOpacity(0.85); stamp.textContent = labels[i];
  setInterval(() => {
    layers[i].setOpacity(0); i = (i + 1) % layers.length;
    layers[i].setOpacity(0.85); stamp.textContent = labels[i];
  }, 700);
}

// Rough NEXRAD coverage box (lower 48, Alaska, Hawaii, Puerto Rico)
const inUS = LAT > 17 && LAT < 72 && LON > -170 && LON < -64;

if (inUS) {
  const offsets = [50, 45, 40, 35, 30, 25, 20, 15, 10, 5, 0];  // minutes ago, oldest first
  const layers = offsets.map(m => L.tileLayer(
    'https://mesonet.agron.iastate.edu/cache/tile.py/1.0.0/nexrad-n0q-900913' +
      (m ? '-m' + String(m).padStart(2, '0') + 'm' : '') + '/{z}/{x}/{y}.png',
    {opacity: 0, attribution: 'NEXRAD via Iowa Environmental Mesonet'}
  ).addTo(map));
  animate(layers, offsets.map(m => m ? m + ' min ago' : 'Now'));
} else {
  fetch('https://api.rainviewer.com/public/weather-maps.json').then(r => r.json()).then(data => {
    const frames = data.radar.past;
    const layers = frames.map(f => L.tileLayer(data.host + f.path + '/256/{z}/{x}/{y}/2/1_1.png', {
      opacity: 0, maxNativeZoom: 7, attribution: 'Radar &copy; RainViewer'
    }).addTo(map));
    animate(layers, frames.map(f => new Date(f.time * 1000).toLocaleTimeString([], {hour: 'numeric', minute: '2-digit'})));
  }).catch(() => { stamp.textContent = 'Radar unavailable right now'; });
}
</script></body></html>"""


def make_radar_widget(parent: QWidget | None = None) -> QWidget:
    """Creates the radar view, or a message label if Qt WebEngine isn't installed.

    QtWebEngine is imported here rather than at the top of the file because it's slow to load, and the radar
    page is only built the first time it's opened.

    Args:
        parent: Optional parent widget.

    Returns:
        A QWebEngineView, or a QLabel fallback.
    """
    try:
        from PySide6.QtWebEngineWidgets import QWebEngineView  # noqa: PLC0415
    except ImportError:
        return make_label(
            "Radar needs Qt WebEngine. Install it with: pip install PySide6-Addons",
            "subtitle",
            wrap=True,
            align=Qt.AlignmentFlag.AlignCenter,
        )
    return QWebEngineView(parent)


def load_radar(view: QWidget, latitude: float, longitude: float) -> None:
    """Points the radar map at a location, using the current theme's colors. Does nothing for the fallback label.

    Args:
        view: The widget from make_radar_widget().
        latitude: Decimal degrees.
        longitude: Decimal degrees.
    """
    if not hasattr(view, "setHtml"):
        return
    colors = theme.current()
    is_light = QColor(colors.window).lightness() > 128
    html = (
        RADAR_HTML.replace("%LAT%", f"{latitude:.4f}")
        .replace("%LON%", f"{longitude:.4f}")
        .replace("%CANVAS%", "Light" if is_light else "Dark")
        .replace("%BG%", colors.window)
        .replace("%TEXT%", colors.text)
        .replace("%ACCENT%", colors.accent)
    )
    view.setHtml(html, QUrl("https://toodamnhot.local/"))
