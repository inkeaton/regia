# Condition words

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 01

## Question

1.5 conditions mix positions:
- prefix: `PURSUING g`, `IN <phase>`;
- postfix: `<Plot>(args) RUNNING`;
- infix: `?x PLAYS Role`.

2.0 adds the infix `?x SENT e`. Apply the principles' rule on where condition words go. For each, keep it or reshape it, and check that the result still parses without knowing what a name is (chapter 01, *Parsing never depends on declarations*). Done when chapters 05, 15, 17, 20 and 26 (and 18, for `SENT`) are edited.

## Resolution

Resolved with Edoardo on 2026-11-20.

- **All five stay as spelled.** `PURSUING g` and `IN p` come first (implicit subject: the Agent, the running Plot); `P(args) RUNNING`, `?x PLAYS R` and `?x SENT e` follow their written subject. All pass *Where condition words go* (chapter 01). `ME PURSUING g` was rejected (an Agent only asks about its own Pursuits) and so was `RUNNING P` (its subject is written). No renames, no new error codes, no ADR.
- **Parsing.** A condition item starts with a keyword (`NOT`, `PURSUING`, `IN`, `(`) or is a term followed by at most one of `RUNNING`, `PLAYS <Role>`, `SENT <Cue>` or a comparison; the word after the term decides, so no declaration is needed (`Poisoning RUNNING` vs the Fact `is_hungry`).
- **Binding.** Condition words bind to their subject as tightly as comparisons, tighter than `NOT`: `NOT ?x PLAYS Guard` is `NOT (?x PLAYS Guard)`.
- **Edits.** Chapter 06 *Conditions*: complete list of what a condition tests (with chapters), the item grammar, the tightest row of the table now includes `!=` (a leftover from *`=` and naming a value*) and the condition words. Chapter 01 *Where condition words go*: parsing and binding sentence. Chapter 26: the `FOR EACH` condition list points to chapter 06. Chapters 05, 15, 17, 18, 20 were swept and nothing contradicted the decision, so they were left unchanged.
