import numpy as np
import random
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import matplotlib.pyplot as plt

from game2048 import Game2048

GRID_SIZE = 4
NUM_EPISODES = 100
MEMORY_SIZE = 1000
BATCH_SIZE = 128
EPSILON_DECAY = 0.995
MIN_EPSILON = 0.01
GAMMA = 0.95

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=MEMORY_SIZE)
        self.epsilon = 1.0
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(128, input_dim=self.state_size, activation='relu'))
        model.add(Dense(64, activation='linear'))
        model.add(Dense(16, activation='linear'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam())
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return

        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + GAMMA * np.max(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > MIN_EPSILON:
            self.epsilon *= EPSILON_DECAY

# Main function for training the AI agent
def train():
    state_size = GRID_SIZE * GRID_SIZE
    action_size = 4
    agent = DQNAgent(state_size, action_size)

    rewards = []  # List to store total rewards per episode
    scores = []

    fig, ax = plt.subplots()
    ax.set_xlabel('Episode')
    ax.set_ylabel('Total Reward')
    ax.set_title('Training Progress')
    line, = ax.plot([], [], lw=2)
    linee, = ax.plot([], [], lw=4)
    
    for episode in range(NUM_EPISODES):
        game = Game2048(GRID_SIZE)
        state_tuple = game.get_state()
        game_board_flat = state_tuple[0]
        total_reward = state_tuple[1]
        done = state_tuple[2]
        
        game_board_flat = game_board_flat.reshape(1, GRID_SIZE*GRID_SIZE)
        state = game_board_flat

        while not done:
            action = agent.act(state)
            next_state, reward, done = game.move(action)
            total_reward += reward
            next_state = next_state.reshape(1, state_size)
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            
        rewards.append(reward)
        scores.append(game.score)
        line.set_data(range(episode + 1), rewards)
        linee.set_data(range(episode + 1), scores)
        ax.relim()
        ax.autoscale_view()

        print(f"Episode: {episode + 1}/{NUM_EPISODES}, Total Reward: {total_reward}")
        if (episode + 1) % BATCH_SIZE == 0:
            agent.replay(BATCH_SIZE)

    agent.model.save('2048_ai_model.keras')
    plt.show()
    

if __name__ == "__main__":
    train()