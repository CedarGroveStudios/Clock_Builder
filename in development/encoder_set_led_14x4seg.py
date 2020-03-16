# encoder_set_led_14x4seg.py
# 2020-03-11 Cedar Grove Studios
# with encoder time set function

import time
import board
import rotaryio
from digitalio import DigitalInOut, Direction, Pull
import rotaryio as enc
from adafruit_ht16k33.segments import Seg14x4

class Led14x4Display:

    def __init__(self, timezone="Pacific", hour_24_12=False, auto_dst=True,
                 sound=False, brightness=15, debug=False):
        #input parameters
        self._timezone   = timezone
        self._hour_24_12 = hour_24_12
        self._dst        = False
        self._auto_dst   = auto_dst
        self._sound      = sound
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

    def show(self, datetime, date=False):
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

            self._display.marquee(self._clock_wday + " " + self._clock_month + " " +
                                  self._clock_mday + ", " + self._clock_year + " " +
                                  self._clock_digits_hour + "." +
                                  self._clock_digits_min + "    ",
                                  delay=0.4, loop=False)

        self._display.show()
        return

    ### SET DATETIME WITH ROTARY ENCODER ###
    def set_datetime(self, xst_datetime):
        """Manual input of time using a rotary encoder."""
        self._xst_datetime = xst_datetime

        if self._sel_sw.value:  # select switch not pressed
            return self._xst_datetime, self._sound, False  # return datetime, sound flag, and "no change" flag

        # self.panel.play_tone(784, 0.030)  # G5 piezo?
        self.show(self._xst_datetime, date=True)

        while not self._sel_sw.value:  # wait until switch is released
            pass
        self._display.print("-SET")
        time.sleep(1)

        self._param_index  = 0      # Reset index of parameter list
        self._enc.position = 0      # Reset encoder position value
        self._changed      = False  # Reset edit change flag

        # Select parameter to change
        self._t0 = time.monotonic()  # start timeout clock
        while self._sel_sw.value and time.monotonic() - self._t0 < 10:  # while select switch not pressed
            self._t0 = time.monotonic()  # start timeout clock
            while self._sel_sw.value and time.monotonic() - self._t0 < 10:  # while select switch not pressed
                self._param_index = self._enc.position
                self._param_index = max(0, min(5, self._param_index))
                if self._enc.position != self._param_index:
                    self._t0 = time.monotonic()  # start timeout clock over
                self._enc.position = self._param_index

                ### display parameter prompt
                if self._param_index == 0:  # Set MON parameter
                    self._display.print("MNTH")
                if self._param_index == 1:  # set DOM parameter
                    self._display.print("DATE")
                if self._param_index == 2:  # set YEAR parameter
                    self._display.print("YEAR")
                if self._param_index == 3:  # set HOUR parameter
                    self._display.print("HOUR")
                if self._param_index == 4:  # set MIN parameter
                    self._display.print("MIN ")
                if self._param_index == 5:  # set SOUND parameter
                    self._display.print("SFX ")

                time.sleep(0.15)

            # Select switch pressed
            # self.panel.play_tone(1319, 0.030)  # E6 piezo?

            while not self._sel_sw.value:  # wait for switch to release
                pass

            # Adjust parameter value
            while self._sel_sw.value and time.monotonic() - self._t0 < 10:  # select switch not pressed
                self._changed = False
                ### hard code parameter edits and actions
                if self._param_index == 0:  # Set MON parameter
                    self._changed = True
                if self._param_index == 1:  # set DOM parameter
                    self._changed = True
                if self._param_index == 2:  # set YEAR parameter
                    self._changed = True
                if self._param_index == 3:  # set HOUR parameter
                    self._changed = True
                if self._param_index == 4:  # set MIN parameter
                    self._changed = True
                if self._param_index == 5:  # set SOUND parameter
                    self._changed = True

                self._parameter_value = self._enc.position

                ### adjust edit values

                time.sleep(.2)

            # Select switch pressed
            # self.panel.play_tone(1319, 0.030)  # E6 piezo

            while not self._sel_sw.value:  # Wait for select switch release
                pass

        # Exit setup process
        if not self._sel_sw.value:  # Select switch pressed
            # self.panel.play_tone(784, 0.030)  # G5 piezo?
            pass
        while not self._sel_sw.value:  # Wait for select switch release
            pass

        ### build updated structured time and sound flag values --> if changed
        # set_yr  =
        # set_mon =
        # set_dom =
        # set_hr  =
        # set_min =
        # self._sound =

        # Build structured time:             ((year, mon, date, hour,
        #                                      min, sec, wday, yday, isdst))
        #self._xst_datetime = time.struct_time((set_yr, set_mon, set_dom, set_hr,
        #                                       set_min, 0, -1, -1, -1))
        # Fix weekday and yearday structured time errors
        #self._xst_datetime = time.localtime(time.mktime(self._xst_datetime))

        if self._changed:
            self.show(self._xst_datetime, date=True)

        # return with new datetime, sound flag, and "something changed" flag
        return self._xst_datetime, self._sound, self._changed
