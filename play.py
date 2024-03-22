import numpy as np
import time
from keras.models import load_model

from game2048 import Game2048
from visuals import Visuals
from CONSTANTS import MODEL_SAVE_LOCATION

def main():
    model = load_model(MODEL_SAVE_LOCATION)
    game = Game2048()
    visuals = Visuals(game, False)

    game_board, reward, is_game_over = game.get_state()
    
    while not is_game_over:
        actions = model.predict(game_board)

        counter = 0
        old = game_board
        while np.array_equal(game_board, old):
            if counter >= 4:
                is_game_over = True
                break

            action_indexes = np.argsort(actions)[::-1]
            game_board, reward, is_game_over = game.move(action_indexes[0][counter])
            counter += 1
            
        visuals.move()
        time.sleep(0.5)
    visuals.stay()

if __name__ == '__main__':
    main()