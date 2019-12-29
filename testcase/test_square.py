import pytest
from GameOfUr.backend import square

normalFalseWhiteSquare = 0
normalFalseBlackSquare = 1
normalFalseEmptySquare = 2
normalTrueWhiteSquare = 3
normalTrueBlackSquare = 4
normalTrueEmptySquare = 5
startWhiteSquare = 6
startBlackSquare = 7
endSquare = 8

@pytest.fixture
def setup():
    return [square.NormalSquare(square.Color.white, False),
    square.NormalSquare(square.Color.black, False),
    square.NormalSquare(square.Color.empty, False),
    square.NormalSquare(square.Color.white, True),
    square.NormalSquare(square.Color.black, True),
    square.NormalSquare(square.Color.empty, True),
    square.StartSquare(square.Color.white, 7),
    square.StartSquare(square.Color.black, 7),
    square.EndSquare(7)]

def test_NormalFalseBlackSquare(setup):
    assert setup[normalFalseBlackSquare].GetClass() == square.SquareClass.Normal
    assert setup[normalFalseBlackSquare].GetColor() == square.Color.black
    assert not setup[normalFalseBlackSquare].GetRosette()
    assert setup[normalFalseBlackSquare].CanMove(setup[normalFalseEmptySquare])
    assert setup[normalFalseBlackSquare].CanMove(setup[normalTrueEmptySquare])
    assert not setup[normalFalseBlackSquare].CanMove(setup[normalFalseBlackSquare])
    assert not setup[normalFalseBlackSquare].CanMove(setup[normalTrueBlackSquare])
    assert setup[normalFalseBlackSquare].CanMove(setup[normalFalseWhiteSquare])
    assert not setup[normalFalseBlackSquare].CanMove(setup[normalTrueWhiteSquare])
    assert not setup[normalFalseBlackSquare].Move(setup[normalFalseEmptySquare])
    assert setup[normalFalseBlackSquare].GetColor() == square.Color.empty
    assert setup[normalFalseEmptySquare].GetColor() == square.Color.black
    setup[normalFalseBlackSquare].SetColor(square.Color.black)
    assert setup[normalFalseBlackSquare].Move(setup[normalTrueEmptySquare])
    assert setup[normalFalseBlackSquare].GetColor() == square.Color.empty
    assert setup[normalFalseEmptySquare].GetColor() == square.Color.black
    setup[normalFalseBlackSquare].SetColor(square.Color.black)
    assert not setup[normalFalseBlackSquare].Move(setup[normalFalseWhiteSquare])
    assert setup[normalFalseBlackSquare].GetColor() == square.Color.empty
    assert setup[normalFalseWhiteSquare].GetColor() == square.Color.black
    setup[normalFalseBlackSquare].SetColor(square.Color.black)
    with pytest.raises(Exception):
        setup[normalFalseBlackSquare].Move(setup[normalTrueWhiteSquare])
    assert setup[normalFalseBlackSquare].GetColor() == square.Color.black
    assert setup[normalTrueWhiteSquare].GetColor() == square.Color.white
    setup[normalFalseBlackSquare].SetColor(square.Color.black)
    with pytest.raises(Exception):
        setup[normalFalseBlackSquare].Move(setup[normalTrueBlackSquare])
    assert setup[normalFalseBlackSquare].GetColor() == square.Color.black
    assert setup[normalTrueBlackSquare].GetColor() == square.Color.black


