import numpy as np
import copy as cp
import random
import os
import sys
import Model

sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

import board
import square

c_puct = 3
tau = 1
action_space = 24
model = Model.generate_model()

class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.children = {}
        self.N = np.zeros(action_space)
        self.W = np.zeros(action_space)
        self.Q = np.zeros(action_space)
        self.P = np.zeros(action_space)
        self.policy = np.zeros(action_space)

    def search(self):
        if self.is_leaf():
            self.expand()
        else:
            self.select().search()

    def select(self):
        U = c_puct * self.P * np.sqrt(np.sum(self.N)) / (1 + self.N)
        action = np.argmax((self.Q + U) * self.available_moves())
        dice = random.randint(0,1) + random.randint(0,1) + random.randint(0,1) + random.randint(0,1)
        if (action, dice) in self.children:
            return self.children[(action, dice)]

        next_state = cp.deepcopy(self.state)
        next_state.ThrowDice(dice)
        if next_state.CanMove():
            next_state.Move(action)
        new_child = Node(next_state, self)
        self.children[(action, dice)] = new_child
        return new_child

    def expand(self):
        if self.state.HasWon(square.Color.white):
            self.backup(1)
        elif self.state.HasWon(square.Color.black):
            self.backup(-1)
        else:
            self.P, V = model.predict(self.state_convert())
            self.backup(V)

    def backup(self, value):
        if self.parent != None:
            self.parent.W[self.move] += value
            self.parent.N[self.move] += 1
            self.parent.Q[self.move] = self.parent.W[self.move] / self.parent.N[self.move]
            self.parent.backup(value)

    def play(self):
        arr = []
        if self.state.HasWon(square.Color.white):
            self.parse(arr, 1)
            return arr
        elif self.state.HasWon(square.Color.black):
            self.parse(arr, -1)
            return arr
        else:
            N = np.power(self.N, 1 / tau)
            self.policy = N / np.sum(N)
            action = np.argmax(self.policy)
            dice = random.randint(0,1) + random.randint(0,1) + random.randint(0,1) + random.randint(0,1)
            if (action, dice) in self.children:
                return self.children[(action, dice)].play()
            
            raise Exception("Failed Play")

    def parse(self, arr, value):
        if self.state.turn == square.Color.white:
            arr.append((self.state_convert(), self.policy, value))
        else:
            arr.append((self.state_convert(), self.policy, -1 * value))

    def state_convert(self):
        def encode_bin(value):
            if value == 0:
                return [0,0,0]
            elif value == 1:
                return [0,0,1]
            elif value == 2:
                return [0,1,0]
            elif value == 3:
                return [0,1,1]
            elif value == 4:
                return [1,0,0]
            elif value == 5:
                return [1,0,1]
            elif value == 6:
                return [1,1,0]
            elif value == 7:
                return [1,1,1]
        
        white = np.zeros((8,3))
        for i in range(3):
            for j in range(8):
                if self.state.GetSquare(i * 8 + j).GetColor() == square.Color.white:
                    white[j][i] = 1
                else:
                    white[j][i] = 0

        black = np.zeros((8,3))
        for i in range(3):
            for j in range(8):
                if self.state.GetSquare(i * 8 + j).GetColor() == square.Color.black:
                    black[j][i] = 1
                else:
                    black[j][i] = 0

        last = np.zeros((8,3))
        last[0] = encode_bin(self.state.GetSquare(4).GetCount())
        last[1] = encode_bin(self.state.GetSquare(5).GetCount())
        last[2] = encode_bin(self.state.GetSquare(20).GetCount())
        last[3] = encode_bin(self.state.GetSquare(21).GetCount())
        last[4] = encode_bin(self.state.dice)

        turn = [0, 0, 0]
        if self.state.turn == square.Color.black:
            turn = [1, 1, 1]

        for i in range(5,8):
            last[i] = turn

        return np.array([white, black, last])
    
    def available_moves(self):
        ret = np.zeros(24)
        if self.dice == 0:
            ret[0] = 1
            return ret

        if self.state.turn == square.Color.white:
            list = self.state.whitelist
            switch = [20,19,18,17,16,8,9,10,11,12,13,14,15,23,22,21]
        else:
            list = self.state.blacklist
            switch = [4,3,2,1,0,8,9,10,11,12,13,14,15,5,6,7]

        for i in range(16 - self.state.dice):
            if list[i].GetColor() == self.state.turn:
                if list[i].CanMove(list[i + self.state.dice]):
                    ret[switch[i]] = 1

        if np.sum(ret) == 0:
            ret[0] = 1

        return ret
            
    def is_leaf(self):
        return len(self.children) == 0

b = board.Board()
b.ThrowDice(-1)
test = Node(b, None)
