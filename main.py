import pygame
import random

pygame.init()

pygame.display.set_caption("Jogo Snake Python")

largura, altura = 1200, 800
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

# cores RGB
preta = (0, 0, 0)
branca = (255, 255, 255)
vermelha = (255, 0, 0)
verde = (0, 255, 0)
salmao = (250, 128, 114)
marrom = (139, 69, 19)

# parametros da cobrinha
tamanho_quadrado = 40
velocidade_jogo = 10
topo_altura = 5
largura_topo = 5
raio_v = 30
raio_m = 15
pontuacao = 0

def gerar_comida():
    comida_x = round(random.randrange(0, largura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
    comida_y = round(random.randrange(0, altura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
    return comida_x, comida_y

def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, verde, [comida_x + (tamanho - largura_topo) // 2, comida_y, largura_topo, topo_altura], border_radius=raio_v)
    pygame.draw.rect(tela, vermelha, [comida_x, comida_y + topo_altura, tamanho, tamanho - topo_altura], border_radius=raio_m)

def desenhar_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, salmao, [pixel[0], pixel[1], tamanho, tamanho])

def desenhar_pontuacao(pontuacao):

    fonte = pygame.font.SysFont("Helvetica", 35)
    texto = fonte.render(f"Pontos: {pontuacao}", True, vermelha)
    tela.blit(texto, [1, 1])

def desenhar_final(pontuacao):
    fonte = pygame.font.SysFont("Helvetica", 60)
    texto = fonte.render(f"Você perdeu!!! Sua pontuação foi {pontuacao}!", True, branca)
    tela.blit(texto, [200, 400])
    texto = fonte.render(f"'ENTER' para sair!", True, branca)
    tela.blit(texto, [350, 500])

def selecionar_velocidade(tecla):
    if tecla == pygame.K_DOWN:
        velocidade_x = 0
        velocidade_y = tamanho_quadrado
    elif tecla == pygame.K_UP:
        velocidade_x = 0
        velocidade_y = -tamanho_quadrado
    elif tecla == pygame.K_RIGHT:
        velocidade_x = tamanho_quadrado
        velocidade_y = 0
    elif tecla == pygame.K_LEFT:
        velocidade_x = -tamanho_quadrado
        velocidade_y = 0
    return velocidade_x, velocidade_y

def desenhar_fundo_xadrez(tamanho_quadrado, largura, altura):
    for y in range(0, altura, tamanho_quadrado):
        for x in range(0, largura, tamanho_quadrado):
            if (x // tamanho_quadrado + y // tamanho_quadrado) % 2 == 0:
                cor = (0, 128, 0)  # Cor escura
            else:
                cor = (60, 180, 60)  # Cor clara
            pygame.draw.rect(tela, cor, [x, y, tamanho_quadrado, tamanho_quadrado])

def rodar_jogo():
    global pontuacao  # Certifique-se de usar a variável global de pontuação
    fim_jogo = False
    x = largura / 2
    y = altura / 2
    velocidade_x = 0
    velocidade_y = 0

    tamanho_cobra = 1
    pixels = []

    comida_x, comida_y = gerar_comida()

    while not fim_jogo:
        tela.fill(preta)
        desenhar_fundo_xadrez(tamanho_quadrado, largura, altura)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True
            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key)

        desenhar_comida(tamanho_quadrado, comida_x, comida_y)

        if x < 0 or x >= largura or y < 0 or y >= altura:
            fim_jogo = True
            desenhar_final(pontuacao)

        x += velocidade_x
        y += velocidade_y

        pixels.append([x, y])

        if len(pixels) > tamanho_cobra:
            del pixels[0]

        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                fim_jogo = True
                desenhar_final(pontuacao)

        desenhar_cobra(tamanho_quadrado, pixels)
        desenhar_pontuacao(pontuacao)  # Usar a pontuação correta

        pygame.display.update()

        # Verifica se a cobra comeu a comida
        if x == comida_x and y == comida_y:
            pontuacao += 1  # Incrementa a pontuação
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida()

        relogio.tick(velocidade_jogo)

    # Espera até que o jogador pressione Enter para fechar o jogo
    esperar_enter()

def esperar_enter():
    # Espera até que o usuário pressione a tecla Enter
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Enter
                    pygame.quit()
                    exit()

rodar_jogo()
