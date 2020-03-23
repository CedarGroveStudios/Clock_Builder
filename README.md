# Clock_Builder
 
## An in-development collection of modules and libraries for building standalone RTC clocks.

![Clock_Builder](https://github.com/CedarGroveStudios/Clock_Builder/blob/master/clock_builder.png)

The __examples__ folder contains primary methods for PyBadge, FeatherM4 w/LED display, and a REPL-only clock.

__Clock_Builder__ currently supports:

_Real-time clock modules:_
- Adafruit DS3231 RTC

_Displays:_
- CircuitPython REPL, including time setting function (tested with PyBadge, ItsyBitsyM4Express, and FeatherM4Express)
- Adafruit 4-digit 7-segment single-color LED displays (only tested on 1.2" HT16K33 backpack with FeatherM4Express)
- Adafruit 4-digit 14-segment single-color LED displays (tested with FeatherM4Express)
- PyBadge and EdgeBadge DisplayIO-based TFT display, including time setting function (tested with PyBadge)

_Time Setting:_
- Time setting for the PyGamer is through the standard on-device buttons. 
- Time setting for the FeatherM4Express is via a rotary encoder connected to pins D5, D6, D9, and GND. 
- REPL time setting via USB using Python's __input()__ statement is supported.

Future support is planned for OLED displays and GPIO-connected time setting buttons.

See the __CedarGroveStudios/Unit_Converter__ repository for a compatible automatic North American Daylight Saving Time method.
 
