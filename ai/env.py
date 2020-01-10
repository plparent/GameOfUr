import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

import board
import square
from gym import spaces
import numpy as np

class Env():
    def __init__(self):
        self.game = board.Board()
        self.action_space = spaces.Discrete(24)
        self.observation_space = spaces.Box(low=0, high=7, shape=(25,), dtype=np.int8)
        
        self.game.ThrowDice(-1)

    def render(self):
        pass

    def reset(self):
        self.game = board.Board()
        return self.get_observation()

    def step(self, action):
        if not self.game.CanMove():
            return (self.get_observation(), 0, False, {})
        
        if self.game.Move(action):
            if self.game.HasWon(square.Color.white) or self.game.HasWon(square.Color.black):
                return (self.get_observation(), 100, True, {})
            return (self.get_observation(), 5, False, {})
        else:
            return (self.get_observation(), 0, False, {})

    def get_observation(self):
        obs = []
        for i in range(24):
            item = self.game.GetSquare(i)
            if item.GetClass() == square.SquareClass.Start or item.GetClass() == square.SquareClass.End:
                obs.append(item.GetCount())
            elif item.GetColor() == square.Color.empty:
                obs.append(0)
            elif item.GetColor() == square.Color.white:
                obs.append(1)
            elif item.GetColor() == square.Color.black:
                obs.append(2)

        return np.array(obs.append(self.game.ThrowDice(-1)))

    def close(self):
        pass
