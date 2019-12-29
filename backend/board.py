import random
from GameOfUr.backend import square

class Board:
    def __init__(self):
        self.turn = square.Color.white
        self.dice = 0
        square5 = square.NormalSquare(square.Color.empty, False)
        square6 = square.NormalSquare(square.Color.empty, False)
        square7 = square.NormalSquare(square.Color.empty, False)
        square8 = square.NormalSquare(square.Color.empty, True)
        square9 = square.NormalSquare(square.Color.empty, False)
        square10 = square.NormalSquare(square.Color.empty, False)
        square11 = square.NormalSquare(square.Color.empty, False)
        square12 = square.NormalSquare(square.Color.empty, False)

        self.whitelist = [square.StartSquare(square.Color.white, 7),
                          square.NormalSquare(square.Color.empty, False),
                          square.NormalSquare(square.Color.empty, False),
                          square.NormalSquare(square.Color.empty, False),
                          square.NormalSquare(square.Color.empty, True),
                          square5,
                          square6,
                          square7,
                          square8,
                          square9,
                          square10,
                          square11,
                          square12,
                          square.NormalSquare(square.Color.empty, False),
                          square.NormalSquare(square.Color.empty, True),
                          square.EndSquare(7)]

        self.blacklist = [square.StartSquare(square.Color.black, 7),
                          square.NormalSquare(square.Color.empty, False),
                          square.NormalSquare(square.Color.empty, False),
                          square.NormalSquare(square.Color.empty, False),
                          square.NormalSquare(square.Color.empty, True),
                          square5,
                          square6,
                          square7,
                          square8,
                          square9,
                          square10,
                          square11,
                          square12,
                          square.NormalSquare(square.Color.empty, False),
                          square.NormalSquare(square.Color.empty, True),
                          square.EndSquare(7)]

    def GetPosition(self, position):
        switch = [4,3,2,1,0,15,14,13,5,6,7,8,9,10,11,12,4,3,2,1,0,15,14,13]
        if position < len(switch):
            return switch[position]
        else:
            return -1

    def NextTurn(self):
        if self.turn == square.Color.white:
            self.turn = square.Color.black
        else:
            self.turn = square.Color.white

    def ThrowDice(self, value):
        if value == -1:
            self.dice = random.randint(0,1) + random.randint(0,1) + random.randint(0,1) + random.randint(0,1)
        else:
            self.dice = value

        return self.dice

    def CanMove(self):
        if self.dice == 0:
            self.NextTurn()
            return False

        if self.turn == square.Color.white:
            list = self.whitelist
        else:
            list = self.blacklist

        for i in range(16 - self.dice):
            if list[i].GetColor() == self.turn:
                if list[i].CanMove(list[i + self.dice]):
                    return True

        self.NextTurn()
        return False

    def Move(self, position):
        truePosition = self.GetPosition(position)

        if truePosition + self.dice > 15:
            return False

        if self.turn == square.Color.white:
            if position < 8:
                return False
            selectedSquare = self.whitelist[truePosition]
            nextSquare = self.whitelist[truePosition + self.dice]
        else:
            if position > 15:
                return False
            selectedSquare = self.blacklist[truePosition]
            nextSquare = self.blacklist[truePosition + self.dice]

        if selectedSquare.GetColor() != self.turn:
            return False

        if not selectedSquare.CanMove(nextSquare):
            return False

        if nextSquare.GetColor() != self.turn:
            if nextSquare.GetColor() == square.Color.white:
                self.whitelist[0].IncCount()
            elif nextSquare.GetColor() == square.Color.black:
                self.blacklist[0].IncCount()

        if not selectedSquare.Move(nextSquare):
            self.NextTurn()

        return True

    def HasWon(self, color):
        if color == square.Color.white:
            return self.whitelist[15].HasWon()
        elif color == square.Color.black:
            return self.blacklist[15].HasWon()
        else:
            return False

    def GetSquare(self, position):
        truePosition = self.GetPosition(position)

        if truePosition == -1:
            return None
        elif position > 15:
            return self.whitelist[truePosition]
        else:
            return self.blacklist[truePosition]

    def GetTurn(self):
        return self.turn
