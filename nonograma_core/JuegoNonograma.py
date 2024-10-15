import sys
import pygame

from nonograma_core.VentanaMenuPrincipal import *
from nonograma_core.VentanaElegirPartida import *
from nonograma_core.VentanaCrearNonograma import *
from nonograma_core.VentanaNonogramaGame import *
from nonograma_core.VentanaVictoria import *
from nonograma_core.AssetManager import *



class JuegoNonograma:
    def __init__(self):
        pygame.init()
        self.estado_actual = 'menu_principal'
        self.running = True
        self.pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
        self.asset = AssetManager()
        self.icono = self.asset.cargar_imagen("Iconojuego.jpg")
        pygame.display.set_caption("Nonograma_Game")
        pygame.display.set_icon(icono)
        # Inicializa la ventana actual
        self.cambiar_ventana('menu_principal')

    def cambiar_ventana(self, nuevo_estado):
        print(f"Cambiando a ventana: {nuevo_estado}")
        if nuevo_estado == 'menu_principal':
            self.ventana_actual = VentanaMenuPrincipal(self.pantalla, self.cambiar_ventana)
        elif nuevo_estado == 'elegir_partida':
            self.ventana_actual = VentanaElegirPartida(self.pantalla, self.cambiar_ventana)
        elif nuevo_estado == 'crear_nonograma':
            self.ventana_actual = VentanaCrearNonograma(self.pantalla, self.cambiar_ventana)
        elif nuevo_estado == 'ventana_nonograma_game':
            self.ventana_actual = VentanaNonogramaGame(self.pantalla, self.cambiar_ventana)
        elif nuevo_estado == 'ventana_victoria':
            self.ventana_actual = VentanaVictoria(self.pantalla, self.cambiar_ventana)

    def ejecutar(self):
        while self.running:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.running = False
            # Llamar a la función de dibujo de la ventana actual
            self.ventana_actual.dibujar()
            pygame.display.update()
    
        pygame.quit()
        sys.exit()

