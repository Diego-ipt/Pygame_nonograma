from nonograma_core.Elementos_graficos.elementos_menus import *
from nonograma_core.Elementos_graficos.colores import *
from nonograma_core.Logica.tablero_nonograma import *
from nonograma_core.Logica.nonograma_numeros import *
from nonograma_core.Ventanas.VentanaBase import *
from nonograma_core.Elementos_graficos.AssetManager import *

class VentanaVictoria(VentanaBase):
    def __init__(self, pantalla, cambiar_ventana):
        super().__init__(pantalla, cambiar_ventana)
        self.asset = AssetManager()
        self.trophy = self.asset.cargar_fotogramas("trofeo_win")
        self.indice_fotograma_trophy = 0

    def dibujar(self):
        self.pantalla.fill(VIOLETA_MENU)
        self.indice_fotograma_trophy = mostrar_fotogramas(self.trophy, self.indice_fotograma_trophy, 170, 100, self.pantalla)
        mostrar_texto("¡Ganaste!", fuente, NEGRO, self.pantalla, 400, 100)
        boton("Volver al menú", 310, 400, 200, 60, NOTHING, FUCSIA, self.pantalla, lambda: self.cambiar_ventana('menu_principal'))

        self.reloj.tick(30)
