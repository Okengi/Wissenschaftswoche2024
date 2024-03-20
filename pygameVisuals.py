import pygame
from pygame.locals import *

from game2048 import Game2048

game = Game2048(4)

GRID_SIZE = game.GRID_SIZE
CELL_SIZE = 100
GRID_OFFSET = 50

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
TILE_COLORS = {
    2: (255, 255, 128),
    4: (255, 255, 0),
    8: (255, 128, 0),
    16: (255, 255, 0),
    32: (255, 255, 128),
    64: (0, 128, 0),
    128: (0, 255, 0),
    256: (128, 255, 0),
    512: (128, 124, 255),
    1024: (0, 0, 255),
    2048: (255, 0, 255)
}

def draw_grid(screen: pygame.display):
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
            # else:
                # color = (128 / GRID_SIZE * (j + 1), 255 / GRID_SIZE * (i + 1), 128 / (GRID_SIZE * GRID_SIZE) * (i + 1) * (j + 1))
                # pygame.draw.rect(screen, color, (GRID_OFFSET + j * CELL_SIZE, GRID_OFFSET + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE + 2 * GRID_OFFSET, GRID_SIZE * CELL_SIZE + 2 * GRID_OFFSET))
    pygame.display.set_caption("2048 Game")

    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    game.move(0)
                elif event.key == K_DOWN:
                    game.move(1)
                elif event.key == K_LEFT:
                    game.move(2)
                elif event.key == K_RIGHT:
                    game.move(3)

        draw_grid(screen)
        draw_tiles(screen, game)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()