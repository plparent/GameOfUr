import random
import os
import sys

sys.path.append(os.path.dirname(__file__))

import square

class Board:
    def __init__(self):
        self.dice = 0
        self.actionList = []
        self.actionPointer = -1
        self.Reset()
        
    def Reset(self):
        self.turn = square.Color.white
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
            self.actionList.append((str(self.turn), self.dice, 0))
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

        self.actionList.append((str(self.turn), self.dice, 100))
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
            if self.actionPointer == -1:
                self.actionList.append((str(self.turn), self.dice, position))
            self.NextTurn()
        else:
            if self.actionPointer == -1:
                self.actionList.append((str(self.turn), self.dice, position))

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

    def SaveGame(self, filename):
        file = open(filename, "w")
        for action in self.actionList:
            file.write(action[0] + '-' +  str(action[1]) + '-' +  str(action[2]) + '\n')
        file.close()

    def LoadGame(self, filename):
        file = open(filename, "r")
        self.actionList = []
        line = file.readline()
        while line:
            items = line.split('-')
            self.actionList.append((items[0], int(items[1]), int(items[2])))
            line = file.readline()
        file.close()
        self.actionPointer = 0

    def NextMove(self):
        if self.actionPointer == 0:
            self.Reset()
            self.ThrowDice(self.actionList[0][1])

        if self.actionPointer >= 0 and self.actionPointer <= len(self.actionList):
            action = self.actionList[self.actionPointer][2]
            if action != 0 and action != 100:
                self.Move(action)
            else:
                self.NextTurn()
            if self.actionPointer + 1 < len(self.actionList):
                self.ThrowDice(self.actionList[self.actionPointer + 1][1])
                self.actionPointer += 1

    def PreviousMove(self):
        pointer = self.actionPointer - 1
        
        if pointer > 0:
            self.actionPointer = 0
            while self.actionPointer < pointer:
                self.NextMove()
        elif pointer == 0:
            self.actionPointer = 0
            self.Reset()
            self.ThrowDice(self.actionList[0][1])
