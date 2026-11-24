# Restore the demo videos and snippet references cut for size

Type: task
Status: closed
Assignee: claude (session 2026-11-23)
Blocked by: 01

## Question

Bring back on `1.0` the content that was cut only to fit the submitted archive under its 25 MB limit.

The user decided on 2026-11-23, after ticket 01, to restore exactly these two:

- `science_game/demo_video/route_{1..4}.mkv` (60.4 MB in total; the largest is 21.6 MB, under GitHub's 50 MB warning, so no LFS is needed)
- `docs/snippets references/` (6 PNGs, 2.9 MB)

Restore them from the old `origin/1.0` (`442b924`) as their own commit after `artifact-submitted`, with byte-identical blobs that are already in history, so the repo doesn't grow. The commit message says they were cut for the 25 MB archive limit. Not restored: `qscores/data_21/`, `_old/`, `game/.godot/`. If a README already mentions the videos, check that the path it gives is right. Wider README wording waits for *One Requirements table and README pass*.

## Resolution (2026-11-23)

Done. `1.0` is now at **`91aeabe` "Restore demo videos and snippet references cut for size"**, the commit right after `artifact-submitted` (`d1a3fc1`). It adds 10 files: `science_game/demo_video/route_{1..4}.mkv` and the 6 PNGs in `docs/snippets references/`. `git diff origin/1.0 1.0` on those paths is empty, so they're byte-identical to the old branch and no new blobs were added. It was built with a temporary index, so main's working tree wasn't touched. Neither README mentioned these paths, so no README edit was needed. **Pushed** on 2026-11-23 (`--force-with-lease` over `442b924`), tag included.
