import pygame
from pygame.locals import *

from game2048 import Game2048
from CONSTANTS import GRID_SIZE, CELL_SIZE, GRID_OFFSET, WHITE, BLACK, GRAY, TILE_COLORS

class Visuals:
    def __init__(self, game: Game2048, training: bool) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE + 2 * GRID_OFFSET, GRID_SIZE * CELL_SIZE + 2 * GRID_OFFSET))
        pygame.display.set_caption("2048 Game")
        self.game = game
        self.training = training
        self.font = pygame.font.Font(None, 36)
    
    def move(self):
        self.draw_grid()
        self.draw_tiles()
        self.score()
        self.draw_reward()
        pygame.display.flip()
        if self.game.is_game_over() and self.training:
            print("Quit")
            pygame.quit()
            return
    
    def stay(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
            self.draw_grid()
            self.draw_tiles()
            self.score()
            self.draw_reward()
            pygame.display.flip()

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

    def score(self):
        score_text = self.font.render("Score: " + str(self.game.score), True, BLACK)
        self.screen.blit(score_text, (GRID_OFFSET, GRID_OFFSET - 40))
    def draw_reward(self):
        reward_text = self.font.render("Reward: " + str(self.game.reward), True, BLACK)
        self.screen.blit(reward_text, (GRID_OFFSET + 250, GRID_OFFSET - 40))