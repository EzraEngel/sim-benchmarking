from dataclasses import dataclass, asdict
from geometry.float3 import Float3
from geometry.float4 import Float4
import json


@dataclass
class SimObject:
    type: str
    position: Float3
    rotation: Float4
    random_seed: int

    def set_random_position(self, first: Float3, second: Float3, distribution: str) -> None:
        match distribution:
            case 'uniform':
                self.position = Float3.from_uniform(first, second)
            case 'normal':
                self.position = Float3.from_normal(first, second)

    @staticmethod
    def write_objects(filename: str, **entity_lists) -> None:
        json_dict = dict()
        for name, entity_list in entity_lists.items():
            json_dict[name] = [asdict(entity) for entity in entity_list]
        with open(filename, 'w') as file:
            json_string = json.dumps(json_dict, indent=4)
            file.write(json_string)