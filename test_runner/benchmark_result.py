from dataclasses import dataclass

@dataclass
class BenchmarkResult:
    """ Simply defines a benchmark result object. """
    result: int
    num_iterations: int
    start_time: float
    time_elapsed: float
    status: str
    correct: str