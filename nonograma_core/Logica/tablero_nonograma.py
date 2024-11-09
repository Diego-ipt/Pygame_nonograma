import pygame
from nonograma_core.Elementos_graficos.colores import *
from nonograma_core.Logica.queueYStack import *
from enum import Enum
#default
class SettingsManager(Enum):
    GRID_SIZE = 10
    DEFAULT_COLOR = (255, 255, 255)
    CLICKED_COLOR = (0, 0, 0)
    BACKGROUND_COLOR = (0, 0, 0)
    matriz_solucion = [[1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


class Cell:
    def __init__(self):
        self.clicked = 0

    def click(self):
        if self.clicked == 1:
            self.clicked = 0
        else:
            self.clicked = 1

    def get_color(self):
        return NEGRO if self.clicked==1 else BLANCO

class Board:
    def __init__(self, grid_size, cell_size, matriz_solucion):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.board = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]
        self.matriz_solucion = matriz_solucion

    def draw(self, surface):
        for row, rowOfCells in enumerate(self.board):
            for col, cell in enumerate(rowOfCells):
                color = cell.get_color()
                pygame.draw.rect(surface, color, (col * self.cell_size + 1, row * self.cell_size + 1, self.cell_size - 2, self.cell_size - 2))
            
    def get_matrix(self):
        # Retorna una matriz con 1 si la celda está clicada y 0 si no
        return [[int(cell.clicked) for cell in row] for row in self.board]
            
    def handle_click(self, pos):
        row = int(pos[1] // self.cell_size)
        col = int(pos[0] // self.cell_size)
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            self.board[row][col].click()
            # Obtener y mostrar la matriz actualizada en tiempo real (para depuración)
            matrix = self.get_matrix()
            # Puedes imprimir la matriz para depuración
            for fila in matrix:
                print(fila)
            if(matrix == self.matriz_solucion):
                print("GANASTE")
                return True
        return False

class Game:
    def __init__(self, grid_size=SettingsManager.GRID_SIZE.value, window_size=300, matriz_solucion=SettingsManager.matriz_solucion.value, identificador=None):
        pygame.init()
        self.cell_size = window_size / grid_size
        self.grid_size = grid_size
        self.window_size = window_size
        self.surface = pygame.Surface((self.window_size, self.window_size))
        self.clock = pygame.time.Clock()
        self.board = Board(grid_size, self.cell_size, matriz_solucion)
        self.running = True
        self.font = pygame.font.Font(None, 74)
        self.won = False
        self.stack = Stack()
        self.stack_redo = Stack()
        self.identificador = identificador

    def draw_text(self, text, position):
        text_surface = self.font.render(text, True, (255, 0, 0))
        self.surface.blit(text_surface, position)

    def handle_events(self, events, offset):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = (event.pos[0] - offset[0], event.pos[1] - offset[1])
                if 0 <= pos[0] < self.window_size and 0 <= pos[1] < self.window_size:
                    if self.board.handle_click(pos):
                        self.won = True
                    self.stack.push(pos)

    def run(self, main_window, x, y, events):
        if self.running == True:
            self.handle_events(events, (x, y))
        self.surface.fill(GRIS)
        self.board.draw(self.surface)
        if self.won:
            return True
        main_window.blit(self.surface, (x, y))
        return False
    
    def getCellSize(self):
        return self.cell_size
    
    def deshacer(self):
        if(self.stack.size() > 0):
            pos_aux = self.stack.pop()
            self.stack_redo.push(pos_aux)
            self.board.handle_click(pos_aux)

    def rehacer(self):
        if(self.stack_redo.size() > 0):
            pos_aux = self.stack_redo.pop()
            self.stack.push(pos_aux)
            self.board.handle_click(pos_aux)

# def main():
#     pygame.init()
#     main_window_size = (600, 600)
#     main_window = pygame.display.set_mode(main_window_size)
#     pygame.display.set_caption("Main Window")
#     clock = pygame.time.Clock()
#     game = Game()
#     game_position = (150, 150)  # Position of the game within the main window

#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#         main_window.fill((200, 200, 200))  # Fill the main window with a background color
#         game.run(main_window, *game_position)
#         pygame.display.flip()
#         clock.tick(60)

#     pygame.quit()

# if __name__ == "__main__":
#     main()