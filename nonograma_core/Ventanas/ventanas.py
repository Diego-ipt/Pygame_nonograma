import sys
import pygame
from nonograma_core.Elementos_graficos.elementos_menus import *
from nonograma_core.Elementos_graficos.colores import *
from nonograma_core.Logica.tablero_nonograma import *
from nonograma_core.Logica.nonograma_numeros import *
from nonograma_core.Elementos_graficos.AssetManager import AssetManager

# Cargador de recursos
asset_manager = AssetManager()

# Cargar fotogramas
snake = asset_manager.cargar_fotogramas("serpiente")
menu = asset_manager.cargar_fotogramas("menu")
trophy = asset_manager.cargar_fotogramas("trofeo_win")
indice_fotograma_snake = 0
indice_fotograma_menu = 0
indice_fotograma_trophy = 0
reloj = pygame.time.Clock()
grid_estado = [[False for _ in range(50)] for _ in range(50)]

confirmando = False  # Controla si se muestra la ventana de confirmación

def menu_principal(cambiar_ventana):
    global indice_fotograma_menu, confirmando

    # Actualizar el estado de la cuadrícula
    actualizar_grid(grid_estado)

    # Dibuja el fondo con la cuadrícula
    pantalla.fill(BLANCO)
    dibujar_grid(pantalla, 50, 50, 16, NEGRO, BLANCO_MENU, grid_estado)

    indice_fotograma_menu = mostrar_fotogramas(menu, indice_fotograma_menu, 75, 0, pantalla)

    boton("Elegir Partida", 270, 350, 260, 60, VIOLETA_MENU, FUCSIA, pantalla, lambda: cambiar_ventana('elegir_partida'))
    boton("Crear Nonograma", 270, 450, 260, 60, VIOLETA_MENU, FUCSIA, pantalla, lambda: cambiar_ventana('crear_nonograma'))
    boton("Salir del juego", 270, 550, 260, 60, VIOLETA_MENU, FUCSIA, pantalla, lambda: iniciar_ventana_confirmacion())

    if confirmando:
        ventana_confirmacion()

    reloj.tick(10)

def iniciar_ventana_confirmacion():
    global confirmando
    confirmando = True 

def ventana_confirmacion():
    global confirmando
    confirm_width = 350
    confirm_height = 150

    confirm_rect = pygame.Rect((ancho_pantalla // 2 - confirm_width // 2, alto_pantalla // 2 - confirm_height // 2), (confirm_width, confirm_height))

    pygame.draw.rect(pantalla, NEGRO, confirm_rect)
    mostrar_texto("¿Seguro que quieres salir?", pygame.font.SysFont(None, 36), BLANCO, pantalla, ancho_pantalla // 2, alto_pantalla // 2 - 20)

    boton("Sí", confirm_rect.left + 55, confirm_rect.top + 80, 80, 40, VERDE, VERDE_PRESIONADO, pantalla, salir_del_juego)
    boton("No", confirm_rect.right - 140, confirm_rect.top + 80, 80, 40, ROJO, ROJO_PRESIONADO, pantalla, cancelar_ventana_confirmacion)

def cancelar_ventana_confirmacion():
    global confirmando
    confirmando = False  # Desactiva la ventana de confirmación

def ventana_elegir_partida(cambiar_ventana):
    pantalla.fill(GRIS)
    mostrar_texto("Elegir Partida", fuente, NEGRO, pantalla, 400, 100)
    boton("Volver al menú", 300, 400, 200, 60, GRIS, AZUL_OSCURO, pantalla, lambda: cambiar_ventana('menu_principal'))
    boton("Jugar", 300, 500, 200, 60, GRIS, AZUL_OSCURO, pantalla, lambda: cambiar_ventana('ventana_nonograma_game'))

def ventana_crear_nonograma(cambiar_ventana):
    pantalla.fill(GRIS)
    mostrar_texto("Crear Nonograma", fuente, NEGRO, pantalla, 400, 100)
    boton("Volver al menú", 300, 400, 200, 60, GRIS, AZUL_OSCURO, pantalla, lambda: cambiar_ventana('menu_principal'))

def salir_del_juego():
    pygame.quit()
    sys.exit()
