
import pygame
import random
from datetime import datetime
from recursos.basicos.extras import desenhar_sol

def mover_nuvem(nuvem_rect):
    nuvem_rect.x += 1
    if nuvem_rect.x > 1000:
        nuvem_rect.x = -150
    return nuvem_rect

pygame.init()
pygame.mixer.init()

LARGURA = 1000
ALTURA = 700
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jardim Secreto")
RELOGIO = pygame.time.Clock()
fonte = pygame.font.SysFont("arial", 30)

som_flor = pygame.mixer.Sound("recursos/assets/som_flor.wav")
som_gameover = pygame.mixer.Sound("recursos/assets/som_gameover.wav")

def tela_inicial():
    pygame.mixer.music.load("recursos/assets/musica_inicio.mp3")
    pygame.mixer.music.play(-1)

    tela_inicio = pygame.image.load("recursos/assets/tela_inicial.png")
    tela_inicio = pygame.transform.scale(tela_inicio, (LARGURA, ALTURA))

    fonte_menor = pygame.font.SysFont("arial", 28)
    nome = ""
    input_ativo = True

    caixa_nome = pygame.Rect(350, 330, 300, 40)
    botao_rect = pygame.Rect(390, 560, 220, 60)

    while True:
        TELA.blit(tela_inicio, (0, 0))
        pygame.draw.rect(TELA, (255, 255, 255), caixa_nome)
        pygame.draw.rect(TELA, (0, 0, 0), caixa_nome, 2)

        texto_nome = fonte_menor.render(nome, True, (0, 0, 0))
        TELA.blit(texto_nome, (caixa_nome.x + 10, caixa_nome.y + 5))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.KEYDOWN and input_ativo:
                if evento.key == pygame.K_RETURN and nome.strip() != "":
                    pygame.mixer.music.stop()
                    return nome
                elif evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                elif len(nome) < 15:
                    nome += evento.unicode

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(evento.pos) and nome.strip() != "":
                    pygame.mixer.music.stop()
                    return nome

nome = tela_inicial()
pygame.mixer.music.load("recursos/assets/musica_jogo.mp3")
pygame.mixer.music.play(-1)
fundo = pygame.image.load("recursos/assets/fundo.png")
coelho = pygame.image.load("recursos/assets/coelho.png")
coelho = pygame.transform.scale(coelho, (120, 120))

flor = pygame.image.load("recursos/assets/flor.png")
flor = pygame.transform.scale(flor, (80, 80))

minhoca = pygame.image.load("recursos/assets/minhoca.png")
minhoca = pygame.transform.scale(minhoca, (80, 80))

tela_final = pygame.image.load("recursos/assets/final.png")
tela_final = pygame.transform.scale(tela_final, (1000, 700))

