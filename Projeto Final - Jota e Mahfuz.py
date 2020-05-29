import pygame
import random
vet = pygame.math.Vector2

 

LARGURA = 480
ALTURA = 600
FPS = 60

 
#Site com cores: https://www.webucator.com/blog/2015/03/python-color-constants-module/
#DEFININDO CORES:
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0) 
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CINZA = (127, 127, 127)
 

AC_JOGADOR = 0.6
F_JOGADOR = -0.15
G_JOGADOR = 1


LISTA_PLATAFORMAS = [(0, ALTURA - 40, LARGURA, 40), 
                    (LARGURA / 2 - 50, ALTURA * 3 / 4, 100, 20),
                    (125, ALTURA - 350, 100, 20),
                    (350, 200, 100, 20),
                    (175, 100, 50, 20)]
 

class Jogador(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((30, 40))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect()
        #DEFINE A POSIÇÃO INCIAL DO JOGADOR
        self.rect.center = (LARGURA / 2, ALTURA / 2)
        self.pos = vet(LARGURA / 2, ALTURA / 2)
        self.vel = vet(0,0)
        self.ac = vet(0,0)

    def pulo(self):
        # pular somente quando estiver sobre uma plataforma
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.plataforma, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20      

    def update(self):
        self.ac = vet(0, G_JOGADOR)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.ac.x = -AC_JOGADOR
        if keys[pygame.K_RIGHT]:
            self.ac.x = AC_JOGADOR

 

        #CONTROLE SOBRE A MOVIMENTAÇÃO DO JOGADOR --> FRICÇÃO E EQUAÇÕES DE MOVIMENTO
        self.ac.x += self.vel.x * F_JOGADOR
        self.vel += self.ac
        self.pos += self.vel + 0.5 * self.ac
        #DAR A VOLTA NA TELA
        if self.pos.x > LARGURA:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = LARGURA

        self.rect.midbottom = self.pos


class Plataformas(pygame.sprite.Sprite):
   
    def __init__(self, x, y, l, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((l, h))
        self.image.fill(BRANCO)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
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
        self.plataforma = pygame.sprite.Group()
        self.jogador = Jogador(self)
        self.all_sprites.add(self.jogador)
        for plat in LISTA_PLATAFORMAS:
            p = Plataformas(*plat)
            self.all_sprites.add(p)
            self.plataforma.add(p)
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
        self.all_sprites.update()
        if self.jogador.vel.y > 0:
            hit = pygame.sprite.spritecollide(self.jogador, self.plataforma, False)
            if hit:
                self.jogador.pos.y = hit[0].rect.top
                self.jogador.vel.y = 0




    def eventos(self):
        #Game loop - eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.jogar:
                    self.jogar = False
                self.gestao = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.jogador.pulo()



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