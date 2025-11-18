import random
from dataclasses import dataclass
from geometry.float3 import Float3
from geometry.float4 import Float4
from sim_objects.base import SimObject


@dataclass
class Occluder(SimObject):
    scale: float
    shape: str

    @classmethod
    def random(cls, scale: float, shape: str) -> 'Occluder':
        position = Float3()
        orientation = Float3.point_on_unit_sphere()
        rotation = Float4.from_axis(orientation)
        random_seed = random.randint(0, 1000000000)
        return cls("occluder", position, rotation, random_seed, scale, shape)