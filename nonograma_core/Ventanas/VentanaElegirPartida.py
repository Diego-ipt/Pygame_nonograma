import json
from nonograma_core.Elementos_graficos.elementos_menus import *
import os
from nonograma_core.Elementos_graficos.colores import *
from nonograma_core.Logica.tablero_nonograma import *
from nonograma_core.Logica.nonograma_numeros import *
from nonograma_core.Ventanas.VentanaBase import *


class VentanaElegirPartida(VentanaBase):
    def __init__(self, pantalla, cambiar_ventana):
        super().__init__(pantalla, cambiar_ventana)

    def iniciar_juego(self, partida_seleccionada):
        game = partida_seleccionada  # Reinicia el juego
        game.running = True
        self.cambiar_ventana('ventana_nonograma_game', game)

    def get_levels_name(self, carpeta_elegida="size_5"):
        base_dir = os.path.join("levels", "Lvl_base", carpeta_elegida)
        levels = []
        for file in os.listdir(base_dir):
            if file.endswith(".json"):
                with open(os.path.join(base_dir, file), 'r') as f:
                    level_data = json.load(f)
                    levels.append(level_data["Name"])
        return levels
    
    def get_levels_file(self, carpeta_elegida="size_5"):
        base_dir = os.path.join("levels", "Lvl_base", carpeta_elegida)
        levels = []
        for file in os.listdir(base_dir):
            if file.endswith(".json"):
                with open(os.path.join(base_dir, file), 'r') as f:
                    levels.append(file)
        return levels

    def dibujar(self):
        self.pantalla.fill(GRIS)
        mostrar_texto("Elegir Partida", fuente, NEGRO, self.pantalla, 400, 100)
        boton("Volver al menú", 300, 400, 200, 60, GRIS, AZUL_OSCURO, self.pantalla, lambda: self.cambiar_ventana('menu_principal'))

        lvl_list=[self.get_levels_name(),self.get_levels_file()]
        # Mostrar lista de niveles
        seleccion = mostrar_lista_nombres(self.pantalla, lvl_list[0], 100, 150, 600, 50, GRIS, AZUL_OSCURO, NEGRO, fuente)
        file_lvl = None
        if seleccion is not None:
            try:
                index = lvl_list[0].index(seleccion)
                file_lvl = lvl_list[1][index]
            except ValueError:
                pass
    
        if seleccion is not None:
            if file_lvl is not None:       
                # Cargar los datos del nivel seleccionado
                with open(os.path.join("levels", "Lvl_base", "size_5", file_lvl)) as file:
                    level_data = json.load(file)
        
                # Crear una instancia de Game con los datos del nivel seleccionado
                grid_size = level_data['grid_size']
                matriz_solucion = level_data['diseno']
                game = Game(grid_size=grid_size, matriz_solucion=matriz_solucion)
                print(seleccion)
                self.iniciar_juego(game)
