import math
from geometry.float3 import Float3

def get_sensor_volume(fov: float, view_range: float) -> float:
    fov_half_angle = math.radians(fov / 2.0)
    sphere_fraction = (1 - math.cos(fov_half_angle)) / 2.0
    sphere_volume = (4.0 / 3.0) * math.pi * view_range ** 3
    sensor_volume = sphere_volume * sphere_fraction
    return sensor_volume

def get_area_from_desired_target_num(desired_targets_per_sensor: int,
                                     num_agents: int,
                                     fov: float,
                                     view_range: float) -> tuple[Float3, Float3, str]:
    sensor_volume = get_sensor_volume(fov, view_range)
    desired_density = desired_targets_per_sensor / sensor_volume
    desired_world_volume = num_agents / desired_density
    desired_world_dimensions = desired_world_volume ** (1.0 / 3.0)
    coord = desired_world_dimensions / 2
    min_f3 = Float3(-coord, -coord, -coord)
    max_f3 = Float3(coord, coord, coord)
    return min_f3, max_f3, "uniform"

def get_normal_from_desired_target_num(desired_targets_per_sensor: int,
                                       num_agents: int,
                                       fov: float,
                                       view_range: float) -> tuple[Float3, Float3, str]:
    sensor_volume = get_sensor_volume(fov, view_range)
    scaling_factor = calculate_normal_scaling_factor(num_agents, sensor_volume, desired_targets_per_sensor)
    mu = Float3.zero()
    sigma = Float3.one()*scaling_factor
    return mu, sigma, "normal"

# This is some very tricky math here. Essentially, the volume, num_agents, and
# desired targets all represent factors which have volumetric components. Because
# we'll be using them to scale three independent axes, we need to take the cubic
# root. The math.pi represents a scalar component that simply seems to work, and
# was validated over a wide range of input values.
def calculate_normal_scaling_factor(num_agents: int, sensor_volume: float, desired_targets_per_sensor: int) -> float:
    return (num_agents * sensor_volume / desired_targets_per_sensor) ** (1.0 / 3.0) / math.pi
