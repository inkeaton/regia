# Regia Benchmark Suite

The Regia benchmark suite is a parametric code generation and performance measurement framework designed to evaluate the scalability of the Regia transpiler. 

It systematically varies structural parameters of the Regia language (roles, phases, playbooks, subplots, vocabulary) to produce valid source code, compiles it in-memory, and measures:
- **Compilation Wall-clock Time** (in seconds)
- **Peak RAM Usage** (in MB, isolated via `tracemalloc`)
- **Code Expansion Ratio** (LoC of output AgentSpeak / LoC of input Regia)

## Prerequisites

Ensure you are using the virtual environment for the `language` package.

```bash
cd language
source ../.venv/bin/activate
```

## CLI Usage

The suite is operated via a standard command-line interface.

### Dependencies

To use the visualization tools (`plot` command), you need to install the optional dependencies:

```bash
pip install -e .[benchmarks]
```

### List Experiments

To see all available experiment suites and the parameters they vary:

```bash
python -m benchmarks list
```

### Validate Generation

Before running a full benchmark (which executes multiple repetitions per configuration), you can dry-run the generators to verify that all produced Regia code is syntactically and semantically valid according to the transpiler. This step runs the compiler but bypasses the timing and CSV output stages.

```bash
# Validate a specific suite
python -m benchmarks validate scale_roles

# Validate all suites
python -m benchmarks validate --all
```

### Run Benchmarks

To execute an experiment and collect metrics:

```bash
# Run a specific suite
python -m benchmarks run scale_roles

# Run all suites sequentially (takes ~5 minutes)
python -m benchmarks run --all
```

**Options:**
- `--output / -o <dir>`: Change the output directory (default: `results`).
- `--reps / -r <int>`: Override the number of timed repetitions per configuration (useful for quick smoke tests).

### Plot Results

Once you have generated CSV results, you can visualize them as PNG plots (requires `pandas` and `matplotlib`):

```bash
# Plot a specific suite
python -m benchmarks plot scale_roles

# Plot all suites in the results directory
python -m benchmarks plot --all
```

**Options:**
- `--output / -o <dir>`: Read from a different results directory (default: `results`).

## Output Layout

For each executed experiment suite, the runner produces a CSV containing performance metrics and the exact Regia source files that were generated. This ensures every benchmark run is completely reproducible.

```text
results/
└── scale_roles/
    ├── scale_roles.csv           # Performance data (one row per rep)
    └── sources/
        ├── scale_roles_1c5b....regia
        └── scale_roles_a3f4....regia
```

## CSV Schema

The output CSV contains the following columns for each run:

### Experiment Metadata
- `experiment`: Name of the suite (e.g., `scale_roles`).
- `run_id`: Monotonically increasing identifier for the run.

### System Information
- `sys_os`: Operating System (e.g., `Linux 7.1.8-arch1-3`).
- `sys_cpu`: Architecture (e.g., `x86_64`).
- `sys_cores`: Number of logical CPU cores.
- `sys_ram_gb`: Total system RAM in GB.
- `sys_python`: Python interpreter version used.

### Generator Config (Reproducibility)
- `n_actions`, `n_events`, `n_facts`: Vocabulary size.
- `n_playbooks`, `n_plans_per_playbook`, `n_branches_per_plan`, `n_stmts_per_branch`: Playbook structure.
- `n_roles`, `n_phases`: Main plot structure.
- `n_subplot_breadth`, `n_subplot_depth`: Subplot hierarchy structure.
- `seed`: Random seed (reserved for future stochastic generation).

### Metrics
- `input_loc`, `input_bytes`: Size of the generated Regia source.
- `output_files`, `output_loc_total`: Size of the emitted AgentSpeak files.
- `output_loc_per_file`: JSON dictionary detailing LoC per generated file.
- `loc_ratio`: `output_loc_total / input_loc` (measures code expansion).
- `compile_time_s`: Wall-clock compile time in seconds.
- `peak_ram_mb`: Peak heap allocation during compilation in MB.
- `success`, `warning_count`, `error_count`: Compilation status.

## Adding New Experiments

Experiments are defined in [`experiments.py`](./experiments.py). To add a new experiment, define a new parameter sweep by varying one field of the `GeneratorConfig` against the `BASELINE`.

Example:
```python
"scale_facts_extreme": _sweep(
    "n_facts", [500, 1000, 2000, 5000]
),
```
