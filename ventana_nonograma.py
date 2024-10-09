import pygame
from enum import Enum

class SettingsManager(Enum):
    GRID_SIZE = 10
    CELL_SIZE = 30
    DEFAULT_COLOR = (255, 255, 255)
    CLICKED_COLOR = (0, 0, 0)
    BACKGROUND_COLOR = (0, 0, 0)
    matriz_solucion = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


class Cell:
    def __init__(self):
        self.clicked = 0

    def click(self):
        self.clicked = 1

    def get_color(self):
        return SettingsManager.CLICKED_COLOR.value if self.clicked else SettingsManager.DEFAULT_COLOR.value
    
    def is_clicked(self):
        return self.clicked

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
        return [[int(cell.is_clicked()) for cell in row] for row in self.board]
            
    def handle_click(self, pos):
        row = pos[1] // self.cell_size
        col = pos[0] // self.cell_size
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
    def __init__(self, grid_size=SettingsManager.GRID_SIZE.value, cell_size=SettingsManager.CELL_SIZE.value, matriz_solucion=SettingsManager.matriz_solucion.value):
        pygame.init()
        self.window_size = grid_size * cell_size
        self.window = pygame.display.set_mode((self.window_size, self.window_size))
        self.clock = pygame.time.Clock()
        self.board = Board(grid_size, cell_size, matriz_solucion)
        self.running = True
        self.font = pygame.font.Font(None, 74)
        self.won = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.board.handle_click(event.pos):
                    self.won = True

    def draw_text(self, text, position):
        text_surface = self.font.render(text, True, (255, 0, 0))
        self.window.blit(text_surface, position)

    def run(self):
        while self.running:
            self.clock.tick(120)
            self.handle_events()
            self.window.fill(SettingsManager.BACKGROUND_COLOR.value)
            self.board.draw(self.window)
            if self.won:
                self.draw_text("GANASTE", (self.window_size // 4, self.window_size // 2))
            pygame.display.flip()
        pygame.quit()

# Ejecución del juego
if __name__ == "__main__":
    game = Game()
    game.run()