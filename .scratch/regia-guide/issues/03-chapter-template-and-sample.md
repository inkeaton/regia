# Fix the chapter template with a sample chapter

Type: prototype
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 02

## Question

What does a guide chapter look like on the page? Write `docs/guide/6 - Matching.md` (Match, Pick, `FOR EACH`, counts; spec 06, 26) as the sample, for the user to react to, and from it fix:
- The four parts: what the construct is for; examples from simple to full; *How this combines with…*; a short *Since 1.0* note with `#changes`.
- Voice ("we", as in the primer), length, how much prose per example, how `#revise` and spec pointers are written.
- How a chapter refers to the showcase and to other chapters.

The settled template is written into the map's Notes, so every writing ticket loads it.

## Resolution

Accepted by the user on 2026-11-11. The sample is [`docs/guide/6 - Matching.md`](../../../docs/guide/6%20-%20Matching.md), about 1,300 words, checked by hand against spec chapters 03, 04, 06, 08, 09 and 26. The template it fixes is written into the map's Notes.

- **Length, voice and `#revise` placement**: accepted as in the sample. A `#revise` is its own paragraph at the end of its section.
- **Showcase-only problems are not `#revise`.** They go in a new section of the showcase README, *Gaps in the showcase*, and are fixed later by adding to the Program. The first entry is `LOWEST`.
- **Mermaid diagrams** are used where they explain a relation. The sample has one, a sequence diagram for the wager Pick in `HonorDuel`.
- **Review notes**: six `#revise` entries in the sample, for *Write: Review List* to collect.
- No glossary change and no ADR.
