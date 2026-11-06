# Basic Action set

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo
Blocked by: 03, 05, 08

## Question

What is the final set of Basic Actions, and what are their names (primer ch.4)? Starting from `PRINT`, `BELIEVE`, `FORGET`, `ACHIEVE`, `WAIT`, `BROADCAST`, `TELL`, `SIGNAL`: rename `ACHIEVE` to `PURSUE`? Add `DISCARD` to drop a Goal? Anything else (e.g. Actions over Groups)? Confirm that only Custom Actions take `DO`, and check every name against the readability rule.

## Comments

- From *Numbers and arithmetic* (04): changing a numeric Fact is `FORGET health(?h)` then `BELIEVE health(?h - ?dmg)` for now. Decide whether a single replacing Basic Action is worth adding, and its name. Also decide how `PRINT` joins text and values (there is no `+` on strings; the spec examples use `PRINT("Ouch! Lost", ?dmg)`). Arithmetic must work inside any Basic Action's arguments. See `docs/spec/04-numbers-and-expressions.md`.
- From *Goals and Trigger kinds* (05): a Body can give itself a Goal and **wait** for it, or start it and carry on; both must exist. Decide their syntax (e.g. `PURSUE g AND WAIT`) and which is the default. Also the action that drops a Goal (it fires `WHEN g DROPPED`). Fact Triggers are written `LEARNED`/`FORGOTTEN`, so check that the Fact action names read well next to them. See `docs/spec/05-goals-and-triggers.md`.
- From *Messaging between Agents* (08): sending is `TELL <recipient> <fact or event>.`, `ASK <recipient> TO <goal>.` and `SIGNAL <event>.`; `BROADCAST` became the recipient `EVERYONE`. Confirm these names next to the rest of the set. Message Statements may later take trailing `,` clauses (`ASK ?g TO find_sword, AND WAIT`); decide whether self-pursuit's "wait" uses the same shape so both line up. `REFUSE`, `TOLD`, `AGREED`, `REFUSED`, `REACHED`, `FAILED` are reserved. See `docs/spec/07-messaging.md`.

## Answer

Spec chapter: `docs/spec/08-basic-actions.md`. ADR 0005 (`PURSUE` waits; `ASK` does not). `BELIEVE` renamed `LEARN` in spec chapters 03–07. Glossary: Basic Action revised.

- **The set:** `LEARN`, `FORGET`, `CHANGE … TO` (Facts); `PURSUE` and `DROP` (Goals); `TELL`, `ASK … TO`, `SIGNAL` (sending, names confirmed); `PRINT`; `WAIT`. Only Custom Actions take `DO`. No empty Statement.
- **Names match their Trigger kinds:** `LEARN`/`LEARNED`, `FORGET`/`FORGOTTEN`, `DROP`/`DROPPED`, `PURSUE`/`PURSUING`. `BELIEVE` and `ACHIEVE` are gone.
- **No-ops:** learning a known Fact, forgetting an unknown one, and dropping a Goal not pursued all do nothing and fire nothing.
- **`CHANGE f TO f2`:** shorthand for `FORGET` + `LEARN` on the same Fact name; fires `FORGOTTEN` then `LEARNED`; fails the Plan if `f` isn't known.
- **`PURSUE g.` waits** until `g` is reached; `PURSUE g, WITHOUT WAITING.` carries on (the trailing-clause shape reserved in chapter 07). `ASK` never waits. Pursuing a Goal already in progress joins it and waits for it.
- **`DROP g`:** stops `g`'s running Plan at once (even its own), then the Goals it was waiting on, then fires `DROPPED`. `WITHOUT WAITING` Goals keep running. A Body waiting on a dropped Goal fails.
- **Arguments:** certainly filled only, Expressions anywhere; no "forget/drop all matching".
- **`PRINT(e1, e2, …)`:** keeps its parentheses, joins Expressions with single spaces, outputs to the Target's log.
- **Handed off:** `WAIT`'s argument to *Time and timers*; Actions over Groups to *Groups*; failing (and a deliberate fail Action, `DROPPED` on stopped sub-Goals) to *Plan failure and fallback*.
