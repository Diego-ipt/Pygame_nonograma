from elementos_menus import *
from colores import *

# Cargar fotogramas
fotogramas = cargar_fotogramas("frames")
indice_fotograma = 0
fps_animacion = 10  # Velocidad de cambio de fotogramas
reloj = pygame.time.Clock()

# Configuramos la cuadrícula
filas = 20
columnas = 20
tamano_celda = 40
grid_estado = [[False for _ in range(columnas)] for _ in range(filas)]

def menu_principal(cambiar_ventana):
    global indice_fotograma

    # Actualizar el estado de la cuadrícula
    actualizar_grid(grid_estado)

    # Dibuja el fondo con la cuadrícula
    pantalla.fill(BLANCO)
    dibujar_grid(pantalla, filas, columnas, tamano_celda, NEGRO, BLANCO, grid_estado)

    mostrar_texto("Menú Principal", fuente, NEGRO, pantalla, 400, 100)
    boton("Elegir Partida", 270, 200, 260, 60, GRIS, AZUL_OSCURO, pantalla, lambda: cambiar_ventana('elegir_partida'))
    boton("Crear Nonograma", 270, 300, 260, 60, GRIS, AZUL_OSCURO, pantalla, lambda: cambiar_ventana('crear_nonograma'))

    # Animación de fotogramas si están disponibles
    if len(fotogramas) > 0:
        pantalla.blit(fotogramas[indice_fotograma], (-50, 100))
        pantalla.blit(fotogramas[indice_fotograma], (500, 100))
        indice_fotograma = (indice_fotograma + 1) % len(fotogramas)
    else:
        print("Error: No se han cargado los fotogramas")

    reloj.tick(fps_animacion)

def ventana_elegir_partida(cambiar_ventana):
    pantalla.fill(GRIS)
    mostrar_texto("Elegir Partida", fuente, NEGRO, pantalla, 400, 100)
    boton("Volver al menú", 300, 400, 200, 60, GRIS, AZUL_OSCURO, pantalla, lambda: cambiar_ventana('menu_principal'))

def ventana_crear_nonograma(cambiar_ventana):
    pantalla.fill(GRIS)
    mostrar_texto("Crear Nonograma", fuente, NEGRO, pantalla, 400, 100)
    boton("Volver al menú", 300, 400, 200, 60, GRIS, AZUL_OSCURO, pantalla, lambda: cambiar_ventana('menu_principal'))
