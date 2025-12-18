from geometry.float3 import Float3
from sim_objects.agent import Agent
import math

def can_sensor_see_target(agent: Agent, target: Agent) -> bool:
    """
    Checks whether target is in sensor volume. Assumes a SphericalSectorSensor.
    """
    # --- A sensor can't see itself ---
    if agent == target:
        return False

    # --- A sensor can only see a target if it's in range AND within the FOV
    distance = Float3.distance(target.position, agent.position)
    direction = target.position - agent.position
    angle = math.degrees(math.acos(direction.dot(agent.sensor.look_direction) / direction.magnitude()))
    if distance <= agent.sensor.view_range and angle <= agent.sensor.field_of_view / 2:
        return True

    # --- Otherwise, we can't see it
    return False