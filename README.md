# Regia

**A Domain-Specific Language for describing video game agents.**

The Regia compiler transpiles `.regia` source files into [AgentSpeak](https://en.wikipedia.org/wiki/AgentSpeak) programs that run on the [JaCaMo](https://jacamo-lang.github.io/) multi-agent platform, which in turn drives characters inside a Godot game via WebSockets.

## Repository Structure

```text
regia/
├── language/           Regia-to-AgentSpeak transpiler (Python)
├── editor/             Visual AST editor (React + Vite + TypeScript)
├── server.py           FastAPI bridge between the editor and the transpiler
├── science_game/
│   ├── game/           "Everything for Science" – Godot 4.7 demo game
│   └── minds/          JaCaMo agent system (Java + AgentSpeak)
├── qscores/            Questionnaire evaluation pipeline (Python)
└── docs/               Additional documentation and snippet references
```

Each component has its own README with install and run instructions:

| Component | Path | README |
|---|---|---|
| Transpiler | `language/` | [`language/README.md`](language/README.md) |
| Visual Editor | `editor/` | [`editor/README.md`](editor/README.md) |
| Benchmark Suite | `language/benchmarks/` | [`language/benchmarks/README.md`](language/benchmarks/README.md) |
| Science Game | `science_game/` | [`science_game/README.md`](science_game/README.md) |
| Questionnaire Scores | `qscores/` | [`qscores/README.md`](qscores/README.md) |

## Quick Start

### 1. Python Environment (shared by `language/` and `qscores/`)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e language/              # transpiler core
pip install -e language/[dev]         # + test dependencies
pip install -e language/[benchmarks]  # + benchmark dependencies
```

### 2. Compile a Regia File

```bash
regia compile language/manual_tests/example.regia -o out/
```

### 3. Launch the Visual Editor

```bash
# Terminal 1 – API server
python server.py

# Terminal 2 – Frontend
cd editor && npm install && npm run dev
```

Open http://localhost:5173 in your browser.

## License

See the individual component directories for licensing information.
