import pygame
import os
import json
from enum import Enum
from nonograma_core.Elementos_graficos.colores import *

class SettingsManager(Enum):
    MIN_GRID_SIZE = 5
    MAX_GRID_SIZE = 10
    CELL_SIZE = 30
    DEFAULT_COLOR = (255, 255, 255)
    CLICKED_COLOR = (0, 0, 0)
    BACKGROUND_COLOR = VERDE_PRESIONADO
    BUTTON_COLOR = (200, 200, 200)
    BUTTON_TEXT_COLOR = (0, 0, 0)

class Cell:
    def __init__(self):
        self.clicked = False

    def click(self):
        self.clicked = not self.clicked

    def get_color(self):
        return SettingsManager.CLICKED_COLOR.value if self.clicked else SettingsManager.DEFAULT_COLOR.value

class CreatorBoard:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.board = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]

    def draw(self, surface, cell_size):
        for row, rowOfCells in enumerate(self.board):
            for col, cell in enumerate(rowOfCells):
                color = cell.get_color()
                pygame.draw.rect(surface, color, (col * cell_size + 1, row * cell_size + 1, cell_size - 2, cell_size - 2))

    #Maneja el click en el tablero
    def handle_click(self, pos, cell_size):
        row = int(pos[1] // cell_size)
        col = int(pos[0] // cell_size)
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            self.board[row][col].click()

    #Redimensiona el tablero
    def resize(self, new_grid_size):
        self.grid_size = new_grid_size
        self.board = [[Cell() for _ in range(new_grid_size)] for _ in range(new_grid_size)]

    #devuelve el tablero , false es blanco y true negro
    def getBoardClicked(self):
        return [[cell.clicked for cell in row] for row in self.board]

#Botones utilizados para reducir y aumentar el tamano del tablero
# class SizeSaveButton:
#     def  __init__(self, x, y, width, height, text, action, image = None,test_flag = None):
#         self.rect = pygame.Rect(x, y, width, height)
#         self.text = text
#         self.action = action
#         self.image = image
#         if (not test_flag): #No se puede usar pygame en el test
#             self.font = pygame.font.Font(None, 32)
#
#
#     def draw(self, surface):
#         pygame.draw.rect(surface, SettingsManager.BUTTON_COLOR.value, self.rect)
#         if self.image:
#             image_rect = self.image.get_rect(center=self.rect.center)
#             surface.blit(self.image, image_rect)
#         else:
#             text_surface = self.font.render(self.text, True, SettingsManager.BUTTON_TEXT_COLOR.value)
#             text_rect = text_surface.get_rect(center=self.rect.center)
#             surface.blit(text_surface, text_rect)
#
#     def isClicked(self, pos):
#         return self.rect.collidepoint(pos)

class CreatorWindow:
    def __init__(self, grid_size=SettingsManager.MIN_GRID_SIZE.value, window_size = 300):
        pygame.init()
        # variables de tamaño
        self.cell_size = window_size / grid_size
        self.grid_size = grid_size
        self.window_size = window_size
        self.clock = pygame.time.Clock()
        self.surface = pygame.Surface((self.window_size, self.window_size))
        self.creator_board = CreatorBoard(self.grid_size)
        self.running = True
        self.font = pygame.font.Font(None, 74)

        # Asset manager para cargar imagenes
        # self.asset_manager = AssetManager()
        # self.iconoSave = self.asset_manager.cargar_imagen("SaveIcon.jpg")

        # Iniciar ejecucion

        # self.size_buttons = [SizeSaveButton(self.windows_width - 100, 50, 50, 50, '+', self.increaseGrid),
        #                      SizeSaveButton(self.windows_width - 100, 150, 50, 50, '-', self.decreaseGrid),
        #                      SizeSaveButton(self.windows_width - 100, 250, 50, 50, 'Save', self.saveDesign, self.iconoSave),
        #                      SizeSaveButton(self.windows_width - 100, 350, 100, 100, 'Volver al menu', self.volverAlMenu)
        #                      ]

    #Incrementa el tamano del tablero
    def increaseGrid(self):
        if self.grid_size < SettingsManager.MAX_GRID_SIZE.value:
            self.grid_size += 1
            self.cell_size = self.window_size / self.grid_size
            self.creator_board.resize(self.grid_size)

    #Decrementa el tamano del tablero
    def decreaseGrid(self):
        if self.grid_size > SettingsManager.MIN_GRID_SIZE.value:
            self.grid_size -= 1
            self.cell_size = self.window_size / self.grid_size
            self.creator_board.resize(self.grid_size)

    def saveDesign(self, test_name = None):
        print("Guardando diseño")
        # Obtiene el diseño actual del tablero
        design = self.creator_board.getBoardClicked()

        # Ruta base calculada en función del archivo actual
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio del archivo actual
        base_dir = os.path.join(script_dir, "..", "levels", "game_levels")

        # Crea el directorio si no existe
        if not os.path.exists(base_dir):
            print(f"Creando el directorio: {base_dir}")
            os.makedirs(base_dir)

        #para debugear
        if test_name:
            name_nivel = f"{test_name}.json"

        else:
        # Encuentra el siguiente número disponible para el archivo de nivel
            num_nivel = 1
            while os.path.exists(os.path.join(base_dir, f"nivel_{num_nivel}.json")):
                num_nivel += 1

            # Nombre del archivo
            name_nivel = f"nivel_{num_nivel}.json"

        file_path = os.path.join(base_dir, name_nivel)

        nivel_info = {
            "nivel": name_nivel if test_name else num_nivel,
            "diseno": design
        }

        # Guarda el diseño en un archivo JSON
        with open(file_path, 'w') as file:
            json.dump(nivel_info, file)

        print(f"{name_nivel} Guardado en {file_path}")
        return name_nivel

    def handle_events(self, events, offset):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = (event.pos[0] - offset[0], event.pos[1] - offset[1])
                if 0 <= pos[0] < self.window_size and 0 <= pos[1] < self.window_size:
                    self.creator_board.handle_click(pos, self.cell_size)

    def run(self, main_window, x, y, events):
        if self.running:
            self.handle_events(events, (x,y))
        self.surface.fill(GRIS)
        self.creator_board.draw(self.surface, self.cell_size)
        main_window.blit(self.surface, (x, y))
        return False


