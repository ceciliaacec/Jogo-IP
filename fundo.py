import pygame
import random
import math
from cores import LARGURA, ALTURA, PRETO

class Fundo:
    """Gerencia as estrelas e galáxias do fundo."""
    
    # Recebe 'tela' para desenhar
    def __init__(self, tela): 
        self.tela = tela
        self.largura = LARGURA
        self.altura = ALTURA
        self.estrelas = []
        
        for velocidade, quantidade in [(1, 80), (2, 60), (3, 40)]:
            for _ in range(quantidade):
                self.estrelas.append([random.randint(0, self.largura), random.randint(0, self.altura), velocidade])

        self.galaxias = [
            {"x": 520, "y": 200, "r": 70},
            {"x": 260, "y": 420, "r": 55}
        ]

    def desenhar_galaxia(self, x, y, r):
        """Desenha uma galáxia no formato espiral."""
        for i in range(70):
            ang = i * 0.35
            raio = r * (i / 70)
            px = int(x + math.cos(ang) * raio)
            py = int(y + math.sin(ang) * raio)
            pygame.draw.circle(self.tela, (120, 90, 150), (px, py), 1)

    def desenhar(self):
        """Preenche o fundo, move e desenha estrelas e galáxias."""
        self.tela.fill(PRETO)
        
        # Desenha e move as estrelas
        for e in self.estrelas:
            e[1] += e[2]
            if e[1] > self.altura:
                e[1] = 0
                e[0] = random.randint(0, self.largura)

            brilho = 120 + e[2] * 20
            pygame.draw.circle(self.tela, (brilho, brilho, brilho), (e[0], e[1]), 1)

        # Desenha as galáxias
        for g in self.galaxias:
            self.desenhar_galaxia(g["x"], g["y"], g["r"])