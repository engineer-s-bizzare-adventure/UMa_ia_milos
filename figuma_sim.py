import random

import colorTest

DIMENSAO_TABULEIRO = 5
NUMERO_PECAS = 25
#######################################
#       CRIAÇÃO DO TABULEIRO          #
#######################################
def inicializa_tabuleiro(n):
    return [['#'] * n for i in range(n)]

#######################################
#       MOSTRA O TABULEIRO            #
#######################################
def mostra_tabuleiro(tabuleiro):
    for linha in tabuleiro:
        for valor in linha:
            print('|',valor,end=' ')
        print(end='|')
        print()

def define_pecas():
    return [random.choice('x+-o') for _ in range(25)] 
    #return [random.choice('+') for _ in range(NUMERO_PECAS)] 
    

def mostra_lista(lista_pecas):
    print(lista_pecas)

def heuristica_aleatoria(tabuleiro):
    linha = random.randint(1, DIMENSAO_TABULEIRO) #random entre 1 e 5
    coluna = random.randint(1, DIMENSAO_TABULEIRO) #random entre 1 e 5

    s_posicao = str(linha) + "," + str(coluna)
    #print (s_posicao)
    jogada = eval(s_posicao)

    while not possivel(tabuleiro,jogada):
        linha = random.randint(1, DIMENSAO_TABULEIRO) #random entre 1 e 5
        coluna = random.randint(1, DIMENSAO_TABULEIRO) #random entre 1 e 5

        s_posicao = str(linha) + "," + str(coluna)
        #print (s_posicao)
        jogada = eval(s_posicao)

    print (s_posicao)
    return jogada

def pede_jogada(tabuleiro):
    jogada = eval(input('A sua jogada (linha,coluna)?: '))
    while not possivel(tabuleiro,jogada):
        print('Jogada invalida...')
        jogada = eval(input('A sua jogada (linha,coluna)?: '))
    return jogada

def possivel(tabuleiro,jogada):
    if(jogada[0] < 1 or jogada[1] < 1):
        return False
    if(jogada[0] > DIMENSAO_TABULEIRO or jogada[1] > DIMENSAO_TABULEIRO):
        return False
    return tabuleiro[jogada[0]-1][jogada[1]-1] == '#'

def actualiza_tabuleiro(tabuleiro, jogada, peca):
    tabuleiro[jogada[0]-1][jogada[1]-1] = peca
    return tabuleiro


def vence_menos(tabuleiro, peca):
    for i in range(len(tabuleiro)):
        conta = 0
        for j in range(len(tabuleiro[0])):
            if tabuleiro[i][j] == peca:
                conta += 1
            else:
                conta = 0 #nao era seguido
        if conta >= 2:
            print("FIGURA '-' COMPLETA, NA LINHA: " + str(i+1))
            return True
            #break
    return False


def figura_plus(tabuleiro, peca):
    #ignora a coluna das pontas
    limite_fim = len(tabuleiro)-1 #ignora ultima coluna
    limite = len(tabuleiro)-2 #ignora ultimas 2 linhas
    result = 0
    for linha in range(limite):
        coluna = 1 #ignora primeira coluna
        for coluna in range(limite_fim):
            if tabuleiro[linha][coluna] == peca:
                if coluna_fig_plus(tabuleiro, linha, coluna, peca):
                    result+=1
                    #print("FANTASTICO, [", str(linha), "][", str(coluna), "]", end="||||")
                    #print("PONTOS GANHOS: ", 2**remove_fig_x(tabuleiro, linha, coluna))
                    #return True
    print(result, " COMBINACOES POSSIVEIS!!")



def coluna_fig_plus(tabuleiro, linha, coluna, peca):
    col_lin = 0
    tamanho_min_fig = 3
    tamanho_fig = len(tabuleiro)
    if tamanho_fig % 2 == 0: #PARA O +, A DIAGONAL TEM DE SER IMPAR
        tamanho_fig -= 1

    while (linha + tamanho_fig > len(tabuleiro) or coluna + tamanho_fig > len(tabuleiro) ):
        tamanho_fig -= 2

    linhas_init = tamanho_fig//2 #parte inteira da divisao

    while tamanho_fig >= tamanho_min_fig and col_lin != tamanho_fig:
        for i in range(tamanho_fig):
            if tabuleiro[linha+i][coluna] == peca and tabuleiro[linha+linhas_init][coluna+i-1] == peca:
                col_lin+=1
        if(col_lin == tamanho_fig):
            return True
        tamanho_fig -= 2
        linhas_init = tamanho_fig//2 #parte inteira da divisao
        col_lin = 0

    return col_lin == tamanho_fig



