from nonograma_core.Elementos_graficos.elementos_menus import *
from nonograma_core.Elementos_graficos.colores import *
from nonograma_core.Logica.tablero_nonograma import *
from nonograma_core.Logica.nonograma_numeros import *
from nonograma_core.Ventanas.VentanaBase import *
from nonograma_core.Elementos_graficos.AssetManager import *

class VentanaCrearNonograma(VentanaBase):
    def __init__(self, pantalla, cambiar_ventana):
        super().__init__(pantalla, cambiar_ventana)

    def dibujar(self):
        self.pantalla.fill(GRIS)
        mostrar_texto("Crear Nonograma", fuente, NEGRO, self.pantalla, 400, 100)
        boton("Volver al menú", 300, 400, 200, 60, GRIS, AZUL_OSCURO, self.pantalla, lambda: self.cambiar_ventana('menu_principal'))
