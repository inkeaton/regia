# Check the redrawn figures in CI, or leave them to the eye

Type: grilling
Status: closed
Assignee: claude (session 2026-11-24, f)
Blocked by: 10, 13

## Question

Should CI run `make figures` and compare the PNGs with the reference, only run it to show that it works, or leave it out?

The map says figures are reproductions, not diffs. matplotlib is locked, and CI now exists and doesn't run `make figures`. Find out first whether the figures come out identical on the CI runner.

## Resolution (2026-11-24)

Decided with the user (yes to all four recommendations) and done. `1.0` is now at **`627710a` "Compare the redrawn figures with the paper's, pixel by pixel, in CI"** (anonymous, no trailer), on top of `a02ff34`. **Pushed** with the user's go-ahead: a fast-forward of 5 commits, `a34eb13..627710a`, so the license, texture, backup and README commits are public too.

- **Decision:** CI redraws the figures and compares decoded pixels exactly, with no tolerance. The comparison is `make compare-figures`, not part of `make all`, because another CPU or OS may draw a pixel differently.
- **Covered:** the 6 questionnaire figures, and the 3 fit figures drawn from the paper's benchmark runs with their 4 CSV/Markdown files (text compared exactly). Rerun plots are drawn in CI but not compared.
- **How:** `qscores/compare_figures.py [FIG_DIR] [REFERENCE_DIR]`; a missing or extra file fails too. No new dependency (matplotlib reads the PNGs). READMEs updated.

**Checks:**
- [Run 45372646606](https://github.com/inkeaton/regia/actions/runs/45372646606) is green in 1m58s: all 13 files match on `ubuntu-24.04`.
- In a clean export on Linux x86_64 here, `make bench REPS=1` then `make compare-figures` pass.
- Negatives, each reported with exit 1: one changed pixel, another size, a missing figure, an extra one, changed fits text, a missing directory.
- Not checked: macOS, Windows or ARM.

### Facts for later tickets

- The PNG bytes do differ from the reference; ticket 10's note was right about that, but only compression differs (checked on `calibration.png`'s chunks; zlib-ng is the likely cause). The README's "fonts and libraries" explanation is gone.
- The run restored the Gradle caches, which ticket 13 hadn't seen yet.
- Not compared: `reference/interaction_full_game_case_study/interaction_full_game_case_study_plots.png`, which no target redraws from the paper's runs.
