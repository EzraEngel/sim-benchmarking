from geometry.float3 import Float3
from dataclasses import dataclass

@dataclass
class AABB:
    """
    Represents an axis aligned bounding box and holds relevant methods.
    """
    min_f3: Float3
    max_f3: Float3

    @classmethod
    def empty(cls) -> 'AABB':
        """ Returns an empty AABB. """
        neg_inf = Float3(float("-inf"), float("-inf"), float("-inf"))
        pos_inf = Float3(float("inf"), float("inf"), float("inf"))
        return cls(pos_inf, neg_inf)

    def expand_point(self, point: Float3) -> None:
        """ Expands a bounding box to include the given point. """
        self.min_f3.x = min(self.min_f3.x, point.x)
        self.min_f3.y = min(self.min_f3.y, point.y)
        self.min_f3.z = min(self.min_f3.z, point.z)
        self.max_f3.x = max(self.max_f3.x, point.x)
        self.max_f3.y = max(self.max_f3.y, point.y)
        self.max_f3.z = max(self.max_f3.z, point.z)

    def expand_aabb(self, aabb: 'AABB') -> None:
        """ Expands a bounding box to include the given AABB. """
        self.expand_point(aabb.min_f3)
        self.expand_point(aabb.max_f3)

    def dimensions(self) -> Float3:
        """ Returns the dimensions of the AABB. """
        return self.max_f3 - self.min_f3

    def volume(self) -> float:
        """ Returns the volume of the AABB. """
        dims = self.dimensions()
        return dims.dot(dims)



