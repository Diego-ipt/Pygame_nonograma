import pygame
import time
import json
import os
from nonograma_core.Elementos_graficos.elementos_menus import *
from nonograma_core.Elementos_graficos.colores import *
from nonograma_core.Logica.tablero_nonograma import *
from nonograma_core.Logica.nonograma_numeros import *
from nonograma_core.Ventanas.VentanaBase import *
from nonograma_core.Logica.registros import *
from nonograma_core.Elementos_graficos.AssetManager import AssetManager


class VentanaNonogramaGame(VentanaBase):
    def __init__(self, pantalla, cambiar_ventana, game, nombre_nivel):
        super().__init__(pantalla, cambiar_ventana)
        self.game = game
        self.nombre_nivel = nombre_nivel
        self.running = True
        self.registro = Guardado(nombre_nivel, game, game.identificador)
        self.mostrar_mensaje = False  # Controla si se debe mostrar el mensaje
        self.tiempo_mensaje = 0       # Registra el tiempo para mostrar el mensaje

    def guardar_progreso(self):
        """Guarda el progreso y activa el mensaje de confirmación."""
        self.registro.Save_progress()
        self.mostrar_mensaje = True
        self.tiempo_mensaje = time.time()

    # En el bucle principal del juego
    def dibujar(self):
        time.sleep(0.1)
        pantalla.fill(ROJO)
        pygame.display.set_caption("Nonograma Game")
        texto_nivel = f"Nivel {self.nombre_nivel}"
        mostrar_texto(texto_nivel, pygame.font.SysFont(None, 35), NEGRO, pantalla, 110, 40)

        filas, columnas = procesar_matriz(self.game.board.matriz_solucion)
        game_position = (120, 160)

        tamano_celda = self.game.getCellSize()
        offset_x = game_position[0]
        offset_y = game_position[1]

        for i, fila in enumerate(filas):
            if not fila:
                mostrar_texto("0", fuente, NEGRO, pantalla,
                              offset_x - 40,
                              offset_y + i * tamano_celda + tamano_celda // 2)
            else:
                for k, num in enumerate(fila):
                    mostrar_texto(str(num), fuente, NEGRO, pantalla,
                                  offset_x - 40 - len(fila) * 15 + k * 25,
                                  offset_y + i * tamano_celda + tamano_celda // 2)

        for j, columna in enumerate(columnas):
            if not columna:
                mostrar_texto("0", fuente, NEGRO, pantalla,
                              offset_x + j * tamano_celda + tamano_celda // 2,
                              offset_y - 40)
            else:
                for k, num in enumerate(columna):
                    mostrar_texto(str(num), fuente, NEGRO, pantalla,
                                  offset_x + j * tamano_celda + tamano_celda // 2,
                                  offset_y - 40 - len(columna) * 15 + k * 25)

        boton("Volver al menú", 500, 100, 200, 60, GRIS, AZUL_OSCURO, pantalla,
              lambda: self.cambiar_ventana('menu_principal'), font=pygame.font.SysFont(None, 36))
        boton("Deshacer", 500, 200, 200, 60, GRIS, AZUL_OSCURO, pantalla, self.game.deshacer, font=pygame.font.SysFont(None, 36))
        boton("Rehacer", 500, 300, 200, 60, GRIS, AZUL_OSCURO, pantalla, self.game.rehacer, font=pygame.font.SysFont(None, 36))
        boton("Guardar", 500, 400, 200, 60, GRIS, AZUL_OSCURO, pantalla, self.guardar_progreso, font=pygame.font.SysFont(None, 36))

        # Mostrar el mensaje de confirmación si está activo
        if self.mostrar_mensaje:
            mostrar_texto("Progreso guardado", pygame.font.SysFont(None, 35), VERDE, pantalla, 300, 550)
            # Desactiva el mensaje después de 2 segundos
            if time.time() - self.tiempo_mensaje > 2:
                self.mostrar_mensaje = False

        if self.game.run(pantalla, *game_position, pygame.event.get()):
            self.game.running = False
            self.cambiar_ventana('ventana_victoria')

        pygame.display.flip()  # Actualiza la pantalla en cada iteración del bucle
