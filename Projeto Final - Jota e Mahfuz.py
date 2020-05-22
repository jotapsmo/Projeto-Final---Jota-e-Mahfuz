import pygame
import random 
import os
import sys

#Definindo cores:
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0) 
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CINZA = (127, 127, 127)

pygame.init() # Iniciando as rotinas do pygame

surf = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Insira o nome do jogo aqui")
