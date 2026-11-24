# Reference outputs vs regenerated outputs

Type: task
Status: open
Assignee:
Blocked by: 04

## Question

Where do the paper's committed results live, where do reruns write, and how are the two compared?

**qscores.** Move the committed `out/` and `fig/` to `qscores/reference/{results,figures}`. Leave the code's defaults `results/` and `figures/` as they are, and gitignore them. Make the defaults resolve relative to the script rather than the cwd, with the data dir defaulting to `qscores/data`. Fix the README (it says `fig/`, while the code says `figures/`) and the `compute_metrics.py` docstring (N = 21; the real N is 32). Add a compare script that diffs the regenerated CSVs against the reference and exits non-zero on any difference. The first thing to check is that today's code reproduces the reference CSVs exactly.

**Benchmarks.** Move `language/results/` (the paper's runs) to a reference location under `language/benchmarks/`, and point the default output somewhere gitignored. Then fix the benchmarks README to match.
