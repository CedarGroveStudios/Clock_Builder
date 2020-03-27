# clock_repl.py
# 2020-01-31 Cedar Grove Studios
# uses cedargrove unit_converter library

import time
import board
import adafruit_ds3231
from cedargrove_unit_converter.chronos import adjust_dst

i2c = board.I2C()
ds3231 = adafruit_ds3231.DS3231(i2c)

### SETTINGS ###
clock_display     = "repl"     # describes display type
clock_zone        = "Pacific"  # free text
clock_24_hour     = False      # 24-hour clock; 12-hour AM/PM
clock_auto_dst    = True       # automatic US DST
weekday = ["Mon", "Tue", "Wed", "Thr", "Fri", "Sat", "Sun"]

### HELPERS ###
def repl_clock_display(date_time, dst):  # REPL Clock Display
    if dst:  # changes the text to show daylight saving time or standard time
        flag_text = clock_zone[0] + "DT"
    else:
        flag_text = clock_zone[0] + "ST"

    hour = date_time.tm_hour  # Format for 24-hour or 12-hour output
    if clock_24_hour:  # 24-hour
        am_pm = ""
    else:  # 12-hour clock with AM/PM
        am_pm = "AM"
        if hour >= 12:
            hour = hour - 12
            am_pm = "PM"

    print("{}: {}/{}/{} {:02}:{:02}:{:02} {}  {}".format(flag_text,
          date_time.tm_mon, date_time.tm_mday, date_time.tm_year,
          hour, date_time.tm_min, date_time.tm_sec, am_pm,
          weekday[date_time.tm_wday]))
    return

# Manually set time upon RTC power failure
if ds3231.lost_power:
    print("power lost since last setting")
    print("REPL setting mode")
    set_yr  = int(input("enter year (YYYY):"))
    set_mon = int(input("enter month (MM):"))
    set_dom = int(input("enter day-of-month (DD):"))
    set_hr  = int(input("enter 24-hour clock hour (hh):"))
    set_min = int(input("enter minute (mm):"))

    # Set RTC time:                     year, mon, date, hour,
    #                                   min, sec, wday, yday, isdst
    ds3231.datetime = time.struct_time((set_yr, set_mon, set_dom, set_hr,
                                        set_min, 0, -1, -1, -1))

    # Fix weekday and yearday structured time errors
    ds3231.datetime = time.localtime(time.mktime(ds3231.datetime))

while True:
    # Check datetime and adjust if DST
    if clock_auto_dst:
        current, is_dst = adjust_dst(ds3231.datetime)  # read the RTC and adjust for DST
    else:
        current = ds3231.datetime  # otherwise, just read the RTC
        is_dst = False

    if clock_display == "repl":
        repl_clock_display(current, is_dst)

    prev_sec = current.tm_sec
    while current.tm_sec == prev_sec:  # wait a second before looping
        current = ds3231.datetime
