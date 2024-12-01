import sys
import pygame
from nonograma_core.Ventanas.VentanaBase import VentanaBase
from nonograma_core.Logica.creador import CreatorWindow
from nonograma_core.Elementos_graficos.elementos_menus import Boton
from nonograma_core.Elementos_graficos.colores import *

class VentanaCrearNonograma(VentanaBase):
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.creador = CreatorWindow()
        self.running = True
        self.guardando = False
        self.nombre_nivel = None

        self.boton_volver = Boton(image=None, pos=(650, 100), text_input="Volver al menú", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO)
        self.boton_guardar = Boton(image=None, pos=(650, 200), text_input="Guardar", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO)
        self.boton_menos = Boton(image=None, pos=(150, 500), text_input="-", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO,rect_padding=(50,10))
        self.boton_mas = Boton(image=None, pos=(320, 500), text_input="+", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO,rect_padding=(50,10))


    def run(self):
        while True:
            self.pantalla.fill(VERDE)
            pygame.display.set_caption("Nonograma Creador")
            mouse_pos = pygame.mouse.get_pos()

            eventos = pygame.event.get()

            for boton in [self.boton_volver, self.boton_mas, self.boton_menos, self.boton_guardar]:
                boton.changeColor(mouse_pos)
                boton.update(self.pantalla)

            game_position = (80, 120)
            offset_x = game_position[0]
            offset_y = game_position[1]

            if self.creador.run(self.pantalla, *game_position, eventos):
                self.creador.running = False
                return 'menu_principal'

            for evento in eventos:
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton_volver.checkInput(mouse_pos):
                        self.running = False
                        return 'menu_principal'
                    if self.boton_mas.checkInput(mouse_pos):
                        self.creador.increaseGrid()
                    if self.boton_menos.checkInput(mouse_pos):
                        self.creador.decreaseGrid()
                    if self.boton_guardar.checkInput(mouse_pos):
                        self.guardarNivel()

            pygame.display.flip()  # Actualiza la pantalla en cada iteración del bucle

    def cerrarPopup(self):
        self.guardando = False

    def guardarNivel(self):
        #Guarda el nivel en un json y devuelve el nombre
        self.nombre_nivel = self.creador.saveDesign()
        self.guardando = True
