import sys
import pygame
from nonograma_core.Elementos_graficos.AssetManager import AssetManager

#Constantes
ANCHO_PANTALLA = 800
ALTO_PANTALLA= 650

#Inicializar
asset_manager = AssetManager()
pygame.init()
PANTALLA = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Nonograma_Game")
icono = asset_manager.cargar_imagen("Iconojuego.jpg")
pygame.display.set_icon(icono)

def main():

    #Importadas aca para evitar conflictos de importacion circular
    from nonograma_core.Ventanas.VentanaVictoria import VentanaVictoria
    from nonograma_core.Ventanas.VentanaMenuPrincipal import VentanaMenuPrincipal
    from nonograma_core.Ventanas.VentanaElegirPartida import VentanaElegirPartida
    from nonograma_core.Ventanas.VentanaCrearNonograma import VentanaCrearNonograma
    from nonograma_core.Ventanas.VentanaNonogramaGame import VentanaNonogramaGame

    ventanas = {
        'menu_principal': VentanaMenuPrincipal(PANTALLA),
        'elegir_partida': VentanaElegirPartida(PANTALLA),
        'ventana_nonograma_game': None, #Sera instanciada dinamicamente para cargar aprtidas
        'crear_nonograma': VentanaCrearNonograma(PANTALLA),
        'ventana_victoria': VentanaVictoria(PANTALLA)
    }

    estado_actual = 'menu_principal'
    partida_cargada = None
    nombre_nivel = None

    while True:
        if estado_actual == 'ventana_nonograma_game':
            ventanas[estado_actual] = VentanaNonogramaGame(PANTALLA, partida_cargada, nombre_nivel)
            partida_cargada = None
            nombre_nivel = None

        ventana_siguiente = ventanas[estado_actual].run()

        if isinstance(ventana_siguiente, tuple): #Caso especial donde se cargo un juego al elegir aprtida
            estado_actual, partida_cargada, nombre_nivel = ventana_siguiente
        else:
            estado_actual = ventana_siguiente


