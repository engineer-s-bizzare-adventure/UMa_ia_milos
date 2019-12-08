#!/usr/bin/env python3
# so that script can be run from Brickman

from ev3dev.ev3 import *
from time  import sleep
from ev3dev2.motor import LargeMotor, MediumMotor, MoveSteering, OUTPUT_D, OUTPUT_A, OUTPUT_B, SpeedRPS
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sound import Sound #dicionário que permite tocar músicas
steer_pair = MoveSteering(OUTPUT_A, OUTPUT_D)
lista = []
lista_final = []

#Adicionar as peças numa lista
def adiciona_pecas(type):
    lista.append(type)

#variaveis:
VELOCIDADE_PADRAO = 20
ROTACOES_CASA = 2.2
# Put the color sensor into COL-COLOR mode.

cl = ColorSensor() 
cl.mode='COL-COLOR'
colors=('unknown','black','blue','green','yellow','red','white','brown')


def peca():
    steer_pair.on(steering=0, speed=VELOCIDADE_PADRAO) 

    while True:
        print(colors[cl.value()] )
        if colors[cl.value()] == 'green' or colors[cl.value()] == 'blue' or colors[cl.value()] == 'yellow' or colors[cl.value()] == 'brown':
            break

    steer_pair.off()

def check_colour():
    num_rot = 0
    current_color = 'null'
    steer_pair.on(steering=0, speed=VELOCIDADE_PADRAO) 
    while True:
        if colors[cl.value()] == 'red':
            steer_pair.off()
            convert_lista()
            move_to_start()
            break

        else:
            if colors[cl.value()] != 'white' and colors[cl.value()] != 'black' and colors[cl.value()] != 'unknown' and colors[cl.value()] !='red' :
                num_rot += 1
                adiciona_pecas(colors[cl.value()])
                current_color = colors[cl.value()]
                print (current_color)
                #Sound.beep()
                while colors[cl.value()] == current_color:
                    pass
                print('next!')

def move_to_start():
    steer_pair.on(steering=0, speed=-VELOCIDADE_PADRAO)

    '''while num_rot>0:
        if colors[cl.value()] != 'white' and colors[cl.value()] != 'unknown' and colors[cl.value()] != 'black' and colors[cl.value()] != 'red' :
            num_rot -= 1
            current_color = colors[cl.value()]
            print (current_color)
            while colors[cl.value()] == current_color:
                pass
            print('next!')'''
    while colors[cl.value()] != 'red':
        pass        


    steer_pair.off()

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
