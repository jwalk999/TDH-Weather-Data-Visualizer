import inspect
from pathlib import Path
import matplotlib as plt
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import meteostat as ms
import FreeSimpleGUI as sg
import io
import contextlib

def capture_help(obj):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        help(obj)
    return buffer.getvalue()




with open("Library Cheatsheets/matplotlib_cheatsheet.txt", "w+", encoding="utf-8") as sheet1:
    sheet1.write("Help Function\n")
    sheet1.write(capture_help(plt))
    sheet1.write("\n__________________\n")
    sheet1.write("Directory Function\n")
    sheet1.write(str(dir(plt)))

with open("Library Cheatsheets/pathlib_cheatsheet.txt", "w+", encoding="utf-8") as sheet2:
    sheet2.write("Help Function\n")
    sheet2.write(capture_help(Path))
    sheet2.write("\n__________________\n")
    sheet2.write("Directory Function\n")
    sheet2.write(str(dir(Path)))

with open("Library Cheatsheets/meteostat_cheatsheet.txt", "w+", encoding="utf-8") as sheet3:
    sheet3.write("Help Function\n")
    sheet3.write(capture_help(ms))
    sheet3.write("\n__________________\n")
    sheet3.write("Directory Function\n")
    sheet3.write(str(dir(ms)))

with open("Library Cheatsheets/freesimplegui_cheatsheet.txt", "w+", encoding="utf-8") as sheet4:
    sheet4.write("Help Function\n")
    sheet4.write(capture_help(sg))
    sheet4.write("\n__________________\n")
    sheet4.write("Directory Function\n")
    sheet4.write(str(dir(sg)))