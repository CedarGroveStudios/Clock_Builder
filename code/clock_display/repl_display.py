# repl_display.py
# 2020-02-05 Cedar Grove Studios

class ReplDisplay:

    def __init__(self, timezone="Pacific", hour_24_12=False, auto_dst=True,
                 alarm=False, debug=False):
        #input parameters
        self._timezone   = timezone
        self._hour_24_12 = hour_24_12
        self._dst        = False
        self._auto_dst   = auto_dst
        self._alarm      = alarm

        self._weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

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
    def alarm(self, alarm=False):
        self._alarm = alarm

    @property
    def show(self):
        """Display time via REPL."""
        return

    @show.setter
    def show(self, datetime):
        """Display time via REPL."""
        self._datetime = datetime

        if self._auto_dst and self._dst:  # changes the text to show DST
            flag_text = self._timezone[0] + "DT"
        else:  # or Standard Time
            flag_text = self._timezone[0] + "ST"

        hour = self._datetime.tm_hour  # Format for 24-hour or 12-hour output
        if self._hour_24_12:  # 24-hour
            am_pm = ""
        else:  # 12-hour clock with AM/PM
            am_pm = "AM"
            if hour >= 12:
                hour = hour - 12
                am_pm = "PM"
            if hour == 0:  # midnight hour fix
                hour = 12

        print("{} {}/{}/{}".format(self._weekday[self._datetime.tm_wday],
                                      self._datetime.tm_year,
                                      self._datetime.tm_mon,
                                      self._datetime.tm_mday))

        print("{}: {:02}:{:02}:{:02}".format(flag_text, hour,
                                             self._datetime.tm_min,
                                             self._datetime.tm_sec, am_pm,
                                             self._weekday[self._datetime.tm_wday]))
        return
