# Endings and kind words

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 01, 07

## Question

A Goal ends `REACHED`, `DROPPED`, `FAILED [WITH r]` or `ENDED`. A Subplot ends `ENDED WITH e`, `ENDED WITHOUT OUTCOME`, `DROPPED` or `ENDED`. A Phase is `ENTERED` and `EXITED[, BY PARENT]` (a clause since *`BY`, `WITH`, `WITHOUT`, `AT` and `UNTIL`*), and a Playbook is `ASSIGNED`/`REMOVED` (`UNASSIGNED` until *`TO` and `FROM` outside Triggers*). Fact Triggers are `LEARNED`/`FORGOTTEN`, and the cast words are `LEFT`/`EMPTIED`.

Decide:
- whether a Goal and a Subplot share `DROPPED` and `ENDED` under the test (ADR 0030 chose to share them);
- whether the Reason/Outcome asymmetry stays, with the specific word on `FAILED` for one and on `ENDED` for the other;
- whether `WITHOUT OUTCOME` keeps its shape;
- whether kind words keep following their item (with the principles' rule on positions).

Done when chapters 05, 11, 17, 19 and 20 and any ADR the decision overturns are edited.

## Resolution

Grilled with the user on 2026-11-20. New ADR 0047 (`docs/adr/0047-a-subplot-finishes-and-ended-is-only-the-catch-all.md`), which revises the spelling in ADR 0030 and keeps its decision.

1. **A Goal and a Subplot keep sharing `DROPPED` and `ENDED`**, which pass the test: `DROPPED` is "stopped on purpose by whoever started it", `ENDED` "over, however it went".
2. **`ENDED` had two jobs in a Subplot** ("ended by itself" with `WITH`/`WITHOUT OUTCOME`, "any ending" when plain). `ENDED WITHOUT OUTCOME` also read as covering a drop, and a plain `ENDED` fired after `ENDED WITH` while a plain `FAILED` competes with `FAILED WITH`. A Subplot that ends by itself now fires **`FINISHED`**, its counterpart of `REACHED`/`FAILED`. `ENDED` is only the catch-all: no complement, always after the specific Trigger.
3. **`WITHOUT OUTCOME` is retired.** `FINISHED WITH e` and a plain `FINISHED` share a Trigger, first match wins, like `FAILED WITH` and plain `FAILED`. A plain `FINISHED` above a `FINISHED WITH` it shadows is `R1716`. The retired `ENDED WITH`/`ENDED WITHOUT OUTCOME` are `R1715`. `R1706` keeps only the unknown Outcome, and `R1708` counts a plain `FINISHED`.
4. **`END SUBPLOT P` → `DROP SUBPLOT P`**, worded like the `DROPPED` it fires, as `DROP g` is. `SUBPLOT` is required: a bare `DROP P` on a Plot is `R0802` with a hint. The retired `END SUBPLOT` is `R1717`.
5. **Reason and Outcome** stay separate terms sharing the gloss of `WITH`. With `FINISHED`, `WITH` sits on a specific word for both, so the asymmetry is gone.
6. **Kind words stay where they are**: after a written item, alone when the subject is implicit (chapter 01's rule).

Edited: chapters 05, 08, 11, 15, 17, 20, 25, 29, 30, 31, 34, 38; `GLOSSARY.md` (*Subplot*, *Outcome*, *Trigger kind*, *Director Statement*); ADR 0047. Chapter 19 needed no change (`LEFT`, `EMPTIED`). No regression case used the old spellings. ADR 0030 is left as the historical record.
