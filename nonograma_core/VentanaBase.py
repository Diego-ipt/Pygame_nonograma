import sys
import pygame
from nonograma_core.AssetManager import *

class VentanaBase:
    def __init__(self, pantalla, cambiar_ventana):
        self.pantalla = pantalla
        self.cambiar_ventana = cambiar_ventana
        self.reloj = pygame.time.Clock()

    def manejar_eventos(self):
        pass
    
    def dibujar(self):
        pass