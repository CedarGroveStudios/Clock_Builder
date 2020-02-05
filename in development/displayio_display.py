# repl_clock.py
# 2020-01-31 Cedar Grove Studios

import board
import displayio

class DisplayioDisplay:

    def __init__(self, timezone="Pacific", hour_24_12=False, dst=True,
                 debug=False):
        #input parameters
        self._timezone = timezone
        self._hour_24_12 = hour_24_12
        self._dst = dst

        self._weekday = ["Mon", "Tue", "Wed", "Thr", "Fri", "Sat", "Sun"]

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
    def auto_dst(self):
        """Automatically display US DST. Default is auto DST (True)."""
        return self._dst

    @auto_dst.setter
    def auto_dst(self, dst):
        self._dst = dst

    @property
    def show(self):
        """Display time via REPL."""
        return

    @show.setter
    def show(self, date_time):
        """Display time via Displayio."""
        self._date_time = date_time

        if self._dst:  # changes the text to show DST or standard time
            flag_text = self._timezone[0] + "DT"
        else:
            flag_text = self._timezone[0] + "ST"

        hour = self._date_time.tm_hour  # Format for 24-hour or 12-hour output
        if self._hour_24_12:  # 24-hour
            am_pm = ""
        else:  # 12-hour clock with AM/PM
            am_pm = "AM"
            if hour >= 12:
                hour = hour - 12
                am_pm = "PM"

        """print("{}: {}/{}/{} {:02}:{:02}:{:02} {}  {}".format(flag_text,
              self._date_time.tm_mon, self._date_time.tm_mday,
              self._date_time.tm_year, hour, self._date_time.tm_min,
              self._date_time.tm_sec, am_pm, self._weekday[date_time.tm_wday]))"""
        return
