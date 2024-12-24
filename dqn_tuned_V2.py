import os
os.environ['SUMO_HOME'] = '/opt/homebrew/share/sumo'
import traci
import stable_baselines3
from sumo_rl import SumoEnvironment
from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import CallbackList, CheckpointCallback, EvalCallback
from stable_baselines3.common.monitor import Monitor

models_dir = "./models/DQN_tuned"
logs_dir = "logs"

#Training code for Tuned V2
if __name__=="__main__":
    steps_per_episode = 4000
    total_episodes = 200
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    # Create custom environment with our configuration xml files and the change in cumulative vehicle delay as a reward function
    env = Monitor(SumoEnvironment(
        net_file="./environments/single-intersection.net.xml",
        route_file="./environments/single-intersection-vhvh.rou.xml",
        single_agent=True,
        reward_fn='diff-waiting-time',
        use_gui=True,
        num_seconds=steps_per_episode,
        begin_time=0
        ), logs_dir)
    model = DQN(
        "MlpPolicy",
        env,
        gamma=0.95,
        learning_rate=0.0002,
        buffer_size=100000,
        batch_size=32,
        target_update_interval=4000 / 5,  # Update target network every episode (agent acts every 5 simulation step)
        exploration_initial_eps=0.9,
        exploration_final_eps=0.1, 
        exploration_fraction=0.1,
        tensorboard_log=logs_dir,
        verbose=1
    )
    model.learn(total_timesteps=steps_per_episode*total_episodes, reset_num_timesteps=False, tb_log_name="DQN_tuned")
    model.save(models_dir)



  