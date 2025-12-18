import random
from dataclasses import dataclass, asdict
from geometry.float3 import Float3
from geometry.float4 import Float4
from sim_objects.base import SimObject
from utils.distributions import SpatialDistribution, GaussianSpatialDistribution
from sim_objects.sensor import Sensor, SphericalSectorSensor
from copy import deepcopy
from typing import Any


@dataclass
class Agent(SimObject):
    """ Represents an agent in the simulation. """
    speed: float
    sensor: Sensor

    @classmethod
    def random(cls, distribution: SpatialDistribution, speed: float, sensor: Sensor) -> 'Agent':
        """ Creates a random agent in the simulation drawn from the given distribution. """
        position = distribution.get_float3()
        look_direction = Float3.point_on_unit_sphere()
        rotation = Float4.from_axis(look_direction)
        random_seed = random.randint(0, 1000000000)
        new_sensor = deepcopy(sensor)
        new_sensor.look_direction = look_direction
        return cls("agent", position, rotation, random_seed, speed, new_sensor)

    def to_dict(self) -> dict[str, Any]:
        """ Returns a dictionary representation of the agent. Flattens sensor data to satisfy standard json interface. """
        data = asdict(self)
        sensor_data = data.pop("sensor")
        return {**data, **sensor_data}