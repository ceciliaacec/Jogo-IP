import pygame
import random
from cores import LARGURA, ALTURA, MARROM, ROXO, VERMELHO, PRETO

class ObjetoMovel(pygame.sprite.Sprite):
    """Classe base para Asteroide, Alien, Coração."""
    
    # Recebe 'tela' para desenhar
    def __init__(self, largura_tela, altura_tela, tamanho, tela, vel=3):
        super().__init__()
        self.vel = vel
        self.tela = tela # Armazena a referência da tela
        
        self.image = pygame.Surface([tamanho, tamanho])
        self.image.set_colorkey(PRETO)
        
        self.rect = self.image.get_rect(x=random.randint(0, largura_tela - tamanho), y=-tamanho)
        
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.tamanho = tamanho
        self.vida = 1 

    def update(self):
        """Move o objeto para baixo."""
        self.rect.y += self.vel

    def fora_da_tela(self):
        """Verifica se o objeto saiu da parte inferior da tela."""
        return self.rect.top > self.altura_tela

    def desenhar(self):
        """Deve ser implementado nas subclasses."""
        raise NotImplementedError

class Asteroide(ObjetoMovel):
    """Um obstáculo que causa dano e pode ser destruído."""
    
    # Passa 'tela' para o construtor base
    def __init__(self, largura, altura, tela): 
        tamanho = 40
        super().__init__(largura, altura, tamanho, tela)
        self.vel = random.randint(2, 4)
        self.vida = 1 

    def desenhar(self):
        p = self.rect
        # Desenho usando self.tela
        pygame.draw.circle(self.tela, MARROM, p.center, p.width // 2)
        pygame.draw.circle(self.tela, (80, 60, 50), p.center, p.width // 2, 2)

        # Detalhes na superfície
        for _ in range(2):
            cx = random.randint(p.left + 6, p.right - 6)
            cy = random.randint(p.top + 6, p.bottom - 6)
            pygame.draw.circle(self.tela, (70, 55, 45), (cx, cy), 3)

class Alien(ObjetoMovel):
    """Um item colecionável."""
    
    # Passa 'tela' para o construtor base
    def __init__(self, largura, altura, tela):
        tamanho = 30
        super().__init__(largura, altura, tamanho, tela)
        self.vel = 3

    def desenhar(self):
        a = self.rect
        # Desenho usando self.tela
        pygame.draw.ellipse(self.tela, ROXO, (a.x, a.y + 4, 30, 18))
        pygame.draw.rect(self.tela, PRETO, (a.x + 6, a.y + 10, 6, 3))
        pygame.draw.rect(self.tela, PRETO, (a.x + 18, a.y + 10, 6, 3))
        pygame.draw.line(self.tela, (120, 60, 150), (a.x + 15, a.y + 6), (a.x + 15, a.y + 18), 2)

class Coracao(ObjetoMovel):
    """Um item que cura a nave."""
    
    # Passa 'tela' para o construtor base
    def __init__(self, largura, altura, tela):
        tamanho = 20
        super().__init__(largura, altura, tamanho, tela)
        self.vel = 3

    def desenhar(self):
        c = self.rect
        # Desenho usando self.tela
        pygame.draw.circle(self.tela, VERMELHO, (c.x + 6, c.y + 6), 6)
        pygame.draw.circle(self.tela, VERMELHO, (c.x + 14, c.y + 6), 6)
        pygame.draw.polygon(self.tela, VERMELHO, [
            (c.x, c.y + 8),
            (c.x + 20, c.y + 8),
            (c.x + 10, c.y + 22)
        ])