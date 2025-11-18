from geometry.float3 import Float3
from sim_objects.agent import Agent
import math

def can_sensor_see_target(sensor: Agent, target: Agent) -> bool:
    # --- A sensor can't see itself ---
    if sensor == target:
        return False

    # --- A sensor can only see a target if it's in range AND within the FOV
    distance = Float3.distance(target.position, sensor.position)
    direction = target.position - sensor.position
    angle = math.degrees(math.acos(direction.dot(sensor.look_direction) / direction.magnitude()))
    if distance <= sensor.view_range and angle <= sensor.field_of_view / 2:
        return True

    # --- Otherwise, we can't see it
    return False