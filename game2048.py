import numpy as np
import random

from CONSTANTS import GRID_SIZE


class Game2048:
    GAME_OVER: bool = False
    tile_before_move = 0
    highest_score = 2
    score_before_move = 0
    reward = 0

    def __init__(self):
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE))
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.75 else 4

    def move(self, direction):
        self.GAME_OVER = self.is_game_over()
        original_grid = np.copy(self.grid)
        self.score = np.sum(self.grid)
        
        self.tile_before_move = np.count_nonzero(self.grid)
        self.score_before_move = self.score

        if direction == 0:  # Up
            self.grid = np.transpose(self.grid)
            self.grid = np.array([self.merge(row) for row in self.grid])
            self.grid = np.transpose(self.grid)
        elif direction == 1:  # Down
            self.grid = np.transpose(self.grid)
            self.grid = np.array([self.merge(row[::-1])[::-1] for row in self.grid])
            self.grid = np.transpose(self.grid)
        elif direction == 2:  # Left
            self.grid = np.array([self.merge(row) for row in self.grid])
        elif direction == 3:  # Right
            self.grid = np.array([self.merge(row[::-1])[::-1] for row in self.grid])

        if not np.array_equal(original_grid, self.grid):
            self.add_new_tile()
        
        return self.get_state()

    def merge(self, row):
        new_row = [i for i in row if i != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                new_row[i + 1] = 0
                if new_row[i] > self.highest_score:
                    self.highest_score = new_row[i]
        new_row = [i for i in new_row if i != 0]
        new_row += [0] * (GRID_SIZE - len(new_row))
        return new_row

    def get_state(self):
        return self.grid.reshape(1, GRID_SIZE * GRID_SIZE), self.calculate_reward(), self.is_game_over()
    
    def calculate_reward(self):
        self.reward = self.score
        max = np.max(self.grid)
        print(max)
        if max == self.grid[0][0] or max == self.grid[GRID_SIZE - 1][GRID_SIZE - 1] or max == self.grid[0][GRID_SIZE - 1] or max == self.grid[GRID_SIZE - 1][0]:
            self.reward = 2 * self.reward
        self.reward = self.reward / 100
        return self.reward

    def is_game_over(self):
        # Check if any empty cells are available
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == 0:
                    return False
        
        # Check if any adjacent tiles have the same value
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if (i < GRID_SIZE - 1 and self.grid[i][j] == self.grid[i + 1][j]) or \
                (j < GRID_SIZE - 1 and self.grid[i][j] == self.grid[i][j + 1]):
                    return False
        return True

    def get_max_tile(self):
        return np.max(self.grid)
