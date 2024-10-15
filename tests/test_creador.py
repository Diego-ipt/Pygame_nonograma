import pytest
from creador.creador import *

def test_claseBoton():
    button = SizeButton(0,0,100,100,"Test",None)
    assert button
    assert button.rect == pygame.Rect(0,0,100,100)
    assert button.text == "Test"
    assert button.action == None

def test_clickBoton():
    button = SizeButton(0,0,100,100,"Test",None)
    assert button.isClicked((50,50)) == True
    assert button.isClicked((150,150)) == False

def test_decreaseGrid():
    game = Game()
    game.decreaseGrid()
    assert game.grid_size == 9

def test_increaseGrid():
    game = Game()
    game.decreaseGrid()
    game.increaseGrid()
    assert  game.grid_size == 10

