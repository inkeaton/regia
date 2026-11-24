# Regia

[![CI](../../actions/workflows/ci.yml/badge.svg?branch=1.0)](../../actions/workflows/ci.yml?query=branch%3A1.0)

**A Domain-Specific Language for describing video game agents.**

The Regia compiler transpiles `.regia` source files into [AgentSpeak](https://en.wikipedia.org/wiki/AgentSpeak) programs that run on the [JaCaMo](https://jacamo-lang.github.io/) multi-agent platform, which in turn drives characters inside a Godot game via WebSockets.

## Repository Structure

```text
regia/
├── language/           Regia-to-AgentSpeak transpiler (Python), with the editor's API server
├── editor/             Visual AST editor (React + Vite + TypeScript)
├── science_game/
│   ├── game/           "Everything for Science" – Godot 4.7 demo game
│   ├── minds/          JaCaMo agent system (Java + AgentSpeak)
│   └── demo_video/     Recordings of the demo game
├── qscores/            Questionnaire evaluation pipeline (Python)
├── docs/               Game design diagrams (see NOTICE)
└── Makefile            Entry point for the whole pipeline
```

Each component has its own README with install and run instructions:

| Component | Path | README |
|---|---|---|
| Transpiler | `language/` | [`language/README.md`](language/README.md) |
| Visual Editor | `editor/` | [`editor/README.md`](editor/README.md) |
| Benchmark Suite | `language/benchmarks/` | [`language/benchmarks/README.md`](language/benchmarks/README.md) |
| Science Game | `science_game/` | [`science_game/README.md`](science_game/README.md) |
| Questionnaire Scores | `qscores/` | [`qscores/README.md`](qscores/README.md) |

## Requirements

| Tool | Version | Needed for | How to get it |
|---|---|---|---|
| make and a POSIX shell | any | the root `Makefile` | your system's packages |
| [uv](https://docs.astral.sh/uv/) | recent | everything in Python, and transpiling the game | install it yourself; it downloads Python 3.14 (`.python-version`) and the packages locked in `uv.lock` |
| A JDK | ≥ 17 | running Gradle | install it yourself |
| JDK | 21 | compiling and running the game's agents | nothing to do: Gradle uses an installed JDK 21 or downloads one |
| Gradle | 9.9.2 | building the game's agents | nothing to do: the wrapper (`science_game/minds/gradlew`) downloads it |
| [Node.js](https://nodejs.org/) with npm | 24 (`editor/.nvmrc`) | the visual editor only | install it yourself, for example with `nvm install` in `editor/` |
| [Godot](https://godotengine.org/download) | 4.7 | playing the demo game only | install it yourself |

`make all` needs only make, uv and a JDK, plus a network connection for the first run's downloads. `make check-env` checks the tools, including Node (required) and Godot (a warning).

## Reproduce the Paper

From the repository root:

```bash
make all
```

It took under 3 minutes on our machine, with the downloads already cached. It runs these targets, which also work one by one (`make help` lists them all):

| Target | What it does | Output | The paper's version |
|---|---|---|---|
| `setup` | creates `.venv` from the lockfile | `.venv/` | |
| `gen` | transpiles the game's Regia sources | `science_game/minds/src/agt/gen/` | |
| `test` | runs the transpiler's tests | | |
| `minds` | builds the game's agents | `science_game/minds/build/` | |
| `bench` | reruns the compile benchmarks | `language/benchmarks/results/` | `language/benchmarks/reference/` |
| `qscores` | recomputes the questionnaire scores (N = 32) and **fails unless every CSV matches the paper's** | `qscores/results/` | `qscores/reference/results/` |
| `figures` | redraws the questionnaire figures, the paper's benchmark fits from its own runs, and the plots and fits of the rerun | `qscores/figures/`, `language/benchmarks/results/` | `qscores/reference/figures/`, `language/benchmarks/reference/fits/` |

The outputs are not tracked; the reference directories hold the paper's data and figures. Benchmark timings depend on the machine, so a rerun reproduces the trends, not the numbers. `make all` doesn't compare the figures, since another CPU or operating system may draw a pixel differently: `make compare-figures` does, and so does CI.

Not part of `make all`:

- `make bench-runtime` runs the runtime benchmarks. **It kills other running Gradle and JaCaMo processes.**
- `make compare-figures` redraws the figures and fails unless those drawn from the paper's data match the paper's pixel by pixel.
- `make editor` builds the visual editor.
- The demo game is played by hand: see [`science_game/README.md`](science_game/README.md).

[CI](.github/workflows/ci.yml) runs the setup, the tests, the minds build, the scores comparison, a quick benchmark pass and the editor build on Ubuntu.

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

## License

The code is under the Apache License 2.0 ([`LICENSE`](LICENSE)). The questionnaire data and the results derived from it are under CC-BY-4.0 ([`LICENSE-data`](LICENSE-data)). [`NOTICE`](NOTICE) lists the parts with other terms: the VEsNA files, the game design diagrams and the game art.
