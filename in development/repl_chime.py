# repl_chime.py
# 2020-01-31 Cedar Grove Studios

import time

class ReplChime:

    def __init__(self, tick="tick", half="half", hour="hour", alarm="alarm",
                 debug=False):
        #input parameters
        self._set_tick  = tick
        self._set_half  = half
        self._set_hour  = hour
        self._set_alarm = alarm

        # debug parameters
        self._debug = debug
        if self._debug:
            print("*Init:", self.__class__)
            print("*Init: ", self.__dict__)

    @property
    def tick(self):
        """Tick sound."""
        return self._tick

    @tick.setter
    def tick(self, tick):
        self._set_tick = tick

    @property
    def half(self):
        """Half-hour sound."""
        return self._half

    @half.setter
    def half(self, half):
        self._set_half = half

    @property
    def hour(self):
        """Hourly sound."""
        return self._hour

    @hour.setter
    def hour(self, hour):
        self._hour = hour

    @property
    def alarm(self):
        """Alarm sound."""
        return self._alarm

    @alarm.setter
    def alarm(self, alarm):
        self._alarm = alarm
