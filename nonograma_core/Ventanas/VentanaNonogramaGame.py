import pygame
import time
from nonograma_core.Elementos_graficos.elementos_menus import *
from nonograma_core.Elementos_graficos.colores import *
from nonograma_core.Logica.tablero_nonograma import *
from nonograma_core.Logica.nonograma_numeros import *
from nonograma_core.Ventanas.VentanaBase import *
from nonograma_core.Elementos_graficos.AssetManager import *


class VentanaNonogramaGame(VentanaBase):
    def __init__(self, pantalla, cambiar_ventana):
        super().__init__(pantalla, cambiar_ventana)
        self.game = Game()
        self.running = True

    # En el bucle principal del juego
    def dibujar(self):
        time.sleep(0.1)  # Agregar un delay de 1 segundo
        pantalla.fill(ROJO)
        pygame.display.set_caption("Nonograma Game")
        mostrar_texto("Nivel X", fuente, NEGRO, pantalla, 80, 50)
    
        filas, columnas = procesar_matriz(self.game.board.matriz_solucion)
        game_position = (80, 120)

        tamano_celda = self.game.getCellSize()
        offset_x = game_position[0]
        offset_y = game_position[1]

        # Dibujar números de filas y columnas
        for i, fila in enumerate(filas):
            mostrar_texto(str(fila), fuente, NEGRO, pantalla, offset_x - 20, offset_y + i * tamano_celda + tamano_celda // 2)

        for j, columna in enumerate(columnas):
            mostrar_texto(str(columna), fuente, NEGRO, pantalla, offset_x + j * tamano_celda + tamano_celda // 2, offset_y - 20)
    
        boton("Volver al menú", 500, 100, 200, 60, GRIS, AZUL_OSCURO, pantalla, lambda: self.cambiar_ventana('menu_principal'))
        boton("Deshacer", 500, 220, 200, 60, GRIS, AZUL_OSCURO, pantalla, self.game.deshacer)
        boton("Rehacer", 500, 340, 200, 60, GRIS, AZUL_OSCURO, pantalla, self.game.rehacer)

        if self.game.run(pantalla, *game_position, pygame.event.get()):
            self.game.running = False
            self.cambiar_ventana('ventana_victoria')

        pygame.display.flip()  # Actualiza la pantalla en cada iteración del bucle