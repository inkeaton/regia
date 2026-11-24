# Changes since the submitted artifact

The tag `artifact-submitted` is the artifact as it was submitted with the paper, except for the paper's supplementary PDF. This file lists what has changed on branch `1.0` since then. No number in the paper changes: CI recomputes the questionnaire scores and redraws the questionnaire figures and the benchmark fits, and compares them with the paper's.

## Build problems and their fixes

| Problem in the submitted artifact | Fix | Commit |
|---|---|---|
| The generated agents (`minds/src/agt/gen/`) were tracked, and nothing regenerated them from the `.regia` files | The Gradle task `compileRegia` generates them before compiling, and again when a `.regia` file or the transpiler changes. They are no longer tracked, and none is copied by hand | [`e7ddab3`](../../commit/e7ddab3), [`1990cb2`](../../commit/1990cb2) |
| The Gradle wrapper was missing, so the Gradle version was unpinned, and `./gradlew` in the README didn't exist | Gradle 9.9.2 wrapper with a pinned checksum, also used by the runtime benchmarks | [`a68d387`](../../commit/a68d387), [`b0bf219`](../../commit/b0bf219) |
| The build was written in Groovy | Kotlin DSL, including the project the runtime benchmarks generate | [`a68d387`](../../commit/a68d387), [`b0bf219`](../../commit/b0bf219) |
| Nothing enforced the JDK version | Gradle toolchain for JDK 21, downloaded if it is missing | [`a68d387`](../../commit/a68d387) |
| scipy, psutil, tabulate and numpy were not declared | Declared by the component that uses them | [`680d4f6`](../../commit/680d4f6) |
| `qscores` had no manifest, and its `pip install` line was incomplete | `qscores/pyproject.toml` | [`680d4f6`](../../commit/680d4f6) |
| No Python lockfile, and no version bounds on core packages | A uv workspace with one `uv.lock` and `.python-version`. Every direct dependency is bounded | [`680d4f6`](../../commit/680d4f6) |
| fastapi, uvicorn and pydantic were core dependencies of the transpiler | Moved to the `server` extra. The core needs only click and lark | [`680d4f6`](../../commit/680d4f6) |
| `server.py` imported `language.src.regia`, so it ran only from the repository root and loaded a second copy of the package | Now `regia.server`, started from anywhere with `regia serve` | [`5a81bca`](../../commit/5a81bca) |
| External requirements were spread over several READMEs | One [Requirements](README.md#requirements) table. `make check-env` checks the tools, and Node is pinned | [`e2fefb7`](../../commit/e2fefb7), [`a02ff34`](../../commit/a02ff34) |
| No single entry point for the pipeline | A root `Makefile`: `make all` sets up, transpiles, tests, builds the agents, reruns the benchmarks, recomputes the scores and redraws the figures | [`e2fefb7`](../../commit/e2fefb7) |
| No CI | GitHub Actions on Ubuntu | [`a34eb13`](../../commit/a34eb13), [`627710a`](../../commit/627710a) |
| Build output, IDE files, caches and backups were packaged | Removed and gitignored | [`3d0c3d1`](../../commit/3d0c3d1), [`e02958e`](../../commit/e02958e) |
| No license | Apache-2.0 for the code, CC-BY-4.0 for the questionnaire data, and the exceptions in [`NOTICE`](NOTICE) | [`853d137`](../../commit/853d137) |
| The `qscores` README named `fig/` where the code writes `figures/` | The README now matches. Reruns write to `results/` and `figures/`, and the paper's outputs are in `reference/` | [`061e7ab`](../../commit/061e7ab) |

## Other changes

- The demo videos and the snippet images in `docs/`, left out of the submitted archive for its size limit, are back ([`91aeabe`](../../commit/91aeabe)).
- Two downloaded paper textures in the game are replaced by generated ones ([`09da043`](../../commit/09da043)).
- The demo instructions start the game before the agents ([`a02ff34`](../../commit/a02ff34)), and the game's main scene is the demo instead of an empty scene ([`c67dd6e`](../../commit/c67dd6e)).
- READMEs and comments cite the sections of the paper and its supplementary material ([`c67dd6e`](../../commit/c67dd6e)).

## Known limits

- The game is played by hand, and needs Godot 4.7. The full compile benchmarks and the runtime benchmarks don't run in CI.
- Benchmark timings depend on the machine: a rerun reproduces the trends, not the numbers.
- The figures are known to match pixel by pixel only on Linux x86_64.
