"""
File Name: theme.py

Author: Jonathan W
Date Created: 10/15/2026
Last Update: 10/20/2026
Version: 2.1.0

Scope: Switchable color themes shared by the Qt window and the matplotlib charts, so the graphs always blend into
    the UI. Importing this module applies the default theme to matplotlib; call apply_theme() to switch at runtime.
    Also owns the app fonts (Archivo, loaded from assets/fonts), the sidebar/page styles and the heat color scale
    used by the Hourly and 10-Day pages.
"""

from dataclasses import dataclass
from pathlib import Path

import matplotlib
from matplotlib import font_manager
from PySide6.QtGui import QColor, QFontDatabase, QPalette
from PySide6.QtWidgets import QApplication


# ===== THEME DEFINITION =====
@dataclass(frozen=True)
class Theme:
    """One complete set of UI and chart colors.

    Attributes:
        name: Display name shown in the View > Theme menu.
        window: Main background, also the chart background.
        surface: Cards and chart plot areas.
        border: Card borders, chart spines and gridlines.
        text: Primary text.
        muted: Secondary text and tick labels.
        accent: Highlights and selections.
        hot: Highs and temperature lines.
        cool: Lows.
        precip: Precipitation bars.
        sunrise: Sunrise marker line.
        sunset: Sunset marker line.
        highlighted_text: Text drawn on top of the accent color.
    """

    name: str
    window: str
    surface: str
    border: str
    text: str
    muted: str
    accent: str
    hot: str
    cool: str
    precip: str
    sunrise: str
    sunset: str
    highlighted_text: str


THEMES: dict[str, Theme] = {
    theme.name: theme
    for theme in (
        Theme(
            name="Midnight",  # The original dark theme
            window="#1b1d23", surface="#252832", border="#343846", text="#e6e6eb", muted="#9aa0ae",
            accent="#ff7a45", hot="#ff6b5b", cool="#5aa9ff", precip="#4f8fe0", sunrise="#f5b041",
            sunset="#b48cff", highlighted_text="#1b1d23",
        ),
        Theme(
            name="Heatwave",  # Warm ember browns, for the Too Damn Hot! mood
            window="#1f1512", surface="#2b1d18", border="#45302a", text="#f4e6dc", muted="#b89c8c",
            accent="#ff8a3d", hot="#ff5a3c", cool="#6fb7c9", precip="#5f9fd6", sunrise="#ffc247",
            sunset="#d97ab0", highlighted_text="#1f1512",
        ),
        Theme(
            name="Overcast",  # Softer, lower-contrast cool grays
            window="#262b30", surface="#30363d", border="#424a53", text="#dfe5ea", muted="#9aa5b1",
            accent="#7cc4e0", hot="#f08a6c", cool="#7fb2f0", precip="#6aa8d8", sunrise="#e8c170",
            sunset="#b9a3e3", highlighted_text="#262b30",
        ),
        Theme(
            name="Daylight",  # Light theme; data colors are darkened so they stay readable on white
            window="#eef1f5", surface="#ffffff", border="#d3d8e0", text="#1f2430", muted="#5f6776",
            accent="#e0602a", hot="#d6453a", cool="#2f74d0", precip="#3b82c4", sunrise="#c98a00",
            sunset="#7a4fd0", highlighted_text="#ffffff",
        ),
        Theme(
            name="Cunty Purple",  # Deep plum with a loud orchid accent. Serving.
            window="#1c1424", surface="#271b33", border="#3d2b4d", text="#f3e8f8", muted="#b7a0c8",
            accent="#d26bff", hot="#ff6b9a", cool="#7fb8ff", precip="#6f9fe8", sunrise="#ffc247",
            sunset="#e48cff", highlighted_text="#1c1424",
        ),
    )
}
DEFAULT_THEME = "Midnight"