def figura_x(tabuleiro, peca):
    limite = len(tabuleiro)-2 #-2 pois são precisos pelo menos 3 'x' para formar a figura (ignora ultimas 2 colunas)
    result = 0
    #ENCONTRAR PRIMEIRO X DE LINHA EM LINHA
    for linha in range(limite): 
        for coluna in range(limite): #procura por todas as colunas de cada linha
            if tabuleiro[linha][coluna] == peca:
                if diagonal_fig_x(tabuleiro, linha, coluna, peca):
                    result+=1
                    #print("FANTASTICO, [", str(linha), "][", str(coluna), "]", end="||||")
                    #print("PONTOS GANHOS: ", 2**remove_fig_x(tabuleiro, linha, coluna))
                    #return True
    print(result, " COMBINACOES POSSIVEIS!!")

def remove_fig_x(tabuleiro, linha, coluna, peca):
    diagonais = 0
    tamanho_fig = len(tabuleiro)

    if int(tamanho_fig) % 2 == 0: #PARA O X, A DIAGONAL TEM DE SER IMPAR
        tamanho_fig -= 1

    if(linha + tamanho_fig > len(tabuleiro) or coluna + tamanho_fig > len(tabuleiro) ):
        tamanho_fig -= 2

    for i in range(tamanho_fig):
        if tabuleiro[linha+i][coluna+i] == peca and tabuleiro[linha+i][coluna + tamanho_fig-1-i] == peca:
            tabuleiro[linha+i][coluna+i] = '#' 
            tabuleiro[linha+i][coluna + tamanho_fig-1-i] = '#'
            diagonais+=1

    return 2*tamanho_fig-1 

def diagonal_fig_x(tabuleiro, linha, coluna, peca):
    diagonais = 0
    tamanho_min_fig = 3
    tamanho_fig = len(tabuleiro)
    if tamanho_fig % 2 == 0: #PARA O X, A DIAGONAL TEM DE SER IMPAR
        tamanho_fig -= 1

    while (linha + tamanho_fig > len(tabuleiro) or coluna + tamanho_fig > len(tabuleiro) ):
        tamanho_fig -= 2

    while tamanho_fig >= tamanho_min_fig and diagonais != tamanho_fig:
        for i in range(tamanho_fig):
            if tabuleiro[linha+i][coluna+i] == peca and tabuleiro[linha+i][coluna + tamanho_fig-1-i] == peca:
                diagonais+=1
        if(diagonais == tamanho_fig):
            return True
        tamanho_fig -= 2
        diagonais = 0

    return diagonais == tamanho_fig

def encontra_circulo(tabuleiro, peca):
    #NAO FUNCIONA PARA:  FUNCIONA PARA:
    # O O O                 O O O
    #   O O                 O   O
    #                       O O O

    for j in range(len(tabuleiro[0])): #de 0 até tamanho-1 (5-1=4)
        for i in range(len(tabuleiro)): #de 0 até tamanho-1 (5-1=4)
            conta_linha = 0
            while j < len(tabuleiro[0]) - conta_linha and conta_linha < len(tabuleiro[0]) and tabuleiro[i][j + conta_linha] == peca:
                conta_linha += 1
            
            
            while conta_linha > 2:
                k=0
                for k in range(conta_linha):
                    if tabuleiro[i+k][j+conta_linha-1] != peca: #verifica coluna direita
                        break
                    
                    if tabuleiro[i+conta_linha-1][j+k] != peca: #verifica linha baixo
                        break
                    
                    if tabuleiro[i+k][j] != peca: #verifica coluna esquerda
                        break
                    
                    print("FIGURA 'o' COMPLETADA, NA LINHA: " + str(i+1) + " E COLUNA: " + str(j+1))
                    return True

                conta_linha -= 1
                
    return False