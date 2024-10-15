import pygame
from nonograma_core.elementos_menus import *
from nonograma_core.colores import *
from nonograma_core.ventana_nonograma import *
from nonograma_core.nonograma_numeros import *
from nonograma_core.VentanaBase import *
from nonograma_core.AssetManager import *


class VentanaNonogramaGame(VentanaBase):
    def __init__(self, pantalla, cambiar_ventana):
        super().__init__(pantalla, cambiar_ventana)
        self.game = Game()
        self.running = True

    def dibujar(self):
        self.pantalla.fill(ROJO)
        pygame.display.set_caption("Nonograma Game")
        mostrar_texto("Nivel X", fuente, NEGRO, self.pantalla, 80, 50)
        filas, columnas = procesar_matriz(self.game.board.matriz_solucion)
        game_position = (80, 120)
        tamano_celda = self.game.getCellSize()

        for i, fila in enumerate(filas):
            mostrar_texto(str(fila), fuente, NEGRO, self.pantalla, game_position[0] - 20, game_position[1] + i * tamano_celda + tamano_celda // 2)

        for j, columna in enumerate(columnas):
            mostrar_texto(str(columna), fuente, NEGRO, self.pantalla, game_position[0] + j * tamano_celda + tamano_celda // 2, game_position[1] - 20)

        self.running = True

        while self.running:
            events = pygame.event.get()
            print("hola")
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    raton = pygame.mouse.get_pos()
                    if 500 <= raton[0] <= 700 and 100 <= raton[1] <= 160:
                        self.cambiar_ventana('menu_principal')  
                        self.running = False
                    elif 500 <= raton[0] <= 700 and 220 <= raton[1] <= 280:
                        self.game.deshacer() 
                    elif 500 <= raton[0] <= 700 and 340 <= raton[1] <= 400:
                        self.game.rehacer()

        boton("Volver al menú", 500, 100, 200, 60, GRIS, AZUL_OSCURO, self.pantalla)
        boton("Deshacer", 500, 220, 200, 60, GRIS, AZUL_OSCURO, self.pantalla)
        boton("Rehacer", 500, 340, 200, 60, GRIS, AZUL_OSCURO, self.pantalla)

        if self.game.run(self.pantalla, *game_position, events=events):
            self.cambiar_ventana('ventana_victoria')
            self.running = False

        pygame.display.flip()  # Actualiza la pantalla en cada iteración del bucle
        self.reloj.tick(60)