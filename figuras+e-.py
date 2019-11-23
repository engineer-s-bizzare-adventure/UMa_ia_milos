import random

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
    #return [random.choice('x+-o') for _ in range(25)] 
    return [random.choice('x') for _ in range(NUMERO_PECAS)] 

def mostra_lista(lista_pecas):
    print(lista_pecas)

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

def figura_x(tabuleiro, peca):
    limite = len(tabuleiro)-2 #-2 pois são precisos pelo menos 3 'x' para formar a figura
    result = 0
    #ENCONTRAR PRIMEIRO X DE LINHA EM LINHA
    for linha in range(limite): 
        for coluna in range(limite): #procura por todas as colunas de cada linha
            if tabuleiro[linha][coluna] == peca:
                if diagonal_fig_x(tabuleiro, linha, coluna):
                    result+=1
                    #print("FANTASTICO, [", str(linha), "][", str(coluna), "]", end="||||")
                    #print("PONTOS GANHOS: ", 2**remove_fig_x(tabuleiro, linha, coluna))
                    #return True
    print(result, " COMBINACOES POSSIVEIS!!")

def remove_fig_x(tabuleiro, linha, coluna):
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
def diagonal_fig_x(tabuleiro, linha, coluna):
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

def teste(tabuleiro):
    tabuleiro[0][0] = '#'
    mostra_tabuleiro(tabuleiro)

# inicializa tabuleiro
tabuleiro = inicializa_tabuleiro(DIMENSAO_TABULEIRO)
# inicializa pecas
lista_pecas = define_pecas()

# mostra tabuleiro
mostra_tabuleiro(tabuleiro)
# mostra lista de pecas aleatoria
mostra_lista(lista_pecas)

#teste(tabuleiro)

# define jogador x ou +
global p 
p = 0

while p+1 <= NUMERO_PECAS: # não há vencedor ou empate
    peca = lista_pecas[p]
    print('PEÇA: ' + peca)

    # pede jogada
    jogada = pede_jogada(tabuleiro)
    # actualiza tabuleiro
    tabuleiro = actualiza_tabuleiro(tabuleiro,jogada,peca)

    # mostra tabuleiro
    mostra_tabuleiro(tabuleiro)
    
    # Vencedor ou empate --> termina
    if vence_menos(tabuleiro,'-') or encontra_circulo(tabuleiro,'o'):
        print("=========== GG ===========")
    """if vencedor(tabuleiro,peca) or empate(tabuleiro):
        break"""
    
    if figura_x(tabuleiro, 'x'):
        print("=========== GG ===========")
        #mostra_tabuleiro(tabuleiro)

   # proxima peca
    p=p+1
            
    # mensagem final
    """print('Finito...')
    if empate(tabuleiro):
        print('PERDEU O JOGO!')
    elif peca == 'x':
        print('FIGURA x CONCLUIDA!')
    else:
        print('FIGURA + CONCLUIDA!') """