import time
from test_runner.ui import TestRunnerUI
from test_runner.harness import BenchmarkHarness

def main() -> None:
    """
    Generates the appropriate benchmarks by parsing the config.yaml and then runs them one by one. Provides visual feedback to
    user through the TestRunnerUI object.
    """
    harness = BenchmarkHarness("config.yaml", "logs.txt")
    harness.write_log_heading()

    with TestRunnerUI(harness.benchmark_results) as ui:
        for benchmark_arg in harness.benchmark_list:
            scenario_name = benchmark_arg["-scenarioName"]
            ui.execute_benchmark(scenario_name)
            harness.write_benchmark_heading(scenario_name)
            harness.run_benchmark(benchmark_arg)
            ui.complete_benchmark(scenario_name)
        ui.finish()
        time.sleep(1)

if __name__ == "__main__":
    main()