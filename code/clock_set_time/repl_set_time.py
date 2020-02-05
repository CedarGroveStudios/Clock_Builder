# repl_set_time.py
# 2020-02-01 Cedar Grove Studios

import time

class ReplSetTime:

    def __init__(self, yr=2000, mon=1, dom=1, hr=0, min=0, debug=False):
        #input parameters
        self._set_yr  = yr
        self._set_mon = mon
        self._set_dom = dom
        self._set_hr  = hr
        self._set_min = min
        self._datetime = time.localtime()

        # debug parameters
        self._debug = debug
        if self._debug:
            print("*Init:", self.__class__)
            print("*Init: ", self.__dict__)

    @property
    def datetime(self):
        """Manual input of time via REPL."""
        print("REPL setting mode")
        set_yr  = input("enter year (YYYY):")
        if set_yr == "":
            set_yr = int(2000)
        else:
            set_yr = max(2000, min(2037, int(set_yr)))

        set_mon = input("enter month (MM):")
        if set_mon == "":
            set_mon = 1
        else:
            set_mon = max(1, min(12, int(set_mon)))

        set_dom = input("enter day-of-month (DD):")
        if set_dom == "":
            set_dom = 1
        else:
            set_dom = max(1, min(31, int(set_dom)))

        set_hr  = input("enter 24-hour clock hour (hh):")
        if set_hr == "":
            set_hr = 0
        else:
            set_hr = max(0, min(24, int(set_hr)))

        set_min = input("enter minute (mm):")
        if set_min == "":
            set_min = 0
        else:
            set_min = max(0, min(59, int(set_min)))

        # Build structured time:         ((year, mon, date, hour,
        #                                  min, sec, wday, yday, isdst))
        self._datetime = time.struct_time((set_yr, set_mon, set_dom, set_hr,
                                           set_min, 0, -1, -1, -1))

        # Fix weekday and yearday structured time errors
        self._datetime = time.localtime(time.mktime(self._datetime))
        return self._datetime

    @datetime.setter
    def datetime(self, date_time):
        return self._datetime
