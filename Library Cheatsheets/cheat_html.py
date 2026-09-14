import pydoc
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import meteostat as ms
import FreeSimpleGUI as sg

#===== BUILD OUTPUT FOLDER =====
output_dir = Path("Library Cheatsheets")
output_dir.mkdir(exist_ok=True)

#===== GENERATE HTML DOCS =====
def write_html_doc(module, filename):
    html = pydoc.HTMLDoc().docmodule(module)
    (output_dir / filename).write_text(html, encoding="utf-8")

write_html_doc(plt, "matplotlib_cheatsheet.html")
write_html_doc(Path, "pathlib_cheatsheet.html")
write_html_doc(ms, "meteostat_cheatsheet.html")
write_html_doc(sg, "freesimplegui_cheatsheet.html")

print("HTML cheatsheets generated in 'Library Cheatsheets/'")