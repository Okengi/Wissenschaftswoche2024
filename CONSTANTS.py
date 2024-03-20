# !!!!!!!!!!
VERSION = 0.1
MODEL_SAVE_LOCATION = f'models/2048_ai_model_{str(VERSION)}.keras'

# Game
GRID_SIZE = 4

# AI
NUM_EPISODES = 1 # In reinforcement learning, each of the repeated attempts by the agent to learn an environment.
MEMORY_SIZE = 1000 #
BATCH_SIZE = 128 # 
EPSILON_DECAY = 0.995 #
MIN_EPSILON = 0.01 #
GAMMA = 0.95 #

# Visulas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
TILE_COLORS = {
    2: (220, 150, 150),    
    4: (220, 180, 150),     
    8: (220, 220, 150),     
    16: (150, 220, 150),    
    32: (100, 150, 100),    
    64: (100, 180, 220),    
    128: (100, 100, 220),   
    256: (120, 100, 120),   
    512: (220, 100, 220),  
    1024: (220, 110, 160),  
    2048: (220, 150, 100), 
    4096: (150, 150, 150)   
}
CELL_SIZE = 100
GRID_OFFSET = 50


import pygame
from pygame.locals import *
import numpy as np

def color_show():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    screen.fill(WHITE)
    for x in range(12):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
        i = np.power(2, x+1)
        pygame.draw.rect(screen, TILE_COLORS.get(i, GRAY), pygame.Rect(x * 500/12, 0, 500/12, 500))
        pygame.display.flip()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
    pygame.quit()

if __name__ == "__main__":
    color_show()