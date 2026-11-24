# Remove build output, IDE files and leftovers from 1.0

Type: task
Status: closed
Assignee: claude (session 2026-11-23)
Blocked by: 01

## Question

What on `1.0` is not source, and what `.gitignore` keeps it out for good?

Delete the following and add a root `.gitignore` covering all of them:

- `science_game/minds/{.gradle,build,bin,logs}`
- `editor/dist`
- `language/src/regia.egg-info`
- every `__pycache__`
- `.idea/` and `.vscode/`, where present
- `qscores/data/*.bak`
- `_old/`, if it survived ticket 01 (it didn't: already absent)

Keep `docs/snippets references/` and `science_game/demo_video/`. They were cut only for the archive size limit, and ticket *Restore the demo videos and snippet references cut for size* brings them back. Don't let the new `.gitignore` match them.

Check that the `.bak` files really are stale. Diff them against the live CSVs and note in the answer anything the live files don't contain. `src/agt/gen/` is handled separately, in ticket *Build generates gen/*. Leave it alone here.

## Resolution (2026-11-23)

Done. `1.0` is now at **`3d0c3d1` "Remove build output, caches and backups; add .gitignore"** (anonymous, no trailer), on top of `91aeabe`. **Not pushed.** It was made in a temporary worktree, so main's working tree wasn't touched.

It untracks 153 files: `science_game/minds/{.gradle,build,bin}` (101), `editor/dist` (5), `language/src/regia.egg-info` (6), every `__pycache__` (37), and `qscores/data/*.bak` (4). The new root `.gitignore` covers these, plus `/science_game/*/logs/`, `/science_game/game/.godot/`, `node_modules/`, `*.py[cod]`, `.pytest_cache/`, `.idea/`, `.vscode/` and `.DS_Store`. Checks: `git ls-files -ci --exclude-standard` is empty, the demo videos and snippet references are still tracked and not ignored, and `src/agt/gen/` isn't ignored (ticket 08 owns that).

### The `.bak` files were stale

They are backups written by `qscores/expand_data.py --write`, which appends blank rows for new respondents in `data.xlsx` and recomputes `answer_key.n_selected`. The live CSVs are a superset:

- `coding_sheet_A` adds 188 rows, `gen_behaviour` adds 15 (respondent 31), and `gen_syntax` adds 1 (respondent 31).
- In `answer_key`, the only difference is column `n_selected` on 10 options (C1_o1 22→27 … C3_o5 25→31).
- No row of any `.bak` is missing from the live file, apart from those `n_selected` values.

### Facts for later tickets

- **`bin/main` held only stale files:** `.asl` files from an older scenario (`director_investigation`, `environment`, `*_testfeatures*`, `*_investigation_*`). `science.jcm` doesn't use them, and they're still reachable in `main`'s history.
- **Gradle versions (06):** the removed `.gradle/` held caches from Gradle 8.9, 8.14.3, 9.2.0 and 9.2.1, so the build has been run on several versions with no pin.
- **uv (04):** `.venv/` isn't in the `.gitignore` yet. Add it when the workspace is created.
