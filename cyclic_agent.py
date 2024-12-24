import os
import sys
import traci
os.environ['SUMO_HOME'] = '/opt/homebrew/share/sumo'
from sumo_rl import SumoEnvironment
import csv
csv_file = "./independent_eval_cyclic.csv"


class CyclicAgent:
    def __init__(self, num_actions):
        self.current_action = 0
        self.num_actions = num_actions

    def select_action(self):
        action = self.current_action
        self.current_action = (self.current_action + 1) % self.num_actions
        return action
# Assuming the environment and agent are already created



if __name__ == "__main__":
    steps_per_episode = 20000
    total_episodes = 1
    env = SumoEnvironment(
    net_file="./environments/single-intersection.net.xml",
    route_file="./environments/random.rou.xml",
    single_agent=True,
    use_gui=False,
    num_seconds=steps_per_episode,  # Duration of the simulation in seconds
    begin_time=0,  # Time when the simulation should start
    reward_fn="diff-waiting-time"
    )
    agent = CyclicAgent(env.action_space.n)
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['step', 'system_total_stopped', 'system_total_waiting_time', 'system_mean_waiting_time', 'system_mean_speed', 't_stopped', 't_accumulated_waiting_time', 't_average_speed', 'agents_total_stopped', 'agents_total_accumulated_waiting_time'])
        writer.writeheader()
        for ep in range(total_episodes):
            observation = env.reset()
            print(f"Starting episode {ep}")
            for step in range(steps_per_episode):
                action = agent.select_action()
                observation, reward, done, ___ , info = env.step(action)
                writer.writerow(info)
