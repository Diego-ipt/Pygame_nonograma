import json
import os
import sys

import pygame.font

from nonograma_core.Ventanas.VentanaBase import VentanaBase
from nonograma_core.Elementos_graficos.colores import *
from nonograma_core.JuegoNonograma import ANCHO_PANTALLA, ALTO_PANTALLA
from nonograma_core.Elementos_graficos.elementos_menus import *
from nonograma_core.Logica.registros import *

def get_levels_name(dificultad_elegida, custom=False):
    folder = "custom_levels" if custom else "base_levels"
    base_dir = os.path.join("levels", folder, dificultad_elegida)
    levels = []
    if os.path.exists(base_dir):
        for file in os.listdir(base_dir):
            if file.endswith(".json"):
                with open(os.path.join(base_dir, file), 'r') as f:
                    level_data = json.load(f)
                    levels.append(level_data["Name"] if "Name" in level_data else level_data["nivel"])
    return levels

def get_levels_file(dificultad_elegida, custom=False):
    folder = "custom_levels" if custom else "base_levels"
    base_dir = os.path.join("levels", folder, dificultad_elegida)
    levels = []
    if os.path.exists(base_dir):
        for file in os.listdir(base_dir):
            if file.endswith(".json"):
                levels.append(file)
    return levels

class VentanaElegirPartida(VentanaBase):
    def __init__(self, pantalla):
        self.pantalla = pantalla

        self.dificultades = ["size_5","size_6", "size_7", "size_8", "size_9", "size_10"]
        self.indice_dificultad = 0 #para simular arreglo circular
        self.niveles = self.cargar_niveles()
        self.nombre_nivel_elegido = ""

        self.search = Search_progress()
        self.custom_toogle = False
        self.game = None

        #Botones menu
        self.boton_volver = Boton(image=None, pos=(ANCHO_PANTALLA / 2, 550), text_input="Volver al menú", font=pygame.font.SysFont(None, 36), base_color=VIOLETA_MENU, hover_color=FUCSIA)
        self.boton_izq = Boton(image=None, pos=(ANCHO_PANTALLA / 2 - 150, 100), text_input="<", font=pygame.font.SysFont(None, 36), base_color=VIOLETA_MENU, hover_color=FUCSIA)
        self.boton_der = Boton(image=None, pos=(ANCHO_PANTALLA / 2 + 150, 100), text_input=">", font=pygame.font.SysFont(None, 36), base_color=VIOLETA_MENU, hover_color=FUCSIA)

        self.boton_niveles_personalizados = Boton(image=None, pos=(100, 100), text_input="Personalizados", font=pygame.font.SysFont(None, 30), base_color=VIOLETA_MENU, hover_color=FUCSIA)
        self.boton_niveles_base = Boton(image=None, pos=(100, 100), text_input="Niveles Base", font=pygame.font.SysFont(None, 30), base_color=VIOLETA_MENU, hover_color=FUCSIA)

        self.boton_niveles_actuales = self.boton_niveles_personalizados

        #Popup de confirmacion
        self.popup_guardado = PopUp(pos=(400, 300), size=(300, 150), message="Se ha encontrado una partida en progreso, quieres cargar?", font=pygame.font.SysFont(None, 36), base_color=NEGRO, text_color=BLANCO)
        self.boton_si = Boton(image=None, pos=(ANCHO_PANTALLA / 2 - 150, 100), text_input="Si", font=pygame.font.SysFont(None, 36), base_color=VERDE, hover_color=VERDE_PRESIONADO)
        self.boton_no = Boton(image=None, pos=(ANCHO_PANTALLA / 2 - 150, 100), text_input="No", font=pygame.font.SysFont(None, 36), base_color=ROJO, hover_color=ROJO_PRESIONADO)
        self.popup_guardado.add_button(self.boton_si)
        self.popup_guardado.add_button(self.boton_no)
        self.popup_guardado.desactivar()

    def cambiar_dificultad(self, direccion):
        #-1 para izquierda, 1 para derecha
        self.indice_dificultad = (self.indice_dificultad + direccion) % len(self.dificultades)
        self.niveles = self.cargar_niveles(self.custom_toogle)

    def cargar_niveles(self, custom = False):
        dificultad_actual = self.dificultades[self.indice_dificultad]
        if custom:
            return [get_levels_name(dificultad_actual, True), get_levels_file(dificultad_actual, True)]
        else:
            return [get_levels_name(dificultad_actual), get_levels_file(dificultad_actual)]

    def toogle_niveles(self):
        self.custom_toogle = not self.custom_toogle
        self.niveles = self.cargar_niveles(custom=self.custom_toogle)

        if self.custom_toogle:
            self.boton_niveles_actuales = self.boton_niveles_base
        else:
            self.boton_niveles_actuales = self.boton_niveles_personalizados

    def cargar_partida(self):
        print("cargando partida en progreso..")
        for row in range(self.game.board.grid_size):
            for col in range(self.game.board.grid_size):
                if self.search.avance[row][col] != 0:
                    self.game.board.board[row][col].click()
                print(self.search.avance[row][col], end=" ")
        return self.iniciar_juego(self.game)

    def run(self):
        while True:
            actualizar_grid_fondo_menu()
            self.pantalla.fill(BLANCO)
            dibujar_grid_fondo_menu(self.pantalla, 50, 50, 16, NEGRO, BLANCO_MENU)
            menu_mouse_pos = pygame.mouse.get_pos()

            if self.popup_guardado.is_active:
                self.popup_guardado.update(self.pantalla)
                for evento in pygame.event.get():
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if self.boton_si.checkInput(menu_mouse_pos):
                            self.popup_guardado.desactivar()
                            return self.cargar_partida()

                        if self.boton_no.checkInput(menu_mouse_pos):
                            self.popup_guardado.desactivar()
                            return self.iniciar_juego(self.game)
            else:
                for boton in [self.boton_izq, self.boton_der, self.boton_volver, self.boton_niveles_actuales]:
                    boton.changeColor(menu_mouse_pos)
                    boton.update(self.pantalla)

                #mostrar dificultas
                dificultad_texto = self.dificultades[self.indice_dificultad].replace("size_", "") + "x" + self.dificultades[self.indice_dificultad].replace("size_", "")
                mostrar_texto(dificultad_texto, NEGRO, self.pantalla, 400, 100)

                niveles_nombres = self.niveles[0]
                botones_niveles = []
                for i, nombre in enumerate(niveles_nombres[:15]):  # Maximo 15 niveles
                    x = 150 + (i % 5) * 130  # Posición en X para cada columna
                    y = 180 + (i // 5) * 100  # Posición en Y para cada fila
                    boton_nivel = Boton(image=None, pos=(x,y), text_input=str(nombre), font=pygame.font.SysFont(None,24), base_color=CIAN, hover_color=AZUL_CLARO)
                    boton_nivel.changeColor(menu_mouse_pos)
                    boton_nivel.update(self.pantalla)
                    botones_niveles.append((boton_nivel, nombre))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.boton_izq.checkInput(menu_mouse_pos):
                            self.cambiar_dificultad(-1)
                        if self.boton_der.checkInput(menu_mouse_pos):
                            self.cambiar_dificultad(1)
                        if self.boton_niveles_actuales.checkInput(menu_mouse_pos):
                            self.toogle_niveles()
                        if self.boton_volver.checkInput(menu_mouse_pos):
                            return 'menu_principal'


                        for boton, nombre in botones_niveles:
                            if boton.checkInput(menu_mouse_pos):
                                if self.seleccionar_nivel(nombre):
                                    return self.iniciar_juego(self.game)

            pygame.display.update()

    def seleccionar_nivel(self, nombre_nivel):
        # Encuentra el archivo correspondiente al nivel seleccionado
        index = self.niveles[0].index(nombre_nivel)
        file_lvl = self.niveles[1][index]
        dificultad_actual = self.dificultades[self.indice_dificultad]

        lvl_type = "custom_levels" if self.custom_toogle else "base_levels"

        with open(os.path.join("levels", lvl_type , dificultad_actual, file_lvl)) as file:
            level_data = json.load(file)

        # Crear una instancia de Game con los datos del nivel seleccionado
        grid_size = level_data['grid_size']
        matriz_solucion = level_data['diseno']
        self.nombre_nivel_elegido = nombre_nivel

        tipo_nivel = "base"
        id = f"{level_data['nivel']}_{level_data['grid_size']}_{tipo_nivel}"

        self.game = Game(grid_size=grid_size, matriz_solucion=matriz_solucion, identificador=id)

        if self.search.Search(id):
            self.popup_guardado.activar()
        else:
            return True

    def iniciar_juego(self, partida_seleccionada):
        game = partida_seleccionada  # Reinicia el juego
        game.running = True
        return 'ventana_nonograma_game', game, self.nombre_nivel_elegido
