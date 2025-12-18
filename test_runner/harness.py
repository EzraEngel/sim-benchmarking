import subprocess
import time
import os
import yaml
from typing import Any
from test_runner.benchmark_result import BenchmarkResult

type BenchmarkArgs = dict[str, Any]
type ScenarioName = str

class BenchmarkHarness:
    """
    Orchestrates the execution of external benchmark processes.
    Manages configuration parsing, subprocess spawning, and log capturing.
    """
    config_path: str
    log_path: str
    benchmark_list: list[BenchmarkArgs]
    benchmark_results: dict[ScenarioName, BenchmarkResult]

    def __init__(self, config_path: str, log_path: str):
        self.config_path = config_path
        self.log_path = log_path
        self._initialize_benchmarks()
        self._initialize_benchmark_results()

    def _initialize_benchmarks(self) -> None:
        """ Parses the yaml config file and writes the benchmark jobs to a list. """
        yaml_dict = yaml.safe_load(open(self.config_path))
        benchmark_args = []
        for config_name, config_params in yaml_dict.items():
            if config_name == "defaults": continue
            if not config_params["run"]: continue
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
        self.benchmark_list = benchmark_args


    def _initialize_benchmark_results(self) -> None:
        """ Initialize the benchmark results dictionary with unexecuted benchmark jobs. """
        self.benchmark_results = dict()
        for benchmark in self.benchmark_list:
            self.benchmark_results[benchmark["-scenarioName"]] = (
                BenchmarkResult(result=-1,
                                start_time=-1,
                                time_elapsed=-1,
                                status="Not Started",
                                num_iterations=int(benchmark["-numUpdates"]),
                                correct="N/A"))


    def run_benchmark(self, clargs: BenchmarkArgs) -> None:
        """
        This method does a few things. Most importantly, it forks and executes the benchmark run with the provided BenchmarkArgs.
        When it forks the process with the subprocess module, it sets up a pipe to intercept standard output from the child process.
        It blocks on that pipe, and waits for appropriate flags in order to start and stop a timer, and parse the actual result.

        Finally, it takes the measured wall clock time and writes it (along with some other data) to the benchmark_results dictionary.
        This looks a bit indirect (why not just return a dictionary entry). But it ends up being much easier to modify the dictionary
        in place to support the visual feedback in the terminal UI by doing it this way.
        """
        scenario_name = clargs["-scenarioName"]
        clargs_list = list()
        clargs_list.append(clargs["executable"])
        for specifier, arg in clargs.items():
            if specifier in "executable":
                continue
            clargs_list.append(specifier)
            if arg:
                clargs_list.append(arg)

        process = subprocess.Popen(clargs_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                   encoding="utf-8")
        self.benchmark_results[scenario_name].start_time = time.perf_counter()

        start_time = 0.0
        end_time = 0.0
        result = None

        with open(self.log_path, "a") as log:
            for line in process.stdout:
                if "### START BENCHMARK ###" in line:
                    start_time = time.perf_counter()
                elif "### END BENCHMARK ###" in line:
                    end_time = time.perf_counter()
                elif "### QUERY RESULT" in line:
                    try:
                        result = int(line.split("|")[1])
                    except (IndexError, ValueError):
                        pass
                log.write(line)
                log.flush()

        stderr_output = process.stderr.read()
        if stderr_output:
            print("\n--- ERRORS ---")
            print(stderr_output)
            print("--------------")

        process.terminate()
        self.benchmark_results[scenario_name].time_elapsed = end_time - start_time
        self.benchmark_results[scenario_name].result = result
        self.benchmark_results[scenario_name].correct = "true"


    def write_log_heading(self) -> None:
        """ Writes a log heading. """
        with open(self.log_path, "w") as log:
            log.write("######################################################\n")
            log.write("################## BENCHMARK LOGS ####################\n")
            log.write("######################################################\n")
            log.write("------------------------------------------------------\n")


    def write_benchmark_heading(self, scenario_name: str) -> None:
        """ Writes an individual benchmark heading. """
        with open(self.log_path, "a") as log:
            log.write("######################################################\n")
            log.write(f"### BENCHMARK FOR: {scenario_name}\n")
            log.write("######################################################\n")
