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
        self.mostrar_mensaje_progreso = False  # Controla si se debe mostrar el mensaje
        self.tiempo_mensaje_progreso = 0       # Registra el tiempo para mostrar el mensaje
        self.mostrar_mensaje_ayudas = False
        self.tiempo_mensaje_ayudas = 0  

    def guardar_progreso(self):
        try:
            self.registro.Save_progress()
            self.mostrar_mensaje_progreso = True
            self.tiempo_mensaje_progreso = time.time()
        except Exception as e:
            print(f"Error al guardar el progreso: {e}")

    def victoria(self):
        self.game.running = False
        self.cambiar_ventana('ventana_victoria')

    def ayudas(self):
        if self.game.ayudas == 0:
            self.mostrar_mensaje_ayudas = True
            self.tiempo_mensaje_ayudas = time.time()
        else:
            self.game.help()

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

        boton("Volver al menú", 500, 50, 200, 60, GRIS, AZUL_OSCURO, pantalla,
              lambda: self.cambiar_ventana('menu_principal'), font=pygame.font.SysFont(None, 31))
        boton("Deshacer", 500, 130, 200, 60, GRIS, AZUL_OSCURO, pantalla, self.game.deshacer, font=pygame.font.SysFont(None, 31))
        boton("Rehacer", 500, 210, 200, 60, GRIS, AZUL_OSCURO, pantalla, self.game.rehacer, font=pygame.font.SysFont(None, 31))
        boton("Guardar progreso", 500, 290, 200, 60, GRIS, AZUL_OSCURO, pantalla, self.guardar_progreso, font=pygame.font.SysFont(None, 31))
        boton("Mostrar solución", 500, 370, 200, 60, GRIS, AZUL_OSCURO, pantalla, self.game.toggle_mostrar_solucion, font=pygame.font.SysFont(None, 31))
        boton("Reiniciar nivel", 500, 450, 200, 60, GRIS, AZUL_OSCURO, pantalla, self.game.reset, font=pygame.font.SysFont(None, 31))
        texto_ayuda = f"Ayuda ({self.game.ayudas})"
        boton(texto_ayuda, 500, 530, 200, 60, GRIS, AZUL_OSCURO, pantalla, self.ayudas, font=pygame.font.SysFont(None, 31))

        # Mostrar el mensaje de confirmación si está activo
        if self.mostrar_mensaje_progreso:
            mostrar_texto("Progreso guardado", pygame.font.SysFont(None, 34), VERDE, pantalla, 270, 480)
            # Desactiva el mensaje después de 2 segundos
            if time.time() - self.tiempo_mensaje_progreso > 2:
                self.mostrar_mensaje_progreso = False

        if self.mostrar_mensaje_ayudas:
            mostrar_texto("No tienes más ayudas", pygame.font.SysFont(None, 34), NEGRO, pantalla, 270, 530)
            # Desactiva el mensaje después de 2 segundos
            if time.time() - self.tiempo_mensaje_ayudas > 2:
                self.mostrar_mensaje_ayudas = False

        if self.game.run(pantalla, *game_position, pygame.event.get()):
            boton("Terminar", 200, 500, 200, 60, GRIS, AZUL_OSCURO, pantalla, self.victoria)

        pygame.display.flip()  # Actualiza la pantalla en cada iteración del bucle
