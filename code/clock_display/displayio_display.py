# displayio_display.py
# 2020-02-05 Cedar Grove Studios

import time
import board
import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font

class DisplayioDisplay:

    def __init__(self, timezone="Pacific", hour_24_12=False, auto_dst=True,
                 alarm=False, brightness=1.0, debug=False):
        #input parameters
        self._timezone   = timezone
        self._hour_24_12 = hour_24_12
        self._dst        = False
        self._auto_dst   = auto_dst
        self._alarm      = alarm
        self._brightness = brightness

        self._weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self._month   = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                         "Sep", "Oct", "Nov", "Dec"]

        # Load the text font from the fonts folder
        self._font_0 = bitmap_font.load_font("/fonts/OpenSans-9.bdf")
        self._font_1 = bitmap_font.load_font("/fonts/Helvetica-Bold-36.bdf")

        # The board's integral display size
        WIDTH  = board.DISPLAY.width   # 160 for PyGamer and PyBadge
        HEIGHT = board.DISPLAY.height  # 128 for PyGamer and PyBadge

        ELEMENT_SIZE = WIDTH // 4  # Size of element_grid blocks in pixels

        board.DISPLAY.brightness = self._brightness

        # Default colors
        BLACK   = 0x000000
        RED     = 0xFF0000
        ORANGE  = 0xFF8811
        YELLOW  = 0xFFFF00
        GREEN   = 0x00FF00
        CYAN    = 0x00FFFF
        BLUE    = 0x0000FF
        VIOLET  = 0x9900FF
        DK_VIO  = 0x110022
        WHITE   = 0xFFFFFF
        GRAY    = 0x444455

        ### Define the display group ###
        self._image_group = displayio.Group(max_size=12)

        # Create a background color fill layer; image_group[0]
        self._color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
        self._color_palette = displayio.Palette(1)
        self._color_palette[0] = DK_VIO
        self._background = displayio.TileGrid(self._color_bitmap,
                                              pixel_shader=self._color_palette,
                                              x=0, y=0)
        self._image_group.append(self._background)

        # Define labels and values using element grid coordinates
        self._clock_digits = Label(self._font_1, text="06:23",
                                   color=WHITE, max_glyphs=5)
        self._clock_digits.x = 30
        self._clock_digits.y = HEIGHT // 2
        self._image_group.append(self._clock_digits)  # image_group[xx]

        self._clock_daydate = Label(self._font_0, text="Wed 02/05/2020",
                                    color=YELLOW, max_glyphs=16)
        self._clock_daydate.x = 27
        self._clock_daydate.y = 25
        self._image_group.append(self._clock_daydate)  # image_group[xx]

        self._clock_ampm = Label(self._font_0, text="PM",
                                 color=WHITE, max_glyphs=2)
        self._clock_ampm.x = 130
        self._clock_ampm.y = (HEIGHT // 2) - 8
        self._image_group.append(self._clock_ampm)  # image_group[xx]

        self._clock_dst = Label(self._font_0, text="PST",
                                color=VIOLET, max_glyphs=3)
        self._clock_dst.x = 130
        self._clock_dst.y = (HEIGHT // 2) + 8
        self._image_group.append(self._clock_dst)  # image_group[xx]

        self._clock_auto_dst = Label(self._font_0, text="AutoDST",
                                     color=VIOLET, max_glyphs=7)
        self._clock_auto_dst.x = 105
        self._clock_auto_dst.y = HEIGHT - 8
        self._image_group.append(self._clock_auto_dst)  # image_group[xx]

        self._clock_alarm = Label(self._font_0, text="ALARM",
                                  color=ORANGE, max_glyphs=5)
        self._clock_alarm.x = 5
        self._clock_alarm.y = HEIGHT - 8
        self._image_group.append(self._clock_alarm)  # image_group[xx]

        self._clock_name = Label(self._font_0, text="Clock_Builder",
                                 color=BLUE, max_glyphs=14)
        self._clock_name.x = 40
        self._clock_name.y = HEIGHT - 24
        self._image_group.append(self._clock_name)  # image_group[xx]

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
        self._dst = alarm

    @property
    def brightness(self):
        """Display brightness (0 - 1.0). Default full brightness (1.0)."""
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        self._brightness = brightness
        board.DISPLAY.brightness = self._brightness

    @property
    def show(self):
        """Display time via REPL."""
        return

    @show.setter
    def show(self, datetime):
        """Display time via REPL."""
        self._datetime = datetime

        if self._auto_dst and self._dst:  # changes the text to show DST
            self._clock_dst.text = self._timezone[0] + "DT"
        else:  # or Standard Time
            self._clock_dst.text = self._timezone[0] + "ST"

        if self._auto_dst:
            self._clock_auto_dst.text = "AutoDST"
        else:
            self._clock_auto_dst.text = "       "

        self._hour = self._datetime.tm_hour  # Format for 24-hour or 12-hour output
        if self._hour_24_12:  # 24-hour
            self._clock_ampm.text = "  "
        else:  # 12-hour clock with AM/PM
            self._clock_ampm.text = "AM"
            if self._hour >= 12:
                self._hour = self._hour - 12
                self._clock_ampm.text = "PM"
            if self._hour == 0:  # midnight hour fix
                self._hour = 12

        if self._alarm:
            self._clock_alarm.text = "ALARM"
        else:
            self._clock_alarm.text = "     "

        self._clock_name.text = ""  # add this feature later
        self._clock_daydate.text = "{} {} {:02d}, {:04d}".format(self._weekday[self._datetime.tm_wday],
                                                                 self._month[self._datetime.tm_mon - 1],
                                                                 self._datetime.tm_mday,
                                                                 self._datetime.tm_year)
        self._clock_digits.text = "{:02}:{:02}".format(self._hour, self._datetime.tm_min)

        # Activate display
        board.DISPLAY.show(self._image_group)
        time.sleep(0.1)  # Allow display to load

        return
