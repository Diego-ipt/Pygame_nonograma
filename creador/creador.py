import pygame
from enum import Enum
from nonograma_core.colores import *

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
    def __init__(self, grid_size, cell_size, x_offset = 0, y_offset = 0):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.board = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]

    def draw(self, surface):
        for row, rowOfCells in enumerate(self.board):
            for col, cell in enumerate(rowOfCells):
                color = cell.get_color()
                pygame.draw.rect(surface, color, (
                self.x_offset + col * self.cell_size + 1,
                self.y_offset + row * self.cell_size + 1,
                self.cell_size - 2,
                self.cell_size - 2))

    def handle_click(self, pos):
        row = (pos[1] - self.y_offset) // self.cell_size
        col = (pos[0] - self.x_offset) // self.cell_size
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            self.board[row][col].click()

    #Redimensiona el tablero
    def resize(self, new_grid_size):
        self.grid_size = new_grid_size
        self.board = [[Cell() for _ in range(new_grid_size)] for _ in range(new_grid_size)]

    #Calcula los offsets de nuevo para centrarlo al cambiar tamano
    def centerBoard(self, window_width, window_height):
        board_width = self.grid_size * self.cell_size
        board_height = self.grid_size * self.cell_size
        self.x_offset = (window_width - board_width) // 2
        self.y_offset = (window_height - board_height) // 2

    def getBoardClicked(self):
        return [[cell.clicked for cell in row] for row in self.board]

#Botones utilizados para reducir y aumentar el tamano del tablero
class SizeSaveButton:
    def  __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        if (text != "Test"): #No se puede usar pygame en el test
            self.font = pygame.font.Font(None, 32)


    def draw(self, surface):
        pygame.draw.rect(surface, SettingsManager.BUTTON_COLOR.value, self.rect)
        text_surface = self.font.render(self.text, True, SettingsManager.BUTTON_TEXT_COLOR.value)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def isClicked(self, pos):
        return self.rect.collidepoint(pos)

class CreatorWindow:
    def __init__(self, grid_size=SettingsManager.MAX_GRID_SIZE.value, cell_size=SettingsManager.CELL_SIZE.value):
        pygame.init()
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.windows_width = 700
        self.windows_height = 500
        self.window = pygame.display.set_mode((self.windows_width, self.windows_height))
        self.clock = pygame.time.Clock()
        self.creator_board = CreatorBoard(grid_size, cell_size, 50, 50)
        self.running = True
        self.size_buttons = [SizeSaveButton(self.windows_width - 100, 50, 50, 50, '+', self.increaseGrid),
                             SizeSaveButton(self.windows_width - 100, 150, 50, 50, '-', self.decreaseGrid),
                             SizeSaveButton(self.windows_width - 100, 150, 50, 50, '-', self.saveDesign)
                             ]

    def increaseGrid(self):
        if self.grid_size < SettingsManager.MAX_GRID_SIZE.value:
            self.grid_size += 1
            self.creator_board.resize(self.grid_size)
            self.creator_board.centerBoard(self.windows_width, self.windows_height)

    #Incrementa el tamano del tablero
    def decreaseGrid(self):
        if self.grid_size > SettingsManager.MIN_GRID_SIZE.value:
            self.grid_size -= 1
            self.creator_board.resize(self.grid_size)
            self.creator_board.centerBoard(self.windows_width, self.windows_height)

    def saveDesign(self):
        print("Guardando diseño")


    #Decrementa el tamano del tablero
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if self.creator_board.x_offset <= pos[0] < self.creator_board.x_offset + self.grid_size * self.cell_size and \
                        self.creator_board.y_offset <= pos[1] < self.creator_board.y_offset + self.grid_size * self.cell_size:
                    self.creator_board.handle_click(event.pos)
                else:
                    for button in self.size_buttons:
                        if button.isClicked(pos):
                            button.action()

    def run(self):
        while self.running:
            self.clock.tick(120)
            self.handle_events()
            self.window.fill(SettingsManager.BACKGROUND_COLOR.value)
            self.creator_board.draw(self.window)
            self.creator_board.centerBoard(self.windows_width, self.windows_height)
            for button in self.size_buttons:
                button.draw(self.window)
            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    game = CreatorWindow()
    game.run()


