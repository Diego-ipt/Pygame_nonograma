import pygame
import sys
import random

from nonograma_core.Elementos_graficos.AssetManager import AssetManager
from nonograma_core.Elementos_graficos.elementos_menus import Boton, mostrar_fotogramas
from nonograma_core.Ventanas.VentanaBase import VentanaBase
from nonograma_core.Elementos_graficos.colores import *
from nonograma_core.JuegoNonograma import ANCHO_PANTALLA


#Funciones para dibujar el fondo del menu


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


class VentanaMenuPrincipal(VentanaBase):
    def __init__(self, pantalla):
        self.pantalla = pantalla

        self.asset = AssetManager()
        self.menu = self.asset.cargar_fotogramas("menu")
        self.indice_fotograma_menu = 0
        self.grid_estado = [[False for _ in range(50)] for _ in range(50)]
        self.contador_fotogramas = 0
        self.retraso_fotogramas = 10

        self.boton_elegir_partida = Boton(image=None, pos=(ANCHO_PANTALLA / 2, 350), text_input="Elegir Partida", font=pygame.font.SysFont(None, 36), base_color=VIOLETA_MENU, hover_color=FUCSIA)
        self.boton_crear_nonograma = Boton(image=None, pos=(ANCHO_PANTALLA / 2, 450), text_input="Crear Nonograma", font=pygame.font.SysFont(None, 36), base_color=VIOLETA_MENU, hover_color=FUCSIA)
        self.boton_salir = Boton(image=None, pos=(ANCHO_PANTALLA / 2, 550), text_input="Salir del juego", font=pygame.font.SysFont(None, 36), base_color=VIOLETA_MENU, hover_color=FUCSIA)

    def run(self):
        while True:
            actualizar_grid(self.grid_estado)
            self.pantalla.fill(BLANCO)
            dibujar_grid(self.pantalla, 50, 50, 16, NEGRO, BLANCO_MENU, self.grid_estado)
            self.indice_fotograma_menu, self.contador_fotogramas = mostrar_fotogramas(self.menu, self.indice_fotograma_menu, self.contador_fotogramas, self.retraso_fotogramas, 75, 0, self.pantalla)

            menu_mouse_pos = pygame.mouse.get_pos()

            for boton in [self.boton_elegir_partida, self.boton_crear_nonograma, self.boton_salir]:
                boton.changeColor(menu_mouse_pos)
                boton.update(self.pantalla)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton_elegir_partida.checkInput(menu_mouse_pos):
                        return 'elegir_partida'
                    if self.boton_crear_nonograma.checkInput(menu_mouse_pos):
                        return 'crear_nonograma'
                    if self.boton_salir.checkInput(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()


