#Desenvolvido por: Tiago Henrique Corsi
#Data: 13/08/2022
#Sobre: Classe com métodos customizados para desenvolver um jogo como tetris
#usando fitas de led do tipo WS2812B e herda a classe NeoPixel

#Utilizando classe like_tetris criada por Leandro Poloni Dantas
#Git Hub: https://github.com/LePoloni/like_tetris

import time, machine, sys, random
from like_tetris import like_tetris
from machine import Pin
from ESP32_BLE import ESP32_BLE

botaoEsq = Pin(15 , Pin.IN, Pin.PULL_UP)
botaoDir = Pin(14, Pin.IN, Pin.PULL_UP)
botaoRot = Pin(12, Pin.IN, Pin.PULL_UP)
botaoDesc = Pin(13, Pin.IN, Pin.PULL_UP)

linhas = 15     #O objeto canvas no Wokwi só funciona com linhas pares
colunas = 10    #O objeto canvas no Wokwi só funciona com linhas pares
posicao = (0,0)

debug = True

#inicializa a classe ESP32BLE
#Necessita do pino #2 para indicar a conexão com o bluetooth
ble = ESP32_BLE("ESP32-BLE-THC")

# create an input pin on pin #4, with a pull up resistor
tt = like_tetris(machine.Pin(4), colunas, linhas, "t_linha_zig_zag")

cor_fundo = (0,0,0)
tt.limpa_matriz(cor_fundo)

def rand(i):
    return random.randint(0,i-1)

def gameOver():    
    for i in range(3):
        #preenche todos os leds com branco
        cor_fundo = (255,255,255)
        tt.limpa_matriz(cor_fundo)
    
        #delay de 300ms
        time.sleep_ms(400)
    
        #Apaga todos os leds
        cor_fundo = (0,0,0)
        tt.limpa_matriz(cor_fundo)
        
        #delay de 300ms
        time.sleep_ms(400)
    
    if debug:
        print('FIM DO JOGO')
    sys.exit()

while True:
    if not ble.isConnected():
        time.sleep_ms(500)
        if debug:
            print('Aguardando conexão bluetooth')
    
    else:
        #1-Cria um novo bloco
        bloco = tt.cria_bloco([5,0],rand(6),(rand(255),rand(255),rand(255)))
        
        #2-Teste se a posição já está ocupada
        if tt.testa_ocupacao(bloco, (0,0,0)) == False:
            tt.desenha_bloco(bloco)
            time.sleep_ms(1000)
        else:
            #Fim do Jogo
            gameOver()      
        
        #3-Inicia um loop de descida do bloco
        estado = True
        while estado == True:            
            #Debug - mostra o bloca a ser movido
            if debug:
                print('bloco a ser movido =', bloco)
            
            #Novo movimento
            estado, bloco = tt.movimento_completo(bloco, cor_fundo)
            
            #loop para verificar se algum botão foi pressionado
            for i in range(5):
                #Testa se o movimento foi possível
                if estado == False:
                    break #Interrompe o laço
                
                #Testa os botões: Esquerdo, Direito, Rotação, Descida           
                
                #Botão esquerdo
                #elif botaoEsq.value() == 0:
                elif (botaoEsq.value() == 0) or (ble.getMessage() == 'botaoEsq'):
                    if debug:
                        print('botaoEsq')
                    
                    #Envia para o blueetooth
                    ble.send('botaoEsq')
                    
                    #Apaga o bloco
                    tt.apaga_bloco(bloco, (0,0,0))
                    #Desloca
                    bloco2 = tt.desloca_bloco(bloco, [-1,0])
                    #Faz ajuste de posição (testa se o bloco ficou partido em duas partes após
                    #rotacionar ou deslocar)
                    bloco2 = tt.ajusta_posicao_bloco(bloco2)
                    #Testa
                    if tt.testa_ocupacao(bloco2, cor_fundo) == False:
                        #Desenha bloco2
                        tt.desenha_bloco(bloco2)
                        #Atualiza o bloco1
                        bloco = bloco2
                    else:
                        #Desenha bloco1
                        tt.desenha_bloco(bloco)
                
                #Botão esquerdo        
                #elif botaoDir.value() == 0:
                elif (botaoDir.value() == 0) or (ble.getMessage() == 'botaoDir'):
                    if debug:
                        print('botaoDir')
                    
                    #Envia para o blueetooth
                    ble.send('botaoDir')
                    
                    #Apaga o bloco
                    tt.apaga_bloco(bloco, (0,0,0))
                    #Desloca
                    bloco2 = tt.desloca_bloco(bloco, [+1,0])
                    #Faz ajuste de posição (testa se o bloco ficou partido em duas partes após
                    #rotacionar ou deslocar)
                    bloco2 = tt.ajusta_posicao_bloco(bloco2)
                    #Testa
                    if tt.testa_ocupacao(bloco2, cor_fundo) == False:
                        #Desenha bloco2
                        tt.desenha_bloco(bloco2)
                        #Atualiza o bloco1
                        bloco = bloco2
                    else:
                        #Desenha bloco1
                        tt.desenha_bloco(bloco)
                
                #Botão de rotação
                #elif botaoRot.value() == 0:
                elif (botaoRot.value() == 0) or (ble.getMessage() == 'botaoRot'):
                    if debug:
                        print('botaoRot')
                    
                    #Envia para o blueetooth
                    ble.send('botaoRot')
                    
                    #Apaga o bloco
                    tt.apaga_bloco(bloco, (0,0,0))
                    #Rotaciona o bloco
                    bloco2 = tt.rotaciona_bloco(bloco)
                    #Faz ajuste de posição (testa se o bloco ficou partido em duas partes após
                    #rotacionar ou deslocar)
                    bloco2 = tt.ajusta_posicao_bloco(bloco2)
                    #Testa
                    if tt.testa_ocupacao(bloco2, cor_fundo) == False:
                        #Desenha bloco2
                        tt.desenha_bloco(bloco2)
                        #Atualiza o bloco1
                        bloco = bloco2
                    else:
                        #Desenha bloco1
                        tt.desenha_bloco(bloco)
                        
                #Botao para acelerar a descida do bloco
                #elif botaoDesc.value() == 0:
                elif (botaoDesc.value() == 0) or (ble.getMessage() == 'botaoDesc'):
                    if debug:
                        print('botaoDesc')
                    
                    #Envia para o blueetooth
                    ble.send('botaoDesc')
                        
                    #Apaga o bloco
                    tt.apaga_bloco(bloco, (0,0,0))
                    #Desloca
                    bloco2 = tt.desloca_bloco(bloco, [0,+1])
                    #Faz ajuste de posição (testa se o bloco ficou partido em duas partes após
                    #rotacionar ou deslocar)
                    bloco2 = tt.ajusta_posicao_bloco(bloco2)
                    #Testa
                    if tt.testa_ocupacao(bloco2, cor_fundo) == False:
                        #Desenha bloco2
                        tt.desenha_bloco(bloco2)
                        #Atualiza o bloco1
                        bloco = bloco2
                    else:
                        #Desenha bloco1
                        tt.desenha_bloco(bloco)
                        
                time.sleep_ms(100)
        
        #4-Verifica o preenchimento de linhas
        tt.testa_preenchimento_linha(cor_fundo)