# Matches the Calibri used by the Qt labels. Picked up front because matplotlib warns about every missing family.
_INSTALLED_FONTS = {font.name for font in font_manager.fontManager.ttflist}
FONT_FAMILY = next((name for name in ("Calibri", "Segoe UI") if name in _INSTALLED_FONTS), "DejaVu Sans")

# Holds the active theme. A dict avoids a `global` statement, which Ruff flags (PLW0603).
_state: dict[str, Theme] = {"theme": THEMES[DEFAULT_THEME]}


# ===== FONTS =====
# Drop the static Archivo .ttf files from Google Fonts in here (Regular, Bold, ExtraCondensed Black/ExtraBold).
# Anything missing falls back to Calibri, so the app still runs without them.
FONTS_DIR = Path(__file__).parent / "assets" / "fonts"
_fonts: dict[str, str] = {"body": FONT_FAMILY, "display": FONT_FAMILY, "mono": "Consolas"}


def load_fonts(folder: Path = FONTS_DIR) -> dict[str, str]:
    """Registers every .ttf in ``folder`` with Qt and picks the body and display families.

    Must be called after the QApplication exists and before apply_theme(), since the stylesheet names the families.

    Args:
        folder: Folder holding the font files. Defaults to assets/fonts next to this file.

    Returns:
        The chosen families, keyed by "body", "display" and "mono".
    """
    if not folder.is_dir():
        return dict(_fonts)

    families: set[str] = set()
    for path in sorted(folder.glob("*.ttf")):
        font_id = QFontDatabase.addApplicationFont(str(path))
        if font_id != -1:
            families.update(QFontDatabase.applicationFontFamilies(font_id))

    if "Archivo" in families:
        _fonts["body"] = "Archivo"
    # Static files sometimes register as "Archivo ExtraCondensed Black", so match on the prefix
    for prefix in ("Archivo ExtraCondensed", "Archivo Condensed", "Archivo"):
        match = next((name for name in sorted(families) if name.startswith(prefix)), None)
        if match:
            _fonts["display"] = match
            break
    return dict(_fonts)


def fonts() -> dict[str, str]:
    """Returns the active font families, keyed by "body", "display" and "mono"."""
    return dict(_fonts)


# ===== HEAT SCALE =====
def heat_color(temp_f: float) -> QColor:
    """Maps a temperature to a blue-to-red color, used for the hourly bars and 10-day highs.

    The scale is fixed in °F (40°F is cool blue, 105°F+ is red) so colors don't shift when the display switches
    to Celsius.

    Args:
        temp_f: Temperature in °F.

    Returns:
        The QColor for that temperature.
    """
    t = max(0.0, min(1.0, (temp_f - 40) / 65))
    return QColor.fromHsvF((200 - t * 195) / 360, 0.62, 0.96)


# ===== PUBLIC API =====
def current() -> Theme:
    """Returns the active theme.

    Graph code should call this at draw time rather than importing colors at module level, because a
    ``from theme import ...`` copies the values once and would never see a theme switch.

    Returns:
        The Theme currently applied.
    """
    return _state["theme"]


def set_theme(name: str) -> Theme:
    """Makes a theme active and applies it to matplotlib. Safe to call without a running Qt app.

    Args:
        name: Key from THEMES. An unknown name (for example a stale saved setting) falls back to DEFAULT_THEME.

    Returns:
        The Theme that was applied.
    """
    theme = THEMES.get(name, THEMES[DEFAULT_THEME])
    _state["theme"] = theme
    _apply_matplotlib(theme)
    return theme


def apply_theme(app: QApplication, name: str) -> Theme:
    """Switches the whole app (Qt widgets and matplotlib) to a theme.

    Call ``app.setStyle("Fusion")`` once before the first call, since the native Windows style ignores most
    palette colors. Charts already on screen keep their old colors until they are redrawn.

    Args:
        app: The running QApplication.
        name: Key from THEMES. Unknown names fall back to DEFAULT_THEME.

    Returns:
        The Theme that was applied.
    """
    theme = set_theme(name)
    app.setPalette(build_palette(theme))
    app.setStyleSheet(build_stylesheet(theme))
    return theme


