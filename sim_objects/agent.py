import random
from dataclasses import dataclass
from geometry.float3 import Float3
from geometry.float4 import Float4
from sim_objects.base import SimObject


@dataclass
class Agent(SimObject):
    speed: float
    look_direction: Float3
    view_range: float
    field_of_view: float

    @classmethod
    def random(cls, speed: float, view_range: float, fov: float) -> 'Agent':
        position = Float3()
        look_direction = Float3.point_on_unit_sphere()
        rotation = Float4.from_axis(look_direction)
        random_seed = random.randint(0, 1000000000)
        return cls("agent", position, rotation, random_seed, speed, look_direction, view_range, fov)