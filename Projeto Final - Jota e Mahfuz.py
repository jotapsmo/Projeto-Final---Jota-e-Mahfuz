import pygame
import random
from os import path
vet = pygame.math.Vector2
 
TITULO = "DUDLE JUMP" 
LARGURA = 480
ALTURA = 600
FPS = 60
FONTE = "times new roman"
SPRITESHEET = "final2.png"
 
#Site com cores: https://www.webucator.com/blog/2015/03/python-color-constants-module/
#DEFININDO CORES:
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0) 
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CINZA = (127, 127, 127)
AZUL_CLARO = (0,154,205)
LARANJA = (255,97,3)
 
AC_JOGADOR = 0.8
F_JOGADOR = -0.16
G_JOGADOR = 1
PULO_JOGADOR = 21

 
LISTA_PLATAFORMAS = [(0, ALTURA - 60), 
                    (LARGURA / 2 - 50, ALTURA * 3 / 4),
                    (125, ALTURA - 350),
                    (350, 200),
                    (175, 100)]
 
class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, altura, largura):
        image = pygame.Surface((largura, altura))
        image.blit(self.spritesheet, (0,0), (x, y, largura, altura))
        image = pygame.transform.scale(image, (largura//4, altura//4))
        return image 

class Jogador(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.andando = False
        self.pulando = False
        self.frame_atual = 0
        self.ultimo_update = 0
        self.carrega_imagens()
        self.image = self.em_pe[0]
        self.rect = self.image.get_rect()
        #DEFINE A POSIÇÃO INCIAL DO JOGADOR
        self.rect.center = (40, ALTURA - 100)
        self.pos = vet(40, ALTURA - 100)
        self.vel = vet(0,0)
        self.ac = vet(0,0)


    def carrega_imagens(self):
        self.em_pe = [self.game.spritesheet.get_image(410,370,270,100), 
        self.game.spritesheet.get_image(530,370,270,100)]
        for frame in self.em_pe:
            frame.set_colorkey(PRETO)

        self.andando_d = [self.game.spritesheet.get_image(410,370,270,100),
        self.game.spritesheet.get_image(160,220,270,150)]
        for frame in self.andando_d:
            frame.set_colorkey(PRETO)
        
        self.andando_e = [pygame.transform.flip(self.game.spritesheet.get_image(410,370,270,100), 
        True, False), pygame.transform.flip(self.game.spritesheet.get_image(160,220,270,150), True, False)]
        for frame in self.andando_e:
            frame.set_colorkey(PRETO)
        
        self.pulando = [self.game.spritesheet.get_image(420,30,270,130)]
        for frame in self.pulando:
            frame.set_colorkey(PRETO)

 
    def pulo(self):
        # pular somente quando estiver sobre uma plataforma
        self.rect.x += 2
        hits = pygame.sprite.spritecollide(self, self.game.plataforma, False)
        self.rect.x -= 2
        if hits:
            self.vel.y = -PULO_JOGADOR
 
    def update(self):
        self.anima()
        self.ac = vet(0, G_JOGADOR)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.ac.x = -AC_JOGADOR
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.ac.x = AC_JOGADOR

        #CONTROLE SOBRE A MOVIMENTAÇÃO DO JOGADOR --> FRICÇÃO E EQUAÇÕES DE MOVIMENTO
        self.ac.x += self.vel.x * F_JOGADOR
        self.vel += self.ac
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.ac
        #DAR A VOLTA NA TELA
        if self.pos.x > LARGURA :
            self.pos.x = 0
        if self.pos.x < 0 :
            self.pos.x = LARGURA
 
        self.rect.midbottom = self.pos


    def anima(self):
        agora = pygame.time.get_ticks()
        if self.vel.x != 0:
            self.andando = True
        else:
            self.andando = False

        if self.andando:
            if agora - self.ultimo_update > 250:
                self.ultimo_update = agora
                self.frame_atual = (self.frame_atual + 1) % len(self.andando_e)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.andando_d[self.frame_atual]
                else:
                    self.image = self.andando_e[self.frame_atual]   
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.pulando and not self.andando:
            if agora - self.ultimo_update > 350:
                self.ultimo_update = agora
                self.frame_atual = (self.frame_atual + 1) % len(self.em_pe)
                bottom = self.rect.bottom
                self.image = self.em_pe[self.frame_atual]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                
class Plataformas(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        imagens = [self.game.spritesheet.get_image(0, 530, 120, 390)]
        self.image = random.choice(imagens)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Game:
    def __init__(self):
        #Abre a janela do jogo 
        pygame.init()
        pygame.mixer.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption(TITULO)
        self.clock = pygame.time.Clock()
        self.gestao = True
        self.nome_fonte = pygame.font.match_font(FONTE)
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        imagem_dir = path.join(self.dir, "imagens")

        self.spritesheet = Spritesheet(path.join(imagem_dir, SPRITESHEET))
        self.som_dir = path.join(self.dir, "sons")
        self.som_pulo = pygame.mixer.Sound(path.join(self.som_dir, "pulo1.wav"))
        self.som_morte = pygame.mixer.Sound(path.join(self.som_dir, "gta.wav"))

    def new(self):
        #Começa um jogo novo
        self.placar = 0
        self.all_sprites = pygame.sprite.Group()
        self.plataforma = pygame.sprite.Group()
        self.jogador = Jogador(self)
        self.all_sprites.add(self.jogador)
        for plat in LISTA_PLATAFORMAS:
            p = Plataformas(self, *plat)
            self.all_sprites.add(p)
            self.plataforma.add(p)
        pygame.mixer.music.load(path.join(self.som_dir, "crab.wav"))
        self.run()


    def run(self):
        #Game loop
        pygame.mixer.music.play(loops=-1)
        self.jogar = True
        while self.jogar:
            self.clock.tick(FPS)
            self.eventos()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(700)
         

    def update(self):
        #Game loop - Update
        self.all_sprites.update()
        if self.jogador.vel.y > 0:
            hit = pygame.sprite.spritecollide(self.jogador, self.plataforma, False)
            if hit:
                mais_baixo = hit[0]
                for h in hit:
                    if h.rect.bottom > mais_baixo.rect.bottom:
                        mais_baixo = h
                if self.jogador.pos.y < mais_baixo.rect.bottom:
                    self.jogador.pos.y = mais_baixo.rect.top
                    self.jogador.vel.y = 0


        if self.jogador.rect.top <= ALTURA / 4:
            self.jogador.pos.y += max(abs(self.jogador.vel.y), 2)
            for plat in self.plataforma:
                plat.rect.y += max(abs(self.jogador.vel.y), 2)
                if plat.rect.top >= ALTURA:
                    plat.kill()
                    self.placar += 1

        if self.jogador.rect.bottom > ALTURA:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.jogador.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.plataforma) == 0:               
            self.jogar = False

        while len(self.plataforma) < 6:
            largura = random.randrange(50, 100)
            p = Plataformas(self, random.randrange(0, LARGURA - largura),
                                            random.randrange(-75, -30))
            self.plataforma.add(p)
            self.all_sprites.add(p)

    def eventos(self):
        #Game loop - eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.jogar:
                    self.jogar = False
                self.gestao = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    self.som_pulo.play()
                    self.jogador.pulo()
                    

    def draw(self):
        #Game loop - draw
        self.tela.fill(AZUL_CLARO)
        self.all_sprites.draw(self.tela)
        self.tela.blit(self.jogador.image, self.jogador.rect)
        self.draw_texto(str(self.placar), 25, BRANCO, LARGURA/2, 15)
        #Depois de desenhar tudo, flip o display
        pygame.display.flip()
 
    def tela_inicio(self):
        pygame.mixer.music.load(path.join(self.som_dir, "nw.wav"))
        pygame.mixer.music.play(loops=-1)
        self.tela.fill(AZUL_CLARO)
        self.draw_texto(TITULO, 48, BRANCO, LARGURA / 2, ALTURA / 4)
        self.draw_texto("Setas para andar, Espaço para pular", 22, BRANCO, LARGURA / 2, ALTURA / 2)
        self.draw_texto("Aperte uma tecla para jogar", 22, BRANCO, LARGURA / 2, ALTURA * 3 / 4)
        pygame.display.flip()
        self.espera_tecla()
        pygame.mixer.music.fadeout(600)
     
    def tela_fim(self):
        #Mostra a tela do Game Over
        if not self.gestao:
            return
        self.som_morte.play()
        self.tela.fill(PRETO)
        self.draw_texto("GAME OVER", 48, BRANCO, LARGURA / 2, ALTURA / 4)
        self.draw_texto("Plataformas " + str(self.placar), 22, BRANCO, LARGURA / 2, ALTURA / 2)
        self.draw_texto("Aperte uma tecla para jogar", 22, BRANCO, LARGURA / 2, ALTURA * 3 / 4)
        pygame.display.flip()
        self.espera_tecla()
        

    def espera_tecla(self):
        espera = True
        while espera:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    espera = False
                    self.gestao = False
                if event.type == pygame.KEYUP:
                    espera = False


    def draw_texto(self, text, tamanho, cor, x, y):
        fonte = pygame.font.Font(self.nome_fonte, tamanho)
        texto_superficie = fonte.render(text, True, cor)
        texto_rect = texto_superficie.get_rect()
        texto_rect.midtop = (x, y)
        self.tela.blit(texto_superficie, texto_rect)

g = Game()
g.tela_inicio()
while g.gestao:
    g.new()
    g.tela_fim()

pygame.quit()