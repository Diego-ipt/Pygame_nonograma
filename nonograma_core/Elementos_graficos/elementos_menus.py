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

def mostrar_fotogramas(fotogramas, indice_fotograma, x, y, pantalla):
    if len(fotogramas) > 0:
        pantalla.blit(fotogramas[indice_fotograma], (x, y))
        indice_fotograma = (indice_fotograma + 1) % len(fotogramas)
        return indice_fotograma
    else:
        print("Error: No se han cargado los fotogramas")
        return indice_fotograma

# Función para mostrar texto en la pantalla
def mostrar_texto(texto, fuente, color, pantalla, x, y):
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect(center=(x, y))
    pantalla.blit(superficie_texto, rect_texto)

# Variable global para controlar el estado del clic
accion_ejecutada = False

# Función para los botones
def boton(texto, x, y, ancho, alto, color_base, color_presionado, pantalla, accion=None, color_text=NEGRO):
    global accion_ejecutada
    raton = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

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

    mostrar_texto(texto, fuente, color_text, pantalla, x + (ancho // 2), y + (alto // 2))

# Función para dibujar una cuadrícula menu
def dibujar_grid(pantalla, filas, columnas, tamano_celda, color_activo, color_inactivo, grid_estado):
    for fila in range(filas):
        for columna in range(columnas):
            x = columna * tamano_celda
            y = fila * tamano_celda
            color = color_activo if grid_estado[fila][columna] else color_inactivo
            pygame.draw.rect(pantalla, color, (x, y, tamano_celda, tamano_celda))

def actualizar_grid(grid_estado, probabilidad_cambio=0.1):
    for fila in range(len(grid_estado)):
        for columna in range(len(grid_estado[0])):
            if random.random() < probabilidad_cambio:
                grid_estado[fila][columna] = not grid_estado[fila][columna]

