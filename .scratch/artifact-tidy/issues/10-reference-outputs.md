# Reference outputs vs regenerated outputs

Type: task
Status: closed
Assignee: claude (session 2026-11-24)
Blocked by: 04

## Question

Where do the paper's committed results live, where do reruns write, and how are the two compared?

**qscores.** Move the committed `out/` and `fig/` to `qscores/reference/{results,figures}`. Leave the code's defaults `results/` and `figures/` as they are, and gitignore them. Make the defaults resolve relative to the script rather than the cwd, with the data dir defaulting to `qscores/data`. Fix the README (it says `fig/`, while the code says `figures/`) and the `compute_metrics.py` docstring (N = 21; the real N is 32). Add a compare script that diffs the regenerated CSVs against the reference and exits non-zero on any difference. The first thing to check is that today's code reproduces the reference CSVs exactly.

**Benchmarks.** Move `language/results/` (the paper's runs) to a reference location under `language/benchmarks/`, and point the default output somewhere gitignored. Then fix the benchmarks README to match.

## Resolution (2026-11-24)

Done. `1.0` is now at **`061e7ab` "Separate the paper's reference outputs from regenerated ones"** (anonymous, no trailer), on top of `b0bf219`. **Not pushed.**

- **qscores:** `out/` and `fig/` are now `qscores/reference/{results,figures}`. `results/` and `figures/` are gitignored. All three scripts resolve their defaults next to themselves, with `data/` as the data dir. README and docstring (N = 32) fixed.
- **Compare:** `qscores/compare_reference.py` requires the same set of CSVs with exactly the same text (only line endings may differ, so Windows works). It prints a diff and exits 1 on any difference, missing CSV or extra CSV. `summary.md` and figures are not compared.
- **Benchmarks:** `language/results/` is now `language/benchmarks/reference/`. The compile benchmarks default to `language/benchmarks/results/` (gitignored) and the runtime ones to `results/runtime/`, whatever the cwd. `--output` / `--out` still override. READMEs fixed, including the `bench_fits.py` path.

**Checks:**
- Before any change, the code with the locked deps reproduced every file in `out/` byte for byte. After it, all 11 CSVs match, run from `/`, and `summary.md` is identical too.
- Negatives: a changed digit, a missing CSV, an extra CSV and a missing results dir all exit 1.
- `bench_fits.py` on the reference runs reproduces `fits.csv`, `fits.md`, `per_kloc.csv` and `mix_comparison.csv` byte for byte.
- `run scale_roles --reps 1` regenerates sources identical to the reference's and `plot` works. The other suites were not rerun. Runtime: only `list` was run, so its new default path is untested end to end.
- 217 tests pass.

### Facts for later tickets

- **11:** the figures PNGs differ in bytes from the reference (first at byte 137), so don't diff them.
- **11:** `bench_fits.py` defaults to PDF and to `RESULTS_DIR/fits`: pass `--format png` to match the reference, and `--out` when reading `reference/`, or it overwrites the committed fits.
- **11:** `single_dimensions.py` reads a flat directory of `scale_*.csv`, not the suite layout, and writes to `./figures`. Left alone.
