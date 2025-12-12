# Kernel-Based Simulation Benchmark Harness

This repository contains the reference test harness for the **"Beyond Entity Count"** benchmarking methodology presented at the SISO Simulation Innovation Workshop. It provides a standardized Python environment to configure scenarios, execute simulation binaries, and verify performance results against a reference implementation.

## Prerequisites

*   Python 3.8+
*   PyYAML (`pip install pyyaml`)

## Project Structure

*   `configuration/`: Python package for generating random scenario distributions. Contains `__main__.py` for module execution.
*   `test_runner.py`: The core harness logic that executes the simulation and verifies results.
*   `config.yaml`: User-defined settings for executable paths and arguments.

## Workflow

### 1. Generate Benchmark Scenarios
Navigate to the root of the repository and execute the configuration module. This generates the standardized JSON scenario files that your simulation engine must parse.

```bash
# Windows
py -m configuration
```
```bash
# Linux / macOS (or standard Python executable)
python -m configuration
```
*Note: The module iterates through a set of density and population hyperparameters to generate a suite of test files.*

### 2. Configure the Harness
Open `config.yaml` and modify the settings to point to your local simulation executable. You must also specify any command-line arguments your engine requires to run in headless mode.

**Example `config.yaml`:**
```yaml
executable_path: "C:/Path/To/Your/SimEngine.exe"
# Arguments passed to the executable. The harness appends the scenario path automatically.
default_args: ["--headless", "--console-logging"] 
```

### 3. Execute the Benchmark
Run the test runner to begin the benchmarking session.

```bash
# Windows
py -m test_runner
```
```bash
# Linux / macOS (or standard Python executable)
python -m test_runner
```


The harness will:
1.  Parse the `config.yaml`.
2.  Iterate through the generated scenario files.
3.  Launch your executable as a blocking subprocess for each scenario.
4.  Capture `stdout` to measure wall-clock time and verify the simulation result.

---

## Integration Specification

To be compatible with this harness, your simulation software must adhere to the following Input/Output protocol.

### Input
The simulation must accept a file path to a JSON configuration file via command line arguments.
*   *Optimization Note:* For high-entity-count scenarios, it is highly recommended to use a streaming JSON parser (e.g., `rapidjson` SAX parser) rather than a DOM parser to avoid memory allocation overheads.

### Output (Standard Out)
The harness monitors `stdout` via a pipe. Your application must print specific flags to control the timing and verification logic.

**1. Start Timer**
Print this flag immediately after the JSON parse is complete and the simulation is initialized. The harness begins the high-precision timer upon receiving this line.
```text
### START BENCHMARK ###
```

**2. End Timer**
Print this flag immediately after the compute kernel (e.g., sensing queries) is complete. The harness stops the timer upon receiving this line.
```text
### END BENCHMARK ###
```

**3. Report Result**
Print the calculation result (e.g., total detections) for verification. The value must be enclosed in pipes.
```text
### QUERY RESULT |<integer_value>| ###
```
*Example:* `### QUERY RESULT |923| ###`

**4. Termination**
The simulation must exit gracefully (return code 0) after printing the result. The harness waits for the process to terminate before starting the next scenario.

---

## Status
**Version: 0.1.0 (Pre-Alpha)**
This harness is currently under active development. Future updates will include expanded kernel support (Pathfinding, Networking) and improved scenario generation tools.