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

# Función para dibujar una cuadrícula menu
def dibujar_grid(pantalla, filas, columnas, tamano_celda, color_activo, color_inactivo, grid_estado):
    for fila in range(filas):
        for columna in range(columnas):
            x = columna * tamano_celda
            y = fila * tamano_celda
            celda_surface = pygame.Surface((tamano_celda, tamano_celda), pygame.SRCALPHA)
            # Definir el color con transparencia (valor alfa entre 0 y 255)
            color = (*color_activo[:3], random.randrange(25, 50)) if grid_estado[fila][columna] else (*color_inactivo[:3], 255)
            # Rellenar la superficie con el color y la transparencia
            celda_surface.fill(color)
            # Dibujar la celda en la pantalla
            pantalla.blit(celda_surface, (x, y))

def actualizar_grid(grid_estado, probabilidad_cambio=0.1):
    for fila in range(len(grid_estado)):
        for columna in range(len(grid_estado[0])):
            if random.random() < probabilidad_cambio:
                grid_estado[fila][columna] = not grid_estado[fila][columna]

def mostrar_lista_nombres(pantalla, nombres, x, y, ancho, alto, color_base, color_presionado, color_texto, fuente, accion=None):
    """
    Muestra una lista de nombres seleccionables en la pantalla.

    :param pantalla: Superficie de Pygame donde se dibujará la lista.
    :param nombres: Lista de nombres a mostrar.
    :param x: Coordenada x de la esquina superior izquierda de la lista.
    :param y: Coordenada y de la esquina superior izquierda de la lista.
    :param ancho: Ancho de cada elemento de la lista.
    :param alto: Alto de cada elemento de la lista.
    :param color_base: Color base de los elementos.
    :param color_presionado: Color de los elementos cuando se presionan.
    :param color_texto: Color del texto.
    :param fuente: Fuente del texto.
    :param accion: Función a ejecutar cuando se selecciona un nombre.
    :return: El nombre seleccionado o None si no se seleccionó ninguno.
    """
    raton = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    for i, nombre in enumerate(nombres):
        item_y = y + i * alto
        if x + ancho > raton[0] > x and item_y + alto > raton[1] > item_y:
            pygame.draw.rect(pantalla, color_presionado, (x, item_y, ancho, alto))
            if click[0] == 1:
                if accion is not None:
                    accion(nombre)
                return nombre
        else:
            pygame.draw.rect(pantalla, color_base, (x, item_y, ancho, alto))

        mostrar_texto(nombre, fuente, color_texto, pantalla, x + (ancho // 2), item_y + (alto // 2))
    
    return None
