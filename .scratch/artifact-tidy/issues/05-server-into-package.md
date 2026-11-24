# Move server.py into the package as regia serve

Type: task
Status: closed
Assignee: claude (session 2026-11-24)
Blocked by: 04

## Question

How does the editor's API server run from anywhere, against the installed `regia` package only?

Move `server.py` to `language/src/regia/server.py`, import from `regia.…`, and add `regia serve [--host --port]` to the CLI. If the `server` extra is missing, it should fail with a clear message. Then update the editor's README and the top-level README. Check that the editor still talks to the server on the port it expects.

## Resolution (2026-11-24)

Done. `1.0` is now at **`5a81bca` "Move the editor's API server into the package as `regia serve`"** (anonymous, no trailer), on top of `680d4f6`. **Not pushed.** Committed in the `1.0/` worktree.

- **`server.py` → `language/src/regia/server.py`** (a `git mv`, CRLF kept). It imports `regia.compiler`. The unused `Program` import is dropped, and a module docstring is added. The endpoint and the JSON encoder are unchanged. The `__main__` block becomes `run(host, port)` with `DEFAULT_HOST`/`DEFAULT_PORT` = `127.0.0.1:8000`, so `python -m regia.server` works too.
- **`regia serve [--host] [--port]`** in `cli.py` (defaults 127.0.0.1 and 8000). It imports `regia.server` lazily, so the core CLI never needs fastapi. If the import fails on fastapi, pydantic, starlette or uvicorn, it raises a `ClickException` (exit 1) that names the missing module and gives both install commands (`uv sync --all-packages --all-extras`, `pip install 'regia[server]'`). Any other ImportError is re-raised.
- **READMEs:** the root README's tree no longer lists `server.py`, and its Quick Start uses `regia serve`. `editor/README.md` covers prerequisites, "Start the API Server" (any working directory) and the port table (`regia serve --port`). `language/README.md` gets a new *Serve* section, the `server` extra row, and `server.py` in the tree.

**Checks.** `regia serve` started from a scratch dir outside the repo, using the workspace venv: `POST /parse` with `manual_tests/example.regia` returns 200 and a `Program` AST. Bad source returns 400 with the error list, and `access-control-allow-origin: *` is present. The editor's `HTTP_API_BASE_URL` (`editor/src/services/transport.ts`) is still `http://127.0.0.1:8000`, which matches the default, so it needed no change. A core-only venv (`pip install language/`, not editable) lists `serve` in `regia --help`, and `regia serve` prints the extra message with exit 1. `pytest` gives 217 passed. No `server.py` or `language.src` references remain outside the package.

### Facts for later tickets

- **Makefile (11):** the `serve` target is just `uv run regia serve` (needs the `server` extra, which `setup`'s `--all-packages --all-extras` installs).
- **README pass (12):** `python server.py` is already gone from all READMEs.
- A non-editable `pip install language/` writes `language/build/`, which isn't gitignored. Nothing in the pipeline does that (uv installs editable), so it was left alone.
