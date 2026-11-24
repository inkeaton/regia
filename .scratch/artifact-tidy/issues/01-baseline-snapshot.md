# Commit the submitted snapshot as the 1.0 baseline

Type: task
Status: closed
Assignee: claude (session 2026-11-23)
Blocked by:

## Question

How do we make branch `1.0` hold exactly what the reviewers saw, so every later fix is a diff against it?

Commit the snapshot at `~/Scaricati/855_Regia_a_Narrative_Oriented_Supplementary Material/regia_paper/` onto `1.0` as one commit, then tag it `artifact-submitted`. `additional_material.pdf` stays out, because it belongs to the paper submission. Commit the snapshot *as is*, junk included, because cleaning it is the next ticket's job. Record which paths differ from the old `origin/1.0` (grammar, editor, qscores data and outputs, manual tests, `_old/` and `docs/` absent from the snapshot), so the answer notes what the commit overwrote. Do not push.

## Resolution (2026-11-23)

Done. Local branch `1.0` is now at **`d1a3fc1` "Replace 1.0 with the artifact as submitted for review"**, tracking `origin/1.0`. **Updated the same day:** the user requires anonymity (double-blind), so the commit was rebuilt as a parentless root commit by `Anonymous <anonymous@anonymous.invalid>` with no attribution trailer. Same tree as before (`7e46210`). The old history (`442b924` and earlier, with the user's name) is no longer reachable from `1.0`. Annotated tag **`artifact-submitted`** points at it. **Pushed** on 2026-11-23 (`--force-with-lease` over `442b924`), tag included.

How: the commit was built with a temporary index whose work tree was the snapshot (`git add -A -f`, so nested ignores like `editor/.gitignore` didn't filter anything). Main's working tree wasn't touched. `git archive 1.0` was diffed against the snapshot: the only differences are `additional_material.pdf` (left out on purpose) and ten empty directories, which git can't track.

### What the commit overwrote (old `origin/1.0` → snapshot)

720 paths changed: 119 added, 531 deleted, 70 modified.

- **Removed, junk:** `science_game/game/.godot/` (184 files), `_old/` (whole tree), `science_game/{game,minds}/logs/*`, `py3.12` `__pycache__` files, root `.gitignore` (the snapshot had none).
- **Removed, content** (the user confirmed these were cut to keep the submitted archive under 25 MB, not because they were obsolete; the videos and snippet references are restored by *Restore the demo videos and snippet references cut for size*): `docs/snippets references/` (6 PNGs), `science_game/demo_video/route_{1..4}.mkv`, `qscores/data_21/` (the older 21-respondent data), the Godot addon `IgnoreFolders`, the unused assets `ball`/`bone` (scenes and PNGs) and `player*.png`/`spritesheet.png` under `bodies/player/res/`, `minds/bin/main/regia/test_features.regia`.
- **Moved:** `language/benchmarks/results/` (100 files) → `language/results/` (about 100 files).
- **Modified:** `language/src/regia/grammars/regia.lark` (the newer grammar), `editor/src/{services,layout,index.css}`, all of `qscores/data/*` and `qscores/out/*` and `qscores/fig/*` (now 32 respondents), `qscores/compute_metrics.py`, 4 `language/manual_tests/*.regia`, `automated_tests/test_new_features.py`, both READMEs, `science_game/README.md`, `game/test_scene.tscn`, 2 files under `minds/src`, and `.gradle`/`__pycache__` churn.
- **Added:** `language/manual_tests/harbour.regia`, `qscores/questionnaire_print.pdf`, `qscores/data/{gen_behaviour,gen_syntax}.csv.bak`, `game/resources/images/backdrop.png`, `editor/dist/*`, py3.14 `__pycache__`.

### Facts for later tickets

- **Remove build output (02):** `_old/` and `docs/snippets references/` are already gone, so those two conditional items are moot. Junk still tracked on `1.0`: `science_game/minds/{.gradle,build,bin}` (32 + 33 + 36 files), `editor/dist` (5), `language/src/regia.egg-info` (6), `__pycache__` under `language/{src/regia,automated_tests,benchmarks,benchmarks/runtime}` (37), and four `qscores/data/*.bak`. No `.idea/` or `.vscode/` is tracked. `logs/` dirs are empty, so they aren't tracked.
- **Replace main's copy (03):** on `main`, `git log 1.0` is ambiguous because `1.0/` is both a branch and a path. Use `refs/heads/1.0` or `--` until ticket 03 removes the directory.
- **Finding, not fixed:** `science_game/game/bodies/items/pickup_item.tscn` references `res://resources/images/test1.jpg`, which isn't in the snapshot (it was in old `origin/1.0`). `flower.tscn` inherits from `pickup_item`, and `GameManager.gd` uses it. Whether the game shows a missing-texture warning or breaks needs a Godot run. It's a defect in the submitted artifact, but the review doesn't name it.
