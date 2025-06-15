import pygame
import math

# Variáveis do sol pulsante
angulo = 0

def desenhar_sol(tela):
    global angulo
    raio_base = 40
    raio = raio_base + int(math.sin(angulo) * 10)
    angulo += 0.05

    pygame.draw.circle(tela, (255, 255, 0), (80, 80), raio)