import pygame
from pygame.locals import *

from game2048 import Game2048
from CONSTANTS import GRID_SIZE, CELL_SIZE, GRID_OFFSET, WHITE, BLACK, GRAY, TILE_COLORS

class Visuals:
    def __init__(self, game: Game2048) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE + 2 * GRID_OFFSET, GRID_SIZE * CELL_SIZE + 2 * GRID_OFFSET))
        pygame.display.set_caption("2048 Game")
        self.game = game
    
    def move(self):
        self.draw_grid()
        self.draw_tiles()
        pygame.display.flip()
        if self.game.is_game_over() == True:
            pygame.quit()
            return
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
        

    def draw_grid(self):
        self.screen.fill(WHITE)
        for i in range(GRID_SIZE + 1):
            pygame.draw.line(self.screen, GRAY, (GRID_OFFSET + i * CELL_SIZE, GRID_OFFSET),
                            (GRID_OFFSET + i * CELL_SIZE, GRID_OFFSET + GRID_SIZE * CELL_SIZE))
            pygame.draw.line(self.screen, GRAY, (GRID_OFFSET, GRID_OFFSET + i * CELL_SIZE),
                            (GRID_OFFSET + GRID_SIZE * CELL_SIZE, GRID_OFFSET + i * CELL_SIZE))

    def draw_tiles(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = int(self.game.grid[i][j])
                if value != 0:
                    color = TILE_COLORS.get(value, BLACK)
                    pygame.draw.rect(self.screen, color, (GRID_OFFSET + j * CELL_SIZE, GRID_OFFSET + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                    font = pygame.font.Font(None, 36)
                    text = font.render(str(value), True, BLACK)
                    text_rect = text.get_rect(center=(GRID_OFFSET + j * CELL_SIZE + CELL_SIZE // 2, GRID_OFFSET + i * CELL_SIZE + CELL_SIZE // 2))
                    self.screen.blit(text, text_rect)
                # else:
                    # color = (128 / GRID_SIZE * (j + 1), 255 / GRID_SIZE * (i + 1), 128 / (GRID_SIZE * GRID_SIZE) * (i + 1) * (j + 1))
                    # pygame.draw.rect(screen, color, (GRID_OFFSET + j * CELL_SIZE, GRID_OFFSET + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))