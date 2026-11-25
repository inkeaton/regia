# Top-level Makefile for the whole pipeline

Type: task
Status: closed
Assignee: claude (session 2026-11-24, b)
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

## Resolution (2026-11-24)

Done. `1.0` is now at **`e2fefb7` "Add a Makefile for the whole pipeline and pin Node 24"** (anonymous, no trailer), on top of `061e7ab`. **Not pushed.**

- **Targets:** as listed above, with `help` as the default. `.NOTPARALLEL`, because parallel work would distort the benchmark timings. Python targets use `uv run --locked --all-packages --all-extras`, so each works alone in a fresh clone. Gradle always runs with `--no-daemon`. `make bench REPS=1` is a quick pass.
- **`all`** = setup, gen, test, minds, bench, qscores, figures. It doesn't include `check-env`, which fails without Node, because only the editor needs Node.
- **`figures`** depends on `qscores`, redraws the paper's fits from `benchmarks/reference/` into `results/reference_fits/`, and plots the rerun if there is one (otherwise it says to run `make bench`).
- **`clean`** keeps `.venv`, `node_modules` and `egg-info`.
- **Node 24:** `editor/.nvmrc` (`24`) and `engines` (`24.x`), in the lockfile too. It matches `@types/node`.
- **READMEs:** the component READMEs point to their targets. The root README has a short *Reproduce Everything* section.

**Checks:**
- `make -j8 all` in a clean export (the Makefile and Node pin, before the README edits; without the mp4s): exit 0 in 2:48, recipes one at a time, 217 tests pass, the qscores comparison passes, and the paper's `fits.csv`, `fits.md`, `per_kloc.csv` and `mix_comparison.csv` are byte-identical. The machine's Gradle and uv caches were warm, and the benchmarks ran while other checks did, so their timings mean nothing.
- `make clean` there leaves only the source files and `egg-info`, outside `.venv`.
- `make editor` and `make check-env` pass with a downloaded Node 24.22.3; npm leaves the lockfile unchanged. Without Node, `check-env` fails. `make serve` answers on port 8000.
- `bench-runtime`: only `make -n`. Not run, because it kills matching JVMs on the host. The wrong-Node and old-JDK paths of `check-env` were not exercised.

### Facts for later tickets

- **12:** requirements for `all` are make, a POSIX shell, uv and a JDK >= 17. Node 24 is for the editor only. The benchmarks README says "about 5 minutes", but the whole pipeline took under 3 here.
- **13:** CI can call the targets directly, with `REPS=1`. `check-env` needs Node.
- `npm ci` reports 6 vulnerabilities (1 low, 1 moderate, 4 high) in locked dependencies. Left alone (scope).
