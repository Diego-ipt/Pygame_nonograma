import pygame
import time
import random
from nonograma_core.Elementos_graficos.colores import *
from nonograma_core.Elementos_graficos.AssetManager import AssetManager

# Inicializar Pygame
pygame.init()

# Cargador de recursos
asset_manager = AssetManager()

# Tamaño de la pantalla
ancho_pantalla = 800
alto_pantalla = 650
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))

# Definir fuente de texto
fuente = pygame.font.SysFont(None, 40)

# Icono
icono = asset_manager.cargar_imagen("Iconojuego.jpg")
pygame.display.set_caption("Nonograma_Game")
pygame.display.set_icon(icono)

# Función para mostrar texto en la pantalla
def mostrar_texto(texto, fuente, color, pantalla, x, y):
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect(center=(x, y))
    pantalla.blit(superficie_texto, rect_texto)

# Variable global para controlar el estado del clic
accion_ejecutada = False

# Función para los botones
def boton(texto, x, y, ancho, alto, color_base, color_presionado, pantalla, accion=None, color_text=NEGRO, font=None):
    global accion_ejecutada
    raton = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Usa la fuente predeterminada si no se pasa una
    font = font or fuente

    if x + ancho > raton[0] > x and y + alto > raton[1] > y:
        if color_presionado != NOTHING:
            pygame.draw.rect(pantalla, color_presionado, (x, y, ancho, alto))
        if click[0] == 1 and accion is not None and not accion_ejecutada:
            accion()
            accion_ejecutada = True
    else:
        if color_base != NOTHING:
            pygame.draw.rect(pantalla, color_base, (x, y, ancho, alto))

    # Resetea la acción cuando se suelta el botón del ratón
    if click[0] == 0:
        accion_ejecutada = False

    mostrar_texto(texto, font, color_text, pantalla, x + (ancho // 2), y + (alto // 2))

