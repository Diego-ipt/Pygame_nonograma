import sys

from nonograma_core.Elementos_graficos.elementos_menus import *
from nonograma_core.Ventanas.VentanaBase import VentanaBase
from nonograma_core.Logica.creador import CreatorWindow
from nonograma_core.Elementos_graficos.Boton import Boton

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
            pantalla.fill(VERDE)
            pygame.display.set_caption("Nonograma Creador")
            mouse_pos = pygame.mouse.get_pos()

            eventos = pygame.event.get()

            for boton in [self.boton_volver, self.boton_mas, self.boton_menos, self.boton_guardar]:
                boton.changeColor(mouse_pos)
                boton.update(pantalla)

            game_position = (80, 120)
            offset_x = game_position[0]
            offset_y = game_position[1]

            if self.creador.run(pantalla, *game_position, eventos):
                self.creador.running = False
                return 'menu_principal'

            if self.guardando:
                self.mostrarPopupGuardar()

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

    def mostrarPopupGuardar(self):
        popup_width = 350
        popup_height = 150

        popup_rect = pygame.Rect((ancho_pantalla // 2 - popup_width // 2, alto_pantalla // 2 - popup_height // 2), (popup_width, popup_height))

        pygame.draw.rect(pantalla, NEGRO, popup_rect)
        mostrar_texto(f"Guardado como {self.nombre_nivel}", pygame.font.SysFont(None, 36), BLANCO, pantalla, ancho_pantalla // 2, alto_pantalla // 2 - 20)
        boton("Ok", popup_rect.left + 55, popup_rect.top + 80, 80, 40, VERDE, VERDE_PRESIONADO, pantalla, lambda: self.cerrarPopup())

    def guardarNivel(self):
        #Guarda el nivel en un json y devuelve el nombre
        self.nombre_nivel = self.creador.saveDesign()
        self.guardando = True
