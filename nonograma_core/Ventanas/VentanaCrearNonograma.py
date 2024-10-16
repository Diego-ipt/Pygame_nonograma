from nonograma_core.Elementos_graficos.elementos_menus import *
from nonograma_core.Ventanas.VentanaBase import *
from creador.creador import *

class VentanaCrearNonograma(VentanaBase):
    def __init__(self, pantalla, cambiar_ventana):
        super().__init__(pantalla, cambiar_ventana)
        self.creador = CreatorWindow()
        self.running = True

    def dibujar(self):
        time.sleep(0.1)  # Agregar un delay de 1 segundo
        pantalla.fill(VERDE)
        pygame.display.set_caption("Nonograma Creador")

        boton("Volver al menú", 500, 100, 200, 60, GRIS, AZUL_OSCURO, pantalla, lambda: self.cambiar_ventana('menu_principal'))
        boton("+", 500, 220, 200, 60, GRIS, AZUL_OSCURO, pantalla, lambda: self.creador.increaseGrid())
        boton("-", 500, 340, 200, 60, GRIS, AZUL_OSCURO, pantalla, lambda: self.creador.decreaseGrid())
        boton("Guardar", 500, 460, 200, 60, GRIS, AZUL_OSCURO, pantalla, lambda: self.creador.saveDesign())

        game_position = (80, 120)
        offset_x = game_position[0]
        offset_y = game_position[1]

        if self.creador.run(pantalla, *game_position, pygame.event.get()):
            self.creador.running = False
            self.cambiar_ventana('menu_principal')

        pygame.display.flip()  # Actualiza la pantalla en cada iteración del bucle
