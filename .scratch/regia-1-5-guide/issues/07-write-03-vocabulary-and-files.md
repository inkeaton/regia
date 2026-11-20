# Write guide chapter 03, Vocabulary and files

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05

## Question

Write `docs/guide/03-vocabulary-and-files.md`, *Vocabulary and files*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 10; 03 (declaring parameters); 12 (*Durations*).
- **Covers:** `GAME`, the kinds of item, parameters, Values, Durations, imports, one namespace, name rules, declaration order, external names, local Vocabulary.
- **Quotes most:** `vocabulary.regia`, the imports at the top of each file.
- **"In 2.0" notes:** none expected.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.

## Resolution

Written: `docs/guide/03-vocabulary-and-files.md`, eleven sections from *The kinds of item* to *Local Cues*, then *How this combines with…*. No "In 2.0" notes, as expected. Beyond the outline's list it covers Propensities (as kinds, with `R1407`, `R1409`), the `.regin` import rules (`R2101`) and Instancing's own namespace for kinds and Agents, and a worked *A name that came through another file* example on `honor_duel.regia`. `Guide:` lines added under the showcase README's 03, 10 and 12 headings. Examples re-read against chapters 03, 05, 08, 10, 12, 14, 21 and 38; retired-spelling grep clean; humanizer pass done.

Four findings (none blocking): `R1016` misses `GAME` on Propensities; chapters 03 and 21 word Agent names differently; the glossary's *Vocabulary* and *Mood* entries; `R1005`'s line doesn't name `GAME`.
