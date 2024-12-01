import json
import os
import sys

import pygame.font

from nonograma_core.Ventanas.VentanaBase import VentanaBase
from nonograma_core.Elementos_graficos.colores import *
from nonograma_core.JuegoNonograma import ANCHO_PANTALLA, ALTO_PANTALLA
from nonograma_core.Elementos_graficos.elementos_menus import mostrar_texto, Boton
from nonograma_core.Logica.registros import *



def get_levels_name(carpeta_elegida):
    base_dir = os.path.join("levels", "base_levels", carpeta_elegida)
    levels = []
    if os.path.exists(base_dir):
        for file in os.listdir(base_dir):
            if file.endswith(".json"):
                with open(os.path.join(base_dir, file), 'r') as f:
                    level_data = json.load(f)
                    levels.append(level_data["Name"])
    return levels

def get_levels_file(carpeta_elegida):
    base_dir = os.path.join("levels", "base_levels", carpeta_elegida)
    levels = []
    if os.path.exists(base_dir):
        for file in os.listdir(base_dir):
            if file.endswith(".json"):
                levels.append(file)
    return levels

class VentanaElegirPartida(VentanaBase):
    def __init__(self, pantalla):
        self.pantalla = pantalla

        self.dificultades = ["size_5", "size_7", "size_10"]
        self.indice_dificultad = 0 #para simular arreglo circular
        self.niveles = self.cargar_niveles()
        self.nombre_nivel_elegido = ""

        self.confirmando = False #para mostrar la ventana de confirmacion
        self.search = Search_progress()
        self.bandera_search = False
        self.game = None

        self.boton_volver = Boton(image=None, pos=(ANCHO_PANTALLA / 2, 550), text_input="Volver al menú", font=pygame.font.SysFont(None, 36), base_color=VIOLETA_MENU, hover_color=FUCSIA)
        self.boton_izq = Boton(image=None, pos=(ANCHO_PANTALLA / 2 - 150, 100), text_input="<", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO)
        self.boton_der = Boton(image=None, pos=(ANCHO_PANTALLA / 2 + 150, 100), text_input=">", font=pygame.font.SysFont(None, 36), base_color=GRIS, hover_color=AZUL_OSCURO)

    def cambiar_dificultad(self, direccion):
        #-1 para izquierda, 1 para derecha
        self.indice_dificultad = (self.indice_dificultad + direccion) % len(self.dificultades)
        self.niveles = self.cargar_niveles()

    def cargar_niveles(self):
        dificultad_actual = self.dificultades[self.indice_dificultad]
        return [get_levels_name(dificultad_actual), get_levels_file(dificultad_actual)]

    def run(self):
        boton_si, boton_no = None, None
        while True:
            self.pantalla.fill(GRIS)
            menu_mouse_pos = pygame.mouse.get_pos()

            #flechas de dificultad

            for boton in [self.boton_izq, self.boton_der, self.boton_volver]:
                boton.changeColor(menu_mouse_pos)
                boton.update(self.pantalla)

            #mostrar dificultas
            dificultad_texto = self.dificultades[self.indice_dificultad].replace("size_", "") + "x" + self.dificultades[self.indice_dificultad].replace("size_", "")
            mostrar_texto(dificultad_texto, NEGRO, self.pantalla, 400, 100)

            niveles_nombres = self.niveles[0]
            botones_niveles = []
            for i, nombre in enumerate(niveles_nombres[:15]):  # Maximo 15 niveles
                x = 150 + (i % 5) * 100  # Posición en X para cada columna
                y = 180 + (i // 5) * 100  # Posición en Y para cada fila
                boton_nivel = Boton(image=None, pos=(x,y), text_input=nombre, font=pygame.font.SysFont(None,24), base_color=GRIS, hover_color=AZUL_OSCURO)
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
                    if self.boton_volver.checkInput(menu_mouse_pos):
                        return 'menu_principal'

                    for boton, nombre in botones_niveles:
                        if boton.checkInput(menu_mouse_pos):
                            return self.seleccionar_nivel(nombre)

            pygame.display.update()

    def seleccionar_nivel(self, nombre_nivel):
        # Encuentra el archivo correspondiente al nivel seleccionado
        index = self.niveles[0].index(nombre_nivel)
        file_lvl = self.niveles[1][index]
        dificultad_actual = self.dificultades[self.indice_dificultad]

        with open(os.path.join("levels", "base_levels", dificultad_actual, file_lvl)) as file:
            level_data = json.load(file)

        # Crear una instancia de Game con los datos del nivel seleccionado
        grid_size = level_data['grid_size']
        matriz_solucion = level_data['diseno']
        self.nombre_nivel_elegido = nombre_nivel

        tipo_nivel = "base"
        id = f"{level_data['nivel']}_{level_data['grid_size']}_{tipo_nivel}"

        self.game = Game(grid_size=grid_size, matriz_solucion=matriz_solucion, identificador=id)

        if self.search.Search(id):
            self.confirmando = True
            self.bandera_search = True

        return self.iniciar_juego(self.game)

    def iniciar_juego(self, partida_seleccionada):
        game = partida_seleccionada  # Reinicia el juego
        game.running = True
        return 'ventana_nonograma_game', game, self.nombre_nivel_elegido
