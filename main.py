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
# NOTA: Assumimos que a classe Personagem foi ajustada para aceitar (x, y, cor, tamanho)
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
fonte = pygame.font.Font(None, 36) # Inicializa a fonte

# -------------------------------------------------------------
# NOVO: Dicionário para armazenar a contagem de cada cor (PERSISTENTE)
# -------------------------------------------------------------
contadores_cores = {
    vermelho: 0,
    verde: 0,
    azul: 0,
    amarelo: 0,
    roxo: 0,
    rosa: 0,
}

# NOVO: Mapeamento de RGB para nomes legíveis
nomes_cores = {
    vermelho: "Vermelho",
    verde: "Verde",
    azul: "Azul",
    amarelo: "Amarelo",
    roxo: "Roxo",
    rosa: "Rosa",
}

# loop principal do jogo
while rodando:
    # 1) processamento das entradas (eventos)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # 2) lógica do jogo 
    # pega o estado de todas as teclas pressionadas (as setas para os lados e cima/baixo) 
    teclas = pygame.key.get_pressed()
    
    # atualiza o jogador (movimento e restrição de tela)
    jogador.update(teclas, largura_tela, altura_tela)

    # verifica colisões: checa se o 'jogador' colidiu com algum sprite no grupo 'colecionaveis'.
    # 'True, True' significa que o sprite do jogador E os colecionáveis colididos são REMOVIDOS
    coletas_encontradas = pygame.sprite.spritecollide(jogador, colecionaveis, True)

    # processa as coletas
    for coleta in coletas_encontradas:
        
        # atualiza o contador no dicionário
        if coleta.cor in contadores_cores:
            contadores_cores[coleta.cor] += 1

        # lógica de pontuação e incremento
        if coleta.cor == vermelho:
            pontuacao -= 5 
        elif coleta.cor == verde:
            pontuacao += 5 
        elif coleta.cor == azul:
            pontuacao -= 5 
        elif coleta.cor == amarelo:
            pontuacao -= 5 
        elif coleta.cor == roxo:
            pontuacao += 5 
        elif coleta.cor == rosa:
            pontuacao += 5 
        
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
        if pontuacao <= 0 or pontuacao >= 150:           
            rodando = False 
            break
            
            
    # 3) desenho na tela
    # fundo preto
    tela.fill(preto)

    # desenha todos os sprites nos seus grupos
    todos_sprites.draw(tela)
    
    # pontuação total
    texto_pontos = fonte.render(f"Pontos: {pontuacao}", True, branco)
    tela.blit(texto_pontos, (10, 10))

    posicao_y = 50 

    for cor_rgb, contagem in contadores_cores.items():
        if contagem > 0: # só mostra a quantidade daquela cor se for maior que zero
            
            # obtém o nome legível da cor no dicionário
            nome_cor = nomes_cores.get(cor_rgb, "Desconhecida") 
            
            texto_contagem = f"{nome_cor}: {contagem}"
            
            # coloca o texto, usando a própria cor do colecionável para destaque
            texto_renderizado = fonte.render(texto_contagem, True, cor_rgb)
            
            tela.blit(texto_renderizado, (10, posicao_y))
            
            # próxima linha
            posicao_y += 30 

    pygame.display.flip()

    # frames por segundo
    relogio.tick(60)

# tela de fim de jogo
if not rodando and (pontuacao <= 0 or pontuacao >= 150):
    # se o loop terminou por causa do 'pontuacao <= 0' ou 'pontuacao >=150' (fim de jogo)
    tela.fill(preto)
    if pontuacao < 0:
        texto_fim = fonte.render("Fim de Jogo! Pontuação Negativa.", True, branco)
        tela.blit(texto_fim, (largura_tela // 2 - texto_fim.get_width() // 2, altura_tela // 2))
    elif pontuacao == 0:
        texto_fim = fonte.render("Fim de Jogo! Você zerou a pontuação!", True, branco)
        tela.blit(texto_fim, (largura_tela // 2 - texto_fim.get_width() // 2, altura_tela // 2))    
    elif pontuacao >= 150:
        texto_fim = fonte.render("Parabéns! Você alcançou 150 pontos!", True, branco)
        tela.blit(texto_fim, (largura_tela // 2 - texto_fim.get_width() // 2, altura_tela // 2))
        
    texto_final_pontos = fonte.render(f"Pontuação Final: {pontuacao}", True, branco)
    tela.blit(texto_final_pontos, (largura_tela // 2 - texto_final_pontos.get_width() // 2, altura_tela // 2 + 50))
    
    pygame.display.flip()
    pygame.time.delay(3000) 

# fim do Jogo
pygame.quit()
