#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep
from threading import Thread
import os
os.system('setfont Lat15-TerminusBold14')
#print('Hello, my name is Ricardo Milos!')
#Sound.play('sounds/ugotthat.wav').wait()
running=True

def noscope():
    ultrasound()

    while(running==False):
        ma = LargeMotor('outA')
        ma.run_timed(time_sp=5000, speed_sp=1000)
        print("set speed (speed_sp) = " + str(ma.speed_sp))
        sleep(5)  # it takes a moment for the motor to start moving
        print("actual speed = " + str(ma.speed))
        
        md = LargeMotor('outD')
        md.run_timed(time_sp=5000, speed_sp=-1000)
        print("set speed (speed_sp) = " + str(md.speed_sp))
        sleep(1)  # it takes a moment for the motor to start moving
        print("actual speed = " + str(md.speed))

def claw(grab):
    if grab == True:
        sp_speed=750
    else:
        sp_speed=-750

    m = MediumMotor('outB')
    m.run_timed(time_sp=1000, speed_sp=sp_speed)
    print("set speed (speed_sp) = " + str(m.speed_sp))
    sleep(1)  # it takes a moment for the motor to start moving
    print("actual speed = " + str(m.speed))

def ultrasound():
    us = UltrasonicSensor() 
    units = us.units
    distance = us.value()/10  # convert mm to cm
    print(str(distance) + " " + units)

    if distance <= 12.8 or distance == 255:  #This is an inconveniently large distance
        #Sound.speak("bring me that ass!")
        Leds.set_color(Leds.LEFT, Leds.GREEN)
        claw(True)
    elif distance >= 15.6:
        reset()
    else:
        Leds.set_color(Leds.LEFT, Leds.RED)


def reset():
    #Sound.speak("My name is Ricardo Milos")
    for i in range (2):
        claw(False)

reset()
while(1):
    ultrasound()
    


"""t = Thread(target=noscope)
t.start()
for i in range(0,5):       # Do five times.
    #claw(True)
    if i == 3:
        running=False
        continue"""
Sound.beep()


