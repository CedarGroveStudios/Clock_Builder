# encoder_set_time 2020-02-20 v00.py
# clock_builder.x_clock_set module

import board
import time
import pulseio
from digitalio import DigitalInOut, Direction, Pull
import microcontroller as mcu  # for checking CPU temperature
import gc  # for checking memory capacity
import rotaryio as enc

### DEFINE AND INITIALIZE PINS AND DEVICES ###
# digital inputs and outputs for encoder

sel_sw = DigitalInOut(board.D12)
sel_sw.direction = Direction.INPUT
sel_sw.pull = Pull.UP

enc = rotaryio.IncrementalEncoder(board.D10, board.D11)


### LISTS AND DICTIONARIES ###

### HELPERS ###

### MAIN CODE SECTION ###
# display system status
gc.collect()  # clean up memory
print("encoder_set_time.py 2020-02-20_v00")
print("GC.mem_free:    %0.3f" % float(gc.mem_free()/1000), "KB")
print("CPU.freqency:    %0.1f" % float(mcu.cpu.frequency/1000000), "MHz")
print("CPU.temperature: %0.1f" % mcu.cpu.temperature, "C")



### Main Loop ###
last_position = None
while True:
    position = enc.position
    if last_position == None or position != last_position:
        print(position, sel_sw.value)
    if last_position > position:
        up   = True
        down = False
    if last_position < position:
        up   = False
        down = True
    if last_position == position:
        up   = False
        down = True
    print("UP:", up, "DOWN:", down)
    last_position = position
