# Retired spellings and their codes

Type: grilling
Status: closed
Assignee: claude (with Edoardo)
Blocked by: 12

## Question

Each rename of the review gave its retired spelling a new error code with a hint, in the chapter that owns the construct (`R0407`, `R0808`, `R0906`, `R1412`, `R1514`, `R1515`, `R1516`, `R1517`, `R1608`, `R1715`, `R1717`, `R2016`, `R2124`, `R2125`, `R2606`, alongside the older `R0513` for `EVENT`). Decide:

- whether that stays the pattern, or the retired spellings are gathered in one place (one chapter section, one code range, or both), and what happens to the codes already given;
- whether a retired keyword **stays reserved**. Chapters 09, 15, 16 and 17 say so for `EITHER`, `PERCENT`, `STARTS` and `OUTCOME`, and chapter 01's *Reserved words* lists those plus `EVENT`; `CHANGE`, `TRANSITION`, `UNASSIGN`/`UNASSIGNED` and `AT RANDOM` have an error with a hint but no word on reservation (found by *Spec examples after the review*);
- how long a retired spelling keeps its hint (for ever, or until a stated version).

Done when chapter 01 (*What syntax can be dropped*, *Reserved words*) and the owning chapters' *Transpiler checks* are edited to match.

## Resolution

Agreed with Edoardo on 2026-11-20.

- **Where they live.** Each retired-spelling error keeps its code in the chapter that owns the construct, as chapter 27 requires (one code range would have renumbered 15 codes and broken never-reuse). Chapter 01 gains a *Retired spellings* section: a table of retired spelling, replacement and code, the index beside *Reserved words*. Chapter 27 says these checks are never dropped and points to it.
- **For ever.** A retired spelling keeps its error and hint for ever; its code is never marked retired. Regia is generated as well as written, and a generator can produce an old spelling long after writers stop (the `EVENT` precedent).
- **Retired keywords stay reserved**, as one rule in chapter 01 (*What syntax can be dropped*) rather than chapter by chapter. The reserved list gains `CHANGE`, `TRANSITION`, `UNASSIGN` and `UNASSIGNED`, next to `EVENT`, `EITHER`, `PERCENT`, `STARTS` and `OUTCOME`. Only the exact all-caps spelling is blocked.
- **Only this spec's own spellings get an error.** Regia 1.0, draft and primer words (`BELIEVE`, `ACHIEVE`, …) get none and aren't reserved: 1.0 is a different language.
- **Not on the list:** `R1517` (a misplaced `%`, not an old word) and `R0111` (a missing comma), plus `R0107`/`R0108` for the removed Flat blocks, which chapter 01 mentions under the table.
- No ADR: the rules and their reasons sit in chapter 01's prose, and nothing about them is surprising once read there.
- **Files changed:** `docs/spec/01` (*What syntax can be dropped*, *Reserved words*, new *Retired spellings*, *Regia 1.5*), `docs/spec/05` (`R0513` worded like the others), `docs/spec/27` (*Diagnostic codes*), `GLOSSARY.md` (*Retired spelling*). The owning chapters' *Transpiler checks* already used the uniform "The retired …" wording and no longer state reservation on their own, so they needed no other edit.
- **For *The hand-off to the showcase*:** the chapter 01 table is an old→new list in the spec, which that ticket may adopt.
