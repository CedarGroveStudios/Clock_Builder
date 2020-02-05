# clock_test.py
# 2020-02-04 Cedar Grove Studios
# uses cedargrove unit_converter library

import time
import board
import adafruit_ds3231
from unit_converter.chronos       import adjust_dst
from clock_display.repl_display   import ReplDisplay
from clock_display.led_14x4seg    import Led14x4Display
# from clock_display.led_7x4seg     import Led7x4Display
from clock_set_time.repl_set_time import ReplSetTime

i2c = board.I2C()
ds3231 = adafruit_ds3231.DS3231(i2c)

### SETTINGS ###
clock_display  = ["led", "repl"]  # Describes display type
clock_zone     = "Pacific"        # Free text
clock_24_hour  = False            # 24-hour clock; 12-hour AM/PM
clock_auto_dst = True             # Automatic US DST
clock_alarm    = False            # Alarm is activated

led_disp  = Led14x4Display(clock_zone, clock_24_hour, clock_auto_dst, clock_alarm, brightness=2, debug=False)
# led_disp  = Led7x4Display(clock_zone, clock_24_hour, clock_auto_dst, clock_alarm, brightness=2, debug=False)
repl_disp = ReplDisplay(clock_zone, clock_24_hour, clock_auto_dst, clock_alarm, debug=False)
repl_set  = ReplSetTime(debug=False)

### HELPERS ###

# Manually set time upon RTC power failure
if ds3231.lost_power:
    ds3231.datetime = repl_set.datetime

min_flag = half_flag = hour_flag = False

while True:
    # Check datetime and adjust if DST
    if clock_auto_dst:
        current, is_dst = adjust_dst(ds3231.datetime)  # read the RTC and adjust for DST
    else:
        current = ds3231.datetime  # otherwise, just read the RTC
        is_dst = False

    # update REPL display
    if "repl" in clock_display:
        repl_disp.show = current

    # update led display
    if "led" in clock_display:
        led_disp.colon  = not led_disp.colon
        led_disp.show   = current

    # Do something every minute
    if current.tm_sec == 0 and not min_flag:
        # do something here
        print("every MIN")
        min_flag = True
    elif current.tm_sec > 0:
        min_flag = False

    # Do something every half-hour
    if current.tm_min == 30 and not half_flag:
        # do something here
        print("every HALF")
        half_flag = True
    elif current.tm_min > 30:
        half_flag = False

    # Do something every hour
    if current.tm_min == 0 and not hour_flag:
        # do something here
        print("every HOUR")
        hour_flag = True
    elif current.tm_min > 0:
        hour_flag = False

    # wait a second before looping
    prev_sec = current.tm_sec
    while current.tm_sec == prev_sec:  # wait a second before looping
        current = ds3231.datetime
