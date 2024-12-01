import sys
import pygame
from nonograma_core.Elementos_graficos.Boton import Boton

from nonograma_core.Elementos_graficos.elementos_menus import *
from nonograma_core.Elementos_graficos.colores import *
from nonograma_core.Logica.tablero_nonograma import *
from nonograma_core.Logica.nonograma_numeros import *
from nonograma_core.Ventanas.VentanaBase import *
from nonograma_core.Elementos_graficos.AssetManager import *


class VentanaMenuPrincipal(VentanaBase):
    def __init__(self, pantalla):
        self.pantalla = pantalla

        self.asset = AssetManager()
        self.menu = self.asset.cargar_fotogramas("menu")
        self.indice_fotograma_menu = 0
        self.grid_estado = [[False for _ in range(50)] for _ in range(50)]

        self.boton_elegir_partida = Boton(image=None, pos=(270, 350), text_input="Elegir Partida", font=pygame.font.SysFont(None, 36), base_color=VIOLETA_MENU, hover_color=FUCSIA)
        self.boton_crear_nonograma = Boton(image=None, pos=(270, 450), text_input="Crear Nonograma", font=pygame.font.SysFont(None, 36), base_color=VIOLETA_MENU, hover_color=FUCSIA)
        self.boton_salir = Boton(image=None, pos=(270, 550), text_input="Salir del juego", font=pygame.font.SysFont(None, 36), base_color=VIOLETA_MENU, hover_color=FUCSIA)

    def run(self):
        while True:
            actualizar_grid(self.grid_estado)
            self.pantalla.fill(BLANCO)
            dibujar_grid(self.pantalla, 50, 50, 16, NEGRO, BLANCO_MENU, self.grid_estado)
            self.indice_fotograma_menu = mostrar_fotogramas(self.menu, self.indice_fotograma_menu, 75, 0, self.pantalla)

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
                        return 'elegir-partida'
                    if self.boton_crear_nonograma.checkInput(menu_mouse_pos):
                        return 'crear-nonograma'
                    if self.boton_salir.checkInput(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
