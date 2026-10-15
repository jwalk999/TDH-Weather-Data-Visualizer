"""
File Name: theme.py

Author: Jonathan W
Date Created: 10/15/2026
Last Update: 10/15/2026
Version: 2.0.0

Scope: Switchable color themes shared by the Qt window and the matplotlib charts, so the graphs always blend into
    the UI. Importing this module applies the default theme to matplotlib; call apply_theme() to switch at runtime.
"""

from dataclasses import dataclass

import matplotlib
from matplotlib import font_manager
from PySide6.QtGui import QColor, QPalette
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
    )
}
DEFAULT_THEME = "Midnight"

# Matches the Calibri used by the Qt labels. Picked up front because matplotlib warns about every missing family.
_INSTALLED_FONTS = {font.name for font in font_manager.fontManager.ttflist}
FONT_FAMILY = next((name for name in ("Calibri", "Segoe UI") if name in _INSTALLED_FONTS), "DejaVu Sans")

# Holds the active theme. A dict avoids a `global` statement, which Ruff flags (PLW0603).
_state: dict[str, Theme] = {"theme": THEMES[DEFAULT_THEME]}


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
    """Builds the Qt stylesheet for the forecast cards, scroll area and menus.

    Args:
        theme: The theme to take colors from.

    Returns:
        A stylesheet string for ``app.setStyleSheet()``.
    """
    return f"""
QScrollArea, #scrollAreaWidgetContents {{ background: {theme.window}; border: none; }}
QFrame[card="true"] {{ background: {theme.surface}; border: 1px solid {theme.border}; border-radius: 8px; }}
QFrame[card="true"] QLabel {{ background: transparent; border: none; }}
QLabel[role="day"] {{ color: {theme.muted}; font-weight: bold; }}
QLabel[role="sub"] {{ color: {theme.muted}; }}
QMenu::item:selected, QMenuBar::item:selected {{ background: {theme.border}; color: {theme.text}; }}
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
