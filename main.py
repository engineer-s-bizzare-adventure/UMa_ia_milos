#!/usr/bin/env python3
#from ev3dev2.sound import Sound #dicionário que permite tocar músicas

from ev3dev.ev3 import * #nao sei a diferença do de cima
from time import sleep
from threading import Thread #dicionário que permite executar ações ao mesmo tempo
    #dicionário dos motores disponíveis e usados no robot
from ev3dev2.motor import LargeMotor, MediumMotor, MoveSteering, OUTPUT_D, OUTPUT_A, OUTPUT_B, SpeedRPS
from PIL import Image #dicionário que permite apresentar imagens .bmp no lcd
from ev3dev2.sensor.lego import GyroSensor

from threading import Thread #dicionário que permite executar ações ao mesmo tempo


import colorTest


            #############################################
            #               TO DO LIST                  #
            #############################################
'''
    definir a melhor velocidade para o robot se mover
    definir a melhor velocidade para a garra abrir e fechar
    definir quantas rotações (ou segundos) são necessarias para andar 1 casa
    definir os angulos de rotação
'''
##########################################################################################

#motores
steer_pair = MoveSteering(OUTPUT_A, OUTPUT_D)
motor_garra = MediumMotor(OUTPUT_B)

#sensores
gyro = GyroSensor()


# Put the gyro sensor into ANGLE mode.
gyro.mode='GYRO-ANG'

#constantes
ROTACOES_CASA = 2.2
VELOCIDADE_PADRAO = 20
#angulos por padrão, sempre à direita
ANGULO_90 = 87

move = False
##########################################################################################
#############################################
#           Funcoes Base Robot              #
#############################################

def move_forward(casas):
    # anda 'casas' elementos da matriz em frente
    '''
    GYRO PARA ANDAR LINHA RETA ....
    '''
    move = True
    steer_pair.on_for_rotations(steering=0, speed=VELOCIDADE_PADRAO, rotations=casas)
    move = False

def move_backward(casas):
    # anda 'casas' elementos da matriz para tras
    steer_pair.on_for_rotations(steering=0, speed=-VELOCIDADE_PADRAO, rotations=casas)

def turn(angulo):
    steer_pair.on(steering=100, speed=VELOCIDADE_PADRAO)

    #ROTAÇÃO DE APROXIMADAMENTE 90º
    gyro.wait_until_angle_changed_by(angulo)
    steer_pair.off() 
    
def pick():
    #apanhar objeto com a garra
    motor_garra.on_for_seconds(speed=50, seconds=4) #fechar garra

def drop():
    #larga objeto da garra
    motor_garra.on_for_seconds(speed=-100, seconds=2) #abrir garra
    
def delta():
    pos_inicial = gy.angle
    print("POS INICIAL: " + str(pos_inicial) + " " + units)
    
    while move:
        while ((pos_inicial-gy.angle > 7)):
            motores.on_for_rotations(steering=-100, speed=40, rotations=0.1)
            print("DIR: " + str(gy.angle) + " " + units)
        while (pos_inicial-gy.angle < -7 ):
            motores.on_for_rotations(steering=-100, speed=40, rotations=0.1)
            print("ESQ: " + str(gy.angle) + " " + units)

        print("POS FINAL: " + str(gy.angle) + " " + units)

def ler_lista():
    colorTest.check_colour()
    print(colorTest.lista)
#############################################
#            Funcoes avançadas              #
#############################################

'''
funcao que conta o numero de elementos para a matriz || ou usar constante = 5
funcao que conta o numero de rotacoes desde baixo até ao topo da matriz e guarda as rotacoes necessarias para cada casa || usar constante
funcao de ultrasom para encontrar inicio da lista de peças e ir até lá (contar rotações até)
  funcao para percorrer, ler e guardar lista de peças e voltar ao inicio
funcao para voltar da lista a matriz
​
funcao que decide onde por a peça (heuristica) - inicialmente num lugar vazio
funcao que movimenta o robot e atualiza a posicao do mesmo na matriz
​
funcao que verifica se há figura completa e atribui pontos
​
'''

#############################################
#              TEST FUNCTIONS               #
#############################################

t = Thread(target=delta)
t.start()

s = Thread(target=ler_lista)
s.start()