# ===== QT =====
def build_palette(theme: Theme) -> QPalette:
    """Builds the Qt palette for a theme.

    Args:
        theme: The theme to take colors from.

    Returns:
        A QPalette covering the roles the Fusion style uses.
    """
    palette = QPalette()
    roles = {
        QPalette.ColorRole.Window: theme.window,
        QPalette.ColorRole.WindowText: theme.text,
        QPalette.ColorRole.Base: theme.surface,
        QPalette.ColorRole.AlternateBase: theme.window,
        QPalette.ColorRole.Text: theme.text,
        QPalette.ColorRole.Button: theme.surface,
        QPalette.ColorRole.ButtonText: theme.text,
        QPalette.ColorRole.ToolTipBase: theme.surface,
        QPalette.ColorRole.ToolTipText: theme.text,
        QPalette.ColorRole.PlaceholderText: theme.muted,
        QPalette.ColorRole.Highlight: theme.accent,
        QPalette.ColorRole.HighlightedText: theme.highlighted_text,
        QPalette.ColorRole.Link: theme.cool,
        QPalette.ColorRole.Mid: theme.border,
        QPalette.ColorRole.Dark: theme.border,
    }
    for role, color in roles.items():
        palette.setColor(role, QColor(color))
    for role in (QPalette.ColorRole.Text, QPalette.ColorRole.WindowText, QPalette.ColorRole.ButtonText):
        palette.setColor(QPalette.ColorGroup.Disabled, role, QColor(theme.muted))
    return palette


