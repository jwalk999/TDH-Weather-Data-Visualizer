"""
File Name: theme.py

Author: Jonathan W
Date Created: 10/15/2026
Last Update: 10/15/2026
Version: 1.0.0

Scope: One dark color palette shared by the Qt window and the matplotlib charts, so the graphs blend into the UI.
    Importing this module also applies the dark matplotlib style.
"""

import matplotlib
from matplotlib import font_manager
from PySide6.QtGui import QColor, QPalette

# ===== PALETTE =====
WINDOW = "#1b1d23"  # Main background, also the chart background
SURFACE = "#252832"  # Cards and chart plot areas
BORDER = "#343846"  # Card borders, chart spines and gridlines
TEXT = "#e6e6eb"  # Primary text
MUTED = "#9aa0ae"  # Secondary text, tick labels
ACCENT = "#ff7a45"  # Highlights and selections

HOT = "#ff6b5b"  # Highs and temperature lines
COOL = "#5aa9ff"  # Lows
PRECIP = "#4f8fe0"  # Precipitation bars
SUNRISE = "#f5b041"
SUNSET = "#b48cff"

# Matches the Calibri used by the Qt labels. Picked up front because matplotlib warns about every missing family.
_INSTALLED_FONTS = {font.name for font in font_manager.fontManager.ttflist}
FONT_FAMILY = next((name for name in ("Calibri", "Segoe UI") if name in _INSTALLED_FONTS), "DejaVu Sans")

# ===== MATPLOTLIB =====
matplotlib.rcParams.update({
    "figure.facecolor": WINDOW,
    "savefig.facecolor": WINDOW,
    "axes.facecolor": SURFACE,
    "axes.edgecolor": BORDER,
    "axes.labelcolor": MUTED,
    "axes.titlecolor": TEXT,
    "axes.titleweight": "bold",
    "axes.titlesize": 13,
    "axes.labelsize": 10,
    "axes.grid": True,
    "axes.grid.axis": "y",
    "axes.axisbelow": True,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "grid.color": BORDER,
    "grid.linewidth": 0.8,
    "text.color": TEXT,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.frameon": False,
    "legend.labelcolor": TEXT,
    "legend.fontsize": 9,
    "font.family": FONT_FAMILY,
})


# ===== QT =====
def dark_palette() -> QPalette:
    """Builds the dark Qt palette used by the whole window.

    Returns:
        A QPalette using the colors above. Apply it after ``app.setStyle("Fusion")``, since the native Windows
        style ignores most palette colors.
    """
    palette = QPalette()
    roles = {
        QPalette.ColorRole.Window: WINDOW,
        QPalette.ColorRole.WindowText: TEXT,
        QPalette.ColorRole.Base: SURFACE,
        QPalette.ColorRole.AlternateBase: WINDOW,
        QPalette.ColorRole.Text: TEXT,
        QPalette.ColorRole.Button: SURFACE,
        QPalette.ColorRole.ButtonText: TEXT,
        QPalette.ColorRole.ToolTipBase: SURFACE,
        QPalette.ColorRole.ToolTipText: TEXT,
        QPalette.ColorRole.PlaceholderText: MUTED,
        QPalette.ColorRole.Highlight: ACCENT,
        QPalette.ColorRole.HighlightedText: WINDOW,
        QPalette.ColorRole.Link: COOL,
        QPalette.ColorRole.Mid: BORDER,
        QPalette.ColorRole.Dark: WINDOW,
    }
    for role, color in roles.items():
        palette.setColor(role, QColor(color))
    for role in (QPalette.ColorRole.Text, QPalette.ColorRole.WindowText, QPalette.ColorRole.ButtonText):
        palette.setColor(QPalette.ColorGroup.Disabled, role, QColor(MUTED))
    return palette


STYLESHEET = f"""
QScrollArea, #scrollAreaWidgetContents {{ background: {WINDOW}; border: none; }}
QFrame[card="true"] {{ background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 8px; }}
QFrame[card="true"] QLabel {{ background: transparent; border: none; }}
QLabel[role="day"] {{ color: {MUTED}; font-weight: bold; }}
QLabel[role="sub"] {{ color: {MUTED}; }}
QMenu::item:selected, QMenuBar::item:selected {{ background: {BORDER}; }}
"""
