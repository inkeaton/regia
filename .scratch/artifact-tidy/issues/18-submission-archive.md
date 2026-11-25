# Submission archive: smaller game images and an export script

Type: task
Status: closed
Assignee: claude (session 2026-11-24, g)
Blocked by: 12, 14, 16

## Question

How small can the archive uploaded to the venue be, and how is it produced without build files, names or broken links?

## Agreed with the user (2026-11-24)

- The 7 game images become WebP q90 on `1.0`, same dimensions, UIDs kept. `.import` and `.uid` files stay. The user sees the images before the commit.
- The zip leaves out the demo videos, `docs/` and `.github/`. Reference figures stay PNG.
- `export.py` lives here on `main`, never on `1.0`. It uses `git archive`, adapts mentions of excluded files, badge and commit links, writes a deterministic zip, and fails above 25 MB or on a private name. `--pdf` adds `additional_material.pdf`.
- Strip the audio track from the videos on `1.0`, without re-encoding and without rewriting history.
- Check in an empty folder: `make all`, `make compare-figures`, the editor build, the game headless. Then push and wait for CI.

## Resolution (2026-11-24)

Done. `1.0` is now at **`717febd`** (three anonymous commits on `57d0a2d`), **pushed** with the user's go-ahead. [Run 45378388221](https://github.com/inkeaton/regia/actions/runs/45378388221) is green.

- **Size:** 5.75 MB with `additional_material.pdf`, against 25.1 MB for the submitted zip and 77.5 MB for all of `1.0` before.
- **Images** (`8511233`): WebP q90 (`box` at q95, to keep its grain), UIDs kept. Approved by the user from side-by-side sheets.
- **Videos** (`61b8b9a`): audio track removed, video streams unchanged (stream MD5s match). The versions with sound remain in the pushed history.
- **Build and import files:** a zip made from git has no build files, as they are untracked. `.import` and `.uid` stay: without `.import` Godot assigns new UIDs and warns.
- **Script:** `.scratch/artifact-tidy/export.py [--ref 1.0] [--out FILE] [--pdf PDF]`. Deterministic. It leaves out the videos and `docs/`, adapts README, `NOTICE` and `CHANGES.md`, and drops commit hashes, which are searchable on GitHub. It stops if a text it adapts has changed.
- **Changed from the plan:** `.github/` is in the zip, so reviewers see the CI setup.

**Checks** on the unzipped archive: `make all` and `make compare-figures` pass (11 CSVs, 13 figure and fit files match); the game listens on 9001-9004 headless. `make editor` passed on the previous zip; the editor hasn't changed since, and CI builds it. Not checked: the game played on screen.

**Left for the user:** `private-names.txt` (untracked, via `.git/info/exclude`) holds only the user's own 5 strings. Add co-authors, university and partner, then export again before uploading.
