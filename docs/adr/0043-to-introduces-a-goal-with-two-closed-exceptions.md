# `TO` introduces a Goal, with two closed exceptions

`TO` had two senses. Before a Goal it was a purpose, like the English infinitive (`TO find_food:`, `ASK ?who TO avenge(?s)`). Everywhere else it was a destination (`ASSIGN P TO Guest`, `MAPPING Host TO host`, `TRANSITION TO feast`, `CHANGE f TO f2`). The syntax review's one-meaning rule (chapter 01, ADR 0041) allows a word one gloss, so one of the two senses had to give up the word. We decided that **`TO` introduces a Goal**: the recipe header and `ASK … TO` are the most-written lines that use `TO`, and they read as plain English. The destination uses changed:

- `TRANSITION TO p` became **`ENTER p`**, which pairs with the `WHEN ENTERED` it fires, as `LEARN` pairs with `LEARNED`;
- `, MAPPING a TO b` became **`, MAPPING a AS b`**, the same gloss as `ext AS name`: the name the thing goes by on the receiving side;
- `UNASSIGN` and `UNASSIGNED` became **`REMOVE`** and **`REMOVED`**, for readability. `REMOVE P FROM Guest ?who` keeps `FROM`, whose one gloss is "where something comes from or leaves", which also covers the Sender.

**Two Statements keep a destination `TO`: `ASSIGN P TO Role` and `UPDATE f TO f2`** (which replaced `CHANGE f TO f2`). "Assign X to Y" and "update X to Y" are the English idioms, and no other word read as well. These are the only exceptions to the one-meaning rule. The list is closed: no other construct may cite them as a precedent.

## Considered options

- **`TO` means destination**: the four Director and Agent uses stay, and the recipe header becomes `WHEN g PURSUED:` or `RECIPE g:`, with `ASK ?who g` modelled on `TELL`. Rejected because the recipe header is the most-written line in the language, and `TO g:` is what makes it read as a recipe.
- **`ASSIGN` without `TO`**: the recipient first, as in `TELL` (`ASSIGN Guest Dining`), or a new preposition (`ONTO`). `FOR` and `ON` were already taken (`FOR EACH`, `PRECEDENCE … ON`). Each read worse than the idiom, and `ASSIGN … TO` / `REMOVE … FROM` read as a pair.
- **`CHANGE f INTO f2`**: it would keep the rule whole, with one new word. Rejected in favour of `UPDATE … TO`, which reads more naturally to its writer. `UPDATE f WITH f2` would have given `WITH` another gloss, and `UPDATE f INTO f2` isn't English.
- **Leaving `UNASSIGN … FROM` alone** because `FROM` is a Clause keyword: chapter 01 already lets a Clause keyword introduce the core's required item (`WAIT UNTIL c`), so the comma rule wasn't at stake. Only the sense was, and it passes.

## Consequences

- Chapter 01's *One sense* rule names the two exceptions. A later ticket that finds `TO` used as a destination elsewhere treats it as a violation.
- `ENTER`, `UPDATE`, `REMOVE` and `REMOVED` are reserved. The retired spellings are errors with a hint: `CHANGE` (`R08_08-retired-change`), `MAPPING a TO b` (`R15_14-retired-mapping-to`), `UNASSIGN` and `UNASSIGNED` (`R15_15-retired-unassign`), and `TRANSITION TO` (`R20_16-retired-transition-to`).
- "Transition" stays the name of moving between Phases, and the Phase map's edges keep it. It is no longer a keyword.
- The Trace's `GIVE … TO … AS …` and `TAKE … FROM …` lines are log output, not Regia, and are unchanged.
- ADR 0029's shapes of `FROM` carry over to `REMOVE` unchanged.
- In Regia 1.5, and the same spellings in 2.0.
