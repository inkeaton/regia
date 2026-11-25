# License for the code and the questionnaire data

Type: grilling
Status: closed
Assignee: claude (session 2026-11-24, d)
Blocked by:

## Question

Under what terms is the artifact published?

Settle three things:

- **The code license** (MIT, Apache-2.0, or "all rights reserved" for now). This needs the co-authors' and institution's agreement.
- **The questionnaire data.** Does it get a separate license, such as CC-BY-4.0? Does participant consent cover publishing the anonymised responses in `qscores/data/data.xlsx`, and is the data actually anonymised?
- **Third-party assets** in the Godot game (`science_game/game/resources/`) and the VEsNA code under `minds/src/`: what licenses do they carry, and are they compatible with the choice?

Close with a `LICENSE` file (and `LICENSE-data`, if needed) committed on `1.0`.

## Answer

Done on 2026-11-24 on `1.0`, not pushed: `09da043` (textures) and `853d137` (license). Decided with the user:

- **Code:** Apache-2.0 (`LICENSE`), with "Copyright (c) 2026 The Regia authors (anonymised for review)" in `NOTICE`. Real names go in at camera-ready. The `license` field is set in both `pyproject.toml` files, `package.json` and its lock; the SPDX form needs `setuptools>=77`.
- **Data:** `qscores/data`, `qscores/reference` and the questionnaire PDF are CC-BY-4.0 (`LICENSE-data`). The user confirmed that publication and reuse are fine, though the form itself doesn't mention publication. `data.xlsx` has no names or emails (checked: those columns, the file metadata, a pattern search over the answers, and every closing comment; not every open answer was read). The start and completion timestamps stay, by the user's choice.
- **VEsNA:** nine core files are excluded from Apache-2.0 in `NOTICE` and all rights stay with their authors, unnamed during review. The other Java (`via/`, `helpers/`) is Regia code.
- **Art:** the portraits and the flower are J. J. Grandville, public domain. The paper textures came from Resource Boy, whose license (for its own exclusive items; third-party items follow their product page) forbids uploading files to repositories, and the product pages weren't checked. `backdrop.png` and `box.png` are now generated, at the same sizes. The old ones stay in the history and in `artifact-submitted`; the demo videos still show them, as use in a finished project.
- **Snippet diagrams:** they belong to an industrial partner that agreed to their publication. All rights reserved, unnamed during review.

Checked: tests (217 passed), the minds build, all 11 qscores CSVs match, the `regia` package builds, and Godot reimports both textures. `make editor` passes with Node 24.22.3. Not checked: how the game looks on screen.

Left over: `science_game/game/resources/images/portraits/cop.png~`, a tracked editor backup identical to `cop.png`, was missed by *Remove build output, IDE files and leftovers from 1.0*; `e02958e` removes it and gitignores `*~`.
