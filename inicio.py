import sys
import pygame
from ventanas import menu_principal, ventana_elegir_partida, ventana_crear_nonograma

# Inicializar Pygame
pygame.init()

# Estado inicial del juego
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
        menu_principal(cambiar_ventana)
    elif estado_actual == 'elegir_partida':
        ventana_elegir_partida(cambiar_ventana)
    elif estado_actual == 'crear_nonograma':
        ventana_crear_nonograma(cambiar_ventana)

    pygame.display.update()
