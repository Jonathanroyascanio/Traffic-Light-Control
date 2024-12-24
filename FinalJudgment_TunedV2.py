from stable_baselines3 import DQN
from stable_baselines3.common.monitor import Monitor
import os
import csv
os.environ['SUMO_HOME'] = '/opt/homebrew/share/sumo'
from sumo_rl import SumoEnvironment
models_dir = "./models"
logs_dir = "logs"
csv_file = "./independent_eval_TunedV2.csv"


if __name__=="__main__":
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    env = Monitor(SumoEnvironment(
        net_file="./environments/single-intersection.net.xml",
        route_file="./environments/random.rou.xml",
        single_agent=True,
        reward_fn='diff-waiting-time',
        use_gui=True,
        num_seconds=100000,
        begin_time=0
    ), logs_dir)
    # Get the trained model and load it
    model_path = os.path.join(models_dir, "DQN_tuned.zip")
    model = DQN.load(model_path, env=env)
    obs = env.reset()[0]
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['step', 'system_total_stopped', 'system_total_waiting_time', 'system_mean_waiting_time', 'system_mean_speed', 't_stopped', 't_accumulated_waiting_time', 't_average_speed', 'agents_total_stopped', 'agents_total_accumulated_waiting_time'])
        writer.writeheader()
        for _ in range(20000):
            action, _states = model.predict(obs)
            obs, rewards, dones,__, info = env.step(action)
            writer.writerow(info)
            if dones:
                print("Episode done, resetting the environment")
                obs = env.reset()
