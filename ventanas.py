from elementos_menus import *
from colores import *
from ventana_nonograma import *
from nonograma_numeros import *

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
    boton("Jugar", 300, 500, 200, 60, GRIS, AZUL_OSCURO, pantalla, lambda: cambiar_ventana('ventana_nonograma_game'))

def ventana_crear_nonograma(cambiar_ventana):
    pantalla.fill(GRIS)
    mostrar_texto("Crear Nonograma", fuente, NEGRO, pantalla, 400, 100)
    boton("Volver al menú", 300, 400, 200, 60, GRIS, AZUL_OSCURO, pantalla, lambda: cambiar_ventana('menu_principal'))

def ventana_nonograma_game(cambiar_ventana):
    pygame.init()
    pygame.display.set_caption("Nonograma Game")
    clock = pygame.time.Clock()
    game = Game()
    filas, columnas = procesar_matriz(game.board.matriz_solucion)
    game_position = (150, 150)  # Position of the game within the main window
    pantalla.fill(ROJO)  # Fill the main window with a background color
    # Calcular las posiciones de los números de las filas y columnas
    tamano_celda = 30  # Tamaño de cada celda del tablero
    offset_x = game_position[0]
    offset_y = game_position[1]
    # Dibujar los números de las filas
    for i, fila in enumerate(filas):
        mostrar_texto(str(fila), fuente, NEGRO, pantalla, offset_x - 20, offset_y + i * tamano_celda + tamano_celda // 2)

    # Dibujar los números de las columnas
    for j, columna in enumerate(columnas):
        mostrar_texto(str(columna), fuente, NEGRO, pantalla, offset_x + j * tamano_celda + tamano_celda // 2, offset_y - 20)


    running = True
    while running:
        if game.run(pantalla, *game_position):
            running = False
            cambiar_ventana('ventana_victoria')
        pygame.display.flip()
        clock.tick(60)

def ventana_victoria(cambiar_ventana):
    pantalla.fill(GRIS)
    mostrar_texto("¡Ganaste!", fuente, NEGRO, pantalla, 400, 100)
    boton("Volver al menú", 300, 400, 200, 60, GRIS, AZUL_OSCURO, pantalla, lambda: cambiar_ventana('menu_principal'))