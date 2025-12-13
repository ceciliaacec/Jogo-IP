import pygame
import random

class Colecionavel(pygame.sprite.Sprite):
    def __init__(self, largura_tela, altura_tela, cor, tamanho):
        super().__init__()
        
        # cria a superfície do colecionável (quadrado da cor específica)
        self.image = pygame.Surface([tamanho, tamanho])
        self.image.fill(cor) 
        
        # define a posição aleatória na tela
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(largura_tela - tamanho)
        self.rect.y = random.randrange(altura_tela - tamanho)
        
        # armazena a cor para a lógica de pontuação
        self.cor = cor