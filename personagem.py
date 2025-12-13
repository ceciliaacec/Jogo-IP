import pygame

class Personagem(pygame.sprite.Sprite):
    def __init__(self, x, y, cor, tamanho):
        # inicializa o sprite base do pygame
        super().__init__()
        
        # cria a superfície (a imagem) do personagem (quadrado branco)
        self.image = pygame.Surface([tamanho, tamanho])
        self.image.fill(cor) # Deve ser Branco (255, 255, 255)
        
        # obtém o retângulo que define a posição e o tamanho
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # velocidade de movimento
        self.velocidade = 5

    def update(self, teclas_pressionadas, largura_tela, altura_tela):
        # lógica pra movimentar o personagem baseada nas teclas
        if teclas_pressionadas[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if teclas_pressionadas[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        if teclas_pressionadas[pygame.K_UP]:
            self.rect.y -= self.velocidade
        if teclas_pressionadas[pygame.K_DOWN]:
            self.rect.y += self.velocidade
            
        # restringe o personagem aos limites da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > largura_tela:
            self.rect.right = largura_tela
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > altura_tela:
            self.rect.bottom = altura_tela