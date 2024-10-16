from nonograma_core.JuegoNonograma import *


# import sys
# import pygame
# from nonograma_core.ventanas import *

# # Inicializar Pygame
# pygame.init()

# # Estado inicial del juego
# estado_actual = 'menu_principal'

# def cambiar_ventana(nuevo_estado):
#     global estado_actual
#     print(f"Cambiando a ventana: {nuevo_estado}")
#     estado_actual = nuevo_estado

# # Bucle principal
# running = True
# while running:
#     for evento in pygame.event.get():
#         if evento.type == pygame.QUIT:
#             running = False

#     # Llamar a la función correspondiente según el estado actual
#     if estado_actual == 'menu_principal':
#         menu_principal(cambiar_ventana)
#     elif estado_actual == 'elegir_partida':
#         ventana_elegir_partida(cambiar_ventana)
#     elif estado_actual == 'crear_nonograma':
#         ventana_crear_nonograma(cambiar_ventana)
#     elif estado_actual == 'ventana_nonograma_game':
#         ventana_nonograma_game(cambiar_ventana)
#     elif estado_actual == 'ventana_victoria':
#         ventana_victoria(cambiar_ventana)

#     pygame.display.update()

# pygame.quit()
# sys.exit()

# Para ejecutar el juego
if __name__ == "__main__":
    juego_nonograma = JuegoNonograma()
    juego_nonograma.ejecutar()

