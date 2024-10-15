from nonograma_core.elementos_menus import *
from nonograma_core.colores import *
from nonograma_core.ventana_nonograma import *
from nonograma_core.nonograma_numeros import *
from nonograma_core.VentanaBase import *

class VentanaElegirPartida(VentanaBase):
    def __init__(self, pantalla, cambiar_ventana):
        super().__init__(pantalla, cambiar_ventana)

    def iniciar_juego(self, Partida_seleccionada):
        game = Partida_seleccionada  # Reinicia el juego
        game.running = True
        self.cambiar_ventana('ventana_nonograma_game')

    def dibujar(self):
        self.pantalla.fill(GRIS)
        mostrar_texto("Elegir Partida", fuente, NEGRO, self.pantalla, 400, 100)
        boton("Volver al menú", 300, 400, 200, 60, GRIS, AZUL_OSCURO, self.pantalla, lambda: self.cambiar_ventana('menu_principal'))
        #Game() se debe reemplazar por el nongrama a jugar elegido en esta ventana
        boton("Jugar", 300, 500, 200, 60, GRIS, AZUL_OSCURO, self.pantalla, lambda: self.iniciar_juego(Game())) 