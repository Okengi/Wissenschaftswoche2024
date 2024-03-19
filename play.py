import pygame
from pygame.locals import *
import numpy as np
import time
from game2048 import Game2048

from keras.models import load_model

game = Game2048(4)

GRID_SIZE = game.GRID_SIZE
CELL_SIZE = 100
GRID_OFFSET = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
TILE_COLORS = {
    2: (255, 255, 128),
    4: (255, 255, 0),
    8: (255, 128, 128),
    16: (255, 255, 0),
    32: (255, 255, 128),
    64: (0, 128, 0),
    128: (0, 255, 0),
    256: (128, 255, 0)
}

def draw_grid(screen):
    screen.fill(WHITE)
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(screen, GRAY, (GRID_OFFSET + i * CELL_SIZE, GRID_OFFSET),
                         (GRID_OFFSET + i * CELL_SIZE, GRID_OFFSET + GRID_SIZE * CELL_SIZE))
        pygame.draw.line(screen, GRAY, (GRID_OFFSET, GRID_OFFSET + i * CELL_SIZE),
                         (GRID_OFFSET + GRID_SIZE * CELL_SIZE, GRID_OFFSET + i * CELL_SIZE))

def draw_tiles(screen, game):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = int(game.grid[i][j])
            if value != 0:
                color = TILE_COLORS.get(value, BLACK)
                pygame.draw.rect(screen, color, (GRID_OFFSET + j * CELL_SIZE, GRID_OFFSET + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                font = pygame.font.Font(None, 36)
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=(GRID_OFFSET + j * CELL_SIZE + CELL_SIZE // 2, GRID_OFFSET + i * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE + 2 * GRID_OFFSET, GRID_SIZE * CELL_SIZE + 2 * GRID_OFFSET))
    pygame.display.set_caption("2048 Game")
    
    model = load_model('2048_ai_model.keras')

    running = True
    state_tuple = game.get_state()
    reward = 0
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        
        game_board_flat = state_tuple[0]
        game_board_flat = game_board_flat.reshape(1, GRID_SIZE*GRID_SIZE)

        action = model.predict(game_board_flat)
        action = np.argmax(action)
        print(action)
        reward += game.calculate_reward()
        print("Reward: "+str(reward))
        state_tuple=game.move(action)

        draw_grid(screen)
        draw_tiles(screen, game)
        pygame.display.flip()
        time.sleep(0.1)

    pygame.quit()

if __name__ == '__main__':
    main()
