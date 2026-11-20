# Write the guide's README, the introduction

Type: task
Status: open
Assignee:
Blocked by: 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29

## Question

Write `docs/guide/README.md`, the introduction and index, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 27 (*Regia 1.5*), ADR 0025.
- **Covers:** what Regia is; Program → Transpiler → Build → Jason → game; what 1.5 is and how the "In 2.0" notes read; the banquet world; how a chapter reads (example first, *Checks*, `Spec:`); that the guide is derived and the spec wins; the chapter index in five parts.
- **Quotes most:** the showcase `README.md`, `courtesy.regia`, `royal_banquet.regia`.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- link the guide from the showcase `README.md`'s opening;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.
