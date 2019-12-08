#!/usr/bin/env python3

from ev3dev2.sound import Sound #dicionário que permite tocar músicas
from ev3dev.ev3 import * #nao sei a diferença do de cima
from time import sleep
#from threading import Thread #dicionário que permite executar ações ao mesmo tempo
from multiprocessing import Process #multi-process
from ev3dev2.motor import LargeMotor, MediumMotor, MoveSteering, OUTPUT_D, OUTPUT_A, OUTPUT_B, SpeedRPM #dicionário dos motores disponíveis e usados no robot
from PIL import Image #dicionário que permite apresentar imagens .bmp no lcd
from ev3dev2.sensor.lego import GyroSensor, TouchSensor, UltrasonicSensor
from threading import Thread #dicionário que permite executar ações ao mesmo tempo

import os
#os.system('setfont Lat15-TerminusBold14')
os.system('setfont Lat15-TerminusBold32x16')

mySound = Sound()

import colorTest
import coord

import figuma_sim

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
ts = TouchSensor()

# Put the gyro sensor into ANGLE mode.
gyro.mode='GYRO-ANG'
us.mode='US-DIST-CM'

#constantes
ROTACOES_CASA = 2 #cada casa é +/- 2.2 rotações
DISTANCIA_PROCURA = 60 #distância maxima a que o objeto tem de estar
DISTANCIA_MIN = 10 #distância final do robot ao objeto

VELOCIDADE_PADRAO = 30
VELOCIDADE_PROCURA = 20 #velocidade durante a procura, mais lenta para maior precisão
VELOCIDADE_AJUSTE = 10 #velocidade para ajustar a posição do robot, super lento para não andar em excesso aos zig zags

#variaveis globais
in_matriz = True
direcao = 'subir'
posicao_coluna = 0
posicao_linha = 5

#angulos por padrão
ANGULO_AJUSTAMENTO = 1 #angulo para ajustar a direção do robot (andar o mais reto possivel) -- talvez mudar para 0 --
ANGULO_60 = 59
ANGULO_90 = 82
ANGULO_180 = 179
##########################################################################################


#############################################
#           Funcoes Base Robot              #
#############################################
def reset_gyro():
    gyro.mode = 'GYRO-RATE'
    gyro.mode = 'GYRO-ANG'

def ajustar():
    
    while gyro.angle != ANGULO_AJUSTAMENTO:
        if gyro.angle < ANGULO_AJUSTAMENTO:
            steer_pair.on(steering=100, speed=VELOCIDADE_AJUSTE)
        else:
            steer_pair.on(steering=-100, speed=VELOCIDADE_AJUSTE)
    
    steer_pair.off()

def move_forward(casas): #anda 'casas' elementos da matriz para a frente
    conta_casas = 0
    global posicao_coluna, posicao_linha

    while conta_casas < casas:
        steer_pair.on_for_rotations(steering=0, speed=VELOCIDADE_PADRAO, rotations=ROTACOES_CASA)
        conta_casas+=1
        steer_pair.wait_until_not_moving()
    steer_pair.off()  

    if in_matriz : #garantir que esta na matriz
        if direcao == 'esquerda':
            posicao_coluna -= casas 
        elif direcao == 'direita':
            posicao_coluna += casas
        elif direcao == 'descer':
            posicao_linha += casas
        elif direcao == 'subir':
            posicao_linha -= casas


def move_backward(casas): #anda 'casas' elementos da matriz para tras
    conta_casas = 0
    global posicao_coluna, posicao_linha
    while conta_casas < casas:
        steer_pair.on_for_rotations(steering=0, speed=-VELOCIDADE_PADRAO, rotations=ROTACOES_CASA)
        conta_casas+=1
        steer_pair.wait_until_not_moving
    steer_pair.off()

    if in_matriz : #garantir que esta na matriz
        if direcao == 'esquerda':
            posicao_coluna += casas 
        elif direcao == 'direita':
            posicao_coluna -= casas
        elif direcao == 'descer':
            posicao_linha -= casas
        elif direcao == 'subir':
            posicao_linha += casas


def turn_right(angulo): #vira 'angulo' para a direita
    steer_pair.wait_until_not_moving #garantir que o robot esta parado, antes que começar a rodar
    global direcao
    steer_pair.on(steering=100, speed=VELOCIDADE_PADRAO)
    gyro.wait_until_angle_changed_by(angulo)
    steer_pair.off() 
    
    Sound.speak("TOUCH ME!")
    while not ts.is_pressed:
        reset_gyro()

    if in_matriz : #garantir que esta na matriz
        if direcao == 'direita' and angulo == ANGULO_90: #se tiver virado para a direita e voltar a virar, fica para baixo
            direcao = 'descer'
        elif direcao == 'esquerda' and angulo == ANGULO_90: #se tiver virado para a esquerda e voltar a direita, fica para cima
            direcao = 'subir'
        elif direcao == 'descer' and angulo == ANGULO_90: #se tiver virado para baixo e voltar a direita, fica para esquerda
            direcao = 'esquerda'
        elif direcao == 'subir' and angulo == ANGULO_90:
            direcao = 'direita'


