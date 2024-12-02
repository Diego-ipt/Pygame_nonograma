from nonograma_core.Elementos_graficos.elementos_menus import *
from nonograma_core.Logica.nonograma_numeros import *
from nonograma_core.Ventanas.VentanaBase import *
from nonograma_core.Logica.registros import *
import time


class VentanaNonogramaGame(VentanaBase):
    def __init__(self, pantalla, game, nombre_nivel):
        self.pantalla = pantalla
        self.game = game
        self.nombre_nivel = nombre_nivel
        self.running = True
        self.registro = Guardado(nombre_nivel, game, game.identificador)
        self.tablero_completo = None

        self.mostrar_mensaje_progreso = False  # Controla si se debe mostrar el mensaje
        self.tiempo_mensaje_progreso = 0       # Registra el tiempo para mostrar el mensaje
        self.mostrar_mensaje_ayudas = False
        self.tiempo_mensaje_ayudas = 0
        
        self.boton_volver = Boton(image=None, pos=(600, 100), text_input="Volver al menú",font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO)
        self.boton_deshacer = Boton(image=None, pos=(600, 180), text_input="Deshacer", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO)
        self.boton_rehacer = Boton(image=None, pos=(600, 260), text_input="Rehacer", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO)
        self.boton_guardar = Boton(image=None, pos=(600, 340), text_input="Guardar", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO)
        self.boton_ayuda = Boton(image=None, pos=(600, 420), text_input=f"Ayuda ({self.game.ayudas})", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO)
        self.boton_mostrar_solucion = Boton(image=None, pos=(600, 500), text_input="Mostrar solución", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO)
        self.boton_reiniciar = Boton(image=None, pos=(600, 580), text_input="Reiniciar nivel", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO)

    def guardar_progreso(self):
        try:
            self.registro.Save_progress()
            self.mostrar_mensaje_progreso = True
            self.tiempo_mensaje_progreso = time.time()
        except Exception as e:
            print(f"Error al guardar el progreso: {e}")

    def ayudas(self):
        if self.game.ayudas == 0:
            self.mostrar_mensaje_ayudas = True
            self.tiempo_mensaje_ayudas = time.time()
        else:
            self.game.help()
        
    def run(self):
        while self.running:
            actualizar_grid_fondo_menu()
            self.pantalla.fill(BLANCO)
            dibujar_grid_fondo_menu(self.pantalla, 50, 50, 16, ROJO, BLANCO)
            pygame.display.set_caption("Nonograma Game")
            texto_nivel = f"Nivel {self.nombre_nivel}"
            mostrar_texto(texto_nivel, NEGRO, self.pantalla, 110, 40, fuente=pygame.font.SysFont(None, 35))

            #boton con texto dinamico
            boton_ayuda = Boton(image=None, pos=(600, 420), text_input=f"Ayuda ({self.game.ayudas})", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO)

            texto_vidas = f"Vidas: {self.game.vidas}"
            mostrar_texto(texto_vidas, ROJO, self.pantalla, 75, 75, fuente=pygame.font.SysFont(None, 28))

            if self.game.vidas == 0:
                self.running = False
                return 'ventana_derrota'
            
            menu_mouse_pos = pygame.mouse.get_pos()
            eventos = pygame.event.get()

            for boton in [self.boton_volver, self.boton_deshacer, self.boton_rehacer, self.boton_guardar, boton_ayuda, self.boton_mostrar_solucion, self.boton_reiniciar]:
                boton.changeColor(menu_mouse_pos)
                boton.update(self.pantalla)

            for evento in eventos:
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
                        self.guardar_progreso()
                    if boton_ayuda.checkInput(menu_mouse_pos):
                        self.ayudas()
                        boton_ayuda.changeText(f"Ayuda ({self.game.ayudas})")
                    if self.boton_mostrar_solucion.checkInput(menu_mouse_pos):
                        self.game.toggle_mostrar_solucion()
                    if self.boton_reiniciar.checkInput(menu_mouse_pos):
                        self.game.reset()


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
                        mostrar_texto(str(num), NEGRO, self.pantalla,
                                      offset_x + j * tamano_celda + tamano_celda // 2,
                                      offset_y - 40 - len(columna) * 15 + k * 25)


            # Mostrar el mensaje de confirmación si está activo
            if self.mostrar_mensaje_progreso:
                mostrar_texto("Progreso guardado", VERDE_PRESIONADO, self.pantalla, 270, 480)
                # Desactiva el mensaje después de 2 segundos
                if time.time() - self.tiempo_mensaje_progreso > 2:
                    self.mostrar_mensaje_progreso = False

            if self.mostrar_mensaje_ayudas:
                mostrar_texto("No tienes más ayudas", NEGRO, self.pantalla, 270, 530)
                # Desactiva el mensaje después de 2 segundos
                if time.time() - self.tiempo_mensaje_ayudas > 2:
                    self.mostrar_mensaje_ayudas = False

            # Correr lógica del juego
            if self.game.run(self.pantalla, *game_position, eventos):
                self.tablero_completo = self.game.board
                self.running = False

            pygame.display.flip()  # Actualizar pantalla en cada iteración

        pygame.display.flip()
        return 'ventana_victoria', self.tablero_completo
