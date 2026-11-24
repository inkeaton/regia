# Regia

**A Domain-Specific Language for describing video game agents.**

The Regia compiler transpiles `.regia` source files into [AgentSpeak](https://en.wikipedia.org/wiki/AgentSpeak) programs that run on the [JaCaMo](https://jacamo-lang.github.io/) multi-agent platform, which in turn drives characters inside a Godot game via WebSockets.

## Repository Structure

```text
regia/
├── language/           Regia-to-AgentSpeak transpiler (Python), with the editor's API server
├── editor/             Visual AST editor (React + Vite + TypeScript)
├── science_game/
│   ├── game/           "Everything for Science" – Godot 4.7 demo game
│   └── minds/          JaCaMo agent system (Java + AgentSpeak)
└── qscores/            Questionnaire evaluation pipeline (Python)
```

Each component has its own README with install and run instructions:

| Component | Path | README |
|---|---|---|
| Transpiler | `language/` | [`language/README.md`](language/README.md) |
| Visual Editor | `editor/` | [`editor/README.md`](editor/README.md) |
| Benchmark Suite | `language/benchmarks/` | [`language/benchmarks/README.md`](language/benchmarks/README.md) |
| Science Game | `science_game/` | [`science_game/README.md`](science_game/README.md) |
| Questionnaire Scores | `qscores/` | [`qscores/README.md`](qscores/README.md) |

## Reproduce Everything

The root `Makefile` is the entry point (`make help` lists its targets):

```bash
make check-env   # check the required tools
make all         # set up, transpile the game, test, build the minds, run the benchmarks, recompute the scores, draw the figures
```

## Quick Start

### 1. Python Environment (shared by `language/` and `qscores/`)

Dependencies are declared in a [uv](https://docs.astral.sh/uv/) workspace (`pyproject.toml`, `uv.lock`, `.python-version`). From the repository root:

```bash
make setup   # creates .venv: Python 3.14, the transpiler with every extra, qscores' dependencies
source .venv/bin/activate
```

### 2. Compile a Regia File

```bash
regia compile language/manual_tests/example.regia -o out/
```

### 3. Launch the Visual Editor

```bash
# Terminal 1 – API server (http://127.0.0.1:8000)
make serve

# Terminal 2 – Frontend
cd editor && npm ci && npm run dev
```

Open http://localhost:5173 in your browser.