def test_NormalTrueBlackSquare(setup):
    assert setup[normalTrueBlackSquare].GetClass() == square.SquareClass.Normal
    assert setup[normalTrueBlackSquare].GetColor() == square.Color.black
    assert setup[normalTrueBlackSquare].GetRosette()
    assert setup[normalTrueBlackSquare].CanMove(setup[normalFalseEmptySquare])
    assert setup[normalTrueBlackSquare].CanMove(setup[normalTrueEmptySquare])
    assert not setup[normalTrueBlackSquare].CanMove(setup[normalFalseBlackSquare])
    assert not setup[normalTrueBlackSquare].CanMove(setup[normalTrueBlackSquare])
    assert setup[normalTrueBlackSquare].CanMove(setup[normalFalseWhiteSquare])
    assert not setup[normalTrueBlackSquare].CanMove(setup[normalTrueWhiteSquare])
    assert not setup[normalTrueBlackSquare].Move(setup[normalFalseEmptySquare])
    assert setup[normalTrueBlackSquare].GetColor() == square.Color.empty
    assert setup[normalFalseEmptySquare].GetColor() == square.Color.black
    setup[normalTrueBlackSquare].SetColor(square.Color.black)
    assert setup[normalTrueBlackSquare].Move(setup[normalTrueEmptySquare])
    assert setup[normalTrueBlackSquare].GetColor() == square.Color.empty
    assert setup[normalTrueEmptySquare].GetColor() == square.Color.black
    setup[normalTrueBlackSquare].SetColor(square.Color.black)
    assert not setup[normalTrueBlackSquare].Move(setup[normalFalseWhiteSquare])
    assert setup[normalTrueBlackSquare].GetColor() == square.Color.empty
    assert setup[normalFalseWhiteSquare].GetColor() == square.Color.black
    setup[normalTrueBlackSquare].SetColor(square.Color.black)
    with pytest.raises(Exception):
        setup[normalTrueBlackSquare].Move(setup[normalTrueWhiteSquare])
    assert setup[normalTrueBlackSquare].GetColor() == square.Color.black
    assert setup[normalTrueWhiteSquare].GetColor() == square.Color.white
    setup[normalFalseBlackSquare].SetColor(square.Color.black)
    with pytest.raises(Exception):
        setup[normalTrueBlackSquare].Move(setup[normalFalseBlackSquare])
    assert setup[normalTrueBlackSquare].GetColor() == square.Color.black
    assert setup[normalFalseBlackSquare].GetColor() == square.Color.black


def test_NormalFalseWhiteSquare(setup):
    assert setup[normalFalseWhiteSquare].GetClass() == square.SquareClass.Normal
    assert setup[normalFalseWhiteSquare].GetColor() == square.Color.white
    assert not setup[normalFalseWhiteSquare].GetRosette()
    assert setup[normalFalseWhiteSquare].CanMove(setup[normalFalseEmptySquare])
    assert setup[normalFalseWhiteSquare].CanMove(setup[normalTrueEmptySquare])
    assert setup[normalFalseWhiteSquare].CanMove(setup[normalFalseBlackSquare])
    assert not setup[normalFalseWhiteSquare].CanMove(setup[normalTrueBlackSquare])
    assert not setup[normalFalseWhiteSquare].CanMove(setup[normalFalseWhiteSquare])
    assert not setup[normalFalseWhiteSquare].CanMove(setup[normalTrueWhiteSquare])
    assert not setup[normalFalseWhiteSquare].Move(setup[normalFalseEmptySquare])
    assert setup[normalFalseWhiteSquare].GetColor() == square.Color.empty
    assert setup[normalFalseEmptySquare].GetColor() == square.Color.white
    setup[normalFalseWhiteSquare].SetColor(square.Color.white)
    assert setup[normalFalseWhiteSquare].Move(setup[normalTrueEmptySquare])
    assert setup[normalFalseWhiteSquare].GetColor() == square.Color.empty
    assert setup[normalTrueEmptySquare].GetColor() == square.Color.white
    setup[normalFalseWhiteSquare].SetColor(square.Color.white)
    assert not setup[normalFalseWhiteSquare].Move(setup[normalFalseBlackSquare])
    assert setup[normalFalseWhiteSquare].GetColor() == square.Color.empty
    assert setup[normalFalseBlackSquare].GetColor() == square.Color.white
    setup[normalFalseWhiteSquare].SetColor(square.Color.white)
    with pytest.raises(Exception):
        setup[normalFalseWhiteSquare].Move(setup[normalTrueBlackSquare])
    assert setup[normalFalseWhiteSquare].GetColor() == square.Color.white
    assert setup[normalTrueBlackSquare].GetColor() == square.Color.black
    setup[normalFalseWhiteSquare].SetColor(square.Color.white)
    with pytest.raises(Exception):
        setup[normalFalseWhiteSquare].Move(setup[normalTrueWhiteSquare])
    assert setup[normalFalseWhiteSquare].GetColor() == square.Color.white
    assert setup[normalTrueWhiteSquare].GetColor() == square.Color.white


