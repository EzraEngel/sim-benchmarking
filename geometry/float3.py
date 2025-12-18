from dataclasses import dataclass
import random
import math

@dataclass
class Float3:
    """
    Represents a vector-3 object, or a point in 3D space. Can do normal vector things.
    """
    x: float = 0
    y: float = 0
    z: float = 0

    @classmethod
    def from_uniform(cls, min_f3: 'Float3', max_f3: 'Float3') -> 'Float3':
        """ Return a random float3 from inside the given bounds. """
        x = random.uniform(min_f3.x, max_f3.x)
        y = random.uniform(min_f3.y, max_f3.y)
        z = random.uniform(min_f3.z, max_f3.z)
        return cls(x, y, z)

    @classmethod
    def from_normal(cls, mu: 'Float3', sigma: 'Float3') -> 'Float3':
        """
        Return a normally distributed float3 given mean and standard deviation. Note that sigma accepts
        a float3, so this method supports non-spherical distributions.
        """
        x = random.gauss(mu.x, sigma.x)
        y = random.gauss(mu.y, sigma.y)
        z = random.gauss(mu.z, sigma.z)
        return cls(x, y, z)

    @classmethod
    def point_on_unit_sphere(cls) -> 'Float3':
        """ Return a point on the unit sphere."""
        return cls.from_normal(cls.zero(), cls.one()).normalized()

    @classmethod
    def zero(cls) -> 'Float3':
        """ Return a zero vector. """
        return cls(0, 0, 0)

    @classmethod
    def one(cls) -> 'Float3':
        """ Return a one vector. """
        return cls(1, 1, 1)

    def to_int(self) -> tuple[int, int, int]:
        """ Convert the object to an integer tuple. Useful for spatial hashing. """
        return int(self.x), int(self.y), int(self.z)

    def __add__(self, other: 'Float3') -> 'Float3':
        """ Return the sum of two Float3. """
        return Float3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Float3') -> 'Float3':
        """ Return the difference of two Float3. """
        return Float3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __floordiv__(self, other: float) -> 'Float3':
        """ Return the element-wise quotient of two Float3. """
        return Float3(self.x // other, self.y // other, self.z // other)

    def __gt__(self, other: 'Float3') -> bool:
        """ Return true if object is strictly greater than the another float3 along all axes. """
        return self.x > other.x and self.y > other.y and self.z > other.z

    def __ge__(self, other: 'Float3') -> bool:
        """ Return true if object is greater than or equal to another float3 along all axes. """
        return self.x >= other.x and self.y >= other.y and self.z >= other.z

    def __lt__(self, other: 'Float3') -> bool:
        """ Return true if object is less than another float3 along all axes. """
        return self.x < other.x and self.y < other.y and self.z < other.z

    def __le__(self, other: 'Float3') -> bool:
        """ Return true if object is less than or equal to another float3 along all axes. """
        return self.x <= other.x and self.y <= other.y and self.z <= other.z

    def __eq__(self, other: 'Float3') -> bool:
        """ Return true if object is equal to another float3 along all axes. """
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other: 'Float3') -> bool:
        """ Return true if object is not equal to another float3 along ANY axis. """
        return not (self == other)

    def __mul__(self, other: float) -> 'Float3':
        """ Return the element-wise scalar product of a float3 with a scalar. """
        return Float3(self.x * other, self.y * other, self.z * other)

    def dot(self, other: 'Float3') -> float:
        """ Returns the dot product of two Float3. """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def magnitude(self) -> float:
        """ Returns the magnitude of the Float3. """
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self) -> None:
        """ Normalizes the Float3. """
        mag = self.magnitude()
        self.x /= mag
        self.y /= mag
        self.z /= mag

    def normalized(self) -> 'Float3':
        """ Returns the normalized Float3. """
        mag = self.magnitude()
        x = self.x / mag
        y = self.y / mag
        z = self.z / mag
        return Float3(x, y, z)

    @staticmethod
    def distance(first: 'Float3', second: 'Float3') -> float:
        """ Returns the distance between two Float3. """
        return (first - second).magnitude()