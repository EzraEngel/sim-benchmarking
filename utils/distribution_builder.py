from dataclasses import dataclass
from utils.distributions import UniformSpatialDistribution, GaussianSpatialDistribution
from utils.sim_world import get_sensor_volume
from geometry.float3 import Float3
import math

@dataclass
class DistributionBuilder:
    desired_targets_per_sensor: int
    num_agents: int
    fov: float
    view_range: float

    def build_gauss(self) -> GaussianSpatialDistribution:
        scaling_factor = self._sigma()
        mu = Float3.zero()
        sigma = Float3.one() * scaling_factor
        return GaussianSpatialDistribution(mu, sigma)

    def build_uniform(self) -> UniformSpatialDistribution:
        sensor_volume = get_sensor_volume(self.fov, self.view_range)
        desired_density = self.desired_targets_per_sensor / sensor_volume
        desired_world_volume = self.num_agents / desired_density
        desired_world_dimensions = desired_world_volume ** (1.0 / 3.0)
        coord = desired_world_dimensions / 2
        min_f3 = Float3(-coord, -coord, -coord)
        max_f3 = Float3(coord, coord, coord)
        return UniformSpatialDistribution(min_f3, max_f3)

    def _sigma(self) -> float:
        sensor_volume = get_sensor_volume(self.fov, self.view_range)
        return (self.num_agents * sensor_volume / self.desired_targets_per_sensor) ** (1.0 / 3.0) / math.pi