import pygame
from personagem import Personagem 
from colecionaveis import Colecionavel 
import random
pygame.init()

# cores (pelo sistema RGB)
branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255) 
amarelo = (255, 255, 0) 
roxo = (128, 0, 128) 
rosa = (255, 0, 220)

# dimensões da Tela
largura_tela = 800
altura_tela = 600
tam_quadrado = 20

# configuração da tela
tela = pygame.display.set_mode([largura_tela, altura_tela])
pygame.display.set_caption("Jogo de Coleta")

# criação dos objetos 

# grupo de sprites para desenhar e atualizar todos os objetos
todos_sprites = pygame.sprite.Group()

# grupo específico para os colecionáveis para verificar colisões
colecionaveis = pygame.sprite.Group()

# 1) cria o personagem
jogador = Personagem(
    largura_tela // 2, 
    altura_tela // 2, 
    branco, 
    tam_quadrado
)
todos_sprites.add(jogador)

# 2) cria os colecionáveis
cores_colecionaveis = [azul, amarelo, roxo, rosa, vermelho, verde]
num_por_cor = 5 

for cor in cores_colecionaveis:
    for _ in range(num_por_cor):
        coleta = Colecionavel(largura_tela, altura_tela, cor, tam_quadrado)
        colecionaveis.add(coleta)
        todos_sprites.add(coleta)

# variáveis
rodando = True
relogio = pygame.time.Clock()
pontuacao = 0

# loop principal do jogo
while rodando:
    # 1) processamento das entradas (eventos)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # 2) lógica do ogo 
    # pega o estado de todas as teclas pressionadas (as setas para os lados e cima/baixo) 
    teclas = pygame.key.get_pressed()
    
    # atualiza o jogador (movimento e restrição de tela)
    jogador.update(teclas, largura_tela, altura_tela)

    # verifica colisões: checa se o 'jogador' colidiu com algum sprite no grupo 'colecionaveis'.
    # O 'True, True' significa que o sprite do jogador E os colecionáveis colididos são REMOVIDOS
    coletas_encontradas = pygame.sprite.spritecollide(jogador, colecionaveis, True)

    qtd_vermelho = qtd_azul = qtd_verde = qtd_amarelo = qtd_roxo = qtd_rosa = 0
    # processa as coletas
    for coleta in coletas_encontradas:
        if coleta.cor == vermelho:
            pontuacao -= 5 
            qtd_vermelho += 1
        elif coleta.cor == verde:
            pontuacao += 15  
            qtd_verde += 1   
        elif coleta.cor == azul:
            pontuacao -= 20  
            qtd_azul += 1
        elif coleta.cor == amarelo:
            pontuacao -= 25  
            qtd_amarelo += 1
        elif coleta.cor == roxo:
            pontuacao += 30 
            qtd_roxo += 1 
        elif coleta.cor == rosa:
            pontuacao += 50  
            qtd_rosa += 1
                
        # adiciona pontos por coletar
        print(f"Coletado! Pontuação: {pontuacao}")
        # remove o colecionável dos grupos
        colecionaveis.remove(coleta)
        todos_sprites.remove(coleta)
        
        # sempre adiciona colecionáveis novos
        nova_cor = random.choice(cores_colecionaveis)
        nova_coleta = Colecionavel(largura_tela, altura_tela, nova_cor, tam_quadrado)
        colecionaveis.add(nova_coleta)
        todos_sprites.add(nova_coleta)
        
        # fim de jogo 
        if pontuacao <= 0:
            break
            texto = fonte.render("Fim de Jogo! Pontuação Negativa.", True, branco)
            tela.blit(texto, (largura_tela // 2 - 150, altura_tela // 2))
            pygame.display.flip()
            pygame.time.delay(3000)
            rodando = False
                   
        
    # 3) desenho na Tela
    # fundo preto
    tela.fill(preto)

    # desenha todos os sprites nos seus grupos
    todos_sprites.draw(tela)
    
    # pontuação
    fonte = pygame.font.Font(None, 36)
    texto = fonte.render(f"Pontos: {pontuacao}", True, branco)
    

    tela.blit(texto, (10, 10))

    pygame.display.flip()

    # frames por segundo
    relogio.tick(60)

pygame.quit()