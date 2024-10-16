import sys
import pygame
from nonograma_core.Elementos_graficos.elementos_menus import *
from nonograma_core.Elementos_graficos.colores import *
from nonograma_core.Logica.tablero_nonograma import *
from nonograma_core.Logica.nonograma_numeros import *
from nonograma_core.Elementos_graficos.AssetManager import AssetManager

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
grid_estado = [[False for _ in range(50)] for _ in range(50)]

confirmando = False  # Controla si se muestra la ventana de confirmación

def menu_principal(cambiar_ventana):
    global indice_fotograma_menu, confirmando

    # Actualizar el estado de la cuadrícula
    actualizar_grid(grid_estado)

    # Dibuja el fondo con la cuadrícula
    pantalla.fill(BLANCO)
    dibujar_grid(pantalla, 50, 50, 16, NEGRO, BLANCO_MENU, grid_estado)

    indice_fotograma_menu = mostrar_fotogramas(menu, indice_fotograma_menu, 75, 0, pantalla)

    boton("Elegir Partida", 270, 350, 260, 60, VIOLETA_MENU, FUCSIA, pantalla, lambda: cambiar_ventana('elegir_partida'))
    boton("Crear Nonograma", 270, 450, 260, 60, VIOLETA_MENU, FUCSIA, pantalla, lambda: cambiar_ventana('crear_nonograma'))
    boton("Salir del juego", 270, 550, 260, 60, VIOLETA_MENU, FUCSIA, pantalla, lambda: iniciar_ventana_confirmacion())

    if confirmando:
        ventana_confirmacion()

    reloj.tick(10)

def iniciar_ventana_confirmacion():
    global confirmando
    confirmando = True 

def ventana_confirmacion():
    global confirmando
    confirm_width = 350
    confirm_height = 150

    confirm_rect = pygame.Rect((ancho_pantalla // 2 - confirm_width // 2, alto_pantalla // 2 - confirm_height // 2), (confirm_width, confirm_height))

    pygame.draw.rect(pantalla, NEGRO, confirm_rect)
    mostrar_texto("¿Seguro que quieres salir?", pygame.font.SysFont(None, 36), BLANCO, pantalla, ancho_pantalla // 2, alto_pantalla // 2 - 20)

    boton("Sí", confirm_rect.left + 55, confirm_rect.top + 80, 80, 40, VERDE, VERDE_PRESIONADO, pantalla, salir_del_juego)
    boton("No", confirm_rect.right - 140, confirm_rect.top + 80, 80, 40, ROJO, ROJO_PRESIONADO, pantalla, cancelar_ventana_confirmacion)

def cancelar_ventana_confirmacion():
    global confirmando
    confirmando = False  # Desactiva la ventana de confirmación

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
    pantalla.fill(ROJO)
    pygame.display.set_caption("Nonograma Game")
    mostrar_texto("Nivel X", fuente, NEGRO, pantalla, 80, 50)
    
    clock = pygame.time.Clock()
    game = Game()
    filas, columnas = procesar_matriz(game.board.matriz_solucion)
    game_position = (80, 120)

    tamano_celda = game.getCellSize()
    offset_x = game_position[0]
    offset_y = game_position[1]

    # Dibujar números de filas y columnas
    for i, fila in enumerate(filas):
        mostrar_texto(str(fila), fuente, NEGRO, pantalla, offset_x - 20, offset_y + i * tamano_celda + tamano_celda // 2)

    for j, columna in enumerate(columnas):
        mostrar_texto(str(columna), fuente, NEGRO, pantalla, offset_x + j * tamano_celda + tamano_celda // 2, offset_y - 20)

    running = True

    while running:
        events = pygame.event.get()

        for event in events:
            # detectar clics en botones
            # si se cambian los botones de posicion, hay q ajustar esto
            if event.type == pygame.MOUSEBUTTONDOWN:
                raton = pygame.mouse.get_pos()
                if 500 <= raton[0] <= 700 and 100 <= raton[1] <= 160:
                    cambiar_ventana('menu_principal')  
                    running = False
                elif 500 <= raton[0] <= 700 and 220 <= raton[1] <= 280:
                    game.deshacer() 
                elif 500 <= raton[0] <= 700 and 340 <= raton[1] <= 400:
                    game.rehacer()


        boton("Volver al menú", 500, 100, 200, 60, GRIS, AZUL_OSCURO, pantalla)
        boton("Deshacer", 500, 220, 200, 60, GRIS, AZUL_OSCURO, pantalla)
        boton("Rehacer", 500, 340, 200, 60, GRIS, AZUL_OSCURO, pantalla)

        if game.run(pantalla, *game_position, events=events):
            running = False
            cambiar_ventana('ventana_victoria')

        pygame.display.flip()  # Actualiza la pantalla en cada iteración del bucle
        clock.tick(60)


def ventana_victoria(cambiar_ventana):
    global indice_fotograma_trophy

    pantalla.fill(VIOLETA_MENU)
    indice_fotograma_trophy = mostrar_fotogramas(trophy, indice_fotograma_trophy, 170, 100, pantalla)
    mostrar_texto("¡Ganaste!", fuente, NEGRO, pantalla, 400, 100)
    boton("Volver al menú", 310, 400, 200, 60, NOTHING, FUCSIA, pantalla, lambda: cambiar_ventana('menu_principal'))

    reloj.tick(30)

def salir_del_juego():
    pygame.quit()
    sys.exit()
