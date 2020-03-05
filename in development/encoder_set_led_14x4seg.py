# led_14x4_display.py
# 2020-02-05 Cedar Grove Studios

import time
import board
import rotaryio
from digitalio import DigitalInOut, Direction, Pull
import rotaryio as enc
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

        self._weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self._month   = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                         "Sep", "Oct", "Nov", "Dec"]

        self._sel_sw = DigitalInOut(board.D9)
        self._sel_sw.direction = Direction.INPUT
        self._sel_sw.pull = Pull.UP
        self._enc = rotaryio.IncrementalEncoder(board.D5, board.D6)

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

    def show(self, datetime, dot=True, date=False):
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
            if hour == 0:  # midnight hour fix
                hour = 12

        if not date:
            if self._colon:
                self._display.print("{:02}.{:02}".format(hour, self._datetime.tm_min))
            else:
                self._display.print("{:02}{:02}".format(hour, self._datetime.tm_min))

        else:
            self._clock_wday  = self._weekday[self._datetime.tm_wday]
            self._clock_month = self._month[self._datetime.tm_mon - 1]
            self._clock_mday  = "{:02d}".format(self._datetime.tm_mday)
            self._clock_year  = "{:04d}".format(self._datetime.tm_year)

            self._clock_digits_hour = "{:02}".format(hour)
            self._clock_digits_min  = "{:02}".format(self._datetime.tm_min)
            if self._colon:
                self._clock_digits_colon = "."
            else:
                self._clock_digits_colon = ""

            self._display.marquee(self._clock_wday + " " + self._clock_month + " " +
                                  self._clock_mday + ", " + self._clock_year +
                                  "    ", delay=0.4, loop=False)

        self._display.show()
        return

        def set_datetime(self, xst_datetime):
            """Manual input of time via PyBadge DisplayIO."""
            self._xst_datetime = xst_datetime

            if not self._sel_sw.value:  # select switch pressed?
                return self._xst_datetime, False  # return datetime and "no change" flag

            while self._sel_sw:  # wait for switch release
                pass

            while True:
                position = enc.position
                if last_position == None or position != last_position:
                    print(position, not sel_sw.value)
                last_position = position
                time.sleep(.1)