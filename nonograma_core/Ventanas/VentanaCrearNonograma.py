from nonograma_core.Elementos_graficos.elementos_menus import *
from nonograma_core.Ventanas.VentanaBase import *
from nonograma_core.Logica.creador import CreatorWindow


class VentanaCrearNonograma(VentanaBase):
    def __init__(self, pantalla, cambiar_ventana):
        super().__init__(pantalla, cambiar_ventana)
        self.creador = CreatorWindow()
        self.running = True
        self.guardando = False
        self.nombre_nivel = None

    def dibujar(self):
        time.sleep(0.1)  # Agregar un delay de 1 segundo
        pantalla.fill(VERDE)
        pygame.display.set_caption("Nonograma Creador")

        boton("Volver al menú", 500, 100, 200, 60, GRIS, AZUL_OSCURO, pantalla, lambda: self.cambiar_ventana('menu_principal'))
        boton("+", 500, 220, 200, 60, GRIS, AZUL_OSCURO, pantalla, lambda: self.creador.increaseGrid())
        boton("-", 500, 340, 200, 60, GRIS, AZUL_OSCURO, pantalla, lambda: self.creador.decreaseGrid())

        boton("Guardar", 500, 460, 200, 60, GRIS, AZUL_OSCURO, pantalla, lambda: self.guardarNivel())

        game_position = (80, 120)
        offset_x = game_position[0]
        offset_y = game_position[1]

        if self.creador.run(pantalla, *game_position, pygame.event.get()):
            self.creador.running = False
            self.cambiar_ventana('menu_principal')

        if self.guardando:
            self.mostrarPopupGuardar()

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
