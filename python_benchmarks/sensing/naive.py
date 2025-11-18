from sim_objects import agent, occluder
from geometry.float3 import Float3
import math
from python_benchmarks.sensing.utils import can_sensor_see_target

def get_targets_no_los(agents: list[agent.Agent]) -> int:
    num_targets = 0
    for sensor in agents:
        for target in agents:
            if can_sensor_see_target(sensor, target):
                num_targets += 1
    return num_targets

def get_targets_with_los(agents: list[agent.Agent], occluders: list[occluder.Occluder]) -> int:
    return 0