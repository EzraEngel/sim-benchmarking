from dataclasses import dataclass
from utils.distributions import UniformSpatialDistribution, GaussianSpatialDistribution
from utils.sim_world import get_sensor_volume
from geometry.float3 import Float3
import math
from sim_objects.sensor import Sensor

@dataclass
class DistributionBuilder:
    num_agents: int

    def build_gauss_from_sensor_and_targets(self, sensor: Sensor, targets_per_sensor: int) -> GaussianSpatialDistribution:
        scaling_factor = self._sigma(sensor, targets_per_sensor)
        mu = Float3.zero()
        sigma = Float3.one() * scaling_factor
        return GaussianSpatialDistribution(mu, sigma)

    def build_uniform_from_sensor_and_targets(self, sensor: Sensor, targets_per_sensor: int) -> UniformSpatialDistribution:
        desired_density = targets_per_sensor / sensor.volume
        desired_world_volume = self.num_agents / desired_density
        desired_world_dimensions = desired_world_volume ** (1.0 / 3.0)
        coord = desired_world_dimensions / 2
        min_f3 = Float3(-coord, -coord, -coord)
        max_f3 = Float3(coord, coord, coord)
        return UniformSpatialDistribution(min_f3, max_f3)

    def _sigma(self, sensor: Sensor, targets_per_sensor: int) -> float:
        return (self.num_agents * sensor.volume / targets_per_sensor) ** (1.0 / 3.0) / math.pi