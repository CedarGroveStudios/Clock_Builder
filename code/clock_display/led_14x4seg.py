# led_14x4_display.py
# 2020-02-04 Cedar Grove Studios

import time
import board
from adafruit_ht16k33.segments import Seg14x4

class Led14x4Display:

    def __init__(self, timezone="Pacific", hour_24_12=False, auto_dst=True,
                 alarm=False, brightness=15, debug=False):
        #input parameters
        self._timezone   = timezone
        self._hour_24_12 = hour_24_12
        self._dst        = False
        self._auto_dst   = auto_dst
        self._alarm      = alarm
        self._colon      = True

        self._weekday = ["Mon", "Tue", "Wed", "Thr", "Fri", "Sat", "Sun"]

        i2c = board.I2C()
        self._display = Seg14x4(i2c, address=0x70)
        self._display.brightness = brightness
        self._display.fill(0)  # Clear the display
        self._display.print("----")
        self._display.show()

        # debug parameters
        self._debug = debug
        if self._debug:
            print("*Init:", self.__class__)
            print("*Init: ", self.__dict__)

    @property
    def zone(self):
        """The clock's time zone. Default is Pacific."""
        return self._timezone

    @zone.setter
    def zone(self, timezone):
        self._timezone = timezone

    @property
    def hour_24(self):
        """Display 24-hour or 12-hour AM/PM. Default is 12-hour (False)."""
        return self._hour_24_12

    @hour_24.setter
    def hour_24(self, hour_24_12):
        self._hour_24_12 = hour_24_12

    @property
    def dst(self):
        """Time is US DST. Default is Standard Time (False)."""
        return self._dst

    @dst.setter
    def dst(self, dst):
        self._dst = dst

    @property
    def auto_dst(self):
        """Automatically display US DST. Default is auto DST (True)."""
        return self._auto_dst

    @auto_dst.setter
    def auto_dst(self, auto_dst):
        self._auto_dst = auto_dst

    @property
    def alarm(self):
        """Alarm is activated. Default is no alarm (False)."""
        return self._alarm

    @alarm.setter
    def alarm(self, alarm):
        self._dst = alarm

    @property
    def brightness(self):
        """Display brightness. Default is 15 (maximum)."""
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        self._dst = brightness

    @property
    def colon(self):
        """Display the colon."""
        return self._colon

    @colon.setter
    def colon(self, colon=True):
        """Display the colon."""
        self._colon = colon

    @property
    def show(self):
        """Display time via LED display."""
        return

    @show.setter
    def show(self, datetime, dot=True):
        """Display time via LED display."""
        self._datetime = datetime

        if self._auto_dst and self._dst:  # changes the text to show DST
            flag_text = self._timezone[0] + "DT"
        else:  # or Standard Time
            flag_text = self._timezone[0] + "ST"

        hour = self._datetime.tm_hour  # Format for 24-hour or 12-hour output
        if not self._hour_24_12:  # 12-hour
            if hour >= 12:
                hour = hour - 12

        if self._colon:
            self._display.print("{:02}.{:02}".format(hour, self._datetime.tm_min))
        else:
            self._display.print("{:02}{:02}".format(hour, self._datetime.tm_min))

        self._display.show()

        return
