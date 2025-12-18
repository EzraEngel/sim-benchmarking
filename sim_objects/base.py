from dataclasses import dataclass, asdict
from geometry.float3 import Float3
from geometry.float4 import Float4
import json
from abc import ABC, abstractmethod
from typing import Any


@dataclass
class SimObject(ABC):
    """ Abstract base class for simulation objects. """
    type: str
    position: Float3
    rotation: Float4
    random_seed: int

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """ Returns a dictionary representation of the object. """
        pass

    @staticmethod
    def write_objects(filename: str, **entity_lists) -> None:
        """
        Writes objects to a json file. Note that this method is a static method which writes a *list*
        of objects. It does not write self. We do this so that we can exploit the nested capabilities of json.dumps,
        since ultimately we'll be writing a list of objects, not a single instance. Strictly, this could and should
        probably be in its own class.
        """
        json_dict = dict()
        for name, entity_list in entity_lists.items():
            json_dict[name] = [entity.to_dict() for entity in entity_list]
        with open(filename, 'w') as file:
            json_string = json.dumps(json_dict, indent=4)
            file.write(json_string)