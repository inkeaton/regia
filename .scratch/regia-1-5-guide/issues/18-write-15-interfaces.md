# Write guide chapter 15, Interfaces

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 05

## Question

Write `docs/guide/15-interfaces.md`, *Interfaces*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 38.
- **Covers:** nothing is declared; the Interface of a Playbook and of a Plot; who sends a Cue; the checks of one side against the other.
- **Quotes most:** across `playbooks/` and `plots/`.
- **"In 2.0" notes:** the asked-Goal rows, `R3805`, `R3806`.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.

## Resolution

Done on 2026-11-20 (task). [`docs/guide/15-interfaces.md`](../../../docs/guide/15-interfaces.md), about 460 lines, written from the template:

- An opening table of what the Transpiler checks between which two sides.
- Sections, simple to full: Nothing is declared (`Keeping_watch`'s `SIGNAL` and the Guard's setup; `regia explain`; Interfaces per Entry); The Interface of a Playbook (`Keeping_watch` as a table, `Serving` for Goals, Reasons and a local Goal); The Interface of a Plot (`HonorDuel` as a table, a mermaid flowchart of `betting` meeting `Wagering`); Who sends a Cue (the five groups over the whole Vocabulary) with *A Cue nothing sends*; Signals and the Plots that give them (*never handles*, *some Phases only* with `insult_thrown` in `reception`, *no Signal can reach*); Requests and the `FROM` that admits them (the `feast` Mappings followed step by step) with *An Agent's own `PURSUE`*; Reasons a Goal never fails with (`bring` through `fetch`); Between a Subplot and its parent (borrows `R1706`, `R1708`, `T3802`).
- The Interfaces of `Keeping_watch` and `HonorDuel` are shown as tables of parts, since no printed form is specified (finding).
- "In 2.0" notes, as listed: the asked-Goal rows (under the Plot's Interface, with `handkerchief_dropped` as the stand-in), and `R3805`/`R3806` (under *An Agent's own `PURSUE`*: in 1.5 such a `PURSUE` fails at run time with `T1104`).
- Throwaway snippets break one line each for `R3801` (no `handkerchief_dropped` Plan), `R3802` (`poison_drunk, FROM Watchman`), `R3803` (`MAPPING Host AS patron`), `R3804` (`have_dinner FAILED WITH sold_out`), `R3807` (`vent` without `TELL ?foe insulted`).
- Every showcase snippet checked against its file by script (10 linked snippets). Codes appear in *Checks* only.
- `Guide: Interfaces` added under *38 Interfaces* in the showcase README.
- Grep for retired spellings: none. The humanizer pass cut one closing line; two wording fixes beforehand (`FROM ?speaker` isn't the same as no `FROM`; a variation's comment).

Four non-blocking findings: whether a `WHEN` Trigger with no `FROM` is in a Playbook's Interface; game Cues in a Plot's "Signals it handles"; whether `R3802` covers `FROM ?who`; the printed form of `regia explain … interface` (and the README's pointer to runs that don't exist yet).
