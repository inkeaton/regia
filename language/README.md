# Regia Transpiler

The Regia transpiler compiles `.regia` source files into [AgentSpeak](https://en.wikipedia.org/wiki/AgentSpeak) (`.asl`) programs.
It implements the full pipeline: preprocessing, parsing (via a Lark grammar), AST construction, semantic validation, and code emission.

## Prerequisites

- **[uv](https://docs.astral.sh/uv/)** (it installs the pinned Python itself; the package supports Python ≥ 3.11)

## Installation

The transpiler is a member of the uv workspace at the repository root. From the repository root:

```bash
uv sync --package regia                  # the regia CLI and its core dependencies (click, lark)
uv sync --all-packages --all-extras      # everything, including the extras below
source .venv/bin/activate
```

### Optional Dependencies

| Extra | Packages | Needed for |
|---|---|---|
| `server` | fastapi, pydantic, uvicorn | the editor's API server (`server.py`) |
| `benchmarks` | pandas, numpy, scipy, matplotlib, psutil | the benchmark suite and its plots |
| `dev` | pytest, syrupy | the test suite |

Install a single extra with `uv sync --package regia --extra <name>`. Versions are locked in `uv.lock`.

## CLI Usage

After installation, the `regia` command is available globally in your virtual environment.

### Compile

Transpile a Regia source file into AgentSpeak:

```bash
regia compile <file.regia> [-o <output_dir>] [--dry-run]
```

- `-o / --output-dir` — Directory to place the generated `.asl` files (defaults to the current directory).
- `--dry-run` — Run the full pipeline without writing any files.

### Check

Validate a source file without emitting code:

```bash
regia check <file.regia>
```

### Global Options

```bash
regia --version    # Show version
regia --quiet      # Suppress warnings, print errors only
```

## Running Tests

```bash
cd language
pytest
```

The test suite covers the grammar, AST builder, validator, emitter, and CLI. Snapshot tests use [syrupy](https://github.com/syrupy-project/syrupy).

## Project Structure

```text
language/
├── pyproject.toml             Package configuration and dependencies
├── src/regia/
│   ├── grammars/              Lark grammar files (.lark)
│   ├── preprocessor.py        Stage 0 – import resolution and preprocessing
│   ├── parser.py              Stage 1 – Lark parser wrapper
│   ├── ast_builder.py         Stage 2 – Concrete Syntax Tree → AST
│   ├── ast_nodes.py           AST node dataclass definitions
│   ├── validator.py           Stage 3 – semantic validation
│   ├── emitter.py             Stage 4 – AgentSpeak code generation
│   ├── compiler.py            Pipeline orchestration
│   ├── cli.py                 Click CLI interface
│   ├── errors.py              Diagnostic message types
│   └── syntax_errors.py       Human-readable syntax error formatting
├── automated_tests/           pytest test suite
├── manual_tests/              Example .regia files for manual testing
├── benchmarks/                Scalability benchmark suite (see its own README)
├── results/                   Benchmark output (CSV + generated sources)
└── vscode-extension/          VS Code syntax highlighting (.vsix)
```

## VS Code Extension

A basic syntax-highlighting extension for `.regia` files is available at `vscode-extension/regia-language.vsix`. Install it with:

```bash
code --install-extension language/vscode-extension/regia-language.vsix
```
