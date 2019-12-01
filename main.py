#!/usr/bin/env python3

from ev3dev2.sound import Sound #dicionário que permite tocar músicas
from ev3dev.ev3 import * #nao sei a diferença do de cima
from time import sleep
#from threading import Thread #dicionário que permite executar ações ao mesmo tempo
from multiprocessing import Process #multi-process
from ev3dev2.motor import LargeMotor, MediumMotor, MoveSteering, OUTPUT_D, OUTPUT_A, OUTPUT_B, SpeedRPS #dicionário dos motores disponíveis e usados no robot
from PIL import Image #dicionário que permite apresentar imagens .bmp no lcd
from ev3dev2.sensor.lego import GyroSensor
from threading import Thread #dicionário que permite executar ações ao mesmo tempo

import os
#os.system('setfont Lat15-TerminusBold14')
os.system('setfont Lat15-TerminusBold32x16')

mySound = Sound()

import colorTest

            #############################################
            #               TO DO LIST                  #
            #############################################
'''
    definir a melhor velocidade para o robot se mover
    definir a melhor velocidade para a garra abrir e fechar
    definir quantas rotações (ou segundos) são necessarias para andar 1 casa
    definir os angulos de rotação
    definir multiprocessing para andar e fazer a leitura ao mesmo tempo
'''
##########################################################################################
#motores
steer_pair = MoveSteering(OUTPUT_A, OUTPUT_D)
motor_garra = MediumMotor(OUTPUT_B)

#sensores
gyro = GyroSensor()
us = UltrasonicSensor() 

# Put the gyro sensor into ANGLE mode.
gyro.mode='GYRO-ANG'
us.mode='US-DIST-CM'

#constantes
ROTACOES_CASA = 2.2 #cada casa é +/- 2.2 rotações
DISTANCIA_PROCURA = 40 #distância maxima a que o objeto tem de estar
DISTANCIA_MIN = 10 #distância final do robot ao objeto

VELOCIDADE_PADRAO = 30
VELOCIDADE_PROCURA = 20 #velocidade durante a procura, mais lenta para maior precisão
VELOCIDADE_AJUSTE = 10 #velocidade para ajustar a posição do robot, super lento para não andar em excesso aos zig zags

#variaveis globais

#angulos por padrão
ANGULO_AJUSTAMENTO = 2 #angulo para ajustar a direção do robot (andar o mais reto possivel) -- talvez mudar para 0 --
ANGULO_60 = 59
ANGULO_90 = 89
ANGULO_180 = 179
##########################################################################################


#############################################
#           Funcoes Base Robot              #
#############################################
def reset_gyro():
    gyro.mode = 'GYRO-RATE'
    gyro.mode = 'GYRO-ANG'

def ajustar(movimento):
    if movimento == 'forward':
        gyro.angle
        while gyro.angle < ANGULO_AJUSTAMENTO:
            steer_pair.on(steering=-100, speed=VELOCIDADE_AJUSTE)
            gyro.angle
        steer_pair.wait_until_not_moving
        gyro.angle
        while gyro.angle > ANGULO_AJUSTAMENTO:
            steer_pair.on(steering=100, speed=VELOCIDADE_AJUSTE)
            gyro.angle
        steer_pair.wait_until_not_moving

        gyro.angle
    
    if movimento == 'backward':
        while gyro.angle > ANGULO_AJUSTAMENTO:
            steer_pair.on(steering=-100, speed=-VELOCIDADE_AJUSTE)
            gyro.angle
        steer_pair.wait_until_not_moving
        gyro.angle
        while gyro.angle < ANGULO_AJUSTAMENTO:
            steer_pair.on(steering=100, speed=-VELOCIDADE_AJUSTE)
            gyro.angle
        steer_pair.wait_until_not_moving

def move_forward(casas): #anda 'casas' elementos da matriz para a frente
    conta_casas = 0

    while conta_casas < casas:
        steer_pair.on_for_rotations(steering=0, speed=VELOCIDADE_PADRAO, rotations=ROTACOES_CASA)
        conta_casas+=1
        steer_pair.wait_until_not_moving
        ajustar('forward') 
    steer_pair.off()    


def move_forward_read(casas): 
    conta_casas = 0
    while conta_casas < casas:
        if colorTest.completed_reading:
            break
        else:
            steer_pair.on_for_rotations(steering=0, speed=VELOCIDADE_PADRAO, rotations=ROTACOES_CASA)
            conta_casas+=1
            steer_pair.wait_until_not_moving 
    steer_pair.off() 

def move_backward(casas): #anda 'casas' elementos da matriz para tras
    conta_casas = 0

    while conta_casas < casas:
        steer_pair.on_for_rotations(steering=0, speed=-VELOCIDADE_PADRAO, rotations=ROTACOES_CASA)
        conta_casas+=1
        steer_pair.wait_until_not_moving
        ajustar('backward')
    steer_pair.off()   


def turn_right(angulo): #vira 'angulo' para a direita
    steer_pair.wait_until_not_moving #garantir que o robot esta parado, antes que começar a rodar
    
    steer_pair.on(steering=100, speed=VELOCIDADE_PADRAO)
    gyro.wait_until_angle_changed_by(angulo)
    steer_pair.off() 
    reset_gyro()