nuvem = pygame.image.load("recursos/assets/nuvem.png")
nuvem = pygame.transform.scale(nuvem, (150, 90))
nuvem_rect = nuvem.get_rect(topleft=(-100, 50))
coelho_rect = coelho.get_rect()
coelho_rect.midbottom = (LARGURA // 2, ALTURA - 50)

itens = []
tempo_spawn = 0
intervalo_spawn = 90
pontos = 0
vel = 8
pausado = False

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                pausado = not pausado

    nuvem_rect = mover_nuvem(nuvem_rect)

    if pausado:
        TELA.blit(fundo, (0, 0))
        TELA.blit(nuvem, nuvem_rect)
        desenhar_sol(TELA)
        TELA.blit(coelho, coelho_rect)

        for item in itens:
            if item["tipo"] == "flor":
                TELA.blit(flor, item["rect"])
            elif item["tipo"] == "minhoca":
                TELA.blit(minhoca, item["rect"])

        texto_pontos = fonte.render(f"Pontos: {pontos}", True, (0, 0, 0))
        TELA.blit(texto_pontos, (10, 10))

        pause_box = pygame.Rect(LARGURA//2 - 320, ALTURA//2 - 60, 640, 120)
        pygame.draw.rect(TELA, (240, 255, 240), pause_box, border_radius=15)
        pygame.draw.rect(TELA, (30, 100, 70), pause_box, 4, border_radius=15)
        fonte_pause = pygame.font.SysFont("arial", 30, bold=True)
        texto = "JOGO PAUSADO. APERTE ESPAÇO PARA CONTINUAR"
        texto_pausa = fonte_pause.render(texto, True, (0, 0, 0))
        texto_x = pause_box.centerx - texto_pausa.get_width() // 2
        texto_y = pause_box.centery - texto_pausa.get_height() // 2
        TELA.blit(texto_pausa, (texto_x, texto_y))
        pygame.display.update()
        continue

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and coelho_rect.left > 0:
        coelho_rect.x -= vel
    if teclas[pygame.K_RIGHT] and coelho_rect.right < LARGURA:
        coelho_rect.x += vel

    tempo_spawn += 1
    if tempo_spawn >= intervalo_spawn:
        tipo = random.choice(["flor", "minhoca"])
        x = random.randint(50, LARGURA - 50)
        y = ALTURA - 80
        rect = flor.get_rect(midbottom=(x, y))
        tempo_criacao = pygame.time.get_ticks()
        itens.append({"tipo": tipo, "rect": rect, "tempo": tempo_criacao, "tipo_sprite": tipo})
        tempo_spawn = 0

    tempo_atual = pygame.time.get_ticks()
    novos_itens = []
    for item in itens:
        if tempo_atual - item["tempo"] > 3000:
            continue

        item_rect = item["rect"]
        if item["tipo_sprite"] == "minhoca":
            item_rect = item["rect"].inflate(-20, -20)

        if coelho_rect.colliderect(item_rect):
            if item["tipo_sprite"] == "flor":
                pontos += 1
                som_flor.play()
            elif item["tipo_sprite"] == "minhoca":
                som_gameover.play()

                agora = datetime.now()
                data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")
                with open("log.dat", "a", encoding="utf-8") as arquivo:
                    linha = f"{nome} - {pontos} pontos - {data_hora}\n"
                    arquivo.write(linha)

                try:
                    with open("log.dat", "r", encoding="utf-8") as arquivo:
                        todas = arquivo.readlines()
                        ultimas = todas[-5:]
                except FileNotFoundError:
                    ultimas = []

                botao_tentar = pygame.Rect(300, 500, 400, 50)
                botao_sair = pygame.Rect(300, 570, 400, 50)

                while True:
                    TELA.blit(tela_final, (0, 0))

                    fonte_final = pygame.font.SysFont("arial", 26, bold=True)
                    y_texto = 220
                    for linha in ultimas:
                        texto = fonte_final.render(linha.strip(), True, (255, 255, 255))
                        TELA.blit(texto, (LARGURA//2 - texto.get_width()//2, y_texto))
                        y_texto += 30

                    pygame.display.update()

                    for evento in pygame.event.get():
                        if evento.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if evento.type == pygame.MOUSEBUTTONDOWN:
                            if botao_tentar.collidepoint(evento.pos):
                                from subprocess import call
                                pygame.quit()
                                call(["python", "main.py"])
                                exit()
                            elif botao_sair.collidepoint(evento.pos):
                                pygame.quit()
                                exit()
        else:
            novos_itens.append(item)
    itens = novos_itens
    TELA.blit(fundo, (0, 0))
    TELA.blit(nuvem, nuvem_rect)
    desenhar_sol(TELA)
    TELA.blit(coelho, coelho_rect)

    for item in itens:
        if item["tipo_sprite"] == "flor":
            TELA.blit(flor, item["rect"])
        elif item["tipo_sprite"] == "minhoca":
            TELA.blit(minhoca, item["rect"])

    texto_pontos = fonte.render(f"Pontos: {pontos}", True, (0, 0, 0))
    TELA.blit(texto_pontos, (10, 10))

    pygame.display.update()
    RELOGIO.tick(60)

pygame.quit()
