#!/usr/bin/env python3
# so that script can be run from Brickman

from ev3dev.ev3 import *
from ev3dev2.motor import LargeMotor, MediumMotor, MoveSteering, OUTPUT_D, OUTPUT_A, OUTPUT_B, SpeedRPS
from time   import sleep
import os
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

while True:    # Stop program by pressing touch sensor button
    # US sensor will measure distance to the closest
    # object in front of it.
    distance = us.value()/10  # convert mm to cm
    print(str(distance) + " " + units)
    if distance < 12 and distance > 10:  #This is an inconveniently large distance
        Leds.set_color(Leds.LEFT, Leds.RED)
            #fechar garra
        #motor_garra.on_for_seconds(speed=50, seconds=4)
    elif distance < 9:
        Leds.set_color(Leds.LEFT, Leds.GREEN)
        sound.speak('DROP THIS SHIT! DROP THIS SHIT!').wait()
            #abrir garra
        #motor_garra.on_for_seconds(speed=-100, seconds=2)

Sound.beep()       
Leds.set_color(Leds.LEFT, Leds.GREEN)  #set left led green before exiting