def turn_left(angulo): #vira 'angulo' para a esquerda
    steer_pair.wait_until_not_moving
    steer_pair.on(steering=-100, speed=VELOCIDADE_PADRAO)

    #ROTAÇÃO DE APROXIMADAMENTE 90º
    gyro.wait_until_angle_changed_by(angulo)
    steer_pair.off() 
    reset_gyro()


def pick():
    #apanhar objeto com a garra
    motor_garra.on_for_seconds(speed=50, seconds=4) #fechar garra


def drop():
    #larga objeto da garra
    motor_garra.on_for_seconds(speed=-100, seconds=2) #abrir garra

#############################################
#            Funcoes avançadas              #
#############################################

'''
funcao que conta o numero de elementos para a matriz || ou usar constante = 5
funcao que conta o numero de rotacoes desde baixo até ao topo da matriz e guarda as rotacoes necessarias para cada casa || usar constante
funcao de ultrasom para encontrar inicio da lista de peças e ir até lá (contar rotações até)
  funcao para percorrer, ler e guardar lista de peças e voltar ao inicio
funcao para voltar da lista a matriz

funcao que decide onde por a peça (heuristica) - inicialmente num lugar vazio
funcao que movimenta o robot e atualiza a posicao do mesmo na matriz

funcao que verifica se há figura completa e atribui pontos

'''

def procura():
    #troca o modo do gyro para dar reset à posição
    reset_gyro()

    encontra = False
    distance = us.value()/10 #lê e guarda na variavel a distancia do centro do sensor ao objeto

    #fica a procura do objeto que indica o inicio da lista de peças:
    while encontra == False:
        gyro.angle
        steer_pair.on(steering=100, speed=VELOCIDADE_PROCURA)
        
        #procura para a direita (até 60º)
        while gyro.angle > -ANGULO_60 and encontra == False:
            distance = us.value()/10
            gyro.angle
            if distance < DISTANCIA_PROCURA: #se encontrar
                encontra = True
                sleep(0.2) #corrigir trajetoria
                steer_pair.off()
        
        steer_pair.on(steering=-100, speed=VELOCIDADE_PROCURA)
       
        #procura para a esquerda (até 60º)
        while gyro.angle < ANGULO_60 and encontra == False:
            distance = us.value()/10
            gyro.angle
            if distance < DISTANCIA_PROCURA:
                encontra = True
                sleep(0.2) #corrigir trajetoria
                steer_pair.off()

    angulo_matriz = gyro.angle #guarda o angulo da matriz à lista de objetos, para no fim voltar à posição inicial

    
    #desloca-se até 'DISTANCIA_MIN' do objeto:
    steer_pair.on(steering=0, speed=VELOCIDADE_PADRAO)
    distance_incial = us.value()/10
    while distance > DISTANCIA_MIN:
        distance = us.value()/10
        
    steer_pair.off()
    
    
    #alinha o robot antes de iniciar a leitura da lista de peças
    #ajustar() #ainda por testar (basicamente o codigo abaixo, mas numa função, porque se repete varias vezes)
    gyro.angle
    while gyro.angle < ANGULO_AJUSTAMENTO:
        steer_pair.on(steering=-100, speed=VELOCIDADE_AJUSTE)
        gyro.angle
    steer_pair.wait_until_not_moving
    gyro.angle
    while gyro.angle > ANGULO_AJUSTAMENTO:
        steer_pair.on(steering=100, speed=VELOCIDADE_AJUSTE)
        gyro.angle
    steer_pair.wait_until_not_moving

    turn_right(ANGULO_90) #roda para a direita, para alinhar à lista de peças
    reset_gyro()
    
    sleep(5) #começar a leitura de peças e guarda num array e volta ao inicio (?de marcha atras?)
    t = Thread(target=colorTest.check_colour)
    t.start()

    move_forward_read(3)
    
    #volta à matriz:
    turn_left(ANGULO_90) #roda para a esquerda, para alinhar à matriz
    reset_gyro()
    turn_left(angulo_matriz-1) #ronda para a esquerda o angulo guardado anterior, para alinhar ao objeto
    
    #anda para tras até distancia ser a distancia inicial (voltar exatamente ao ponto de inicio de procura)
    distance = us.value()/10
    while distance < distance_incial:
        steer_pair.on(steering=0, speed=-VELOCIDADE_PADRAO)
        distance = us.value()/10
    steer_pair.off()

    #alinha o robot:
    #ajustar() #ainda por testar (basicamente o codigo abaixo, mas numa função, porque se repete varias vezes)
    ajustar('forward')

    steer_pair.off()


#############################################
#              TEST FUNCTIONS               #
#############################################

procura() #iniciar a procura da lista de peças -- (esta funcão já da reset ao gyro, cuidado!)


#exemplo (nao sei)
#############################################
#         POSICAO DO ROBOT   ??             #
#############################################

#posicao[4][0]
#move_forward(4)
#posicao[0][0]
#turn(ANGULO_180)
#move_forward(4)
#posicao[4][0]

'''
posicao do robot, usar gyro (não dar reset ao gyro durante o jogo)
ou
atualizar posicao a cada uso de funcao
    podemos usar direita e esquerda com casas a andar - descer usando marcha atras
'''

