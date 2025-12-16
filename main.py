import pygame
import sys
from jogo import Jogo
from cores import LARGURA, ALTURA

# 1. Configuração do Pygame e Criação da TELA
pygame.init() 
TELA = pygame.display.set_mode((LARGURA, ALTURA)) 
pygame.display.set_caption("Em Uma Galáxia Muito Distante (POO Modular)")

if __name__ == '__main__':
    try:
        # 2. Inicializa Jogo, passando o objeto TELA
        jogo = Jogo(TELA) 
        jogo.loop_principal()
    except Exception as e:
        print(f"Ocorreu um erro fatal: {e}")
    finally:
        pygame.quit()
        sys.exit()