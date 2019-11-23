#!/usr/bin/env python3
# so that script can be run from Brickman

from ev3dev.ev3 import *
from time   import sleep

# Connect EV3 color and touch sensors to any sensor ports
cl = ColorSensor() 
ts = TouchSensor()

lista = []

#Adicionar as peças numa lista
def adiciona_pecas(type):
    lista.append(type)


# Put the color sensor into COL-COLOR mode.

cl.mode='COL-COLOR'
def check_colour():
    colors=('unknown','black','blue','green','yellow','red','white','brown')
    while True:    # Stop program by pressing touch sensor button
        if colors[cl.value()] == 'red':
            return lista

        else:
            if colors[cl.value()] != 'white':
                adiciona_pecas(colors[cl.value()])

    Sound.beep()
    