def turn_left(angulo): #vira 'angulo' para a esquerda
    steer_pair.wait_until_not_moving
    steer_pair.on(steering=-100, speed=VELOCIDADE_PADRAO)
    global direcao
    #ROTAÇÃO DE APROXIMADAMENTE 90º
    gyro.wait_until_angle_changed_by(angulo)
    steer_pair.off() 
    
    Sound.speak("TOUCH ME!")
    while not ts.is_pressed:
        reset_gyro()

    if in_matriz : #garantir que esta na matriz
        if direcao == 'esquerda' and angulo == ANGULO_90: #se tiver virado para a esquerda e voltar a virar, fica para baixo
            direcao = 'descer'
        elif direcao == 'direita' and angulo == ANGULO_90: #se tiver virado para a direita e voltar a esquerda, fica para cima
            direcao = 'subir'
        elif direcao == 'descer' and angulo == ANGULO_90: #se tiver virado para baixo e voltar a esquerda, fica para direita
            direcao = 'direita'
        elif direcao == 'subir' and angulo == ANGULO_90:
            direcao = 'esquerda'


def pick():
    #apanhar objeto com a garra
    motor_garra.on_for_seconds(speed=50, seconds=3) #fechar garra


def drop():
    #larga objeto da garra
    motor_garra.on_for_seconds(speed=-50, seconds=3) #abrir garra

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
    '''while encontra == False:
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

    angulo_matriz = gyro.angle #guarda o angulo da matriz à lista de objetos, para no fim voltar à posição inicial'''

    #desloca-se até 'DISTANCIA_MIN' do objeto:
    steer_pair.on(steering=0, speed=VELOCIDADE_PADRAO)
    distance_incial = us.value()/10
    while distance > DISTANCIA_MIN:
        distance = us.value()/10
        
    steer_pair.off()
    
    #alinha o robot antes de iniciar a leitura da lista de peças
    '''ajustar() '''

    turn_right(ANGULO_90) #roda para a direita, para alinhar à lista de peças

    colorTest.check_colour() #começar a leitura de peças e guarda num array e volta ao inicio (?de marcha atras?)
    
    #volta à matriz:
    turn_left(ANGULO_90) #roda para a esquerda, para alinhar à matriz
    
    #turn_left(angulo_matriz-1) #ronda para a esquerda o angulo guardado anterior, para alinhar ao objeto
    
    #anda para tras até distancia ser a distancia inicial (voltar exatamente ao ponto de inicio de procura)
    distance = us.value()/10
    while distance < distance_incial:
        steer_pair.on(steering=0, speed=-VELOCIDADE_PADRAO)
        distance = us.value()/10
    steer_pair.off()

    #alinha o robot
    #ajustar()
    #turn_right(angulo_matriz)

    steer_pair.off()

def music():
    Sound.play("sounds/titanic.wav").wait()

def sobe_busca_peca():
    #vai linha 0
    if direcao == 'descer':
        turn_right(ANGULO_90)
        turn_right(ANGULO_90)
    elif direcao == 'direita':
        turn_left(ANGULO_90)
    elif direcao == 'esquerda':
        turn_right(ANGULO_90)    
    move_forward(posicao_linha-1)

    #vai coluna 0
    if(posicao_coluna > 1):
        turn_left(ANGULO_90)
        move_forward(posicao_coluna-1)
        turn_right(ANGULO_90)

def busca_peca():
    #troca o modo do gyro para dar reset à posição
    reset_gyro()

    encontra = False
    distance = us.value()/10 #lê e guarda na variavel a distancia do centro do sensor ao objeto

    #fica a procura do objeto que indica o inicio da lista de peças:
    '''while encontra == False:
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
                steer_pair.off()'''

    #angulo_matriz = gyro.angle #guarda o angulo da matriz à lista de objetos, para no fim voltar à posição inicial'''

    #desloca-se até 'DISTANCIA_MIN' do objeto:
    steer_pair.on(steering=0, speed=VELOCIDADE_PADRAO)
    distance_incial = us.value()/10
    while distance > DISTANCIA_MIN:
        distance = us.value()/10
        
    steer_pair.off()
    
    #alinha o robot antes de iniciar a leitura da lista de peças
    '''ajustar() '''
    turn_right(ANGULO_90)
    colorTest.peca()
    #espera pelo toque, quando toca apanha peca e continua
    Sound.speak("TOUCH ME!")
    while not ts.is_pressed:
        pass

    pick()

    colorTest.move_to_start()
    
    #volta à matriz:
    turn_left(ANGULO_90) #roda para a esquerda, para alinhar à matriz
    
    #turn_left(angulo_matriz-1) #ronda para a esquerda o angulo guardado anterior, para alinhar ao objeto
    
    #anda para tras até distancia ser a distancia inicial (voltar exatamente ao ponto de inicio de procura)
    distance = us.value()/10
    steer_pair.on(steering=0, speed=-VELOCIDADE_PADRAO)
    #print(distance_incial + " - " + distance)
    while distance < distance_incial:
        distance = us.value()/10
    steer_pair.off()

    #alinha o robot
    #ajustar()
    #turn_right(angulo_matriz)

    steer_pair.off()

