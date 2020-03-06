import numpy as np
import copy as cp
import random
import os
import sys
import Model

sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

import board
import square

k = 100
i = 1000
j = 1000
c_puct = 3
max_tau = 30
action_space = 25
model = Model.generate_model()

def state_convert(state):
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
                if state.GetSquare(i * 8 + j).GetColor() == square.Color.white:
                    white[j][i] = 1
                else:
                    white[j][i] = 0

        black = np.zeros((8,3))
        for i in range(3):
            for j in range(8):
                if state.GetSquare(i * 8 + j).GetColor() == square.Color.black:
                    black[j][i] = 1
                else:
                    black[j][i] = 0

        last = np.zeros((8,3))
        last[0] = encode_bin(state.GetSquare(4).GetCount())
        last[1] = encode_bin(state.GetSquare(5).GetCount())
        last[2] = encode_bin(state.GetSquare(20).GetCount())
        last[3] = encode_bin(state.GetSquare(21).GetCount())
        last[4] = encode_bin(state.dice)

        turn = [0, 0, 0]
        if state.GetTurn() == square.Color.black:
            turn = [1, 1, 1]

        for i in range(5,8):
            last[i] = turn

        return np.array([white, black, last]).reshape((-1,3,8,3))

def available_moves(state):
        ret = np.zeros(25)
        if state.dice == 0:
            ret[24] = 1
            return ret

        if state.GetTurn() == square.Color.white:
            list = state.whitelist
            switch = [20,19,18,17,16,8,9,10,11,12,13,14,15,23,22,21]
        else:
            list = state.blacklist
            switch = [4,3,2,1,0,8,9,10,11,12,13,14,15,5,6,7]

        for i in range(16 - state.dice):
            if list[i].GetColor() == state.GetTurn():
                if list[i].CanMove(list[i + state.dice]):
                    ret[switch[i]] = 1

        if np.sum(ret) == 0:
            ret[24] = 1

        return ret


class Node:
    def __init__(self, state, move, parent, depth):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.children = {}
        self.N = np.zeros(action_space)
        self.W = np.zeros(action_space)
        self.Q = np.zeros(action_space)
        self.P = np.zeros(action_space)

    def search(self):
        if np.sum(self.P) == 0:
            self.expand()
        else:
            self.select().search()

    def select(self):
        self.state.ThrowDice(-1)
        U = c_puct * self.P * np.sqrt(np.sum(self.N)) / (1 + self.N)
        moves = available_moves(self.state)
        tmp = ((self.Q + U) + moves) * moves
        action = np.argmax(tmp / np.sum(tmp))
        dice = self.state.dice
        if (action, dice) in self.children:
            return self.children[(action, dice)]

        next_state = cp.deepcopy(self.state)
        if next_state.CanMove():
            if not next_state.Move(action):
                print(action, dice)
                print(moves)
                print(state_convert(self.state))
                assert(False)
        new_child = Node(next_state, action, self, self.depth + 1)
        self.children[(action, dice)] = new_child
        return new_child

    def expand(self):
        if self.state.HasWon(square.Color.white):
            self.backup(1)
        elif self.state.HasWon(square.Color.black):
            self.backup(-1)
        else:
            P, V = model.predict(state_convert(self.state))
            self.P = P[0]
            self.backup(V[0])

    def backup(self, value):
        if self.parent != None:
            self.parent.W[self.move] += value
            self.parent.N[self.move] += 1
            self.parent.Q[self.move] = self.parent.W[self.move] / self.parent.N[self.move]
            self.parent.backup(value)

    def play(self):
        arr = []
        if self.state.HasWon(square.Color.white):
            self.parse(arr, [1], self.N)
            return arr
        elif self.state.HasWon(square.Color.black):
            self.parse(arr, [-1], self.N)
            return arr
        else:
            if np.sum(self.N) == 0:
                P, V = model.predict(state_convert(self.state))
                self.parse(arr, V[0], P[0])
                return arr
            
            action = np.argmax(self.N / np.sum(self.N))
            dice = random.randint(0,1) + random.randint(0,1) + random.randint(0,1) + random.randint(0,1)
            i = 0
            while (action, dice) not in self.children:
                i += 1
                if i > 100:
                    raise Exception("Failed Play")
                dice = random.randint(0,1) + random.randint(0,1) + random.randint(0,1) + random.randint(0,1)
            return self.children[(action, dice)].play()

    def parse(self, arr, value, policy = []):
        if len(policy) == 0:
            policy = self.N / np.sum(self.N)
        
        if self.state.GetTurn() == square.Color.white:
            arr.append((state_convert(self.state)[0], policy, value))
        else:
            arr.append((state_convert(self.state)[0], policy, -1 * value))

        if self.parent != None:
            self.parent.parse(arr, value)
    

def train():
    for k_prime in range(k):
        print("Round: ", k_prime)
        game = board.Board()
        
        tree = Node(game, None, None, 0)
        for _ in range(i):
            tree.search()
        
        dataset = []
        for _ in range(j):
            dataset += tree.play()

        inputs = []
        policy = []
        value = []
        for d in dataset:
            inputs.append(d[0])
            policy.append(d[1])
            value.append(d[2])

        inputs = np.array(inputs)
        policy = np.array(policy)
        value = np.array(value)

        model.fit(x=inputs, y=[policy, value])

        if k_prime % 10 == 0:
            print("Saved weights")
            model.save_weights("savetime-" + k_prime + ".h5")

if __name__ == "__main__":
    train()
