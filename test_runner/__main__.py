import subprocess
import time
import os

from test_runner.ui import TestRunnerUI
from test_runner.benchmark_result import BenchmarkResult
from typing import Any
import yaml

def gen_benchmarks_from_config() -> list[dict[str, Any]]:
    yaml_dict = yaml.safe_load(open("config.yaml"))
    benchmark_args = []
    for config_name, config_params in yaml_dict.items():
        if config_name == "defaults": continue
        for distribution in config_params["distributions"]:
            directory = os.path.join(os.getcwd(), "benchmarks", "geometry", f"{distribution}_{config_name}")
            for size, num_updates in config_params["sizes"].items():
                clargs = dict()
                file_name = f"{distribution}_{config_name}_{size}.json"
                file_path = os.path.join(directory, file_name)
                clargs["executable"] = config_params["executable"]
                clargs["-scenarioPath"] = file_path
                clargs["-scenarioName"] = file_name
                clargs["-numUpdates"] = str(num_updates)
                clargs = clargs | config_params["clargs"]
                benchmark_args.append(clargs)
    return benchmark_args



def run_benchmark(benchmark_results: dict[str, BenchmarkResult], clargs : dict) -> None:

    scenario_name = clargs["-scenarioName"]
    clargs_list = list()
    clargs_list.append(clargs["executable"])
    for specifier, arg in clargs.items():
        if specifier in "executable":
            continue
        clargs_list.append(specifier)
        if arg:
            clargs_list.append(arg)

    process = subprocess.Popen(clargs_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
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

def main():
    write_log_heading("logs.txt")
    benchmark_args = gen_benchmarks_from_config()
    benchmark_results = dict()
    for arg in benchmark_args:
        benchmark_results[arg["-scenarioName"]] = BenchmarkResult(result=-1, start_time=-1, time_elapsed=-1, status="Not Started", num_iterations=int(arg["-numUpdates"]), correct="N/A")

    with TestRunnerUI(benchmark_results) as ui:
        for benchmark_arg in benchmark_args:
            scenario_name = benchmark_arg["-scenarioName"]
            ui.execute_benchmark(scenario_name)
            write_benchmark_heading("logs.txt", scenario_name)
            run_benchmark(benchmark_results, benchmark_arg)
            ui.complete_benchmark(scenario_name)
        ui.finish()
        time.sleep(1)

# def main():
#     gen_benchmarks_from_config()

if __name__ == "__main__":
    main()