import os
import random
from typing import Callable, Any
from geometry.float3 import Float3
from sim_objects.agent import Agent
from sim_objects.occluder import Occluder
from sim_objects.base import SimObject
from utils.sim_world import get_area_from_desired_target_num, get_normal_from_desired_target_num
import copy

distribution_generator = Callable[[int, int, float, float], tuple[Float3, Float3, str]]
class BenchmarkSetup:
    benchmark_dirs = [
        os.path.join("benchmarks", "geometry", "uniform_static_no_los"),
        os.path.join("benchmarks", "geometry", "uniform_static_los"),
        os.path.join("benchmarks", "geometry", "uniform_dynamic_no_los"),
        os.path.join("benchmarks", "geometry", "uniform_dynamic_los"),
        os.path.join("benchmarks", "geometry", "normal_static_no_los"),
        os.path.join("benchmarks", "geometry", "normal_static_los"),
        os.path.join("benchmarks", "geometry", "normal_dynamic_no_los"),
        os.path.join("benchmarks", "geometry", "normal_dynamic_los"),
        os.path.join("benchmarks", "graphs", "disjoint_network"),
        os.path.join("benchmarks", "graphs", "pathfinding"),
        os.path.join("benchmarks", "graphs", "network_routing"),
        os.path.join("benchmarks", "graphs", "weapon_target_assignment"),
        os.path.join("benchmarks", "graphs", "supply_network"),
        os.path.join("benchmarks", "propagation", "radar"),
        os.path.join("benchmarks", "propagation", "threat"),
        os.path.join("benchmarks", "propagation", "contamination")
    ]

    @staticmethod
    def set_up_benchmark_dirs() -> None:
        for benchmark_dir in BenchmarkSetup.benchmark_dirs:
            if not os.path.exists(benchmark_dir):
                os.makedirs(benchmark_dir)

    @staticmethod
    def generate_geometric_benchmark_jobs(sim_size, writer_args) -> list[dict[str, Any]]:
        # --- Be wary of changing these unless you make updates to the hardcoded directory structure ---
        distributions = ["uniform", "normal"]
        movements = ["static", "dynamic"]
        los_strs = ["los", "no_los"]

        # --- Distribution generators ---
        generators: dict[str, distribution_generator] = {
            "uniform": get_area_from_desired_target_num,
            "normal": get_normal_from_desired_target_num
        }
        writer_args['dist_generator'] = generators

        job_list: list[dict[str, Any]] = []
        # --- Write all the benchmark configs ---
        for dist in distributions:
            for move in movements:
                for los in los_strs:
                    for size_name, num_agents in sim_size.items():
                        file_name = f"{dist}_{move}_{los}_{size_name}.json"
                        file_path = os.path.join("benchmarks", "geometry", f"{dist}_{move}_{los}", file_name)
                        writer_args["file_path"] = file_path
                        writer_args["los"] = los
                        writer_args["dist"] = dist
                        writer_args["num_agents"] = num_agents
                        job_list.append(copy.deepcopy(writer_args))
        return job_list

    @staticmethod
    def process_objects(file_path: str,
                        random_seed: int,
                        num_agents: int,
                        speed: float,
                        fov: float,
                        view_range: float,
                        occ_per_agent: int,
                        scale: float,
                        shape: str,
                        targets_per_sensor: int,
                        dist: str,
                        dist_generator: dict[str, distribution_generator],
                        los: str):

        # --- Set the random seed ---
        random.seed(random_seed)

        # --- Make and write the Agents ---
        agents = [Agent.random(speed=speed, view_range=view_range, fov=fov) for i in range(num_agents)]
        dist_params = dist_generator[dist](targets_per_sensor, num_agents, fov, view_range)
        for agent in agents:
            agent.set_random_position(*dist_params)
        if los == "no_los":
            SimObject.write_objects(file_path, agents=agents)
            return

        # --- Make and write the occluders ---
        occluders = [Occluder.random(scale=scale, shape=shape) for i in range(occ_per_agent * num_agents)]
        for occluder in occluders:
            occluder.set_random_position(*dist_params)
        SimObject.write_objects(file_path, agents=agents, occluders=occluders)