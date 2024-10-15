import sys
import pygame
from nonograma_core.elementos_menus import *
from nonograma_core.colores import *
from nonograma_core.ventana_nonograma import *
from nonograma_core.nonograma_numeros import *
from nonograma_core.VentanaBase import *
from nonograma_core.AssetManager import *


class VentanaMenuPrincipal(VentanaBase):
    def __init__(self, pantalla, cambiar_ventana):
        super().__init__(pantalla, cambiar_ventana)
        self.indice_fotograma_menu = 0
        self.asset = AssetManager()
        self.menu = self.asset.cargar_fotogramas("menu")
        self.grid_estado = [[False for _ in range(50)] for _ in range(50)]
        self.confirmando = False

    def dibujar(self):
        actualizar_grid(self.grid_estado)
        self.pantalla.fill(BLANCO)
        dibujar_grid(self.pantalla, 50, 50, 16, NEGRO, BLANCO_MENU, self.grid_estado)
        self.indice_fotograma_menu = mostrar_fotogramas(self.menu, self.indice_fotograma_menu, 75, 0, self.pantalla)

        boton("Elegir Partida", 270, 350, 260, 60, VIOLETA_MENU, FUCSIA, self.pantalla, lambda: self.cambiar_ventana('elegir_partida'))
        boton("Crear Nonograma", 270, 450, 260, 60, VIOLETA_MENU, FUCSIA, self.pantalla, lambda: self.cambiar_ventana('crear_nonograma'))
        boton("Salir del juego", 270, 550, 260, 60, VIOLETA_MENU, FUCSIA, self.pantalla, self.iniciar_ventana_confirmacion)
        self.reloj.tick(10)

        if self.confirmando:
            self.ventana_confirmacion()

        self.reloj.tick(80) #fps

    def iniciar_ventana_confirmacion(self):
        self.confirmando = True

    def ventana_confirmacion(self):
        confirm_width, confirm_height = 350, 150

        confirm_rect = pygame.Rect((ancho_pantalla // 2 - confirm_width // 2, alto_pantalla // 2 - confirm_height // 2), (confirm_width, confirm_height))

        pygame.draw.rect(self.pantalla, NEGRO, confirm_rect)
        mostrar_texto("¿Seguro que quieres salir?", pygame.font.SysFont(None, 36), BLANCO, self.pantalla, ancho_pantalla // 2, alto_pantalla // 2 - 20)

        boton("Sí", confirm_rect.left + 55, confirm_rect.top + 80, 80, 40, VERDE, VERDE_PRESIONADO, self.pantalla, self.salir_del_juego)
        boton("No", confirm_rect.right - 140, confirm_rect.top + 80, 80, 40, ROJO, ROJO_PRESIONADO, self.pantalla, self.cancelar_ventana_confirmacion)

    def cancelar_ventana_confirmacion(self):
        self.confirmando = False

    def salir_del_juego(self):
        pygame.quit()
        sys.exit()