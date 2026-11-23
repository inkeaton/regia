# Write the guide's README, the introduction

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
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

## Resolution

Written: [`docs/guide/README.md`](../../../docs/guide/README.md), resolved on 2026-11-23.

- Sections: *What Regia is* (the `take_seat` Plans from `courtesy.regia` and `arrival` from `royal_banquet.regia`), *From a Program to a running game* (pipeline mermaid with the Visual Editor beside it), *Regia 1.5* (the four left-out systems, each with its showcase stand-in and the chapters that carry its "In 2.0" note; one sample note; `R0109` and `T1902` in *Checks*), *The banquet* (`banquet.regin`'s opening; how snippets and throwaway variations read), *How a chapter reads*, *The chapters* (the five parts as tables of chapter, spec chapters and coverage, with the outline's reading-order mermaid).
- The opening table maps each kind of file and tool to the chapter that covers it, in place of the old introduction's `#revise`/*Since 1.0* parts.
- The showcase `README.md`'s opening now links the guide.
- Examples re-read against chapters 05, 15, 20, 21, 23 and 27; no retired spellings; all chapter links resolve; humanizer pass done.
- No findings.
