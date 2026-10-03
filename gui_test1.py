"""
File Name: gui_test.py

Author: Jonathan W
Date Created: 10/2/2026

Scope: Testing FreeSimpleGUI elements and usage
"""
# ============================================================================
# =============================== IMPORTS ====================================
# ============================================================================

import sys
from pathlib import Path

import FreeSimpleGUI as sg

from Daily_Graph import make_daily_graphs
from Hourly_Graph import make_hourly_graphs


# Create function to mark the root directory
def _find_project_root(marker="Config"):
    """
    Set the folder directory for all scripts to append their search queries

    Returns: the full folder path of the program
    Errors: Raise a runtime error if it cannot find the Config file
    """

    path = Path(__file__).resolve().parent
    while not (path / marker).is_dir():
        if path.parent == path:
            raise RuntimeError(
                f"Could not find project root (looking for '{marker}' folder)"
            )
        path = path.parent
    return path

# set system file path to project root
sys.path.append(str(_find_project_root()))
# set the project's root folder
PROJECT_ROOT = _find_project_root()


# ============================================================================
# =============================== VARIABLES ==================================
# ============================================================================

layout = [[sg.Text('Window that Auto-saves position', font='_ 25')],
          [sg.Button('Ok'), sg.Button('Exit')]]

window = sg.Window('Auto-saves Location', layout, enable_close_attempted_event=True, location=sg.user_settings_get_entry('-location-', (None, None)))

while True:
    event, values = window.read()
    print(event, values)
    if event in ('Exit', sg.WINDOW_CLOSE_ATTEMPTED_EVENT):
        sg.user_settings_set_entry('-location-', window.current_location())  # The line of code to save the position before exiting
        break

window.close()

