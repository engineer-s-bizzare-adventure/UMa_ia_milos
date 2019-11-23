#!/usr/bin/env python3
# so that script can be run from Brickman

from ev3dev.ev3 import *
from time   import sleep

# Connect EV3 color and touch sensors to any sensor ports
cl = ColorSensor() 
ts = TouchSensor()

# Put the color sensor into COL-COLOR mode.
cl.mode='COL-COLOR'

colors=('unknown','black','blue','green','yellow','red','white','brown')
while True:    # Stop program by pressing touch sensor button
    print(colors[cl.value()])
    Sound.speak(colors[cl.value()]).wait()
    sleep(3)
Sound.beep()