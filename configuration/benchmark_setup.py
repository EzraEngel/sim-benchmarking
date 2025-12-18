import os
import random
from typing import Any, Union
from sim_objects.agent import Agent
from sim_objects.occluder import Occluder
from sim_objects.base import SimObject
import copy
from enum import StrEnum, auto
from sim_objects.sensor import SphericalSectorSensor
from utils.distribution_builder import DistributionBuilder


type WriterArgs = dict[str, Union[str, int]]

class DistType(StrEnum):
    UNIFORM = auto()
    NORMAL = auto()

class MoveType(StrEnum):
    STATIC = auto()
    DYNAMIC = auto()

class LOSType(StrEnum):
    LOS = auto()
    NO_LOS = auto()

class BenchmarkSetup:
    """
    This is a class that holds most of the methods and parameterization for the benchmark configuration.
    It defines a directory structure, and calls a series of methods to instantiate the correct objects and
    dump them into json files.
    """
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
        """ Sets up the directory structure on the host. """
        for benchmark_dir in BenchmarkSetup.benchmark_dirs:
            if not os.path.exists(benchmark_dir):
                os.makedirs(benchmark_dir)

    @staticmethod
    def generate_geometric_benchmark_jobs(sim_size: dict[str, int], writer_args: WriterArgs) -> list[WriterArgs]:
        """
        Generates a list of benchmark jobs to run in parallel. Be wary of modifying the hardcoded parameters below
        without corresponding changes to the directory structure.
        """

        distributions = [DistType.UNIFORM, DistType.NORMAL]
        movements = [MoveType.STATIC, MoveType.DYNAMIC]
        los_strs = [LOSType.LOS, LOSType.NO_LOS]

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
                        dist: DistType,
                        los: LOSType) -> None:
        """
        This is the callable which is dispatched to the multiprocessing module. The scrip in __main__.py will fork
        the process and execute this method in the child. It takes an unpacked set of writer arguments as parameters
        which you can observe in the __main__.py file.
        """

        # --- Set the random seed ---
        random.seed(random_seed)

        # --- Build the sensor ---
        sensor = SphericalSectorSensor(view_range=view_range, field_of_view=fov)

        # --- Build the distribution from scenario ---
        distribution_builder = DistributionBuilder(num_agents)
        if dist == DistType.UNIFORM:
            distribution = distribution_builder.build_uniform_from_sensor_and_targets(sensor, targets_per_sensor)
        elif dist == DistType.NORMAL:
            distribution = distribution_builder.build_gauss_from_sensor_and_targets(sensor, targets_per_sensor)
        else:
            raise NotImplementedError

        # --- Make and write the Agents ---
        agents = [Agent.random(distribution=distribution, speed=speed, sensor=sensor) for i in range(num_agents)]
        if los == LOSType.NO_LOS:
            SimObject.write_objects(file_path, agents=agents)
            return

        # --- Make and write the occluders ---
        occluders = [Occluder.random(distribution=distribution, scale=scale, shape=shape) for i in range(occ_per_agent * num_agents)]
        SimObject.write_objects(file_path, agents=agents, occluders=occluders)