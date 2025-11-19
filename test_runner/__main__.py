import subprocess
import time
import os
from test_runner.ui import TestRunnerUI
from test_runner.benchmark_result import BenchmarkResult
import random
import yaml

def gen_benchmark_args() -> list[tuple[str, str, str, str, int]]:
    size_to_num_updates = {
        "no_los_sm": 5000,
        "no_los_md": 500,
        "no_los_lg": 50,
        "no_los_xl": 5,
        "los_sm": 1000,
        "los_md": 100,
        "los_lg": 10,
        "los_xl": 2,
    }

    los_to_type = {
        "no_los": "GEO_NO_LOS",
        "los": "GEO_LOS"
    }

    sim_sizes = ["sm", "md", "lg", "xl"]
    distributions = ["uniform", "normal"]
    movements = ["static", "dynamic"]
    los_strs = ["los", "no_los"]

    executable: str = os.path.join("DOTSBuild", "Benchmarks.exe")
    benchmark_args = []
    for dist in distributions:
        for move in movements:
            for los in los_strs:
                for size in sim_sizes:
                    file_name = f"{dist}_{move}_{los}_{size}.json"
                    file_path = os.path.join(os.getcwd(), "benchmarks", "geometry", f"{dist}_{move}_{los}", file_name)
                    benchmark_args.append((executable, file_path, file_name, los_to_type[los], size_to_num_updates[f"{los}_{size}"]))

    return benchmark_args


def gen_benchmarks_from_config() -> None:
    yaml_dict = yaml.safe_load(open("../config.yaml"))
    print(yaml_dict)


def run_benchmark(benchmark_results: dict[str, BenchmarkResult],
                  executable: str,
                  scenario_path: str,
                  scenario_name: str,
                  scenario_type: str,
                  num_updates: int) -> None:

    command_args = [executable,
                    "-batchmode",
                    "-nographics",
                    "-logFile", "-",
                    "-numUpdates", str(num_updates),
                    f"-scenarioPath", scenario_path,
                    f"-scenarioName", scenario_name,
                    f"-scenarioType", scenario_type]

    process = subprocess.Popen(command_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    benchmark_results[scenario_name].start_time = time.perf_counter()

    start_time = 0.0
    end_time = 0.0
    result = None

    for line in process.stdout:
        if "### START BENCHMARK ###" in line:
            start_time = time.perf_counter()
        if "### END BENCHMARK ###" in line:
            end_time = time.perf_counter()
        if "### QUERY RESULT" in line:
            result = int(line.split("|")[1])

        with open("logs.txt", "a") as log:
            log.write(line)

    stderr_output = process.stderr.read()
    if stderr_output:
        print("\n--- ERRORS ---")
        print(stderr_output)
        print("--------------")


    process.terminate()
    benchmark_results[scenario_name].time_elapsed = end_time - start_time
    benchmark_results[scenario_name].result = result
    benchmark_results[scenario_name].correct = "true"


def write_log_heading(file_name: str) -> None:
    with open(file_name, "w") as log:
        log.write("######################################################\n")
        log.write("################## BENCHMARK LOGS ####################\n")
        log.write("######################################################\n")
        log.write("------------------------------------------------------\n")

def write_benchmark_heading(file_name: str, scenario_name: str) -> None:
    with open(file_name, "a") as log:
        log.write("######################################################\n")
        log.write(f"### BENCHMARK FOR: {scenario_name}\n")
        log.write("######################################################\n")

# def main():
#     write_log_heading("logs.txt")
#     benchmark_args = gen_benchmark_args()
#     benchmark_results = dict()
#     for arg in benchmark_args:
#         benchmark_results[arg[2]] = BenchmarkResult(result=-1, start_time=-1, time_elapsed=-1, status="Not Started", num_iterations=arg[4], correct="N/A")
#
#     with TestRunnerUI(benchmark_results) as ui:
#         for benchmark_arg in benchmark_args:
#             scenario_name = benchmark_arg[2]
#             ui.execute_benchmark(scenario_name)
#             write_benchmark_heading("logs.txt", scenario_name)
#             run_benchmark(benchmark_results, *benchmark_arg)
#             ui.complete_benchmark(scenario_name)
#         ui.finish()
#         time.sleep(1)

def main():
    gen_benchmarks_from_config()

if __name__ == "__main__":
    main()