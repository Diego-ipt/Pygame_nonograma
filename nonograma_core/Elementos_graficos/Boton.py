import pygame
import sys

class Boton:
    def __init__(self, image, pos, text_input, font, base_color, hover_color):
        ''''''
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hover_color = base_color, hover_color
        self.curr_color = base_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, "black")
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos,self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.rect_padding = 10

    def update(self, screen):
        rect = pygame.Rect(
            self.text_rect.left - self.rect_padding,
            self.text_rect.top - self.rect_padding,
            self.text_rect.width + 2 * self.rect_padding,
            self.text_rect.height + 2 * self.rect_padding
        )
        pygame.draw.rect(screen, self.curr_color, rect, border_radius=5)

        #Soporte para imagen de fondo de boton
        if self.image is not None:
            screen.blit(self.image, self.rect)

        screen.blit(self.text, self.text_rect)

    def checkInput(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            self.curr_color = self.hover_color
        else:
            self.curr_color = self.base_color