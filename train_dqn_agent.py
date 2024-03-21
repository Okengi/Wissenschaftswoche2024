import numpy as np
import random
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import time

from game2048 import Game2048
from learning_graph import Graph
from visuals import Visuals
from CONSTANTS import GRID_SIZE, NUM_EPISODES, MEMORY_SIZE, BATCH_SIZE, EPSILON_DECAY, MIN_EPSILON, GAMMA, MODEL_SAVE_LOCATION

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=MEMORY_SIZE)
        self.epsilon = 1.0
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(GRID_SIZE * GRID_SIZE, activation='relu'))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=MIN_EPSILON))
        
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        x = np.random.rand()
        if x <= self.epsilon:
            arr = np.random.choice(self.action_size, size=self.action_size, replace=False)

            return [arr,], True
        act_values = self.model.predict(state)
        return act_values, False
        #return np.argmax(act_values[0]), False

    def replay(self, batch_size):
        if len(self.memory) < batch_size: # when es nicht genug sampels gibt in der memory wird die function nicht ausgeführt
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
        
def train():
    state_size = GRID_SIZE * GRID_SIZE
    action_size = 4
    agent = DQNAgent(state_size, action_size)
    graph = Graph()
    
    for episode in range(NUM_EPISODES):
        game = Game2048()
        #visuals = Visuals(game, True)
        game_board, reward, is_game_over = game.get_state()
        #print(f"game_board: {game_board}\nreward: {reward}\nis_game_over: {is_game_over}")
        random_counter = 0
        desicion_counter = 0
        
        while not is_game_over:
            
            old_state = game_board
            actions, desicion_was_random = agent.act(game_board)
            if desicion_was_random:
                random_counter += 1
            else:
                desicion_counter += 1
            
            counter = 0
            old = game_board
            action = 0
            while np.array_equal(game_board, old):
                if counter >= 4:
                    is_game_over = True
                    break

                action_indexes = np.argsort(actions)[::-1]
                game_board, reward, is_game_over = game.move(action_indexes[0][counter])
                action = action_indexes[0][counter]
                counter += 1
                
            # game_board, reward, is_game_over = game.move(action)
            # visuals.move()
            
            agent.remember(old_state, action, reward, game_board, is_game_over)


        print(f"Episode: {episode + 1}/{NUM_EPISODES}, Reward: {reward}")
        graph.add_reward(reward, episode + 1)
        graph.add_random(random_counter, episode + 1)
        graph.add_desicion(desicion_counter, episode + 1)

        if (episode + 1) % BATCH_SIZE == 0:
            agent.replay(BATCH_SIZE)

    agent.model.save(MODEL_SAVE_LOCATION)
    

if __name__ == "__main__":
    train()