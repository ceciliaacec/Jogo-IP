import pygame
import random
from cores import AZUL, CINZA, AMBAR, LARGURA

class Tiro:
    """Projetil disparado pela nave."""
    
    # Recebe 'tela' para desenhar
    def __init__(self, x, y, tela): 
        self.rect = pygame.Rect(x, y, 2, 14)
        self.vel = 12
        self.tela = tela

    def mover(self):
        self.rect.y -= self.vel

    def desenhar(self):
        pygame.draw.line(self.tela, AMBAR, (self.rect.centerx, self.rect.top), (self.rect.centerx, self.rect.bottom), 3)

    def fora_da_tela(self):
        return self.rect.bottom < 0

class Nave(pygame.sprite.Sprite):
    """A nave do jogador."""
    
    # Recebe 'tela' para desenhar e criar tiros
    def __init__(self, x, y, tela): 
        super().__init__()
        self.rect = pygame.Rect(x, y, 40, 50) 
        self.tela = tela
        self.vel = 6
        self.vida = 100
        self.invencivel_timer = 0
        self.max_tiros = 6

    def desenhar(self):
        """Desenha a nave na tela, com efeito de piscar durante a invencibilidade."""
        if self.invencivel_timer > 0 and self.invencivel_timer % 4 < 2:
            return
            
        r = self.rect
        
        # Desenho da nave (corpo, asas, cabine, chama)
        pygame.draw.polygon(self.tela, CINZA, [(r.centerx, r.top), (r.left + 6, r.bottom - 14), (r.right - 6, r.bottom - 14)])
        pygame.draw.rect(self.tela, CINZA, (r.left - 6, r.bottom - 26, 8, 22))
        pygame.draw.rect(self.tela, CINZA, (r.right - 2, r.bottom - 26, 8, 22))
        pygame.draw.circle(self.tela, AZUL, (r.centerx, r.centery - 4), 6)

        # Chama do motor
        for _ in range(3):
            pygame.draw.circle(
                self.tela,
                (80, 170, 255),
                (r.centerx, r.bottom - 2),
                random.randint(4, 7)
            )

    def mover(self, teclas):
        """Processa a movimentação horizontal da nave, respeitando os limites LARGURA."""
        if teclas[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.vel
        if teclas[pygame.K_d] and self.rect.right < LARGURA:
            self.rect.x += self.vel

    def atirar(self, tiros_list):
        """Cria um novo tiro, respeitando o limite de tiros na tela."""
        if len(tiros_list) < self.max_tiros:
            # Passamos 'self.tela' para a instância do Tiro
            tiros_list.append(Tiro(self.rect.centerx, self.rect.top, self.tela))

    def atualizar_invencibilidade(self):
        """Decrementa o temporizador de invencibilidade."""
        if self.invencivel_timer > 0:
            self.invencivel_timer -= 1

    def levar_dano(self, dano=20):
        """Aplica dano e ativa o timer de invencibilidade."""
        if self.invencivel_timer == 0:
            self.vida -= dano
            self.invencivel_timer = 30
            if self.vida < 0:
                self.vida = 0
            return True 
        return False

    def curar(self, cura=20):
        """Aumenta a vida da nave, limitado a 100."""
        self.vida = min(100, self.vida + cura)