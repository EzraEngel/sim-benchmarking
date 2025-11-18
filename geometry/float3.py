from dataclasses import dataclass
import random
import math

@dataclass
class Float3:
    x: float = 0
    y: float = 0
    z: float = 0

    @classmethod
    def from_uniform(cls, min_f3: 'Float3', max_f3: 'Float3') -> 'Float3':
        x = random.uniform(min_f3.x, max_f3.x)
        y = random.uniform(min_f3.y, max_f3.y)
        z = random.uniform(min_f3.z, max_f3.z)
        return cls(x, y, z)

    @classmethod
    def from_normal(cls, mu: 'Float3', sigma: 'Float3') -> 'Float3':
        x = random.gauss(mu.x, sigma.x)
        y = random.gauss(mu.y, sigma.y)
        z = random.gauss(mu.z, sigma.z)
        return cls(x, y, z)

    @classmethod
    def point_on_unit_sphere(cls) -> 'Float3':
        theta = random.uniform(0, math.pi)
        phi = random.uniform(0, 2 * math.pi)
        x = math.sin(theta) * math.cos(phi)
        y = math.sin(theta) * math.sin(phi)
        z = math.cos(theta)
        return cls(x, y, z)

    @classmethod
    def zero(cls) -> 'Float3':
        return cls(0, 0, 0)

    @classmethod
    def one(cls) -> 'Float3':
        return cls(1, 1, 1)

    def to_int(self) -> tuple[int, int, int]:
        return int(self.x), int(self.y), int(self.z)

    def __add__(self, other: 'Float3') -> 'Float3':
        return Float3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Float3') -> 'Float3':
        return Float3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __floordiv__(self, other: float) -> 'Float3':
        return Float3(self.x // other, self.y // other, self.z // other)

    def __gt__(self, other: 'Float3') -> bool:
        return self.x > other.x and self.y > other.y and self.z > other.z

    def __ge__(self, other: 'Float3') -> bool:
        return self.x >= other.x and self.y >= other.y and self.z >= other.z

    def __lt__(self, other: 'Float3') -> bool:
        return self.x < other.x and self.y < other.y and self.z < other.z

    def __le__(self, other: 'Float3') -> bool:
        return self.x <= other.x and self.y <= other.y and self.z <= other.z

    def __eq__(self, other: 'Float3') -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other: 'Float3') -> bool:
        return self.x != other.x or self.y != other.y or self.z != other.z

    def __mul__(self, other: float) -> 'Float3':
        return Float3(self.x * other, self.y * other, self.z * other)

    def dot(self, other: 'Float3') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self) -> None:
        mag = self.magnitude()
        self.x /= mag
        self.y /= mag
        self.z /= mag

    def normalized(self) -> 'Float3':
        mag = self.magnitude()
        x = self.x / mag
        y = self.y / mag
        z = self.z / mag
        return Float3(x, y, z)

    @staticmethod
    def distance(first: 'Float3', second: 'Float3') -> float:
        return (first - second).magnitude()