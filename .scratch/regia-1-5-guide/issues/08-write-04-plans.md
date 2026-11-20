# Write guide chapter 04, Plans

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05

## Question

Write `docs/guide/04-plans.md`, *Plans*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 05, 06.
- **Covers:** Trigger, Context and Body; Trigger kinds; Cues and Events; several Plans under one Trigger; `IF`; loops.
- **Quotes most:** `courtesy.regia`, `dining.regia`, `serving.regia`.
- **"In 2.0" notes:** `FROM GAME`, `FROM ME`.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.

## Resolution

Done on 2026-11-20 (task). [`docs/guide/04-plans.md`](../../../docs/guide/04-plans.md), about 530 lines, written from the template:

- Sections, simple to full: A Trigger and a Body; Cues, Facts and Events; Trigger kinds (with *A Goal's Triggers*, kept short and pointing at *Goals and Failure*); `FROM` (pointing at *Messages* for the full story); the shape of a Trigger; the Context; several Plans under one Trigger (with *A `GIVEN` chain or an `IF`*); falling through (its own section, with a flowchart, since one rule covers every Trigger kind and the showcase's "no ELSE" comments read two ways); `IF` in a Body and its Placeholders; Loops.
- Two "In 2.0" notes where the 1.5 stand-in shows: `FROM GAME` on `Keeping_watch`'s bare `saw_pouring`, and `FROM ME` on `Duelling`'s `TO fight` starting a `strike` that has no `FROM`.
- Every showcase snippet checked line by line against its file by script. The one throwaway is `WHEN duel_on` rewritten with an `IF`.
- Checks borrow `R0802`, `R1105`, `R1405`, `R1412`, `R1502`, `R1508`, `R1714`, `R2014`, `R1307`, `R0806`, `T1104`, `T0702` and `R0109` where the misuse is in this chapter's constructs.
- `Guide: Plans` added under *05 Goals and triggers* and *06 Context and control flow* in the showcase README.
- Grep for retired spellings: only the deliberate error examples (`EVENT`, a clause without its comma, `SUITS … AND …`). The humanizer pass rewrote two sentences.

No findings.
