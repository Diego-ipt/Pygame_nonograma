import pygame
from nonograma_core.Elementos_graficos.colores import *
from nonograma_core.Logica.queueYStack import *
from enum import Enum
import random
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
        self.state = 0  # 0: Desmarcada, 1: Clickeada, 2: Bandera

    def click(self):
        if self.state != 2:  # Solo permite clic si no está marcada con bandera
            self.state = 1 if self.state == 0 else 0

    def toggle_flag(self):
        if self.state != 1:  # Solo permite bandera si no está clickeada
            self.state = 2 if self.state == 0 else 0

    def get_color(self):
        if self.state == 2:  # Bandera
            return ROJO
        return NEGRO if self.state == 1 else BLANCO

class Board:
    def __init__(self, grid_size, cell_size, matriz_solucion):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.board = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]
        self.matriz_solucion = matriz_solucion

    def draw(self, surface, mostrar_solucion=False):
        for row, rowOfCells in enumerate(self.board):
            for col, cell in enumerate(rowOfCells):
                if mostrar_solucion:
                    # Dibuja usando la matriz solución
                    color = NEGRO if self.matriz_solucion[row][col] == 1 else BLANCO
                else:
                    # Dibuja usando el estado actual del tablero
                    color = cell.get_color()
                pygame.draw.rect(surface, color, (col * self.cell_size + 1, row * self.cell_size + 1, self.cell_size - 2, self.cell_size - 2))


    # Retorna una matriz que refleja el estado actual de las celdas:
    # 0: Desmarcada
    # 1: Clickeada
    # 2: Bandera
    def get_matrix(self):
        return [[cell.state for cell in row] for row in self.board]

    def handle_click(self, pos):
        row = int(pos[1] // self.cell_size)
        col = int(pos[0] // self.cell_size)
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            previous_state = self.board[row][col].state
            self.board[row][col].click()
            return (row, col, previous_state, self.board[row][col].state)

    def handle_flag(self, pos):
        row = int(pos[1] // self.cell_size)
        col = int(pos[0] // self.cell_size)
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            previous_state = self.board[row][col].state
            self.board[row][col].toggle_flag()
            return (row, col, previous_state, self.board[row][col].state)
        

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
        self.mostrar_solucion = False  # Atributo para alternar entre solución y estado actual

    def draw_text(self, text, position):
        text_surface = self.font.render(text, True, (255, 0, 0))
        self.surface.blit(text_surface, position)

    def toggle_mostrar_solucion(self):
        self.mostrar_solucion = not self.mostrar_solucion
        if self.mostrar_solucion == True:
            self.won = True
        else:
            self.won = False

    def handle_events(self, events, offset):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = (event.pos[0] - offset[0], event.pos[1] - offset[1])
                if 0 <= pos[0] < self.window_size and 0 <= pos[1] < self.window_size:
                    if event.button == 1:  # Click izquierdo
                        change = self.board.handle_click(pos)
                        if change:
                            self.stack.push(change)
                            if self.board.get_matrix() == self.board.matriz_solucion:
                                self.won = True
                    elif event.button == 3:  # Click derecho
                        change = self.board.handle_flag(pos)
                        if change:
                            self.stack.push(change)
    

    def run(self, main_window, x, y, events):
        self.surface.fill(GRIS)
        #se añade la opcion para mostrar solucion
        self.board.draw(self.surface, mostrar_solucion=self.mostrar_solucion) 
        if self.running:
            self.handle_events(events, (x, y))
            main_window.blit(self.surface, (x, y))
        if self.won:
            return True
        return False
    
    def getCellSize(self):
        return self.cell_size
    
    def deshacer(self):
        if self.stack.size() > 0:
            row, col, prev_state, _ = self.stack.pop()
            self.stack_redo.push((row, col, self.board.board[row][col].state, prev_state))
            self.board.board[row][col].state = prev_state

    def rehacer(self):
        if self.stack_redo.size() > 0:
             # Obtener los valores desde la pila de redo
            row, col, current_state, prev_state = self.stack_redo.pop()
            
            # Restaurar el estado de la celda al estado "rehacer"
            current_cell = self.board.board[row][col]
            self.stack.push((row, col, current_cell.state, prev_state))  # Guardar el estado actual en undo
            current_cell.state = current_state  # Aplicar el estado almacenado
        
    def help(self):
        matriz_diferencias = [[0 for _ in range(self.board.grid_size)] for _ in range(self.board.grid_size)]
        for j in range(self.board.grid_size):
            for i in range(self.board.grid_size):
                matriz_diferencias[i][j] = [self.board.matriz_solucion[i][j] - self.board.board[i][j].clicked]

        for j in range(self.board.grid_size):
            for i in range(self.board.grid_size):
                neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                valid_neighbors = [(x, y) for x, y in neighbors if 0 <= x < self.board.grid_size and 0 <= y < self.board.grid_size]
        valid_positions = []
        for instancia in valid_neighbors:
            x, y = instancia
            if matriz_diferencias[x][y] != 0:
                valid_positions.append(instancia)

        if valid_positions:
            instancia_rand = random.choice(valid_positions)
            x, y = instancia_rand
            self.board.board[x][y].click()
        else:
            valid_positions = [(i, j) for i in range(self.board.grid_size) for j in range(self.board.grid_size) if matriz_diferencias[i][j] != 0]
            if valid_positions:
                instancia_rand = random.choice(valid_positions)
                x, y = instancia_rand
                self.board.board[x][y].click()
            else:
                print("Ya ganaste")

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