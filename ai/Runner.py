import numpy as np
import os
import sys
import Model
import MCTS

sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

import board

model = Model.generate_model()
model.load_weights("savetime-10.h5")

game = board.Board()

for _ in range(20):
    game.ThrowDice(-1)
    moves = MCTS.available_moves(game)
    P, _ = model.predict(MCTS.state_convert(game))
    action = np.argmax(P[0] * moves)
    print(action, game.dice)
    if game.CanMove():
        assert(game.Move(action))

game.SaveGame("test.txt")


