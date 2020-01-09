from GameOfUr.backend import board
from gym import spaces
import numpy as np

class Env():
    def __init__():
        self.game = board.Board()
        self.action_space = spaces.Discrete(24)
        self.observation_space = spaces.Box((25,), dtype=np.integer)

    def render():
        pass

    def reset():
        self.game = board.Board()

    def step(action):
        pass

    def close():
        pass
