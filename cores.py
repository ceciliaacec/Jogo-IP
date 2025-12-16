import pygame

# 🚨 Nota: Inicialização do Pygame aqui é para garantir que as fontes funcionem.
pygame.init()

# Configurações da Tela
LARGURA, ALTURA = 900, 600

# Cores Principais
PRETO = (3, 3, 10)
BRANCO = (230, 230, 240)
AZUL = (80, 140, 255)
VERMELHO = (220, 60, 60)
AMBAR = (255, 190, 100)
ROXO = (170, 90, 220)
CINZA = (140, 150, 170)
MARROM = (110, 90, 70)

# Fontes
fonte = pygame.font.SysFont("consolas", 20)
fonte_grande = pygame.font.SysFont("consolas", 42, bold=True)