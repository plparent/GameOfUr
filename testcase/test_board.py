import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

import board
import square

def test_Board():
    game = board.Board()

    assert game.GetTurn() == square.Color.white
    assert not game.HasWon(game.GetTurn())
    assert game.ThrowDice(2) == 2 #white
    assert game.GetSquare(18).GetColor() == square.Color.empty
    assert not game.Move(4)
    assert not game.Move(16)
    assert game.Move(20)
    assert game.GetSquare(18).GetColor() == square.Color.white
    assert game.GetTurn() == square.Color.black
    assert game.ThrowDice(4) == 4 #black
    assert game.GetSquare(0).GetColor() == square.Color.empty
    assert not game.Move(20)
    assert game.Move(4)
    assert game.GetSquare(0).GetColor() == square.Color.black
    assert game.GetTurn() == square.Color.black
    assert not game.HasWon(game.GetTurn())
    for i in range(7):
        game.GetSquare(5).SetColor(square.Color.empty)
    assert game.HasWon(game.GetTurn())
    assert game.ThrowDice(4) == 4 #black
    assert game.CanMove()
    assert game.Move(0)
    assert game.ThrowDice(2) == 2 #black
    assert game.CanMove()
    assert game.Move(4)
    assert game.ThrowDice(4) == 4 #white
    assert game.CanMove()
    assert game.Move(20)
    assert game.ThrowDice(2) == 2 #white
    assert game.CanMove()
    assert game.Move(16)
    assert game.ThrowDice(1) == 1 #black
    assert game.CanMove()
    assert game.Move(2)
    assert game.ThrowDice(2) == 2 #white
    assert game.CanMove()
    assert game.Move(18)
    assert game.ThrowDice(2) == 2 #white
    assert game.CanMove()
    assert game.Move(20)
    assert game.ThrowDice(1) == 1 #black
    assert game.CanMove()
    assert game.Move(4)
    assert game.ThrowDice(2) == 2 #white
    assert not game.CanMove()
    assert not game.Move(20)
    assert game.ThrowDice(1) == 1 #black
    assert game.CanMove()
    assert game.Move(1)
    assert game.GetSquare(20).GetCount() == 4
    assert game.ThrowDice(2) == 2 #black
    assert game.CanMove()
    assert game.Move(0)
    assert game.GetSquare(20).GetCount() == 5
    assert game.GetSquare(4).GetCount() == 4
    assert game.ThrowDice(2) == 2 #white
    assert game.CanMove()
    assert game.Move(16)
    assert game.GetSquare(4).GetCount() == 5
    assert game.ThrowDice(0) == 0 #black
    assert not game.CanMove()
    assert game.GetTurn() == square.Color.white

    diceCheck = game.ThrowDice(-1)
    assert diceCheck >= 0 and diceCheck < 5
    assert not game.HasWon(square.Color.empty)
    assert game.GetSquare(25) == None
    game.SaveGame("savefile.txt")