def coloca_peca(jogada):
    #ir para linha certa
    if(jogada[0]>posicao_linha):
        turn_right(ANGULO_90)
        turn_right(ANGULO_90)
        move_forward(jogada[0] - posicao_linha)
    '''if(jogada[0]>posicao_linha):
        if direcao == 'subir':
            turn_right(ANGULO_90)
            turn_right(ANGULO_90)
        elif direcao == 'direita':
            turn_right(ANGULO_90)
        elif direcao == 'esquerda':
            turn_left(ANGULO_90)
        move_forward(jogada[0] - posicao_linha)
    elif(jogada[0]<posicao_linha):
        if direcao == 'descer':
            turn_right(ANGULO_90)
            turn_right(ANGULO_90)
        elif direcao == 'direita':
            turn_esquerda(ANGULO_90)
        elif direcao == 'esquerda':
            turn_right(ANGULO_90)
        move_forward(posicao_linha - jogada[0])'''

    #ir para coluna certa
    if(jogada[1]>posicao_coluna):
        turn_left(ANGULO_90)
        move_forward(jogada[1] - posicao_coluna)
    elif(jogada[1]<posicao_coluna):
        turn_left(ANGULO_90)
        move_forward(posicao_coluna - jogada[1])

    '''if(jogada[1]>posicao_coluna):
        if direcao == 'subir':
            turn_right(ANGULO_90)
        elif direcao == 'esquerda':
            turn_right(ANGULO_90)
            turn_right(ANGULO_90)
        elif direcao == 'descer':
            turn_left(ANGULO_90)
        move_forward(jogada[0] - posicao_coluna)
    elif(jogada[1]<posicao_coluna):
        if direcao == 'subir':
            turn_left(ANGULO_90)
        elif direcao == 'direita':
            turn_left(ANGULO_90)
            turn_left(ANGULO_90)
        elif direcao == 'descer':
            turn_right(ANGULO_90)
        move_forward(posicao_coluna - jogada[1])'''

    sleep(2)
    drop()
    sleep(2)

#############################################
#              TEST FUNCTIONS               #
#############################################

#coord.move()
#sleep(50)
#procura() #iniciar a procura da lista de peças -- (esta funcão já da reset ao gyro, cuidado!)
'''
s = Thread(target=music)
s.start()
'''
#music()

#exemplo (nao sei)
#############################################
#         POSICAO DO ROBOT   ??             #
#############################################
'''
reset_gyro()

while True:
    move_forward(4)
    turn_right(ANGULO_90)
'''



##############################################################
reset_gyro()
in_matriz = True
direcao = 'subir'

#posicao inicial
posicao_linha = 5
posicao_coluna = 1

move_forward(4) #só sobe

in_matriz = False #sai da matriz para procurar e fazer leitura das peças
procura() #procura, le peças, guarda e volta ao sitio [0,0]

in_matriz = True #voltou à matriz




# inicializa tabuleiro
tabuleiro = figuma_sim.inicializa_tabuleiro(figuma_sim.DIMENSAO_TABULEIRO)

# inicializa pecas
lista_pecas = colorTest.lista_final

# mostra tabuleiro
figuma_sim.mostra_tabuleiro(tabuleiro)
    
# mostra lista de pecas
figuma_sim.mostra_lista(lista_pecas)

global p 
p = 0

while p+1 <= len(lista_pecas):
    peca = lista_pecas[p]
        
    print('PECA: ' + peca)

    # pede jogada

    #BUSCAR PEÇA ?????
    print("SOBE")
    sobe_busca_peca()
    in_matriz = False #sai da matriz para buscar peça
    print("busca")
    busca_peca() #procura, vai ate peça, apanha e volta ao sitio
    print("agraa")
    in_matriz = True #voltou à matriz

    #jogada = pede_jogada(tabuleiro)
    jogada = figuma_sim.heuristica_aleatoria(tabuleiro)

    ########################################
    #       MOVE ROBOT ATÉ A JOGADA        #
    ########################################
    coloca_peca(jogada)
        
    # actualiza tabuleiro
    tabuleiro = figuma_sim.actualiza_tabuleiro(tabuleiro,jogada,peca)

    # mostra tabuleiro
    figuma_sim.mostra_tabuleiro(tabuleiro)
        
    # Vencedor --> termina

    # proxima peca
    p=p+1

sobe_busca_peca()
print("THE END")
sleep(20)