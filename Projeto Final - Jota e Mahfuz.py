
import pygame
import random 
import os
import sys

LARGURA = 360
ALTURA = 480
FPS = 30

#Definindo cores:
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0) 
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CINZA = (127, 127, 127)


#INICIANDO A ROTINA DO PYGAME
pygame.init()
pygame.mixer.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("DUDLE JUMP")
clock = pygame.time.Clock()

#GAME LOOP
gestao = True
while gestao:
    #Deixar na velocidade certa
    clock.tick(FPS)
    #Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gestao = False
    #Update
    #Render - Draw
    tela.fill(PRETO)
    #Depois de desenhar tudo, flip o display
    pygame.display.flip()


pygame.quit()
