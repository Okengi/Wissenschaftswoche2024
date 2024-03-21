import matplotlib.pyplot as plt
from CONSTANTS import NUM_EPISODES

class Graph:
    rewards = []
    randoms = []
    desicions = []
    def __init__(self) -> None:
        self.fig, self.ax = plt.subplots(2)
        self.fig.suptitle('Training Progress')
        self.reward_line, = self.ax[0].plot([], [], lw=2)
        self.random_line, = self.ax[1].plot([], [], lw=2)
        self.desicion_line, = self.ax[1].plot([], [], lw=4)

    def add_reward(self, reward, episode):
        self.rewards.append(reward)
        self.reward_line.set_data(range(len(self.rewards)), self.rewards)
        self.ax[0].relim()
        self.ax[0].autoscale_view()
        plt.pause(0.01)
        if episode >= NUM_EPISODES:
            plt.show()

    def add_random(self, random, episode):
        self.randoms.append(random)
        self.random_line.set_data(range(len(self.randoms)), self.randoms)
        self.ax[1].relim()
        self.ax[1].autoscale_view()
        plt.pause(0.01)
        if episode >= NUM_EPISODES:
            plt.show()

    def add_desicion(self, desicion, episode):
        self.desicions.append(desicion)
        self.desicion_line.set_data(range(len(self.desicions)), self.desicions)
        self.ax[1].relim()
        self.ax[1].autoscale_view()
        plt.pause(0.01)
        if episode >= NUM_EPISODES:
            plt.show()