def test_NormalTrueWhiteSquare(setup):
    assert setup[normalTrueWhiteSquare].GetClass() == square.SquareClass.Normal
    assert setup[normalTrueWhiteSquare].GetColor() == square.Color.white
    assert setup[normalTrueWhiteSquare].GetRosette()
    assert setup[normalTrueWhiteSquare].CanMove(setup[normalFalseEmptySquare])
    assert setup[normalTrueWhiteSquare].CanMove(setup[normalTrueEmptySquare])
    assert setup[normalTrueWhiteSquare].CanMove(setup[normalFalseBlackSquare])
    assert not setup[normalTrueWhiteSquare].CanMove(setup[normalTrueBlackSquare])
    assert not setup[normalTrueWhiteSquare].CanMove(setup[normalFalseWhiteSquare])
    assert not setup[normalTrueWhiteSquare].CanMove(setup[normalTrueWhiteSquare])
    assert not setup[normalTrueWhiteSquare].Move(setup[normalFalseEmptySquare])
    assert setup[normalTrueWhiteSquare].GetColor() == square.Color.empty
    assert setup[normalFalseEmptySquare].GetColor() == square.Color.white
    setup[normalTrueWhiteSquare].SetColor(square.Color.white)
    assert setup[normalTrueWhiteSquare].Move(setup[normalTrueEmptySquare])
    assert setup[normalTrueWhiteSquare].GetColor() == square.Color.empty
    assert setup[normalTrueEmptySquare].GetColor() == square.Color.white
    setup[normalTrueWhiteSquare].SetColor(square.Color.white)
    assert not setup[normalTrueWhiteSquare].Move(setup[normalFalseBlackSquare])
    assert setup[normalTrueWhiteSquare].GetColor() == square.Color.empty
    assert setup[normalFalseBlackSquare].GetColor() == square.Color.white
    setup[normalTrueWhiteSquare].SetColor(square.Color.white)
    with pytest.raises(Exception):
        setup[normalTrueWhiteSquare].Move(setup[normalTrueBlackSquare])
    assert setup[normalTrueWhiteSquare].GetColor() == square.Color.white
    assert setup[normalTrueBlackSquare].GetColor() == square.Color.black
    setup[normalTrueWhiteSquare].SetColor(square.Color.white)
    with pytest.raises(Exception):
        setup[normalTrueWhiteSquare].Move(setup[normalFalseWhiteSquare])
    assert setup[normalTrueWhiteSquare].GetColor() == square.Color.white
    assert setup[normalFalseWhiteSquare].GetColor() == square.Color.white


def test_StartBlackSquare(setup):
    assert setup[startBlackSquare].GetClass() == square.SquareClass.Start
    assert setup[startBlackSquare].GetColor() == square.Color.black
    assert not setup[startBlackSquare].GetRosette()
    assert setup[startBlackSquare].GetCount() == 7
    assert setup[startBlackSquare].CanMove(setup[normalTrueEmptySquare])
    assert setup[startBlackSquare].CanMove(setup[normalFalseEmptySquare])
    assert not setup[startBlackSquare].CanMove(setup[normalTrueBlackSquare])
    assert not setup[startBlackSquare].CanMove(setup[normalFalseBlackSquare])
    assert setup[startBlackSquare].Move(setup[normalTrueEmptySquare])
    assert setup[normalTrueEmptySquare].GetColor() == square.Color.black
    assert setup[startBlackSquare].GetCount() == 6
    assert not setup[startBlackSquare].Move(setup[normalFalseEmptySquare])
    assert setup[normalFalseEmptySquare].GetColor() == square.Color.black
    assert setup[startBlackSquare].GetCount() == 5
    with pytest.raises(Exception):
        setup[startBlackSquare].Move(setup[normalTrueBlackSquare])
    assert setup[normalTrueBlackSquare].GetColor() == square.Color.black
    assert setup[startBlackSquare].GetCount() == 5
    with pytest.raises(Exception):
        setup[startBlackSquare].Move(setup[normalFalseBlackSquare])
    assert setup[normalFalseBlackSquare].GetColor() == square.Color.black
    assert setup[startBlackSquare].GetCount() == 5
    setup[startBlackSquare].IncCount()
    assert setup[startBlackSquare].GetCount() == 6


