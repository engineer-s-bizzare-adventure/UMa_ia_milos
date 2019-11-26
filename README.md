# milos

move_forward(casas): anda 'casas' elementos da matriz para a frente

move_backward(casas): anda 'casas' elementos da matriz para tras

turn_right(angulo): vira 'angulo' para a direita

turn_left(angulo): vira 'angulo' para a esquerda

pick(): apanhar objeto com a garra

drop(): larga objeto da garra

procura(): procura por um objeto a menos de 'DISTANCIA_PROCURA' cm de distancia, quando encontra o robot desloca-se até uma distância de 'DISTANCIA_MIN' do objeto e alinha-se de com a matriz, roda 90º à direita para iniciar a leitura das peças.
No sitio inicial, roda os 90º à esquerda e roda o angulo calculado anterior e desloca-se para trás até estar à distância inicial do objeto, volta a alinhar e assim o robot volta à posição de quando inicio à função
