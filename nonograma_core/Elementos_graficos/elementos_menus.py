import pygame

# Función para mostrar texto en la pantalla
def mostrar_texto(texto, color, pantalla, x, y, fuente=pygame.font.SysFont(None, 40)):
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect(center=(x, y))
    pantalla.blit(superficie_texto, rect_texto)

class Boton:
    def __init__(self, image, pos, text_input, font, base_color, hover_color, rect_padding= (10,10)):
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
        self.rect_padding = rect_padding

        self.hitbox = pygame.Rect(
            self.text_rect.left - self.rect_padding[0],
            self.text_rect.top - self.rect_padding[1],
            self.text_rect.width + 2 * self.rect_padding[0],
            self.text_rect.height + 2 * self.rect_padding[1]
        )

    def update(self, screen):

        pygame.draw.rect(screen, self.curr_color, self.hitbox, border_radius=5)

        #Soporte para imagen de fondo de boton
        if self.image is not None:
            screen.blit(self.image, self.rect)

        screen.blit(self.text, self.text_rect)

    def checkInput(self, pos):
        return self.hitbox.collidepoint(pos)

    def changeColor(self, pos):
        if self.hitbox.collidepoint(pos):
            self.curr_color = self.hover_color
        else:
            self.curr_color = self.base_color
