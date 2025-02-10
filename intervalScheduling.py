import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Constantes de configuração

tempo_max = 11
max_tarefas = 21
min_tarefas = 8
peso_max = 10

offsetX = 30
screen_width = tempo_max * 100 + (offsetX*2)  

screen_height = 900 + (40 * (abs(max_tarefas - 20) * (max_tarefas > 20))) 
offsetY = screen_height/2 + 60
offsetY2 = offsetY + 200

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Interval Scheduling')

# Definir cores
""" PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0) """

COR_FUNDO = (255, 255, 255)
COR_FONTE = (0, 0, 0)
COR_TEXTO_FUNDO = (255, 255, 255)
COR_TAREFA = (0, 0, 255)
COR_SEPARADOR = (255, 0, 0)
COR_LINHA = (0, 0, 0)

font = pygame.font.SysFont('arial', 30)

def desenhar_linha():
    start_pos = (offsetX, offsetY)
    end_pos = (screen_width-offsetX, offsetY)
    pygame.draw.line(screen, COR_LINHA, start_pos, end_pos, 3)

    start_pos = (offsetX, offsetY2)
    end_pos = (screen_width-offsetX, offsetY2)
    pygame.draw.line(screen, COR_LINHA, start_pos, end_pos, 3)

def desenhar_tarefa(tarefa):
    inicio = (tarefa[1] * 100) + offsetX
    termino = ((tarefa[2]-tarefa[1]) * 100) 
    pygame.draw.rect(screen, COR_TAREFA, (inicio, offsetY-50, termino, 50))
    pygame.draw.line(screen, COR_SEPARADOR, (inicio, offsetY), (inicio, offsetY-50), 3)

    texto = '{}'.format(tarefa[0])  # Formata string 
    text = font.render(texto, True, COR_FONTE, COR_TAREFA)
    textRect = text.get_rect()
    textRect.center = (inicio+(termino/2), offsetY-25)
    screen.blit(text, textRect)

def desenhar_tarefa2(tarefa):
    inicio = (tarefa[1] * 100) + offsetX
    termino = ((tarefa[2]-tarefa[1]) * 100) 
    pygame.draw.rect(screen, COR_TAREFA, (inicio, offsetY2-50, termino, 50))
    pygame.draw.line(screen, COR_SEPARADOR, (inicio, offsetY2), (inicio, offsetY2-50), 3)

    texto = '{}'.format(tarefa[0])  # Formata string 
    text = font.render(texto, True, COR_FONTE, COR_TAREFA)
    textRect = text.get_rect()
    textRect.center = (inicio+(termino/2), offsetY2-25)
    screen.blit(text, textRect)

def intervalScheduling(tarefas):
    tarefas.sort(key=lambda x: x[2])
    contador = 0
    final = 0
    solucao = []

    for intervalo in tarefas:
        if(final <= intervalo[1]):
            final = intervalo[2]
            contador +=1
            solucao.append(intervalo)
            desenhar_tarefa(intervalo)
    
    print(f"Maximo de tarefas: {contador}") 
    print(f"Lista de tarefas: {solucao}") 

def weightedIntervalScheduling(tarefas):
    tarefas.sort(key=lambda x: x[2])
    n = len(tarefas)
    
    last_non_overlapping = [-1] * n
    for j in range(n):
        for i in range(j - 1, -1, -1):
            if tarefas[i][2] <= tarefas[j][1]:
                last_non_overlapping[j] = i
                break

    M = [0] * (n + 1)
    
    for j in range(1, n + 1):
        tarefa_atual = tarefas[j-1]
        #print(tarefa_atual)
        prev_task_index = last_non_overlapping[j-1]
        M[j] = max(tarefa_atual[3] + (M[prev_task_index + 1] if prev_task_index >= 0 else 0), M[j-1])
    
    solution = FindSolution(n, tarefas, M, last_non_overlapping)

    peso_total = sum(tarefas[i][3] for i in solution)
    print(f"Peso total: {peso_total}")
    tarefas_escolhidas = [tarefas[i] for i in solution]
    print(f"Lista de tarefas: {tarefas_escolhidas}")
    
    return M[n]  

def FindSolution(j, tarefas, M, last_non_overlapping):
    if j == 0:
        return set() 
    
    prev_task_index = last_non_overlapping[j-1]
    if tarefas[j-1][3] + (M[prev_task_index + 1] if prev_task_index >= 0 else 0) > M[j-1]:
        #print(tarefas[j-1])
        desenhar_tarefa2(tarefas[j-1])

        return {j-1} | FindSolution(prev_task_index + 1, tarefas, M, last_non_overlapping)
    else:
        return FindSolution(j-1, tarefas, M, last_non_overlapping)

def gerar_tarefas():
    tarefas = []
    contador = random.randint(min_tarefas, max_tarefas)

    for i in range(ord('A'), ord('A') + contador):
        #print(chr(i))
        inicio = random.randint(0, tempo_max - 1)
        fim = random.randint(inicio + 1, tempo_max)
        peso = random.randint(1, peso_max)
        tarefas.append((chr(i), inicio, fim, peso))
    #print(tarefas)

    return tarefas

def desenhar_lista(tarefas):
    font = pygame.font.SysFont('arial', 15)
    texto = ' LISTA DE TAREFAS: '
    text = font.render(texto, True, COR_FONTE, COR_TEXTO_FUNDO)
    textRect = text.get_rect()
    textRect.left = offsetX
    textRect.top = 10
    screen.blit(text, textRect)

    texto = ' Aperte \'G\' para gerar novas tarefas '
    text = font.render(texto, True, COR_FONTE, COR_TEXTO_FUNDO)
    textRect.left = offsetX + 300
    screen.blit(text, textRect)

    texto = ' Aperte \'I\' para fazer o Interval Scheduling'
    text = font.render(texto, True, COR_FONTE, COR_TEXTO_FUNDO)
    textRect.left = offsetX + 600
    screen.blit(text, textRect)

    texto = ' Aperte \'Esc\' para sair '
    text = font.render(texto, True, COR_FONTE, COR_TEXTO_FUNDO)
    textRect.right = screen_width - offsetX
    screen.blit(text, textRect)

    y = 35
    for tarefa in tarefas:
        texto = ' Tarefa: {} -> Inicio: {} | Fim: {} | Peso: {} '.format(tarefa[0], tarefa[1], tarefa[2], tarefa[3])  # Formata string 
        font = pygame.font.SysFont('arial', 12)
        text = font.render(texto, True, COR_FONTE, COR_TEXTO_FUNDO)
        textRect = text.get_rect()
        textRect.left = offsetX
        textRect.top = y 
        screen.blit(text, textRect)
        y += 20

def game_loop():
    running = True
    tarefas = [('A', 0, 6, 5), ('B', 1, 4, 3), ('C', 3, 5, 7), ('D', 3, 8, 2), ('E', 4, 7, 8), ('F', 5, 9, 6), ('G', 6, 10, 4), ('H', 8, 11, 1)] # Tarefas iniciais iguais ao slide
    screen.fill(COR_FUNDO)
    desenhar_lista(tarefas)

    while running:
        
        desenhar_linha()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Apertou Esc
                    pygame.quit() #Fecha jogo e programa
                    sys.exit()
                elif event.key == pygame.K_i: # Apertou i
                    intervalScheduling(tarefas)
                    weightedIntervalScheduling(tarefas)
                elif event.key == pygame.K_g: # Apertou g
                    tarefas = gerar_tarefas()
                    screen.fill(COR_FUNDO)
                    desenhar_lista(tarefas)

        pygame.display.flip()


game_loop()