def build_stylesheet(theme: Theme) -> str:
    """Builds the Qt stylesheet for the sidebar, pages, cards and label roles.

    Labels pick up a style by setting a ``role`` property (in Designer or with ``label.setProperty("role", ...)``).

    Args:
        theme: The theme to take colors from.

    Returns:
        A stylesheet string for ``app.setStyleSheet()``.
    """
    body, display, mono = _fonts["body"], _fonts["display"], _fonts["mono"]
    return f"""
QWidget {{ font-family: "{body}"; font-size: 14px; }}
QWidget[page="true"], QScrollArea {{ background: {theme.window}; border: none; }}
QStatusBar {{ background: {theme.window}; color: {theme.muted}; border-top: 1px solid {theme.border}; }}
QMenu::item:selected, QMenuBar::item:selected {{ background: {theme.border}; color: {theme.text}; }}

QListWidget#navList {{
    background: {theme.window}; border: none; border-right: 1px solid {theme.border};
    padding: 12px 10px; font-size: 15px; outline: 0;
}}
QListWidget#navList::item {{ padding: 8px 12px; margin: 1px 0; border-radius: 6px; color: {theme.text}; }}
QListWidget#navList::item:hover {{ background: {theme.surface}; }}
QListWidget#navList::item:selected {{ background: {theme.accent}; color: {theme.highlighted_text}; }}

QFrame[card="true"] {{ background: {theme.surface}; border: 1px solid {theme.border}; border-radius: 8px; }}
QFrame[card="true"] QLabel {{ background: transparent; border: none; }}
QFrame[banner="true"] {{ background: {theme.accent}; border-radius: 8px; }}
QFrame[banner="true"] QLabel {{ background: transparent; color: {theme.highlighted_text}; font-size: 15px; }}
QFrame[row="true"] {{ background: transparent; border: none; border-top: 1px solid {theme.border}; }}
QFrame[now="true"] {{ background: {theme.surface}; border-radius: 6px; }}

QLabel[role="title"] {{ font-family: "{display}"; font-size: 40px; font-weight: 900; color: {theme.text}; }}
QLabel[role="subtitle"] {{ font-size: 15px; color: {theme.muted}; }}
QLabel[role="section"] {{ font-size: 15px; font-weight: bold; color: {theme.muted}; }}
QLabel[role="location"] {{ font-size: 26px; font-weight: 800; }}
QLabel[role="bigtemp"] {{ font-family: "{display}"; font-size: 150px; font-weight: 900; color: {theme.accent}; }}
QLabel[role="headline"] {{ font-family: "{display}"; font-size: 46px; font-weight: 800; color: {theme.text}; }}
QLabel[role="kicker"] {{ font-family: "{mono}"; font-size: 11px; color: {theme.muted}; }}
QLabel[role="mono"] {{ font-family: "{mono}"; font-size: 12px; color: {theme.muted}; }}
QLabel[role="body"] {{ font-size: 16px; }}
QLabel[role="strong"] {{ font-size: 16px; font-weight: bold; }}
QLabel[role="small"] {{ font-size: 13px; }}
QLabel[role="h3"] {{ font-size: 18px; font-weight: bold; }}
QLabel[role="accent"] {{ font-size: 15px; font-weight: bold; color: {theme.accent}; }}
QLabel[role="sub"] {{ color: {theme.muted}; }}
QLabel[role="hot"] {{ color: {theme.hot}; }}
QLabel[role="cool"] {{ font-size: 17px; color: {theme.cool}; }}
QLabel[role="precip"] {{ font-size: 13px; color: {theme.precip}; }}
QLabel[role="sunrise"] {{ font-size: 15px; color: {theme.sunrise}; }}
QLabel[role="sunset"] {{ font-size: 15px; color: {theme.sunset}; }}
QLabel[role="dayname"] {{ font-family: "{display}"; font-size: 18px; font-weight: 800; }}
QLabel[role="dayhi"] {{ font-family: "{display}"; font-size: 38px; font-weight: 900; }}
QLabel[role="placetemp"] {{ font-family: "{display}"; font-size: 34px; font-weight: 900; }}
QLabel[role="pill"] {{ padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }}
QLabel[role="tag"] {{
    padding: 1px 6px; border-radius: 4px; font-size: 11px; background: {theme.border}; color: {theme.muted};
}}

QLabel[role="day"] {{ color: {theme.muted}; font-weight: bold; }}
QLabel[role="main"] {{ font-size: 22px; font-weight: bold; color: {theme.hot}; }}
QLabel[role="low"] {{ color: {theme.cool}; }}

QPushButton {{
    padding: 6px 14px; border: 1px solid {theme.border}; border-radius: 6px;
    background: {theme.surface}; color: {theme.text};
}}
QPushButton:hover {{ border-color: {theme.muted}; }}
QPushButton[primary="true"] {{
    background: {theme.accent}; color: {theme.highlighted_text}; border: none; font-weight: bold;
}}
QComboBox, QSpinBox {{ padding: 4px 8px; min-width: 160px; }}
"""


# ===== MATPLOTLIB =====
def _apply_matplotlib(theme: Theme) -> None:
    """Points matplotlib's defaults at a theme. Affects figures and axes created after the call.

    Args:
        theme: The theme to take colors from.
    """
    matplotlib.rcParams.update({
        "figure.facecolor": theme.window,
        "savefig.facecolor": theme.window,
        "axes.facecolor": theme.surface,
        "axes.edgecolor": theme.border,
        "axes.labelcolor": theme.muted,
        "axes.titlecolor": theme.text,
        "axes.titleweight": "bold",
        "axes.titlesize": 13,
        "axes.labelsize": 10,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "grid.color": theme.border,
        "grid.linewidth": 0.8,
        "text.color": theme.text,
        "xtick.color": theme.muted,
        "ytick.color": theme.muted,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.frameon": False,
        "legend.labelcolor": theme.text,
        "legend.fontsize": 9,
        "font.family": FONT_FAMILY,
    })


set_theme(DEFAULT_THEME)  # Standalone graph scripts get a styled chart without any Qt setup
