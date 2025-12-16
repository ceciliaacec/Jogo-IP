import pygame
import random
import sys
# Importa apenas constantes
from cores import LARGURA, ALTURA, AZUL, VERMELHO, ROXO, AMBAR, fonte, fonte_grande
# Importa as classes
from fundo import Fundo
from nave import Nave, Tiro  
from colecionavel import Asteroide, Alien, Coracao 

class Jogo:
    """Gerencia o estado e o loop principal do jogo."""
    
    def __init__(self, tela):
        self.tela = tela
        self.largura = LARGURA
        self.altura = ALTURA
        self.game_over = False

        # Passa 'self.tela' ao inicializar outras classes
        self.fundo = Fundo(self.tela)
        self.nave = Nave(self.largura // 2 - 20, self.altura - 80, self.tela) 

        # Listas de objetos (usando Group para ObjetoMovel)
        self.tiros = []
        self.asteroides = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.coracoes = pygame.sprite.Group()

        # Placar
        self.aliens_coletados = 0
        self.asteroides_destruidos = 0
        
        self.clock = pygame.time.Clock()
        self.FPS = 60
        

    def processar_entradas(self):
        """Trata eventos do usuário (sair, atirar)."""
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            if not self.game_over:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    self.nave.atirar(self.tiros)
        return True

    def gerar_objetos(self):
        """Gera asteroides, aliens e corações com probabilidades variadas."""
        
        # Passa 'self.tela' ao criar novos objetos
        if random.randint(1, 35) == 1:
            self.asteroides.add(Asteroide(self.largura, self.altura, self.tela))
        if random.randint(1, 120) == 1:
            self.aliens.add(Alien(self.largura, self.altura, self.tela))
        if random.randint(1, 220) == 1:
            self.coracoes.add(Coracao(self.largura, self.altura, self.tela))

    def atualizar_objetos(self):
        """Move todos os objetos e remove os que saem da tela."""
        
        for t in self.tiros[:]:
            t.mover()
            if t.fora_da_tela():
                self.tiros.remove(t)

        self.asteroides.update()
        self.aliens.update()
        self.coracoes.update()
        
        for grupo in [self.asteroides, self.aliens, self.coracoes]:
             for o in list(grupo): 
                if o.fora_da_tela():
                    o.kill() 

    def verificar_colisoes(self):
        """Verifica e processa todas as colisões do jogo."""
        self.nave.atualizar_invencibilidade()

        # Colisão Nave <-> Asteroide
        colisoes_asteroide = pygame.sprite.spritecollide(self.nave, self.asteroides, True) 
        for _ in colisoes_asteroide:
            if self.nave.levar_dano(20):
                if self.nave.vida <= 0:
                    self.game_over = True
        
        # Colisão Nave <-> Alien (coleta)
        colisoes_alien = pygame.sprite.spritecollide(self.nave, self.aliens, True) 
        self.aliens_coletados += len(colisoes_alien)

        # Colisão Nave <-> Coração (cura)
        colisoes_coracao = pygame.sprite.spritecollide(self.nave, self.coracoes, True) 
        for _ in colisoes_coracao:
            self.nave.curar(20)

        # Colisão Tiro <-> Asteroide
        tiros_a_remover = set()
        for t in self.tiros:
            asteroides_atingidos = pygame.sprite.spritecollide(t.rect, self.asteroides, False)
            for asteroide in asteroides_atingidos:
                asteroide.vida -= 1
                if asteroide.vida <= 0:
                    asteroide.kill() 
                    self.asteroides_destruidos += 1
                tiros_a_remover.add(t)
                break 

        self.tiros = [t for t in self.tiros if t not in tiros_a_remover]

    def desenhar_hud(self):
        """Desenha o placar e a vida do jogador. Usa self.tela."""
        
        # Retângulo do placar
        pygame.draw.rect(self.tela, (20, 30, 60), (10, 10, 280, 90), border_radius=12)
        pygame.draw.rect(self.tela, AZUL, (10, 10, 280, 90), 2, border_radius=12)

        self.tela.blit(fonte.render("Sistema da Nave", True, AZUL), (20, 16))

        # Barra de Vida
        self.tela.blit(fonte.render("Vida", True, VERMELHO), (20, 42))
        pygame.draw.rect(self.tela, VERMELHO, (80, 44, self.nave.vida * 2, 12))
        pygame.draw.rect(self.tela, AZUL, (80, 44, 200, 12), 2)

        # Contadores de itens/destruídos
        self.tela.blit(fonte.render(f"👽 {self.aliens_coletados}", True, ROXO), (20, 65))
        self.tela.blit(fonte.render(f"☄️ {self.asteroides_destruidos}", True, AMBAR), (120, 65))
        
        if self.game_over:
            txt = fonte_grande.render("GAME OVER", True, VERMELHO)
            self.tela.blit(txt, (self.largura // 2 - txt.get_width() // 2, self.altura // 2 - 20))

    def desenhar(self):
        """Desenha todos os elementos do jogo na tela."""
        self.fundo.desenhar()

        self.nave.desenhar()
        for t in self.tiros:
            t.desenhar()

        for a in self.asteroides:
            a.desenhar()
        for al in self.aliens:
            al.desenhar()
        for c in self.coracoes:
            c.desenhar()

        self.desenhar_hud()

        pygame.display.flip()

    def loop_principal(self):
        """Loop principal do jogo."""
        rodando = True
        while rodando:
            self.clock.tick(self.FPS)

            rodando = self.processar_entradas()
            
            if not rodando:
                break

            if not self.game_over:
                teclas = pygame.key.get_pressed()
                self.nave.mover(teclas) 
                
                self.gerar_objetos()
                self.atualizar_objetos()
                self.verificar_colisoes()

            self.desenhar()