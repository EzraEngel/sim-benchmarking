import os
import random
from typing import Any, Union
from sim_objects.agent import Agent
from sim_objects.occluder import Occluder
from sim_objects.base import SimObject
import copy
from utils.distribution_builder import DistributionBuilder


type WriterArgs = dict[str, Union[str, int]]

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
    def generate_geometric_benchmark_jobs(sim_size: dict[str, int], writer_args: WriterArgs) -> list[WriterArgs]:
        # --- Be wary of changing these unless you make updates to the hardcoded directory structure ---
        distributions = ["uniform", "normal"]
        movements = ["static", "dynamic"]
        los_strs = ["los", "no_los"]

        desired_targets_per_sensor: int
        num_agents: int
        fov: float
        view_range: float


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
                        los: str):

        # --- Set the random seed ---
        random.seed(random_seed)

        # --- Build the distribution from scenario ---
        distribution_builder = DistributionBuilder(targets_per_sensor, num_agents, fov, view_range)
        if dist == "uniform":
            distribution = distribution_builder.build_uniform()
        elif dist == "normal":
            distribution = distribution_builder.build_gauss()
        else:
            raise NotImplementedError

        # --- Make and write the Agents ---
        agents = [Agent.random(distribution=distribution, speed=speed, view_range=view_range, fov=fov) for i in range(num_agents)]
        if los == "no_los":
            SimObject.write_objects(file_path, agents=agents)
            return

        # --- Make and write the occluders ---
        occluders = [Occluder.random(distribution=distribution, scale=scale, shape=shape) for i in range(occ_per_agent * num_agents)]
        SimObject.write_objects(file_path, agents=agents, occluders=occluders)