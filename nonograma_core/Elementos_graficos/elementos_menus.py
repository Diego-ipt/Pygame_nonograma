import pygame

# Función para mostrar texto en la pantalla
def mostrar_texto(texto, color, pantalla, x, y, fuente=pygame.font.SysFont(None, 40)):
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect(center=(x, y))
    pantalla.blit(superficie_texto, rect_texto)

class Boton:
    def __init__(self, image, pos, text_input, font, base_color, hover_color, rect_padding= (10,10)):
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

    def changeText(self, text):
        self.text_input = text
        self.text = self.font.render(str(self.text_input), True, "black")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

class PopUp:
    def __init__(self, pos, size, message, font, base_color, text_color, border_radius=10, padding=20):
        self.x_pos, self.y_pos = pos
        self.width, self.height = size
        self.message = message
        self.font = font
        self.base_color = base_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.padding = padding
        self.text = self.font.render(self.message, True, self.text_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos - size[1] // 4))  # Texto en la parte superior
        self.rect = pygame.Rect(
            self.x_pos - self.width // 2, self.y_pos - self.height // 2, self.width, self.height
        )
        self.is_active = False
        self.buttons = []

        self.lines = self._wrap_text()

    def _wrap_text(self):
        words = self.message.split(' ')
        lines = []
        current_line = ""

        for word in words:
            # Prueba añadir la palabra a la línea actual
            test_line = f"{current_line} {word}".strip()
            line_width, _ = self.font.size(test_line)

            if line_width + self.padding * 2 <= self.width:
                current_line = test_line
            else:
                # La línea actual está llena; agrega y empieza una nueva
                lines.append(current_line)
                current_line = word

        # Agrega la última línea si hay texto
        if current_line:
            lines.append(current_line)

        return lines

    def add_button(self, button):
        self.buttons.append(button)
        self.arrange_buttons()

    def update(self, screen):

        pygame.draw.rect(screen, self.base_color, self.rect, border_radius=self.border_radius)

        line_height = self.font.size("Tg")[1]  # Altura de una línea de texto
        start_y = self.rect.top + self.padding

        for i, line in enumerate(self.lines):
            line_surface = self.font.render(line, True, self.text_color)
            line_rect = line_surface.get_rect(center=(self.x_pos, start_y + i * line_height))
            screen.blit(line_surface, line_rect)

        # Dibujar los botones
        for button in self.buttons:
            button.update(screen)

    def arrange_buttons(self):
        if not self.buttons:
            return

        total_width = sum(button.rect.width for button in self.buttons) + 20 * (len(self.buttons) - 1)
        start_x = self.x_pos - total_width // 2 - 20
        y_pos = self.y_pos + self.height // 4

        for button in self.buttons:
            button.rect.center = (start_x + button.rect.width // 2, y_pos)
            button.text_rect.center = button.rect.center
            button.hitbox = pygame.Rect(
                button.text_rect.left - button.rect_padding[0],
                button.text_rect.top - button.rect_padding[1],
                button.text_rect.width + 2 * button.rect_padding[0],
                button.text_rect.height + 2 * button.rect_padding[1]
            )
            start_x += button.rect.width + 60

    def activar(self):
        self.is_active = True

    def desactivar(self):
        self.is_active = False


def mostrar_fotogramas(fotogramas, indice_fotograma, contador, retraso, x, y, pantalla):
    if len(fotogramas) > 0:
        if contador >= retraso:
            indice_fotograma = (indice_fotograma + 1) % len(fotogramas)
            contador = 0
        pantalla.blit(fotogramas[indice_fotograma], (x, y))
        contador += 1
        return indice_fotograma, contador
    else:
        print("Error: No se han cargado los fotogramas")
        return indice_fotograma, contador
