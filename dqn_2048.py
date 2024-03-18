import numpy as np
import tensorflow as tf
import random
from collections import deque
from game2048 import Game2048

# Hyperparameter
LEARNING_RATE = 0.001
GAMMA = 0.95
MEMORY_SIZE = 10000
BATCH_SIZE = 32

class DQN:
    def __init__(self):
        self.model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(128, input_dim=GRID_SIZE**2, activation='relu'),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(4, activation='linear')
        ])
        self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE), loss='mse')
        self.memory = deque(maxlen=MEMORY_SIZE)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state, epsilon):
        if np.random.rand() <= epsilon:
            return random.randrange(4)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + GAMMA * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

def train_dqn():
    agent = DQN()
    game = Game2048()

    epsilon = 1.0
    epsilon_min = 0.01
    epsilon_decay = 0.995

    episodes = 10000
    for episode in range(1, episodes+1):
        state = game.get_state().reshape(1, -1)
        done = False
        while not done:
            action = agent.act(state, epsilon)
            game.move(action)
            next_state = game.get_state().reshape(1, -1)
            reward = game.score
            done = game.is_game_over()
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                print(f"Episode: {episode}, Score: {game.score}, Max Tile: {game.get_max_tile()}")
                break
            if len(agent.memory) > BATCH_SIZE:
                agent.replay(BATCH_SIZE)
        if epsilon > epsilon_min:
            epsilon *= epsilon_decay

    agent.save("dqn_2048.h5")

def play_game_with_dqn():
    agent = DQN()
    agent.load("dqn_2048.h5")
    game = Game2048()

    while True:
        state = game.get_state().reshape(1, -1)
        action = agent.act(state, 0)
        game.move(action)
        print("Score:", game.score)
        print(game.grid)
        if game.is_game_over():
            print("Game Over!")
            break

if __name__ == "__main__":
    train_dqn()
    play_game_with_dqn()
