import pytest
from creador.creador import *

# Actualmente no se usa esta clase
# def test_claseBoton():
#     button = SizeSaveButton(0, 0, 100, 100, "Test", None)
#     assert button
#     assert button.rect == pygame.Rect(0,0,100,100)
#     assert button.text == "Test"
#     assert button.action == None
#
#
# def test_clickBoton():
#     button = SizeSaveButton(0, 0, 100, 100, "Test", None, None,True)
#     assert button.isClicked((50,50)) == True
#     assert button.isClicked((150,150)) == False

def test_boardResize():
    board = CreatorBoard(7)
    board.resize(10)
    assert board.grid_size == 10

def test_decreaseGrid():
    game = CreatorWindow()
    game.decreaseGrid()
    assert game.grid_size == 5

def test_increaseGrid():
    game = CreatorWindow()
    game.increaseGrid()
    assert  game.grid_size == 6

def test_guardarBoard():
    game = CreatorWindow()
    game.creator_board.board[0][0].click()
    game.creator_board.board[0][1].click()
    game.creator_board.board[0][2].click()
    game.creator_board.board[1][0].click()
    game.creator_board.board[2][0].click()
    design = game.creator_board.getBoardClicked()
    assert design[0][0] == 1
    assert design[0][1] == 1
    assert design[0][2] == 1
    assert design[1][0] == 1
    assert design[2][0] == 1
    assert design[1][1] == 0

def test_guardarDiseno():
    game = CreatorWindow()
    game.creator_board.board[0][0].click()
    game.saveDesign("Test")
    with open("../levels/game_levels/Test.json", "r") as file:
        data = json.load(file)
        data["diseno"] == [[1,0,0],[0,0,0],[0,0,0]]


