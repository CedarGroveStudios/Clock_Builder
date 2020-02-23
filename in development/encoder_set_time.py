# encoder_set_time 2020-02-20 v00.py
# clock_builder.x_clock_set module

import board
import time
import rotaryio
from digitalio import DigitalInOut, Direction, Pull
import rotaryio as enc

### DEFINE AND INITIALIZE PINS AND DEVICES ###
# digital inputs and outputs for encoder

sel_sw = DigitalInOut(board.D9)
sel_sw.direction = Direction.INPUT
sel_sw.pull = Pull.UP

enc = rotaryio.IncrementalEncoder(board.D5, board.D6)

### LISTS AND DICTIONARIES ###

### HELPERS ###

### MAIN CODE SECTION ###

### Main Loop ###

last_position = None
while True:
    position = enc.position
    if last_position == None or position != last_position:
        print(position, not sel_sw.value)
    last_position = position
    time.sleep(.1)
