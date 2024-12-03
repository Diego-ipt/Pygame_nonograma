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
            self.state = 1

    def toggle_flag(self):
        if self.state != 1:  # Solo permite bandera si no está clickeada
            self.state = 2

    def get_color(self):
        if self.state == 2: # Bandera
            return BLANCO # Volver al color blanco para que la X sea visible
        return NEGRO if self.state == 1 else BLANCO

class Board:
    def __init__(self, grid_size, cell_size, matriz_solucion):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.board = self.create_empty_board()
        self.matriz_solucion = matriz_solucion

    def create_empty_board(self):
        return [[Cell() for _ in range(self.grid_size)] for _ in range(self.grid_size)]


    def draw(self, surface, mostrar_solucion=False):
        for row, rowOfCells in enumerate(self.board):
            for col, cell in enumerate(rowOfCells):
                if mostrar_solucion:
                    # Dibuja usando la matriz solución
                    color = NEGRO if self.matriz_solucion[row][col] == 1 else BLANCO
                    pygame.draw.rect(surface, color, (col * self.cell_size + 1, row * self.cell_size + 1, self.cell_size - 2, self.cell_size - 2))
                else:
                    # Dibuja usando el estado actual del tablero
                    color = cell.get_color()
                    pygame.draw.rect(surface, color, (col * self.cell_size + 1, row * self.cell_size + 1, self.cell_size - 2, self.cell_size - 2))
                    if cell.state == 2: # Dibuja una X para las celdas marcadas con bandera
                        thickness = 6 # Ajusta el grosor de las líneas diagonales
                        pygame.draw.line(surface, NEGRO, (col * self.cell_size + 1, row * self.cell_size + 1), (col * self.cell_size + self.cell_size - 1, row * self.cell_size + self.cell_size - 1), thickness)
                        pygame.draw.line(surface, NEGRO, (col * self.cell_size + self.cell_size - 1, row * self.cell_size + 1), (col * self.cell_size + 1, row * self.cell_size + self.cell_size - 1), thickness)

    def reset(self):
        self.board = self.create_empty_board()


    # Retorna una matriz que refleja el estado actual de las celdas:
    # 0: Desmarcada
    # 1: Clickeada
    # 2: Bandera
    def get_matrix(self):
        return [[cell.state for cell in row] for row in self.board]


     # Crear una matriz que refleja el estado actual de las celdas excluyendo el estado de banderas. Se ocupa para comparar la solucion final con la actual:
        # 0: Desmarcada o Bandera
        # 1: Clickeada
    def get_matriz_actual(self):
        return [[1 if cell.state == 1 else 0 for cell in row] for row in self.board]
    
    
    def handle_click(self, pos):
        row = int(pos[1] // self.cell_size)
        col = int(pos[0] // self.cell_size)
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            previous_state = self.board[row][col].state

            if previous_state == 2:
                es_correcto = True
            else:
                self.board[row][col].click()

                es_correcto = (self.matriz_solucion[row][col] == 1 and self.board[row][col].state == 1) or \
                            (self.matriz_solucion[row][col] == 0 and self.board[row][col].state == 0)
            if not es_correcto:
                # Corrige el estado al correcto y retorna que hubo un error
                if self.matriz_solucion[row][col] == 1:
                    self.board[row][col].state = 1  # Debió ser negra
                else:
                    self.board[row][col].state = 2  # Debió ser bandera (X)

                return (row, col, previous_state, self.board[row][col].state, False)

            return (row, col, previous_state, self.board[row][col].state, True)

    def handle_flag(self, pos):
        row = int(pos[1] // self.cell_size)
        col = int(pos[0] // self.cell_size)
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            previous_state = self.board[row][col].state

            if previous_state == 1:
                es_correcto = True
            else:
                self.board[row][col].toggle_flag()

                # Verificar si la bandera es correcta
                es_correcto = self.matriz_solucion[row][col] == 0 and self.board[row][col].state == 2

            if not es_correcto:
                # Corrige el estado al correcto y retorna que hubo un error
                if self.matriz_solucion[row][col] == 1:
                    self.board[row][col].state = 1  # Debió ser negra
                else:
                    self.board[row][col].state = 0  # Debió ser blanca
                return (row, col, previous_state, self.board[row][col].state, False)

            return (row, col, previous_state, self.board[row][col].state, True)



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
        self.ayudas = 3
        self.vidas = 3

    def draw_text(self, text, position):
        text_surface = self.font.render(text, True, (255, 0, 0))
        self.surface.blit(text_surface, position)

    def toggle_mostrar_solucion(self):
        self.mostrar_solucion = not self.mostrar_solucion
        if self.mostrar_solucion == True:
            self.won = True
        else:
            if self.board.get_matriz_actual() == self.board.matriz_solucion:
                self.won = True
            else:
                self.won = False

    # def handle_events(self, events, offset):
    #     for event in events:
    #         if event.type == pygame.QUIT:
    #             self.running = False
    #         elif event.type == pygame.MOUSEBUTTONDOWN:
    #             pos = (event.pos[0] - offset[0], event.pos[1] - offset[1])
    #             if 0 <= pos[0] < self.window_size and 0 <= pos[1] < self.window_size:
    #                 if event.button == 1:  # Click izquierdo
    #                     change = self.board.handle_click(pos)
    #                     if change:
    #                         self.stack.push(change)
    #                         if self.board.get_matriz_actual() == self.board.matriz_solucion:
    #                             self.won = True
    #                         else:
    #                             self.won = False
    #                 elif event.button == 3:  # Click derecho
    #                     change = self.board.handle_flag(pos)
    #                     if change:
    #                         self.stack.push(change)
    #                         if self.board.get_matriz_actual() == self.board.matriz_solucion:
    #                             self.won = True
    #                         else:
    #                             self.won = False
        
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
                            row, col, prev_state, new_state, es_correcto = change
                            if new_state != prev_state:
                                self.stack.push((row, col, prev_state, new_state))
                            if not es_correcto:  # Si fue incorrecto
                                self.vidas -= 1
                            
                            self.won = self.board.get_matriz_actual() == self.board.matriz_solucion
  
                    elif event.button == 3:  # Click derecho (bandera)
                        change = self.board.handle_flag(pos)
                        if change:
                            row, col, prev_state, new_state, es_correcto = change
                            if new_state != prev_state:
                                self.stack.push((row, col, prev_state, new_state))
                            if not es_correcto:  # Si fue incorrecto
                                self.vidas -= 1
                            self.won = self.board.get_matriz_actual() == self.board.matriz_solucion


    def reset(self):
        self.board.reset()
        self.won = False
        self.stack.clear()
        self.stack_redo.clear()
        self.vidas = 3
        # print("Tablero reiniciado")
        # for row in self.board.get_matrix():
        #     print(row)
        # print("\n")

    def run(self, main_window, x, y, events):
        self.surface.fill(GRIS)
        #se añade la opcion para mostrar solucion
        self.board.draw(self.surface, mostrar_solucion=self.mostrar_solucion)
        if self.running:
            self.handle_events(events, (x, y))
            main_window.blit(self.surface, (x, y))
        if self.won:
            main_window.blit(self.surface, (x, y))
            return True
        return False
    
    def getCellSize(self):
        return self.cell_size
    
    def deshacer(self):
        if self.stack.size() > 0:
            row, col, prev_state, _ = self.stack.pop()
            self.stack_redo.push((row, col, self.board.board[row][col].state, prev_state))
            self.board.board[row][col].state = prev_state
            if self.board.get_matriz_actual() == self.board.matriz_solucion:
                self.won = True
            else:
                self.won = False

    def rehacer(self):
        if self.stack_redo.size() > 0:
             # Obtener los valores desde la pila de redo
            row, col, current_state, prev_state = self.stack_redo.pop()

            # Restaurar el estado de la celda al estado "rehacer"
            current_cell = self.board.board[row][col]
            self.stack.push((row, col, current_cell.state, prev_state))  # Guardar el estado actual en undo
            current_cell.state = current_state  # Aplicar el estado almacenado
            if self.board.get_matriz_actual() == self.board.matriz_solucion:
                self.won = True
            else:
                self.won = False

    # def help(self):
    #     matriz_diferencias = [[0 for _ in range(self.board.grid_size)] for _ in range(self.board.grid_size)]
    #     for j in range(self.board.grid_size):
    #         for i in range(self.board.grid_size):
    #             matriz_diferencias[i][j] = [self.board.matriz_solucion[i][j] - self.board.board[i][j].clicked]

    #     for j in range(self.board.grid_size):
    #         for i in range(self.board.grid_size):
    #             neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
    #             valid_neighbors = [(x, y) for x, y in neighbors if 0 <= x < self.board.grid_size and 0 <= y < self.board.grid_size]
    #     valid_positions = []
    #     for instancia in valid_neighbors:
    #         x, y = instancia
    #         if matriz_diferencias[x][y] != 0:
    #             valid_positions.append(instancia)

    #     if valid_positions:
    #         instancia_rand = random.choice(valid_positions)
    #         x, y = instancia_rand
    #         self.board.board[x][y].click()
    #     else:
    #         valid_positions = [(i, j) for i in range(self.board.grid_size) for j in range(self.board.grid_size) if matriz_diferencias[i][j] != 0]
    #         if valid_positions:
    #             instancia_rand = random.choice(valid_positions)
    #             x, y = instancia_rand
    #             self.board.board[x][y].click()
    #         else:
    #             print("Ya ganaste")

    def help(self):
        matriz_actual = self.board.get_matriz_actual()
        matriz_solucion = self.board.matriz_solucion

        # Buscar casillas que están cerca de las ya seleccionadas y que pertenecen a la solución
        posibles_casillas = []

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if matriz_actual[i][j] == 1:  # Casilla ya seleccionada por el jugador
                    # Buscar vecinos válidos
                    vecinos = [ (i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                    for x, y in vecinos:
                        if (0 <= x < self.grid_size and 0 <= y < self.grid_size and matriz_actual[x][y] == 0 and matriz_solucion[x][y] == 1):
                            posibles_casillas.append((x, y))

        # Si hay casillas candidatas, elegir una aleatoria
        if posibles_casillas:
            x, y = random.choice(posibles_casillas)
            self.board.board[x][y].click()
        else:
            # Si no hay vecinos cercanos válidos, buscar cualquier casilla no seleccionada de la solución
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    if matriz_actual[i][j] == 0 and matriz_solucion[i][j] == 1:
                        posibles_casillas.append((i, j))

            if posibles_casillas:
                x, y = random.choice(posibles_casillas)
                self.board.board[x][y].click()
            else:
                self.won = True

        if self.board.get_matriz_actual() == matriz_solucion:
            self.won = True
        else:
            self.ayudas = self.ayudas - 1

