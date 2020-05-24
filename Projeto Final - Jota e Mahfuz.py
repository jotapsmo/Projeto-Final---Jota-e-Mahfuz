
import pygame
import random 
from sprites import *

LARGURA = 480
ALTURA = 600
FPS = 60

#DEFININDO CORES:
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0) 
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CINZA = (127, 127, 127)

class Game:
    def __init__(self):
        #Abre a janela do jogo 
        pygame.init()
        pygame.mixer.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("DUDLE JUMP")
        self.clock = pygame.time.Clock()
        self.gestao = True

    def new(self):
        #Começa um jogo novo
        self.all_sprites = pygame.sprite.Group()
        self.run()

    def run(self):
        #Game loop
        self.jogar = True
        while self.jogar:
            self.clock.tick(FPS)
            self.eventos()
            self.update()
            self.draw()

    def update(self):
        #Game loop - Update
        self.all_sprites.update

    def eventos(self):
        #Game loop - eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.jogar:
                    self.jogar = False
                self.gestao = False

    def draw(self):
        #Game loop - draw
        self.tela.fill(PRETO)
        self.all_sprites.draw(self.tela)
        #Depois de desenhar tudo, flip o display
        pygame.display.flip()
    
    def show_tela_inicio(self):
        #Mostra a tela de início
        pass

    def show_tela_fim(self):
        #Mostra a tela do Game Over
        pass


g = Game()
g.show_tela_inicio()
while g.gestao:
    g.new()
    g.show_tela_fim()

pygame.quit()
