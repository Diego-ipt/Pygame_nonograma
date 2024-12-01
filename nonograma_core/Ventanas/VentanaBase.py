import sys
import pygame
from nonograma_core.Elementos_graficos.AssetManager import *

class VentanaBase:

    def run(self):
        raise NotImplementedError("Debe implementarse en la subclase")
