import sys

import pygame
from nonograma_core.Elementos_graficos.colores import *
from nonograma_core.Elementos_graficos.elementos_menus import mostrar_fotogramas, mostrar_texto, Boton
from nonograma_core.Ventanas.VentanaBase import VentanaBase
from nonograma_core.Elementos_graficos.AssetManager import AssetManager
from nonograma_core.JuegoNonograma import ANCHO_PANTALLA, ALTO_PANTALLA


class VentanaDerrota(VentanaBase):
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.asset = AssetManager()
        self.gamelose = self.asset.cargar_fotogramas("game_lose")
        self.indice_fotograma_gamelose = 0
        self.contador_fotogramas = 0
        self.retraso_fotogramas = 15

        # Posicion 
        self.gamelose_x = 150
        self.gamelose_y = 20

        self.boton_volver = Boton(image=None, pos=(ANCHO_PANTALLA/2, 550), text_input="Volver al menú", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO)

    def run(self):
        while True:
            self.pantalla.fill(ROJO)
            mostrar_texto("Inténtalo de nuevo :(", NEGRO, self.pantalla, ANCHO_PANTALLA/2, 480)
            mouse_pos = pygame.mouse.get_pos()

            self.indice_fotograma_gamelose, self.contador_fotogramas = mostrar_fotogramas(
                self.gamelose, self.indice_fotograma_gamelose, self.contador_fotogramas,
                self.retraso_fotogramas, self.gamelose_x, self.gamelose_y, self.pantalla
            )

            self.boton_volver.changeColor(mouse_pos)
            self.boton_volver.update(self.pantalla)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton_volver.checkInput(mouse_pos):
                        return 'menu_principal'

            pygame.display.update()

