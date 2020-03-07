import numpy as np
import os
import sys
import Model
import MCTS

sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

import board
import square

model1 = Model.generate_model()
model2 = Model.generate_model()
model1.load_weights("savetime-1.h5")
model2.load_weights("savetime-1.h5")

game = board.Board()
i = 0
j = 0

for k in range(100):
    print(k)
    while True:
        game.ThrowDice(-1)
        moves = MCTS.available_moves(game)
        if game.GetTurn() == square.Color.white:
            P, _ = model1.predict(MCTS.state_convert(game))
        else:
            P, _ = model2.predict(MCTS.state_convert(game))
        action = np.argmax(P[0] * moves)
        if game.CanMove():
            assert(game.Move(action))
        if game.HasWon(square.Color.white):
            i += 1
            break;
        if game.HasWon(square.Color.black):
            j += 1
            break;
 
print(i, "/100 for white")
print(j, "/100 for black")
#game.SaveGame("test.txt")


