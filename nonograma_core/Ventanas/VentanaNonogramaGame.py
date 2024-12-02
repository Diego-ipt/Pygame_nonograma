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

            for i, fila in enumerate(filas):
                if not fila:
                    mostrar_texto("0", NEGRO, self.pantalla,
                                  offset_x - 40,
                                  offset_y + i * tamano_celda + tamano_celda // 2)
                else:
                    for k, num in enumerate(fila):
                        mostrar_texto(str(num), NEGRO, self.pantalla,
                                      offset_x - 40 - len(fila) * 15 + k * 25,
                                      offset_y + i * tamano_celda + tamano_celda // 2)

             for j, columna in enumerate(columnas):
                if not columna:
                    mostrar_texto("0", NEGRO, self.pantalla,
                                  offset_x + j * tamano_celda + tamano_celda // 2,
                                  offset_y - 40)
                else:
                    for k, num in enumerate(columna):
                        mostrar_texto(str(num), NEGRO, pantalla,
                                      offset_x + j * tamano_celda + tamano_celda // 2,
                                      offset_y - 40 - len(columna) * 15 + k * 25)
        ##Por arreglar refactoring
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

            # Correr lógica del juego
            if self.game.run(self.pantalla, *game_position, pygame.event.get()):
                self.running = False
                return 'ventana_victoria'

            pygame.display.flip()  # Actualizar pantalla en cada iteración
