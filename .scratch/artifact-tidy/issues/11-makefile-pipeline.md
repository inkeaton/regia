# Top-level Makefile for the whole pipeline

Type: task
Status: open
Assignee:
Blocked by: 05, 08, 09, 10

## Question

What single entry point takes a fresh clone through set up → test → rerun benchmarks → recompute qscores → rebuild figures?

Write a root `Makefile` with these targets:

- `check-env`: uv, Java via the wrapper's toolchain, Node matching `.nvmrc`, and Godot 4.7 as a warning only
- `setup`: `uv sync`
- `gen`, `test`, `minds` (build only)
- `bench` (compile benchmarks) and `bench-runtime` (opt-in)
- `qscores` (with the reference diff), `figures`
- `editor` (`npm ci && npm run build`) and `serve`
- `all` (the reviewer's pipeline, without Godot or the runtime benchmarks)
- `clean`

Add `.nvmrc` and `engines` to the editor. `make help` lists the targets. Each component README points to its target instead of repeating commands.
