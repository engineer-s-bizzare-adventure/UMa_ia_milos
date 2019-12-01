#!/usr/bin/env python3
# so that script can be run from Brickman

from ev3dev.ev3 import *
from time  import sleep

lista = []
lista_final = []

#Adicionar as peças numa lista
def adiciona_pecas(type):
    lista.append(type)

#variaveis globais
completed_reading = False


# Put the color sensor into COL-COLOR mode.

cl = ColorSensor() 
cl.mode='COL-COLOR'


def check_colour():
    colors=('unknown','black','blue','green','yellow','red','white','brown')

    while True:    
        current_color = cl.value()
        if colors[cl.value()] == 'red':
            completed_reading = True
            convert_lista()
            break

        else:
            if colors[cl.value()] != 'white' and colors[cl.value()] != 'unknown' and colors[cl.value()] != 'black' and colors[cl.value()] != 'red' :
                adiciona_pecas(colors[cl.value()])
                current_color = colors[cl.value()]
                print (current_color)
                while colors[cl.value()] == current_color:
                    pass
                print('next!')
    
            
    Sound.beep()

def convert_lista():

    for i in lista:
        if i == 'green':
            lista_final.append('X')
        if i == 'blue':
            lista_final.append('O')
        if i == 'yellow':
            lista_final.append('-')
        if i == 'brown':
            lista_final.append('+')
    
    print(' '.join(lista_final))
    sleep(10)
    
#amarelo verde verde azul amarelo verde azul castanho vermelho
#   -     X      X    O      -      X    O      +
