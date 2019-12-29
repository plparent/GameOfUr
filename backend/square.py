import enum

class SquareClass(enum.Enum):
    Normal = 1
    Start = 2
    End = 3

class Color(enum.Enum):
    white = 1
    black = 2
    empty = 3

class Square:
    def __init__(self):
        self.color = Color.empty
        self.rosette = False

    def GetColor(self):
        return self.color

    def SetColor(self, color):
        self.color = color

    def GetRosette(self):
        return self.rosette

class NormalSquare(Square):
    def __init__(self, color, rosette):
        self.color = color
        self.rosette = rosette

    def CanMove(self, square):
        if Color.empty == square.GetColor():
            return True
        elif self.color == square.GetColor():
            return False
        elif square.GetRosette():
            return False
        else:
            return True

    def Move(self, square):
        if not self.CanMove(square):
            raise Exception('Invalid Move')
        else:
            square.SetColor(self.color)
            self.color = Color.empty
            return square.GetRosette()

    def GetClass(self):
        return SquareClass.Normal

class StartSquare(NormalSquare):
    def __init__(self, color, count):
        super().__init__(color, False)
        self.count = count

    def CanMove(self, square):
        return Color.empty == square.GetColor() and self.count > 0

    def Move(self, square):
        if not self.CanMove(square):
            raise Exception('Invalid Move')
        else:
            square.SetColor(self.color)
            self.count -= 1
            return square.GetRosette()

    def GetCount(self):
        return self.count

    def IncCount(self):
        self.count += 1

    def GetClass(self):
        return SquareClass.Start

class EndSquare(Square):
    def __init__(self, count):
        self.color = Color.empty
        self.count = 0
        self.rosette = False
        self.winCondition = count

    def SetColor(self, color):
        self.count += 1

    def HasWon(self):
        return self.count == self.winCondition

    def GetCount(self):
        return self.count

    def GetClass(self):
        return SquareClass.End
