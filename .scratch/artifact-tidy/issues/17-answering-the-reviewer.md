# Answer the reviewer: a change log from review point to fix

Type: grilling
Status: closed
Assignee: claude (session 2026-11-24, g)
Blocked by: 12, 16

## Question

Should there be a short change log that maps each point of the build critique to its fix, and where does it live: in the README, in a separate file on `1.0`, or only in the rebuttal? Also decide what to do with the "thesis" and section-number mentions in the component READMEs, and whether the empty main scene in the game is worth fixing (see *One Requirements table and README pass*).

## Resolution (2026-11-24)

Decided with the user (yes to all seven recommendations) and done. `1.0` is now at **`57d0a2d` "List the changes since the submitted artifact"**, on top of `c67dd6e` (both anonymous, no trailer). **Pushed** with the user's go-ahead, a fast-forward `627710a..57d0a2d`.

- **Change log:** `CHANGES.md` on `1.0`, linked from the root README: a table of problem, fix and commit, then changes beyond the review and known limits. Neutral wording, no quotes from the review, whose text is kept out of the repository and the tracker. The rebuttal can reuse its rows.
- **Coverage:** the user supplied the review, and every point of its build critique was checked against HEAD. None is unanswered.
- **Section numbers:** the "thesis" and wrong section mentions (two READMEs, three scripts) now cite the paper (Sections 5 and 6) and the supplementary material (Sections 3.2 and 4.3), as numbered in the submitted PDFs.
- **Main scene:** `run/main_scene` is `test_scene.tscn`, so F5 starts the demo. `main.tscn` stays, unused.
- **Install hints:** the three `pip install` messages now say `make setup`.
- The README's CI line also mentions the figure comparison.

**Checks:** 217 tests pass; all 11 CSVs match; `make compare-figures` matches all 13 files; headless Godot on a clean copy, with no scene given, listens on 9001-9004; every commit in `CHANGES.md` is an ancestor of HEAD. [Run 45373768022](https://github.com/inkeaton/regia/actions/runs/45373768022) is green in 1m42s. Not checked: the demo played on screen, and the commit links (`../../commit/…`) in the rendered page.
