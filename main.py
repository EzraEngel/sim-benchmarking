import random
from sim_objects.agent import Agent, SimObject
from sim_objects.occluder import Occluder
from utils.sim_world import get_area_from_desired_target_num, get_normal_from_desired_target_num
from python_benchmarks import sensing
from geometry.float3 import Float3

def main():
    # --- Parameterize the Agents Randomly ---
    random.seed(42)
    targets_per_sensor, num_agents, speed, fov, view_range = 5, 1000, 1, 60, 5
    num_occluders = 5000
    dist = "normal"

    agents = [Agent.random(speed=speed, view_range=view_range, fov=fov) for i in range(num_agents)]
    occluders = [Occluder.random(scale=0.1, shape="cube") for i in range(num_occluders)]

    # We'd like to sample from the same distribution for both agents *and* occluders.
    # The fact that we're deriving distribution params from num_agents for both sets of
    # simulation objects is the intended behavior.
    distribution_generator = {"uniform": get_area_from_desired_target_num, "normal": get_normal_from_desired_target_num}
    distribution_params = distribution_generator[dist](targets_per_sensor, num_agents, fov, view_range)

    for agent in agents:
        agent.set_random_position(*distribution_params)

    for occluder in occluders:
        occluder.set_random_position(*distribution_params)

    # --- Write the Agents to a File ---
    SimObject.write_objects("objects.json", agents=agents, occluders=occluders)

    # --- Test Output Internally ---
    num_targets = sensing.spatial_hashing.get_targets_no_los(agents)
    print(num_targets)

if __name__ == '__main__':
    main()