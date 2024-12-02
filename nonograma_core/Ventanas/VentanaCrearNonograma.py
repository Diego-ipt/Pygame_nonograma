import sys
import pygame
from nonograma_core.Ventanas.VentanaBase import VentanaBase
from nonograma_core.Logica.creador import CreatorWindow
from nonograma_core.Elementos_graficos.elementos_menus import *
from nonograma_core.Elementos_graficos.colores import *

class VentanaCrearNonograma(VentanaBase):
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.creador = CreatorWindow()
        self.running = True
        self.nombre_nivel = None

        self.boton_volver = Boton(image=None, pos=(650, 100), text_input="Volver al menú", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO)
        self.boton_guardar = Boton(image=None, pos=(650, 200), text_input="Guardar", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO)
        self.boton_menos = Boton(image=None, pos=(150, 500), text_input="-", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO,rect_padding=(50,10))
        self.boton_mas = Boton(image=None, pos=(320, 500), text_input="+", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO,rect_padding=(50,10))

        #popup de confirmacion
        self.popup_guardado = PopUp(pos=(400, 300), size=(300, 150), message="Nivel guardado", font=pygame.font.SysFont(None, 36), base_color=NEGRO, text_color=BLANCO)
        self.boton_ok = Boton(image=None, pos=(0, 0), text_input="OK", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO,rect_padding=(30,10))
        self.popup_guardado.add_button(self.boton_ok)
        self.popup_guardado.desactivar()

    def run(self):
        while True:
            actualizar_grid_fondo_menu(0.00005)
            self.pantalla.fill(BLANCO)
            dibujar_grid_fondo_menu(self.pantalla, 50, 50, 16, VERDE_PRESIONADO, BLANCO)
            pygame.display.set_caption("Nonograma Creador")
            mouse_pos = pygame.mouse.get_pos()
            eventos = pygame.event.get()

            if self.popup_guardado.is_active:
                self.popup_guardado.update(self.pantalla)

                for evento in eventos:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if self.boton_ok.checkInput(mouse_pos):
                            self.popup_guardado.desactivar()
                            return 'menu_principal'

            else:
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
                            self.popup_guardado.activar()
                            self.guardarNivel()



            pygame.display.flip()  # Actualiza la pantalla en cada iteración del bucle


    def guardarNivel(self):
        #Guarda el nivel en un json y devuelve el nombre
        self.nombre_nivel = self.creador.saveDesign()

