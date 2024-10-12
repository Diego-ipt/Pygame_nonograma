from NonogramaCore.elementos_menus import *
from NonogramaCore.colores import *
from NonogramaCore.ventana_nonograma import *
from NonogramaCore.nonograma_numeros import *
from NonogramaCore.AssetManager import AssetManager


# Cargador de recursos
asset_manager = AssetManager()

# Cargar fotogramas
snake = asset_manager.cargar_fotogramas("serpiente")
menu = asset_manager.cargar_fotogramas("menu")
trophy = asset_manager.cargar_fotogramas("trofeo_win")
indice_fotograma_snake = 0
indice_fotograma_menu = 0
indice_fotograma_trophy = 0
reloj = pygame.time.Clock()
grid_estado= [[False for _ in range(50)] for _ in range(50)]
def menu_principal(cambiar_ventana):
    global indice_fotograma_snake
    global indice_fotograma_menu
    # Actualizar el estado de la cuadrícula
    actualizar_grid(grid_estado)

    # Dibuja el fondo con la cuadrícula
    pantalla.fill(BLANCO)
    dibujar_grid(pantalla, 50, 50, 16, NEGRO, BLANCO_MENU, grid_estado)

    indice_fotograma_menu=mostrar_fotogramas(menu, indice_fotograma_menu, 75, 0,pantalla)

    boton("Elegir Partida", 270, 350, 260, 60, VIOLETA_MENU, FUCSIA, pantalla, lambda: cambiar_ventana('elegir_partida'))
    boton("Crear Nonograma", 270, 450, 260, 60, VIOLETA_MENU, FUCSIA, pantalla, lambda: cambiar_ventana('crear_nonograma'))

    # Animación de fotogramas si están disponibles
    # if len(snake) > 0:
    #     pantalla.blit(snake[indice_fotograma_snake], (-50, 100))
    #     pantalla.blit(snake[indice_fotograma_snake], (500, 100))
    #     indice_fotograma_snake = (indice_fotograma_snake + 1) % len(snake)
    # else:
    #     print("Error: No se han cargado los fotogramas")

    reloj.tick(10)

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
    game_position = (150, 150)  
    pantalla.fill(ROJO)  
    

    tamano_celda = 30  
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
    global indice_fotograma_trophy

    pantalla.fill(VIOLETA_MENU)
    indice_fotograma_trophy=mostrar_fotogramas(trophy, indice_fotograma_trophy, 170, 100,pantalla)
    mostrar_texto("¡Ganaste!", fuente, NEGRO, pantalla, 400, 100)
    boton("Volver al menú", 310, 400, 200, 60, NOTHING, FUCSIA, pantalla, lambda: cambiar_ventana('menu_principal'))

    reloj.tick(30)