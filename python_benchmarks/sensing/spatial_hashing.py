from sim_objects.agent import Agent
from sim_objects.occluder import Occluder
from geometry.float3 import Float3
from geometry.aabb import AABB
from python_benchmarks.sensing.utils import can_sensor_see_target
from typing import NamedTuple

class Int3(NamedTuple):
    x: int
    y: int
    z: int

class SpatialGrid:
    aabb: AABB
    cell_size: float
    grid: list[list[list[list[Agent]]]]
    dims: Int3
    entity_count: int = 0

    def __init__(self, aabb, cell_size) -> None:
        self.aabb = aabb
        self.cell_size = cell_size
        self.dims = Int3(*((aabb.dimensions() // cell_size) + Float3.one()).to_int())
        self.grid = [[[[] for z in range(self.dims[2])] for y in range(self.dims[1])] for x in range(self.dims[0])]

    def _position_to_index(self, position: Float3) -> Int3:
        delta = position - self.aabb.min_f3
        assert (delta >= Float3.zero())
        x_idx = int(delta.x / self.cell_size)
        y_idx = int(delta.y / self.cell_size)
        z_idx = int(delta.z / self.cell_size)
        return self._clamp_idx(Int3(x_idx, y_idx, z_idx))

    def _clamp_idx(self, idx: Int3) -> Int3:
        x_idx = max(0, min(idx.x, self.dims.x - 1))
        y_idx = max(0, min(idx.y, self.dims.y - 1))
        z_idx = max(0, min(idx.z, self.dims.z - 1))
        return Int3(x_idx, y_idx, z_idx)

    def emplace_agent(self, agent: Agent) -> None:
        idx = self._position_to_index(agent.position)
        self.grid[idx.x][idx.y][idx.z].append(agent)
        self.entity_count += 1

    def query_grid(self, position: Float3, view_range: float) -> list[Agent]:
        # --- Get the center index and the spread ---
        d_idx = int(view_range // self.cell_size)
        ctr = self._position_to_index(position)

        # --- Set the iterations ranges for the loop with bounds checks ---
        min_x, max_x = max(0, ctr.x - d_idx), min(self.dims.x, ctr.x + d_idx + 1)
        min_y, max_y = max(0, ctr.y - d_idx), min(self.dims.y, ctr.y + d_idx + 1)
        min_z, max_z = max(0, ctr.z - d_idx), min(self.dims.z, ctr.z + d_idx + 1)

        # --- Iterate through the cells and add to potential target list ---
        targets_in_range = []
        for x_idx in range(min_x, max_x):
            for y_idx in range(min_y, max_y):
                for z_idx in range(min_z, max_z):
                    targets_in_range.extend(self.grid[x_idx][y_idx][z_idx])
        return targets_in_range


def get_targets_no_los(agents: list[Agent]) -> int:
    # --- Get the world AABB ---
    world_aabb = AABB.empty()
    for agent in agents:
        world_aabb.expand_point(agent.position)

    # --- Make and populate the spatial grid ---
    cell_size = agents[0].view_range # Only efficient if agents all have same view range
    spatial_grid = SpatialGrid(world_aabb, cell_size)
    for agent in agents:
        spatial_grid.emplace_agent(agent)

    # --- Query the spatial grid ---
    num_targets = 0
    for sensor in agents:
        targets = spatial_grid.query_grid(sensor.position, sensor.view_range)
        for target in targets:
            if can_sensor_see_target(sensor, target):
                num_targets += 1
    return num_targets


def get_targets_with_los(agents: list[Agent], occluders: list[Occluder]) -> int:
    return 0