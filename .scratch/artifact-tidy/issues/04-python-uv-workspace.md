# Python manifests and lockfile with a uv workspace

Type: task
Status: closed
Assignee: claude (session 2026-11-23)
Blocked by: 02

## Question

How does every Python dependency become declared, bounded and locked?

Steps:

1. Add a root `pyproject.toml` defining a uv workspace with members `language` and `qscores`, plus `.python-version` and `uv.lock`.
2. Give `qscores/` its own `pyproject.toml`, covering numpy, pandas, scipy, openpyxl, matplotlib and tabulate.
3. In `language/pyproject.toml`, keep the core as `click` and `lark` only. Add extras `server` (fastapi, uvicorn, pydantic), `benchmarks` (pandas, numpy, scipy, matplotlib, psutil) and `dev` (pytest, syrupy).
4. Give every dependency lower and upper bounds.

Grep every import to make sure nothing is missed. The answer records the Python version picked and why: the snapshot ran on CPython 3.14, and `requires-python` says ≥ 3.11. `uv sync --all-extras --all-packages` followed by `pytest` must pass.

## Resolution (2026-11-23)

Done. `1.0` is now at **`680d4f6` "Declare and lock Python dependencies in a uv workspace"** (anonymous, no trailer), on top of `3d0c3d1`. **Not pushed.** Committed in the `1.0/` worktree.

- **Root:** a virtual uv workspace (`pyproject.toml` with only `[tool.uv.workspace]`, members `language` and `qscores`), `uv.lock` (43 packages), `.python-version` = **3.14**.
- **`language/pyproject.toml`:** core is `click` and `lark`. Extras: `server` (fastapi, pydantic, uvicorn), `benchmarks` (matplotlib, numpy, pandas, psutil, scipy; numpy, scipy and psutil were imported but never declared), `dev` (pytest, syrupy). CRLF line endings kept.
- **`qscores/pyproject.toml`:** `regia-qscores`, `[tool.uv] package = false` (scripts, not a package). matplotlib, numpy, openpyxl, pandas, scipy, **tabulate** (not imported directly; pandas' `to_markdown` needs it for `summary.md`).
- **Bounds rule:** lower = the oldest minor in the lock (so Python 3.11 still resolves: numpy ≥ 2.4, scipy ≥ 1.17), upper = next major (`<1` for 0.x: fastapi, uvicorn, tabulate). Exception: qscores has **`pandas>=3.0,<3.1`** (see below).
- READMEs (root, `language/`, `language/benchmarks/`, `qscores/`) now say `uv sync …` + `source .venv/bin/activate` instead of `pip install`. `.venv/` is gitignored.

**Why Python 3.14:** the snapshot's `__pycache__` was CPython 3.14, so the paper's outputs were produced on it, and every dependency has 3.14 wheels. `requires-python` stays `>=3.11`; the lock resolves for 3.11 to 3.14+.

**Checks, on the final lock:** `uv lock --check` ok; `uv sync --all-packages --all-extras`; `cd language && pytest`: **217 passed**; `regia --help` and `python -m benchmarks list` run; every extra imports.

### Facts for later tickets

- **qscores reproduces exactly (10).** `python compute_metrics.py data <dir>` from `qscores/` gives files byte-identical to `qscores/out/` (all 12, `summary.md` included) with pandas 2.3.3 and 3.0.0 to 3.0.6, whatever the numpy (2.3–2.5). pandas **3.1.0/3.1.1 differ** in `respondents.csv` only, in the last digit of floats (e.g. `0.7053571428571428` → `…429`). Hence the `<3.1` pin. `make_figures.py` writes all 6 PNGs. Note `compute_metrics.py`'s data dir defaults to `.`, which ticket 10 changes.
- **uv isn't installed on the author's machine.** This session used a throwaway uv 0.13.9 in a scratch venv. Tickets 08, 11 and 13 need a real one (`uv` on the PATH for the Gradle Exec and Make).
- **`uv sync --package X` is exact:** it removes other members' packages from `.venv`. The Makefile's `setup` should use `--all-packages --all-extras`.
- **Server (05):** `server.py` now needs the `server` extra, and still imports `language.src.regia…`, so it only works from the repo root.
- **Benchmarks** run as `python -m benchmarks` from `language/`.
- **syrupy is declared but unused:** `test_compiler.py`'s snapshot tests are a TODO. Kept, as the ticket said.
- **Figure checking (fog):** matplotlib is now locked at 3.11.2.
