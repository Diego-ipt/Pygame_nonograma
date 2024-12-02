import sys

import pygame
from nonograma_core.Elementos_graficos.colores import *
from nonograma_core.Elementos_graficos.elementos_menus import *
from nonograma_core.Ventanas.VentanaBase import VentanaBase
from nonograma_core.Elementos_graficos.AssetManager import AssetManager
from nonograma_core.JuegoNonograma import ANCHO_PANTALLA, ALTO_PANTALLA


class VentanaVictoria(VentanaBase):
    def __init__(self, pantalla, tablero_completo):
        self.pantalla = pantalla
        self.asset = AssetManager()
        self.trophy = self.asset.cargar_fotogramas("trofeo_win")
        self.indice_fotograma_trophy = 0
        self.contador_fotogramas = 0
        self.retraso_fotogramas = 5

        self.tablero_completo = tablero_completo

        # Dimensiones del tablero, queremos evitar que un tablero 10x10 ocupe toda la pantalla
        max_tablero_ancho = ANCHO_PANTALLA // 2.5
        max_tablero_alto = ALTO_PANTALLA - 230
        self.escala_celda = min(max_tablero_ancho // self.tablero_completo.grid_size, max_tablero_alto // self.tablero_completo.grid_size, 60)
        self.tablero_ancho = self.tablero_completo.grid_size * self.escala_celda
        self.tablero_alto = self.tablero_completo.grid_size * self.escala_celda
        self.tablero_x = (ANCHO_PANTALLA - self.tablero_ancho) // 4
        self.tablero_y = (ALTO_PANTALLA - self.tablero_alto) // 2


        # Posicion trofeo
        self.trofeo_x = 350
        self.trofeo_y = 100

        self.boton_volver = Boton(image=None, pos=(ANCHO_PANTALLA / 2, 550), text_input="Volver al menú", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO)

    def run(self):
        while True:
            actualizar_grid_fondo_menu()
            self.pantalla.fill(BLANCO)
            dibujar_grid_fondo_menu(self.pantalla, 50, 50, 16, VIOLETA_MENU, BLANCO)
            mostrar_texto("¡Ganaste!", NEGRO, self.pantalla, 400, 100)
            mouse_pos = pygame.mouse.get_pos()

            surface_tablero = pygame.Surface((self.tablero_completo.grid_size * self.escala_celda,
                                              self.tablero_completo.grid_size * self.escala_celda))
            self.tablero_completo.cell_size = self.escala_celda
            self.tablero_completo.draw(surface_tablero, mostrar_solucion=True)
            self.pantalla.blit(surface_tablero, (self.tablero_x, self.tablero_y))

            self.indice_fotograma_trophy, self.contador_fotogramas = mostrar_fotogramas(
                self.trophy, self.indice_fotograma_trophy, self.contador_fotogramas,
                self.retraso_fotogramas, self.trofeo_x, self.trofeo_y, self.pantalla
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

