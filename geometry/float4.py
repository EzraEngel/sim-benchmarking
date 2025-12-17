from dataclasses import dataclass
import random
import math
from geometry.float3 import Float3

@dataclass
class Float4:
    w: float = 1
    x: float = 0
    y: float = 0
    z: float = 0

    def __post_init__(self) -> None:
        magnitude = math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
        if not math.isclose(magnitude, 1):
            raise ValueError(f"Quaternions must have magnitude 1.")

    @classmethod
    def from_theta_and_axis(cls, theta: float, axis: Float3) -> 'Float4':
        axis = axis.normalized()
        w = math.cos(theta / 2)
        x = axis.x * math.sin(theta / 2)
        y = axis.y * math.sin(theta / 2)
        z = axis.z * math.sin(theta / 2)
        return cls(w, x, y, z)

    @classmethod
    def from_axis(cls, axis: Float3) -> 'Float4':
        theta = random.random() * 2 * math.pi
        return cls.from_theta_and_axis(theta, axis)

    @classmethod
    def random(cls) -> 'Float4':
        theta = random.random() * 2 * math.pi
        axis = Float3.point_on_unit_sphere()
        return cls.from_theta_and_axis(theta, axis)