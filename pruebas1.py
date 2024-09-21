import pygame
import sys
import os

# Inicializar Pygame
pygame.init()

# Definir algunos colores
AZUL_CLARO = (173, 216, 230)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
AZUL_OSCURO = (50, 50, 150)

# Tamaño de la pantalla
ancho_pantalla = 800
alto_pantalla = 600
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))

# Definir fuente de texto
fuente = pygame.font.SysFont(None, 40)

# Cargar los fotogramas del GIF 
def cargar_fotogramas(directorio):
    fotogramas = []
    for archivo in sorted(os.listdir(directorio)):
        if archivo.endswith('.png'):  # Cambia a '.jpg' si usas imágenes JPG
            img = pygame.image.load(os.path.join(directorio, archivo))
            fotogramas.append(img)
    return fotogramas

fotogramas = cargar_fotogramas("Proyecto_programacion_nonograma/frames")
indice_fotograma = 0
fps_animacion = 10  # Velocidad de cambio de fotogramas
reloj = pygame.time.Clock()

# Función para mostrar texto en la pantalla
def mostrar_texto(texto, fuente, color, pantalla, x, y):
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect(center=(x, y))
    pantalla.blit(superficie_texto, rect_texto)

# Función para los botones
def boton(texto, x, y, ancho, alto, color_claro, color_oscuro, accion=None):
    raton = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + ancho > raton[0] > x and y + alto > raton[1] > y:
        pygame.draw.rect(pantalla, color_oscuro, (x, y, ancho, alto))
        if click[0] == 1 and accion is not None:
            accion()  # Llama a la función asociada con el botón
    else:
        pygame.draw.rect(pantalla, color_claro, (x, y, ancho, alto))

    mostrar_texto(texto, fuente, NEGRO, pantalla, x + (ancho // 2), y + (alto // 2))

def menu_principal():
    global indice_fotograma
    pantalla.fill(BLANCO)
    mostrar_texto("Menú Principal", fuente, NEGRO, pantalla, 400, 100)
    boton("Elegir Partida", 270, 200, 260, 60, GRIS, AZUL_OSCURO, lambda: cambiar_ventana('elegir_partida'))
    boton("Crear Nonograma", 270, 300, 260, 60, GRIS, AZUL_OSCURO, lambda: cambiar_ventana('crear_nonograma'))
    
    # Verificar si los fotogramas están correctamente cargados
    if len(fotogramas) > 0:
        pantalla.blit(fotogramas[indice_fotograma], (-50, 100))
        pantalla.blit(fotogramas[indice_fotograma], (500, 100))
        indice_fotograma = (indice_fotograma + 1) % len(fotogramas)
    else:
        print("Error: No se han cargado los fotogramas")
    
    reloj.tick(fps_animacion)


def ventana_elegir_partida():
    pantalla.fill(BLANCO)  # Fondo blanco
    mostrar_texto("Elegir Partida", fuente, NEGRO, pantalla, 400, 100)
    boton("Volver al menú", 300, 400, 200, 60, GRIS, AZUL_OSCURO, lambda: cambiar_ventana('menu_principal'))

def ventana_crear_nonograma():
    pantalla.fill(BLANCO)  # Fondo blanco
    mostrar_texto("Crear Nonograma", fuente, NEGRO, pantalla, 400, 100)
    boton("Volver al menú", 300, 400, 200, 60, GRIS, AZUL_OSCURO, lambda: cambiar_ventana('menu_principal'))

# Variable global para manejar el estado actual de la ventana
estado_actual = 'menu_principal'

def cambiar_ventana(nuevo_estado):
    global estado_actual
    print(f"Cambiando a ventana: {nuevo_estado}")
    estado_actual = nuevo_estado

# Bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Llamar a la función correspondiente según el estado actual
    if estado_actual == 'menu_principal':
        menu_principal()
    elif estado_actual == 'elegir_partida':
        ventana_elegir_partida()
    elif estado_actual == 'crear_nonograma':
        ventana_crear_nonograma()

    pygame.display.update()
