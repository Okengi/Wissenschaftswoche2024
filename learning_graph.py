import matplotlib.pyplot as plt
from CONSTANTS import NUM_EPISODES

class Graph:
    rewards = []
    def __init__(self) -> None:
        self.fig, self.ax = plt.subplots()
        self.ax.set_title('Training Progress')
        self.reward_line, = self.ax.plot([], [], lw=2)

    def add_reward(self, reward, episode):
        self.rewards.append(reward)
        self.reward_line.set_data(range(len(self.rewards)), self.rewards)
        self.ax.relim()
        self.ax.autoscale_view()
        plt.pause(0.01)
        if episode >= NUM_EPISODES:
            plt.show()