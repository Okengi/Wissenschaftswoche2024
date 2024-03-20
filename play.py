import numpy as np
import time
from keras.models import load_model

from game2048 import Game2048
from visuals import Visuals
from CONSTANTS import GRID_SIZE, MODEL_SAVE_LOCATION

def main():
    model = load_model(MODEL_SAVE_LOCATION)
    game = Game2048()
    visuals = Visuals(game)

    state_tuple = game.get_state()
    is_game_over = False
    while not is_game_over:
        game_board_flat = state_tuple[0]
        game_board_flat = game_board_flat.reshape(1, GRID_SIZE*GRID_SIZE)
        is_game_over = state_tuple[2]

        action = model.predict(game_board_flat)

        action = np.argmax(action)

        state_tuple = game.move(action)
        visuals.move()
        time.sleep(0.5)

if __name__ == '__main__':
    main()