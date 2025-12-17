import math

def get_sensor_volume(fov: float, view_range: float) -> float:
    fov_half_angle = math.radians(fov / 2.0)
    sphere_fraction = (1 - math.cos(fov_half_angle)) / 2.0
    sphere_volume = (4.0 / 3.0) * math.pi * view_range ** 3
    sensor_volume = sphere_volume * sphere_fraction
    return sensor_volume