def test_StartWhiteSquare(setup):
    assert setup[startWhiteSquare].GetClass() == square.SquareClass.Start
    assert setup[startWhiteSquare].GetColor() == square.Color.white
    assert not setup[startWhiteSquare].GetRosette()
    assert setup[startWhiteSquare].GetCount() == 7
    assert setup[startWhiteSquare].CanMove(setup[normalTrueEmptySquare])
    assert setup[startWhiteSquare].CanMove(setup[normalFalseEmptySquare])
    assert not setup[startWhiteSquare].CanMove(setup[normalTrueWhiteSquare])
    assert not setup[startWhiteSquare].CanMove(setup[normalFalseWhiteSquare])
    assert setup[startWhiteSquare].Move(setup[normalTrueEmptySquare])
    assert setup[normalTrueEmptySquare].GetColor() == square.Color.white
    assert setup[startWhiteSquare].GetCount() == 6
    assert not setup[startWhiteSquare].Move(setup[normalFalseEmptySquare])
    assert setup[normalFalseEmptySquare].GetColor() == square.Color.white
    assert setup[startWhiteSquare].GetCount() == 5
    with pytest.raises(Exception):
        setup[startWhiteSquare].Move(setup[normalTrueWhiteSquare])
    assert setup[normalTrueWhiteSquare].GetColor() == square.Color.white
    assert setup[startWhiteSquare].GetCount() == 5
    with pytest.raises(Exception):
        setup[startWhiteSquare].Move(setup[normalFalseWhiteSquare])
    assert setup[normalFalseWhiteSquare].GetColor() == square.Color.white
    assert setup[startWhiteSquare].GetCount() == 5
    setup[startWhiteSquare].IncCount()
    assert setup[startWhiteSquare].GetCount() == 6


def test_EndSquare(setup):
    assert setup[endSquare].GetClass() == square.SquareClass.End
    assert setup[endSquare].GetColor() == square.Color.empty
    assert not setup[endSquare].GetRosette()
    assert setup[endSquare].GetCount() == 0
    assert not setup[endSquare].HasWon()
    setup[endSquare].SetColor(square.Color.black)
    assert setup[endSquare].GetColor() == square.Color.empty
    assert setup[endSquare].GetCount() == 1
    setup[endSquare].SetColor(square.Color.white)
    assert setup[endSquare].GetColor() == square.Color.empty
    assert setup[endSquare].GetCount() == 2
    setup[endSquare].SetColor(square.Color.white)
    assert setup[endSquare].GetColor() == square.Color.empty
    assert setup[endSquare].GetCount() == 3
    setup[endSquare].SetColor(square.Color.white)
    assert setup[endSquare].GetColor() == square.Color.empty
    assert setup[endSquare].GetCount() == 4
    setup[endSquare].SetColor(square.Color.white)
    assert setup[endSquare].GetColor() == square.Color.empty
    assert setup[endSquare].GetCount() == 5
    setup[endSquare].SetColor(square.Color.white)
    assert setup[endSquare].GetColor() == square.Color.empty
    assert setup[endSquare].GetCount() == 6
    setup[endSquare].SetColor(square.Color.white)
    assert setup[endSquare].HasWon()
    
    