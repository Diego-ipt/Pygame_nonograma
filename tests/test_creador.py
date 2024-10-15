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

def test_boardResize():
    board = CreatorBoard(7,30 )
    board.resize(10)
    assert board.grid_size == 10

def test_decreaseGrid():
    game = CreatorWindow()
    game.decreaseGrid()
    assert game.grid_size == 9

def test_increaseGrid():
    game = CreatorWindow()
    game.decreaseGrid()
    game.increaseGrid()
    assert  game.grid_size == 10

