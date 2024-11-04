import json
import os
from nonograma_core.Logica.tablero_nonograma import Game
from nonograma_core.Ventanas.VentanaBase import VentanaBase
from nonograma_core.Elementos_graficos.elementos_menus import *
from nonograma_core.Elementos_graficos.colores import *

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
    def __init__(self, pantalla, cambiar_ventana):
        super().__init__(pantalla, cambiar_ventana)
        self.dificultades = ["size_5", "size_7", "size_10"]
        self.indice_dificultad = 0 #para simular arreglo circular
        self.niveles = self.cargar_niveles()

    def cambiar_dificultad(self, direccion):
        #-1 para izquierda, 1 para derecha
        self.indice_dificultad = (self.indice_dificultad + direccion) % len(self.dificultades)
        self.niveles = self.cargar_niveles()

    def cargar_niveles(self):
        dificultad_actual = self.dificultades[self.indice_dificultad]
        return [get_levels_name(dificultad_actual), get_levels_file(dificultad_actual)]

    def iniciar_juego(self, partida_seleccionada):
        game = partida_seleccionada  # Reinicia el juego
        game.running = True
        self.cambiar_ventana('ventana_nonograma_game', game)

    def dibujar(self):
        self.pantalla.fill(GRIS)
        mostrar_texto("Elegir Partida", fuente, NEGRO, self.pantalla, 400, 50)

        # Flechas de navegación de dificultad
        boton("<", 250, 100, 50, 50, GRIS, AZUL_OSCURO, self.pantalla, lambda: self.cambiar_dificultad(-1))
        boton(">", 500, 100, 50, 50, GRIS, AZUL_OSCURO, self.pantalla, lambda: self.cambiar_dificultad(1))

        # Mostrar la dificultad actual
        dificultad_texto = self.dificultades[self.indice_dificultad].replace("size_", "") + "x" + self.dificultades[self.indice_dificultad].replace("size_", "")
        mostrar_texto(dificultad_texto, fuente, NEGRO, self.pantalla, 400, 130)

        # Botón para volver al menú principal
        boton("Volver al menú", 300, 500, 200, 60, GRIS, AZUL_OSCURO, self.pantalla, lambda: self.cambiar_ventana('menu_principal'))

        # dibujar una cuadrícula para mostrar niveles
        niveles_nombres = self.niveles[0]
        for i, nombre in enumerate(niveles_nombres[:15]):  # Maximo 15 niveles
            x = 150 + (i % 5) * 100  # Posición en X para cada columna
            y = 180 + (i // 5) * 100  # Posición en Y para cada fila
            boton(nombre, x, y, 80, 80, GRIS, AZUL_OSCURO, self.pantalla, lambda n=nombre: self.seleccionar_nivel(n), font=pygame.font.SysFont(None, 20))

    def seleccionar_nivel(self, nombre_nivel):
        # Encuentra el archivo correspondiente al nivel seleccionado
        index = self.niveles[0].index(nombre_nivel)
        file_lvl = self.niveles[1][index]

        # Cargar los datos del nivel seleccionado
        dificultad_actual = self.dificultades[self.indice_dificultad]
        with open(os.path.join("levels", "base_levels", dificultad_actual, file_lvl)) as file:
            level_data = json.load(file)

        # Crear una instancia de Game con los datos del nivel seleccionado
        grid_size = level_data['grid_size']
        matriz_solucion = level_data['diseno']
        game = Game(grid_size=grid_size, matriz_solucion=matriz_solucion)
        self.iniciar_juego(game)
