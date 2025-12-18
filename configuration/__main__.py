from configuration.benchmark_setup import BenchmarkSetup, WriterArgs
from multiprocessing import Process
from typing import Any
from configuration.ui import SetupUI

def main() -> list[WriterArgs]:
    """
    This method exists only as an access point to control the configuration of the scenario builder.
    First, it sets up the directory structure. Then, the user can define sizes and parameters. Then,
    it returns a list of jobs to run. We return a list of jobs, because generating the configs can
    actually take quite a long time without multithreading support. The multithreading support is
    baked into the module itself at the bottom of this file.
    """
    BenchmarkSetup.set_up_benchmark_dirs()

    # --- Sim size corresponds to number of agents in the sim ---
    # --- Num occluders is set with the occ_per_agent param ---
    sim_sizes = {"sm": 100, "md": 1000, "lg": 10000, "xl": 100000}

    # --- Configure Writer kwargs ---
    writer_args: dict[str, Any] = {
        'random_seed': 42,

    # --- Parameterized Agent Data ---
        'targets_per_sensor': 5,
        'speed': 1,
        'fov': 60,
        'view_range': 10,

    # --- Parameterized Occluder Data ---
        'scale': 0.1,
        'shape': "cube",
        'occ_per_agent': 10,
    }

    job_list = BenchmarkSetup.generate_geometric_benchmark_jobs(sim_sizes, writer_args)
    return job_list


if __name__ == "__main__":
    process_args = main()
    num_jobs = len(process_args)

    processes = []
    for p_arg in process_args:
        p = Process(target=BenchmarkSetup.process_objects, kwargs=p_arg)
        processes.append(p)
        p.start()

    ui = SetupUI(num_jobs, processes)
    ui.poll()
    ui.finish()
