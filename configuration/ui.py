from multiprocessing import Process
import time
from typing import Any
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.text import Text

class SetupUI:
    welcome_message = Text("Welcome to the ABM Simulation Benchmark Generator", justify="center", style="bold green")
    welcome_panel = Panel(welcome_message, title="[bold cyan]Setup[/bold cyan]", border_style="cyan")
    progress_columns = [
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("({task.completed} of {task.total})"),
        TimeRemainingColumn(),
    ]

    num_jobs: int
    processes: list[Process]
    console: Console
    start_time: Any
    end_time: Any

    def __init__(self, num_jobs: int, processes: list[Process]) -> None:
        self.num_jobs = num_jobs
        self.processes = processes
        self.console = Console()
        self.welcome()

    def welcome(self) -> None:
        self.console.print(self.welcome_panel)
        self.console.print(f"Found [bold yellow]{self.num_jobs}[/bold yellow] benchmark scenarios to generate.")

    def poll(self) -> None:
        self.start_time = time.time()
        with Progress(*self.progress_columns, console=self.console) as progress:
            task = progress.add_task("[green]Generating scenarios...", total=self.num_jobs)
            completed_processes = 0
            while completed_processes < self.num_jobs:
                for p in self.processes:
                    if not p.is_alive():
                        p.join()
                        self.processes.remove(p)
                        completed_processes += 1
                        progress.update(task, advance=1)
                time.sleep(0.1)
        self.end_time = time.time()

    def finish(self) -> None:
        self.console.print(
            f"\n[bold green]✓ Successfully finished building {self.num_jobs} benchmarks in {self.end_time - self.start_time:.2f} seconds.[/bold green]")
