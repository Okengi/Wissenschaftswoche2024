import numpy as np
import random

GRID_SIZE = 4

class Game2048:
    def __init__(self):
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE))
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def move(self, direction):
        original_grid = np.copy(self.grid)
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

    def merge(self, row):
        new_row = [i for i in row if i != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                new_row[i + 1] = 0
                self.score += new_row[i]
        new_row = [i for i in new_row if i != 0]
        new_row += [0] * (GRID_SIZE - len(new_row))
        return new_row

    def get_state(self):
        return self.grid.flatten()

    def is_game_over(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == 0:
                    return False
                if j < GRID_SIZE - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
                if i < GRID_SIZE - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
        return True

    def get_max_tile(self):
        return np.max(self.grid)
