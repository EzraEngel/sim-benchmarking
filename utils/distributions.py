from geometry.float3 import Float3
from dataclasses import dataclass
from abc import ABC, abstractmethod
import random

class SpatialDistribution(ABC):
    @abstractmethod
    def get_float3(self) -> Float3:
        pass


@dataclass
class UniformSpatialDistribution(SpatialDistribution):
    min_f3: Float3
    max_f3: Float3

    def get_float3(self) -> Float3:
        x = random.uniform(self.min_f3.x, self.max_f3.x)
        y = random.uniform(self.min_f3.y, self.max_f3.y)
        z = random.uniform(self.min_f3.z, self.max_f3.z)
        return Float3(x, y, z)


@dataclass
class GaussianSpatialDistribution(SpatialDistribution):
    mu: Float3
    sigma: Float3

    def get_float3(self) -> Float3:
        x = random.gauss(self.mu.x, self.sigma.x)
        y = random.gauss(self.mu.y, self.sigma.y)
        z = random.gauss(self.mu.z, self.sigma.z)
        return Float3(x, y, z)

