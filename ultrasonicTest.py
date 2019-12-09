#!/usr/bin/env python3
# so that script can be run from Brickman

from ev3dev.ev3 import *
from ev3dev2.motor import LargeMotor, MediumMotor, MoveSteering, OUTPUT_D, OUTPUT_A, OUTPUT_B, SpeedRPS
from time   import sleep
import os
import main
#os.system('setfont Lat15-TerminusBold14')
os.system('setfont Lat15-TerminusBold32x16')
# Connect ultrasonic and touch sensors to any sensor port
us = UltrasonicSensor() 
ts = TouchSensor()

# Put the US sensor into distance mode.
us.mode='US-DIST-CM'

units = us.units
# reports 'cm' even though the sensor measures 'mm'
sound = Sound()
    #declarar motor da garra
motor_garra = MediumMotor(OUTPUT_B)

apanhou = False

main.pick()

Sound.beep()       
Leds.set_color(Leds.LEFT, Leds.GREEN)  #set left led green before exiting