# Map: Tidy the Regia 1.0 paper artifact

Label: wayfinder:map

## Destination

Branch `1.0` of `inkeaton/regia` is the paper's artifact, and it answers every point of the reviewer's build critique (paper 855, *Regia: a Narrative-Oriented …*). A fresh clone needs only the tools listed in one Requirements table. `make all` runs setup → transpile the game → tests → build minds → benchmarks → qscores → figures. Generated files are never tracked. CI on GitHub Actions shows that it builds. Regenerated qscores CSVs match the paper's (N = 32) exactly.

Charted with the user on 2026-11-23.

## Notes

- **Decide and do.** This map overrides wayfinder's "plan, don't do": a ticket closes when its decision is made *and* carried out as commits on branch `1.0`. Planning files stay here on `main`. Commit only on `1.0` (except ticket *Replace main's `1.0/` copy*), one or more commits per ticket. **Push only when the user says so.**
- **Anonymous.** The paper is under double-blind review. Every commit and tag on `1.0` uses `Anonymous <anonymous@anonymous.invalid>` as author, committer and tagger, with no `Co-Authored-By` or other attribution trailer, and no names in file contents. `1.0` is an orphan history: its root is the snapshot commit, and the old named commits stay only on `main`/`origin/1.0`. So the first push of `1.0` replaces `origin/1.0` and needs `--force-with-lease` (only when the user says so). Set the identity per command with the `GIT_AUTHOR_*` / `GIT_COMMITTER_*` env vars; don't change the repo's git config.
- **Where to commit on `1.0`:** branch `1.0` is checked out as a worktree at `~/Progetti/PhD/regia/1.0/` (gitignored on `main`). Commit there, not in a temporary worktree.
- **Scope is the review.** Fix exactly what the review names, plus whatever those fixes force. No refactoring, no new features, no Regia 1.5/2.0 work, no change to any number in the paper.
- **The baseline is the submitted snapshot**, at `~/Scaricati/855_Regia_a_Narrative_Oriented_Supplementary Material/regia_paper/`, not the old `origin/1.0`, which is behind it (26 respondents instead of 32, plus an older grammar and editor). It is tagged `artifact-submitted`, so every fix is a diff against what the reviewers saw.
- **The 25 MB limit.** The submitted archive had to stay under 25 MB, so some content was cut from the snapshot (demo videos, `docs/snippets references/`, `_old/`, `game/.godot/`). The GitHub branch has no such limit. Restoring a cut is a choice that needs the user's decision: see *Restore the demo videos and snippet references cut for size*.
- **Reference vs. regenerated.** The paper's outputs stay committed as *reference* data. The pipeline writes to separate, gitignored dirs and compares against the reference. qscores CSVs must match it exactly. Figures and benchmark timings are reproductions, not diffs.
- **Standing choices** (settled while charting):
  - Make is the task runner.
  - uv workspace with one `uv.lock` and `.python-version`. qscores gets its own `pyproject.toml`. The transpiler core is only `click` and `lark`, with extras `server`, `benchmarks` and `dev`, all bounded.
  - Gradle wrapper (latest 9.x), Kotlin DSL, Java toolchain 21 via the foojay resolver.
  - The Gradle build regenerates `gen/` from `.regia` (Exec `uv run regia compile`, with inputs and outputs declared), and `gen/` is gitignored.
  - `server.py` becomes `regia.server`, launched with `regia serve`.
  - Node is pinned with `.nvmrc` and `engines`. Godot 4.7 stays a manual step and is only version-checked.
  - CI runs on Ubuntu and leaves out Godot, the full benchmarks and the runtime benchmarks.
  - The license is decided in its own ticket.
- Tickets: `.scratch/artifact-tidy/issues/NN-<slug>.md`, with `Type:`, `Status:`, `Assignee:` and `Blocked by:` lines. The frontier is the open, unblocked, unclaimed tickets, lowest number first.
- Skills: `grilling` + `domain-modeling` for grilling tickets, `prototype` for prototype tickets.

## Decisions so far

<!-- one line per resolved ticket: [title](issues/NN-slug.md): gist -->

- [Commit the submitted snapshot as the 1.0 baseline](issues/01-baseline-snapshot.md): local `1.0` = `d1a3fc1`, a root commit (orphan, anonymous), tagged `artifact-submitted`, matches the snapshot minus `additional_material.pdf`; pushed (forced) with the tag on 2026-11-23. The answer lists what it overwrote and the junk left for ticket 02.
- [Restore the demo videos and snippet references cut for size](issues/15-restore-size-cuts.md): `91aeabe` on `1.0` brings back the 4 demo videos and the 6 snippet PNGs, byte-identical to the old `origin/1.0`. `data_21`, `_old` and `.godot` stay out.
- [Remove build output, IDE files and leftovers from 1.0](issues/02-clean-junk.md): `3d0c3d1` on `1.0` untracks 153 build/cache/backup files and adds a root `.gitignore`. The `.bak` files were stale `expand_data.py` backups. Not pushed.
- [Replace main's 1.0/ copy with a pointer to the branch](issues/03-main-copy-pointer.md): `20a59c9` on `main` untracks `1.0/`, adds a root README pointing to `1.0` and `artifact-submitted`, and gitignores `/1.0/`, which is now a worktree of branch `1.0`. Not pushed.
- [Python manifests and lockfile with a uv workspace](issues/04-python-uv-workspace.md): `680d4f6` on `1.0` adds a uv workspace (Python 3.14, one `uv.lock`), core `click`+`lark` with extras `server`/`benchmarks`/`dev`, qscores' own manifest, all bounded. pandas is held at 3.0.x because 3.1 changes a float digit in `respondents.csv`; with the lock, the qscores CSVs match the paper's byte for byte. Not pushed.
- [Move server.py into the package as regia serve](issues/05-server-into-package.md): `5a81bca` on `1.0` turns `server.py` into `regia.server`, started with `regia serve [--host --port]` (default 127.0.0.1:8000, as the editor expects). Without the `server` extra it exits with an install hint. Checked from outside the repo. Not pushed.

## Not yet specified

- **Release and archive.** After acceptance: a release tag on `1.0`, probably a Zenodo DOI, and which commit the camera-ready cites. This depends on the license and on the venue's artifact rules, which are still unknown. Any archive uploaded to the venue again must stay under 25 MB, so it would be built from `1.0` without the demo videos.
- **Answering the reviewer.** Whether to write a short change log that maps each review point to its fix (it could live in the README or in the rebuttal). This waits until the fixes exist.
- **Figure checking.** Whether "compare visually" is enough for figures, or whether CI should diff the PNGs. matplotlib is now locked (3.11.2); revisit once CI exists.

## Out of scope

- Godot in CI, and running the full or runtime benchmarks in CI: the game needs a display and the benchmarks take too long. They stay documented manual steps.
- Changes to the compiler's output, such as an emitter path prefix for `.create_agent` (option C in charting). This would change snapshots and goes beyond the review.
- `main`'s own housekeeping (docs, `.gitignore`, the Rust transpiler work), except the `1.0/` copy.
