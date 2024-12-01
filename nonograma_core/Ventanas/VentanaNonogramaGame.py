from nonograma_core.Elementos_graficos.elementos_menus import *
from nonograma_core.Logica.nonograma_numeros import *
from nonograma_core.Ventanas.VentanaBase import *
from nonograma_core.Logica.registros import *


class VentanaNonogramaGame(VentanaBase):
    def __init__(self, pantalla, game, nombre_nivel):
        self.pantalla = pantalla
        self.game = game
        self.nombre_nivel = nombre_nivel
        self.running = True
        self.registro = Guardado(nombre_nivel, game, game.identificador)

        self.boton_volver = Boton(image=None, pos=(600, 100), text_input="Volver al menu",font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO)
        self.boton_deshacer = Boton(image=None, pos=(600, 200), text_input="Deshacer", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO)
        self.boton_rehacer = Boton(image=None, pos=(600, 300), text_input="Rehacer", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO)
        self.boton_guardar = Boton(image=None, pos=(600, 400), text_input="Guardar", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO)

    def run(self):
        while True:
            self.pantalla.fill(ROJO)
            pygame.display.set_caption("Nonograma Game")
            texto_nivel = f"Nivel {self.nombre_nivel}"
            mostrar_texto(texto_nivel, NEGRO, self.pantalla, 110, 40, fuente=pygame.font.SysFont(None, 35))

            menu_mouse_pos = pygame.mouse.get_pos()

            for boton in [self.boton_volver, self.boton_deshacer, self.boton_rehacer, self.boton_guardar]:
                boton.changeColor(menu_mouse_pos)
                boton.update(self.pantalla)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton_volver.checkInput(menu_mouse_pos):
                        self.running = False
                        return 'menu_principal'
                    if self.boton_deshacer.checkInput(menu_mouse_pos):
                        self.game.deshacer()
                    if self.boton_rehacer.checkInput(menu_mouse_pos):
                        self.game.rehacer()
                    if self.boton_guardar.checkInput(menu_mouse_pos):
                        self.registro.Save_progress()


            # Obtener posición y tamaño del tablero
            filas, columnas = procesar_matriz(self.game.board.matriz_solucion)
            game_position = (120, 160)
            tamano_celda = self.game.getCellSize()
            offset_x, offset_y = game_position

            # Dibujar números de las filas
            for i, fila in enumerate(filas):
                for k, num in enumerate(fila or [0]):
                    mostrar_texto(str(num), NEGRO, self.pantalla,
                                  offset_x - 40 - len(fila) * 15 + k * 25,
                                  offset_y + i * tamano_celda + tamano_celda // 2,
                                  fuente=pygame.font.SysFont(None, 30))

            # Dibujar números de las columnas
            for j, columna in enumerate(columnas):
                for k, num in enumerate(columna or [0]):
                    mostrar_texto(str(num), NEGRO, self.pantalla,
                                  offset_x + j * tamano_celda + tamano_celda // 2,
                                  offset_y - 40 - len(columna) * 15 + k * 25,
                                  fuente=pygame.font.SysFont(None, 30))


            # Correr lógica del juego
            if self.game.run(self.pantalla, *game_position, pygame.event.get()):
                self.running = False
                return 'ventana_victoria'

            pygame.display.flip()  # Actualizar pantalla en cada iteración
