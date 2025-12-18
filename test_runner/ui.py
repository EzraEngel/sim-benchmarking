from test_runner.benchmark_result import BenchmarkResult
from rich.console import Console, Group
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, MofNCompleteColumn, TaskID
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

class TestRunnerUI:
    """
    Represents the UI for the rest runner module. Provides rich visual feedback to the user about benchmarking
    progress and results process.
    """
    welcome_message = Text("Welcome to the ABM Simulation Benchmark Runner", justify="center", style="bold green")
    welcome_panel = Panel(welcome_message, title="[bold cyan]Benchmark Runner[/bold cyan]", border_style="cyan")
    progress_cols = [
        TextColumn("[bold blue]Overall Progress"),
        BarColumn(bar_width=80),
        MofNCompleteColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        "•",
        TimeElapsedColumn(),
    ]

    num_tests: int
    benchmark_results: dict[str, BenchmarkResult]
    console: Console
    progress: Progress
    task_id: TaskID

    def __init__(self, benchmark_results: dict[str, BenchmarkResult]) -> None:
        self.num_tests = len(benchmark_results)
        self.benchmark_results = benchmark_results
        self.console = Console()
        self.progress = Progress(*self.progress_cols, console=self.console)
        self.task_id = self.progress.add_task("Running benchmarks...", total=self.num_tests)
        self.table = self._generate_results_table()
        self.display_group = Group(self.progress, self.table)
        self.live = Live(self.display_group, console=self.console, screen=False, redirect_stderr=False, vertical_overflow="visible")

    def __enter__(self) -> 'TestRunnerUI':
        """ Enters the context manager. """
        self.welcome()
        self.live.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """ Exits the context manager. """
        self.live.stop()

    def welcome(self) -> None:
        """ Prints the welcome message. """
        self.console.print(self.welcome_panel)
        self.console.print(f"Found [bold yellow]{self.num_tests}[/bold yellow] benchmark scenarios to run.")

    def execute_benchmark(self, scenario_name: str) -> None:
        """ Updates UI to show the benchmark is executing. """
        self.benchmark_results[scenario_name].status = "Executing"
        self.table = self._generate_results_table()
        self.live.update(Group(self.progress, self.table))

    def complete_benchmark(self, scenario_name: str) -> None:
        """ Updates UI to show the benchmark is complete. """
        self.benchmark_results[scenario_name].status = "Finished"
        self.progress.update(self.task_id, advance=1)
        self.table = self._generate_results_table()
        self.live.update(Group(self.progress, self.table))

    def finish(self) -> None:
        """ Updates UI to show full test suite is complete. """
        self.progress.update(self.task_id, description="[bold green]All benchmarks complete!")

    @staticmethod
    def _get_status_style(status: str) -> str:
        """ Helper function to style status text. """
        if status == "Finished": return "bold green"
        if status == "Executing": return "bold yellow"
        return "dim"

    @staticmethod
    def _get_assert_text(correct: str) -> str:
        """ Helper function to style assertion text."""
        if correct=="true": return f"[bold green]TRUE[/]"
        elif correct=="false" : return f"[bold red]FALSE[/]"
        else: return f"[dim]N/A[/]"

    def _generate_results_table(self) -> Table:
        """ Helper function to generate a table with benchmark results. """
        table = Table(show_header=True, header_style="bold magenta", title="Benchmark Results")
        table.add_column("Scenario Name", style="dim", width=45)
        table.add_column("Status")
        table.add_column("Time (s)", justify="right")
        table.add_column("Updates", justify="right")
        table.add_column("FPS (Hz)", justify="right")
        table.add_column("Result", justify="right")
        table.add_column("Assert")

        for name, data in self.benchmark_results.items():
            time_str = f"{data.time_elapsed:.4f}" if data.time_elapsed >= 0 else "N/A"
            time_per_iter =f"{data.num_iterations/data.time_elapsed:.4f}" if data.time_elapsed >= 0 else "N/A"
            data_str = f"{data.result}" if data.result >= 0 else "N/A"
            status_style = self._get_status_style(data.status)
            table.add_row(
                name,
                f"[{status_style}]{data.status}[/]",
                time_str,
                str(data.num_iterations),
                time_per_iter,
                data_str,
                self._get_assert_text(data.correct))

        return table
