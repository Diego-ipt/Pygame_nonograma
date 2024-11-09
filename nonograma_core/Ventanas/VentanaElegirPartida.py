import json
import os
from nonograma_core.Logica.tablero_nonograma import Game
from nonograma_core.Ventanas.VentanaBase import VentanaBase
from nonograma_core.Elementos_graficos.elementos_menus import *
from nonograma_core.Elementos_graficos.colores import *
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
    def __init__(self, pantalla, cambiar_ventana):
        super().__init__(pantalla, cambiar_ventana)
        self.dificultades = ["size_5", "size_7", "size_10"]
        self.indice_dificultad = 0 #para simular arreglo circular
        self.niveles = self.cargar_niveles()
        self.nombre_nivel_elegido = ""
        self.confirmando = False #para mostrar la ventana de confirmacion
        self.selectt = False #para confirmar si se selecciono un boton
        self.eleccion = False   #para confirmar si se desea cargar el progreso
        self.search = Search_progress()
        
    def seleccion_boton(self):
        self.selectt = True

    def iniciar_ventana_confirmacion(self):
        self.confirmando = True

    def rechazo(self):
        self.seleccion_boton()
        self.eleccion=False
        self.confirmando = False
    
    def acepta(self):
        self.seleccion_boton()
        self.eleccion=True
        self.confirmando = False

    def ventana_confirmacion(self):
        confirm_width, confirm_height = 350, 150

        confirm_rect = pygame.Rect((ancho_pantalla // 2 - confirm_width // 2, alto_pantalla // 2 - confirm_height // 2), (confirm_width, confirm_height))

        pygame.draw.rect(self.pantalla, NEGRO, confirm_rect)
        mostrar_texto("¿desea cargar el progreso?", pygame.font.SysFont(None, 36), BLANCO, self.pantalla, ancho_pantalla // 2, alto_pantalla // 2 - 20)

        boton("Sí", confirm_rect.left + 55, confirm_rect.top + 80, 80, 40, VERDE, VERDE_PRESIONADO, self.pantalla, self.acepta)
        boton("No", confirm_rect.right - 140, confirm_rect.top + 80, 80, 40, ROJO, ROJO_PRESIONADO, self.pantalla, self.rechazo)

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
        self.cambiar_ventana('ventana_nonograma_game', game, self.nombre_nivel_elegido)

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


        if self.confirmando:
            self.ventana_confirmacion()


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
        self.nombre_nivel_elegido = nombre_nivel

        #search level selected
        typelvl = "base" #cambiar cuando se eliga nivel personalizado    
        id= (str(level_data['nivel']) + "_" + str(level_data['grid_size'])+"_"+typelvl) 

        game = Game(grid_size=grid_size, matriz_solucion=matriz_solucion, identificador=id)
        self.search.Search(id)

        if(self.search.avance != None):
            self.iniciar_ventana_confirmacion()
            if self.selectt:
                if self.eleccion:
                    for row in range(grid_size):
                        for col in range(grid_size):
                            game.board.board[row][col].clicked = self.search.avance[row][col]
                    self.iniciar_juego(game)
                else:
                    self.iniciar_juego(game)
        else:
            self.iniciar_juego(game)