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
- **Reference vs. regenerated.** The paper's outputs stay committed as *reference* data. The pipeline writes to separate, gitignored dirs and compares against the reference. qscores CSVs must match it exactly. Figures drawn from the paper's data are checked pixel by pixel in CI (`make compare-figures`) and are reproductions elsewhere. Benchmark timings are reproductions, not diffs.
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
- [Remove build output, IDE files and leftovers from 1.0](issues/02-clean-junk.md): `3d0c3d1` on `1.0` untracks 153 build/cache/backup files and adds a root `.gitignore`. The `.bak` files were stale `expand_data.py` backups.
- [Replace main's 1.0/ copy with a pointer to the branch](issues/03-main-copy-pointer.md): `20a59c9` on `main` untracks `1.0/`, adds a root README pointing to `1.0` and `artifact-submitted`, and gitignores `/1.0/`, which is now a worktree of branch `1.0`.
- [Python manifests and lockfile with a uv workspace](issues/04-python-uv-workspace.md): `680d4f6` on `1.0` adds a uv workspace (Python 3.14, one `uv.lock`), core `click`+`lark` with extras `server`/`benchmarks`/`dev`, qscores' own manifest, all bounded. pandas is held at 3.0.x because 3.1 changes a float digit in `respondents.csv`; with the lock, the qscores CSVs match the paper's byte for byte.
- [Move server.py into the package as regia serve](issues/05-server-into-package.md): `5a81bca` on `1.0` turns `server.py` into `regia.server`, started with `regia serve [--host --port]` (default 127.0.0.1:8000, as the editor expects). Without the `server` extra it exits with an install hint. Checked from outside the repo.
- [Gradle wrapper, Kotlin DSL and JDK 21 toolchain for minds](issues/06-gradle-wrapper-kotlin.md): `a68d387` on `1.0` builds the minds with the Gradle 9.9.2 wrapper (checksum pinned), Kotlin DSL and a JDK 21 toolchain that foojay downloads when it's missing. Checked on JDK 27, and also with JDK detection off. `run` is still the default and now creates `logs/`. Found on the way: the README's start order is wrong, since Godot is the server (noted for ticket 12).
- [Where generated agents live: asl-path or src/agt](issues/07-where-generated-agents-live.md): option B. `e7ddab3` on `1.0` adds `asl-path: "src/agt", "src/agt/gen"` (after the agents) to `science.jcm`, so `.create_agent` finds subplot directors and includes need no `gen/` prefix (shown by a headless probe run). `director_missingdonut.asl` goes back into `gen/`, a stale playbook is removed, and `gen/` matches the compiler output exactly.
- [The minds build generates its agents from .regia](issues/08-build-generates-gen.md): `1990cb2` on `1.0` adds the Gradle task `compileRegia` (via `uv run`), which runs before `compileJava` and reruns when a `.regia` file or the transpiler changes. `gen/` is untracked and gitignored, and a clean build reproduces it exactly. A missing uv gives a clear error.
- [Runtime benchmarks run through the wrapper](issues/09-runtime-benchmark-gradle.md): `b0bf219` on `1.0` generates a Kotlin/JDK 21 project and launches it with the minds' `gradlew -p`, with `asl-path: "gen"` in the `.jcm` and downloads done before measuring. Smoke-tested on two points. Found and left alone: the runner samples and kills every matching JVM, Gradle daemons included.
- [Reference outputs vs regenerated outputs](issues/10-reference-outputs.md): `061e7ab` on `1.0` moves the paper's outputs to `qscores/reference/` and `language/benchmarks/reference/`, and sends reruns to gitignored dirs that don't depend on the cwd. `compare_reference.py` fails on any CSV difference; all 11 CSVs match exactly.
- [Top-level Makefile for the whole pipeline](issues/11-makefile-pipeline.md): `e2fefb7` on `1.0` adds the root `Makefile` (`make help`, `make check-env`, `make all`), pins the editor to Node 24 and points the READMEs at the targets. `make all` passes in a clean export in under 3 minutes, scores comparison included. `bench-runtime` not run.
- [CI on GitHub Actions](issues/13-ci.md): `a34eb13` on `1.0` runs the Makefile targets on Ubuntu (with `bench REPS=1`) and checks that the tree stays clean. Green on the first run in 1m46s, and the qscores CSVs match the paper's there too. `1.0` was pushed up to this commit on 2026-11-24.
- [License for the code and the questionnaire data](issues/14-license.md): `09da043` and `853d137` on `1.0` (not pushed): code Apache-2.0, data CC-BY-4.0, `NOTICE` for VEsNA, Grandville art and the partner's diagrams, all anonymised. The two downloaded paper textures are replaced by generated ones. `e02958e` removes the leftover `cop.png~`.
- [One Requirements table and README pass](issues/12-requirements-readme.md): `a02ff34` on `1.0` (not pushed) adds the Requirements table, Reproduce the Paper, license section and CI badge, and fixes the demo instructions: Godot starts first, and the scene is `test_scene.tscn` because the main scene is empty (checked headless).
- [Check the redrawn figures in CI, or leave them to the eye](issues/16-figure-checking.md): `627710a` on `1.0` adds `make compare-figures`, run by CI and not by `make all`: exact pixels, no tolerance. All 6 questionnaire figures and the 3 fits match on the runner. `1.0` was pushed up to this commit.
- [Answer the reviewer: a change log from review point to fix](issues/17-answering-the-reviewer.md): `c67dd6e` and `57d0a2d` on `1.0` (pushed, CI green) add `CHANGES.md` (problem, fix, commit), correct the section references, make the demo the main scene and drop the `pip` hints. Every point of the review's build critique is answered at HEAD.
- [Submission archive: smaller game images and an export script](issues/18-submission-archive.md): `717febd` on `1.0` (pushed, CI green) has WebP game images and silent demo videos. `export.py`, next to this map, builds the anonymous zip from git: 5.75 MB with the PDF. Before uploading, complete `private-names.txt` and export again.

## Not yet specified

- **Release and archive.** After acceptance: a release tag on `1.0`, probably a Zenodo DOI, and which commit the camera-ready cites. This depends on the venue's artifact rules, which are still unknown. Any archive uploaded to the venue again must stay under 25 MB, so it is built with `export.py`, without the demo videos. Also at release: put real names in `NOTICE`, get the VEsNA authors' permission to redistribute, and leave the old paper textures out of the archive (they remain in the history and in `artifact-submitted`).

## Out of scope

- Godot in CI, and running the full or runtime benchmarks in CI: the game needs a display and the benchmarks take too long. They stay documented manual steps.
- Changes to the compiler's output, such as an emitter path prefix for `.create_agent` (option C in charting). This would change snapshots and goes beyond the review.
- `main`'s own housekeeping (docs, `.gitignore`, the Rust transpiler work), except the `1.0/` copy.
