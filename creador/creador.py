import pygame
from enum import Enum

class SettingsManager(Enum):
    MIN_GRID_SIZE = 5
    MAX_GRID_SIZE = 10
    CELL_SIZE = 30
    DEFAULT_COLOR = (255, 255, 255)
    CLICKED_COLOR = (0, 0, 0)
    BACKGROUND_COLOR = (0, 0, 0)
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
    def __init__(self, grid_size, cell_size):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.board = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]

    def draw(self, surface):
        for row, rowOfCells in enumerate(self.board):
            for col, cell in enumerate(rowOfCells):
                color = cell.get_color()
                pygame.draw.rect(surface, color, (
                col * self.cell_size + 1, row * self.cell_size + 1, self.cell_size - 2, self.cell_size - 2))

    def handle_click(self, pos):
        row = pos[1] // self.cell_size
        col = pos[0] // self.cell_size
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            self.board[row][col].click()

    def resize(self, new_grid_size):
        self.grid_size = new_grid_size
        self.board = [[Cell() for _ in range(new_grid_size)] for _ in range(new_grid_size)]

class SizeButton:
    def  __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, SettingsManager.BUTTON_COLOR.value, self.rect)
        text_surface = self.font.render(self.text, True, SettingsManager.BUTTON_TEXT_COLOR.value)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def isClicked(self, pos):
        return self.rect.collidepoint(pos)

class Game:
    def __init__(self, grid_size=SettingsManager.MAX_GRID_SIZE.value, cell_size=SettingsManager.CELL_SIZE.value):
        pygame.init()
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.windows_width = 700
        self.windows_height = 500
        self.window = pygame.display.set_mode((self.windows_width, self.windows_height))
        self.clock = pygame.time.Clock()
        self.board = CreatorBoard(grid_size, cell_size)
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.board.handle_click(event.pos)

    def run(self):
        while self.running:
            self.clock.tick(120)
            self.handle_events()
            self.window.fill(SettingsManager.BACKGROUND_COLOR.value)
            self.board.draw(self.window)
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()


