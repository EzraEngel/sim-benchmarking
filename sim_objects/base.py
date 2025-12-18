from dataclasses import dataclass, asdict
from geometry.float3 import Float3
from geometry.float4 import Float4
import json
from abc import ABC, abstractmethod
from typing import Any


@dataclass
class SimObject(ABC):
    type: str
    position: Float3
    rotation: Float4
    random_seed: int

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        pass

    @staticmethod
    def write_objects(filename: str, **entity_lists) -> None:
        json_dict = dict()
        for name, entity_list in entity_lists.items():
            json_dict[name] = [entity.to_dict() for entity in entity_list]
        with open(filename, 'w') as file:
            json_string = json.dumps(json_dict, indent=4)
            file.write(json_string)