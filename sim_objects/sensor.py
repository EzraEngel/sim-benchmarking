from abc import ABC, abstractmethod
import math
from dataclasses import dataclass, field
from geometry.float3 import Float3


@dataclass(kw_only=True)
class Sensor(ABC):
    """ Abstract sensor class. Must have an orientation. """
    look_direction: Float3 = field(default_factory=Float3.zero)

    @property
    @abstractmethod
    def volume(self):
        pass

@dataclass(kw_only=True)
class SphericalSectorSensor(Sensor):
    """
    Represents a spherical sector sensor. In a piece of simulation software, this can be queries via
    a sphere overlap query and dot product check.
    """
    field_of_view: float
    view_range: float

    @property
    def volume(self):
        """ Returns the volume of the spherical sector. """
        fov_half_angle = math.radians(self.field_of_view / 2.0)
        sphere_fraction = (1 - math.cos(fov_half_angle)) / 2.0
        sphere_volume = (4.0 / 3.0) * math.pi * self.view_range ** 3
        sensor_volume = sphere_volume * sphere_fraction
        return sensor_volume