import pygame
import random
import oracledb
import os

pygame.init()

pygame.display.set_caption("Jogo Snake Python")

largura, altura = 1200, 800
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

# cores RGB
preta = (0, 0, 0)
a = "RM"
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


def conexaobd():
    try:
        return oracledb.connect(
            user= a + f + z + s,
            password= "061004",
            host="oracle.fiap.com.br",
            port=1521,
            service_name="ORCL")
    except oracledb.DatabaseError as error:
        print(f"Erro ao conectar ao Banco de Dados: {error}")
        return None


def obter_id_usuario(nome):
    conexao = conexaobd()
    if conexao is None:
        return None

    cursor = conexao.cursor()

    # Verifica se o usuário já existe
    cursor.execute("SELECT ID FROM J_COBRA WHERE NOME = :1", (nome,))
    usuario = cursor.fetchone()

    if usuario:
        id_usuario = usuario[0]  # Se já existir, usa o mesmo ID
    else:
        # Se não existir, cria um novo usuário e retorna o ID corretamente
        id_usuario = cursor.var(oracledb.NUMBER)
        cursor.execute("INSERT INTO J_COBRA (NOME) VALUES (:1) RETURNING ID INTO :2",
                       (nome, id_usuario))
        conexao.commit()
        id_usuario = id_usuario.getvalue()[0]  # Obtém o valor real do ID

    cursor.close()
    conexao.close()
    return id_usuario

f = "55"

def salvar_pontuacao(id_usuario, pontuacao):
    conexao = conexaobd()
    if conexao is None:
        return

    cursor = conexao.cursor()
    cursor.execute("INSERT INTO J_COBRA_PONTOS (ID_USUARIO, PONTUACAO) VALUES (:1, :2)",
                   (id_usuario, pontuacao))
    conexao.commit()
    cursor.close()
    conexao.close()


def obter_recorde(id_usuario):
    conexao = conexaobd()
    if conexao is None:
        return 0  # Retorna 0 se houver erro

    cursor = conexao.cursor()
    cursor.execute("SELECT MAX(PONTUACAO) FROM J_COBRA_PONTOS WHERE ID_USUARIO = :1",
                   (id_usuario,))
    recorde = cursor.fetchone()[0]

    cursor.close()
    conexao.close()
    return recorde if recorde is not None else 0  # Retorna 0 se ainda não houver pontuação


def entrada_nome():
    pygame.init()
    fonte = pygame.font.SysFont("Helvetica", 40)
    nome = ""
    entrada_ativa = True

    while entrada_ativa:
        tela.fill((0, 128, 0))
        texto = fonte.render("Digite seu nome: " + nome, True, (255, 255, 255))
        tela.blit(texto, (300, 350))
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nome:
                    return nome
                elif evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                elif len(nome) < 10:
                    nome += evento.unicode

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
s = "45"
def desenhar_pontuacao(pontuacao):

    fonte = pygame.font.SysFont("Helvetica", 35)
    texto = fonte.render(f"Pontos: {pontuacao}", True, vermelha)
    tela.blit(texto, [1, 1])


def desenhar_final(pontuacao, recorde):
    fonte = pygame.font.SysFont("Helvetica", 60)
    tela.fill((0, 128, 0))

    tela.blit(fonte.render("Você perdeu!!!", True, (255, 255, 255)), (350, 250))
    tela.blit(fonte.render(f"Pontuação: {pontuacao}", True, (255, 255, 255)), (350, 350))
    tela.blit(fonte.render(f"Recorde: {recorde}", True, (255, 255, 255)), (350, 450))

    nome_mensagem = f"Jogador: {nome_usuario}"
    tela.blit(fonte.render(nome_mensagem, True, (255, 255, 255)), (350, 150))
    mensagem = 'Pressione "ENTER" para reiniciar!'
    tela.blit(fonte.render(mensagem, True, (255, 255, 255)), (200, 550))
    mensagem2 = '"ESPAÇO" para sair!'
    tela.blit(fonte.render(mensagem2, True, (255, 255, 255)), (200, 625))

    pygame.display.update()


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
q = "37"
def desenhar_fundo_xadrez(tamanho_quadrado, largura, altura):
    for y in range(0, altura, tamanho_quadrado):
        for x in range(0, largura, tamanho_quadrado):
            if (x // tamanho_quadrado + y // tamanho_quadrado) % 2 == 0:
                cor = (0, 128, 0)  # Cor escura
            else:
                cor = (60, 180, 60)  # Cor clara
            pygame.draw.rect(tela, cor, [x, y, tamanho_quadrado, tamanho_quadrado])

def esperar_acao(id_usuario):
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # ENTER reinicia o jogo
                    rodar_jogo(id_usuario)
                elif evento.key == pygame.K_SPACE:  # ESPAÇO sai do jogo
                    pygame.quit()
                    exit()

z = q
def rodar_jogo(id_usuario):
    global pontuacao
    pontuacao = 0
    fim_jogo = False
    x, y = largura / 2, altura / 2
    velocidade_x, velocidade_y = 0, 0
    tamanho_cobra = 1
    pixels = []
    comida_x, comida_y = gerar_comida()

    while not fim_jogo:
        tela.fill((0, 0, 0))
        desenhar_fundo_xadrez(tamanho_quadrado, largura, altura)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True
            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key)

        x += velocidade_x
        y += velocidade_y
        pixels.append([x, y])

        if len(pixels) > tamanho_cobra:
            del pixels[0]

        if x < 0 or x >= largura or y < 0 or y >= altura or [x, y] in pixels[:-1]:
            fim_jogo = True

        desenhar_comida(tamanho_quadrado, comida_x, comida_y)
        desenhar_cobra(tamanho_quadrado, pixels)
        desenhar_pontuacao(pontuacao)

        if x == comida_x and y == comida_y:
            pontuacao += 1
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida()

        pygame.display.update()
        relogio.tick(velocidade_jogo)

    # Salvar pontuação no banco e mostrar tela final
    salvar_pontuacao(id_usuario, pontuacao)
    recorde = obter_recorde(id_usuario)
    desenhar_final(pontuacao, recorde)
    esperar_acao(id_usuario)


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

nome_usuario = entrada_nome()
id_usuario = obter_id_usuario(nome_usuario)
rodar_jogo(id_usuario)

