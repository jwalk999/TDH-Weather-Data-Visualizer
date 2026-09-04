"""
File Name: weather_data.py
Author: Jonathan W
Date: 9/1/2026
Version: 0.0.1
Scope: Testing the DateTime() function 
"""
# importing functions for date and time from DateTime library
from datetime import datetime
import datetime as dt
from zoneinfo import ZoneInfo
# e is the variable that is set to Eastern Standard Time, returns current date and tiem
date_time_now = datetime.now(ZoneInfo('US/Eastern'))
date_time_end = date_time_now.replace(hour=23, minute=59, second=59, microsecond=0)

print(date_time_now)
print(date_time_end)

