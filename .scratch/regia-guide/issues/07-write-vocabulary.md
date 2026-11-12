# Write: Vocabulary

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 03

## Task

Write `docs/guide/3 - Vocabulary.md`.

Covers: Facts, Events, Actions, Goals, Propensities (Traits and Moods), Values, Numbers, Durations, Parameter names, Multi-definition, External names, Local Vocabulary.

Sources: 03, 04, 05, 10, 12.

Follow the chapter template fixed in *Fix the chapter template with a sample chapter* (03) and the map's Notes. Take snippets from `docs/guide/showcase/`; if a construct has no natural place there, either add it to the showcase or tag it `#revise`. Finish by re-reading every example against the cited spec chapters.

## Resolution

Written on 2026-11-12: [`docs/guide/3 - Vocabulary.md`](../../../docs/guide/3%20-%20Vocabulary.md), about 2,450 words counting snippets and the table, over nine sections (the kinds, Parameter names, Values, Durations, Multi-definition, External names, Propensities, Local Vocabulary, declaring an item twice). Not yet read by the user.

- The showcase Program is unchanged. Every snippet is cut from it except the two-file re-declaration of `served` and a few one-line variants in the prose.
- Numbers are covered only as Values (how they are written); arithmetic, comparisons and `RANDOM` are left to *Placeholders and Expressions*. Durations get the form and the "not a Value" rule; `WAIT` itself is left to *Plans*.
- Examples re-read against spec chapters 03, 04, 05, 08, 10, 12 and 14 (14 was not in the ticket's sources, but it is where Propensities are declared).

Six `#revise`:

1. One name per kind gives families of near-twin names (`wager`/`wagered`, `take_seat`/`took_seat`/`seat`, `poured`/`poison_poured`).
2. Every `EVENT` looks the same: game Events, Messages, Signals and Outcomes are told apart only by the showcase's comment banners; likewise Facts the game keeps and Facts the Agents keep.
3. Parameter names are used as if they were types (`person` sixteen times), a convention nothing checks.
4. Name Values are never declared, so a misspelt `kitchn` is a correct Program.
5. Events can't be local, so `challenged`, `hit` and `yielded`, used by `Duelling` alone, are in the shared Vocabulary.
6. When a Custom Action is done and whether it can be refused is known only from Doc comments.

Added to the README: one *Spec wording* note (whether a Playbook Role or a declared item's name can be a Name Value) and two *Gaps in the showcase* (no String or `PRINT`; no `AS` inside a Multi-definition and no item declared in two files).

Glossary fixes seen, added to the map's *Not yet specified*: Duration is listed with the Vocabulary though nothing declares one and no slot holds one; the entry for Mood carries a stray second `_Avoid_` line (`Notification, message`) that belongs to Signal.
