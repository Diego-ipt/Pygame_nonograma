import sys

import pygame
from nonograma_core.Elementos_graficos.colores import *
from nonograma_core.Elementos_graficos.elementos_menus import mostrar_fotogramas, mostrar_texto, Boton
from nonograma_core.Ventanas.VentanaBase import VentanaBase
from nonograma_core.Elementos_graficos.AssetManager import AssetManager
from nonograma_core.JuegoNonograma import ANCHO_PANTALLA

class VentanaVictoria(VentanaBase):
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.asset = AssetManager()
        self.trophy = self.asset.cargar_fotogramas("trofeo_win")
        self.indice_fotograma_trophy = 0
        self.contador_fotogramas = 0
        self.retraso_fotogramas = 60
        self.boton_volver = Boton(image=None, pos=(ANCHO_PANTALLA / 2, 500), text_input="Volver al menú", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO)

    def run(self):
        while True:
            self.pantalla.fill(VIOLETA_MENU)
            mostrar_texto("¡Ganaste!", NEGRO, self.pantalla, 400, 100)
            self.indice_fotograma_trophy, self.contador_fotogramas = mostrar_fotogramas(self.trophy, self.indice_fotograma_trophy, self.contador_fotogramas, self.retraso_fotogramas, 170, 100, self.pantalla)

            mouse_pos = pygame.mouse.get_pos()

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

