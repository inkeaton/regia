# Map: Regia 1.5 syntax review

Label: wayfinder:map

## Destination

A decision on every symbol and keyword of the Regia 1.5 language, `.regin` Instancing included: keep it, rename it, or restructure the construct, so that each symbol has one meaning wherever it can and the syntax stays simple. Every decision is carried into `docs/spec/`, `GLOSSARY.md` and `docs/adr/`. A ticket closes when those are edited, not when the answer is agreed.

Charted with the user on 2026-11-19.

## Notes

- **The baseline** is `inventory.md`, a snapshot of the syntax when the map was charted: symbols, keywords, words with several meanings, and spec examples that contradict the spec. Tickets point into it.
- **The test for one meaning** (agreed when charting): a word or symbol may appear in several constructs only if it has the same grammatical role and the same English sense in each, so a reader who knows one use can predict the others. *The principles of the 1.5 syntax* sharpens it, and it can't be reopened elsewhere.
- **Scope.** Only 1.5 constructs open tickets. When a 1.5 rename hits a word that 2.0-only constructs share (`BY` on a Goal's ending, `FROM GAME`, `FROM ME`, `FROM a OR b`, Quotas, `SENT`, `JOINED`), the ticket also decides the 2.0 spelling, as the smallest change that follows from it, so the two never disagree (ADR 0025).
- **Renames are welcome** when they make the language simpler. Beyond overloads, the scope also covers syntax nobody uses, condition words in mixed positions, and asymmetric forms.
- **The user's own leanings** (the tickets weigh them, they aren't decided yet):
  - `,` means "let me add something more", which covers both an optional addition to a Statement or header and the next item of a list. For example, the optional `FROM` would be written `WHEN e, FROM DIRECTOR:`.
  - `%` is free now that `#%` is retired, so it can write percentages.
- **Contradicting examples** (inventory §4) are fixed in the ticket that covers their construct. *Spec examples after the review* sweeps up what is left.
- **Memories to weigh:** *Regia is generated too* (explicit `.` and `;` stay optional, for one-line code; indentation is the default, generated code included) and *Language vs game design*.
- Tickets: `.scratch/syntax-review/issues/NN-<slug>.md`, with `Type:`, `Status:`, `Assignee:` and `Blocked by:` lines. The frontier is the open, unblocked, unclaimed tickets, lowest number first.
- Skills: `grilling` and `domain-modeling` for every grilling ticket.

## Decisions so far

<!-- one line per resolved ticket: [title](issues/NN-slug.md): gist -->

- [The principles of the 1.5 syntax](issues/01-principles.md): one gloss and one structural job per word (nouns and mainstream symbols pass); `,` means "more follows", a Clause is `, KEYWORD …` after the core; condition words follow a written subject; keywords UPPERCASE and reserved (`R0110`); drop syntax only if no hand, generator or editor needs it. Chapter 01, ADR 0041.
- [The comma](issues/02-the-comma.md): `FROM`/`BY` on Triggers and `LIKE`/`PLAYS` on `KIND`/`AGENT` become `, CLAUSE`; inline Context `WHEN x, GIVEN c:` removed; `,` never means AND; lists end at a clause keyword or a non-item; missing comma is `R0111`.
- [`.`, `;` and the Block styles](issues/03-dot-semicolon-blocks.md): `:` `.` `;` are the one-line spellings of indent, new line, dedent; indentation is the default style, for generated code too; Flat blocks and `R0107` removed; `PASS` stays and the empty-Option exception goes; trailing `.` silent. Chapters 01, 09.
- [`=` and naming a value](issues/04-equals-and-naming.md): `=` only compares; a Body fills with `LET ?x BE e.`; not-equal is `!=`; `.regin` settings are `key value.`; "naming" retired for "fill". Retired spellings `R0407`, `R2124`; `LET` in a condition `R0408`. ADR 0042.
- [`TO` and `FROM` outside Triggers](issues/05-to-and-from.md): `TO` introduces a Goal (`TO g:`, `ASK x TO g`), with two closed exceptions for the idiom, `ASSIGN P TO R` and `UPDATE f TO f2` (was `CHANGE`); `TRANSITION TO p` → `ENTER p.`; `MAPPING a TO b` → `MAPPING a AS b`; `UNASSIGN(ED)` → `REMOVE(D)`, keeping `FROM`. Retired `R0808`, `R1514`, `R1515`, `R2016`. ADR 0043.
- [`AND`, `OR` and `EITHER`](issues/06-and-or.md): `AND`/`OR` are only condition operators; Label Propensities, `SHIFT` Moods and `PLAYS` Roles become `,` lists (`R1412`, `R2125`); `FROM a OR b` stays; Random choice is `RANDOMLY:` with `OPTION:` Blocks, a single Option warns (`R0905`), `EITHER:`/`OR:` retired (`R0906`). Chapters 01, 05, 09, 14, 21.
- [`BY`, `WITH`, `WITHOUT`, `AT` and `UNTIL`](issues/07-by-with-at-until.md): `BY` names who did it, `WHEN EXITED, BY PARENT:` is a clause; `SHIFT m BY n` keeps `BY` as a closed exception; `, AT RANDOM` → `, RANDOMLY` (`R2606`, a second closed exception); `STARTS WITH:` must lose `WITH` (left to *Setups and `ROLE`*); `WITHOUT`, `UNTIL`, `AT` as a level stay. ADR 0044.
- [Quantities: `%`, `OF`, `COUNT`, `RANDOM` and `WEIGHT`](issues/08-quantities.md): `n% OF Role` replaces `n PERCENT OF` (`R1516`), with `%` allowed only before `OF` (`R1517`); `%` is never a remainder, and any future modulo will be a word; `COUNT`, `RANDOM`, `WEIGHT`, `OF` and `ALL Guest` stay. ADR 0045.
- [Setups and `ROLE`](issues/09-setups-and-roles.md): a setup is the Role's Block, `ROLE Guest:` / `CAST:`, also inside `DURING` (`STARTS WITH:` retired, `R1608`); `LEARN`/`PURSUE` keep one gloss, and the source follows from where the line is written; Playbooks keep `ROLE`, with no Block; a setup may use the Plot's parameters. ADR 0046.
- [Endings and kind words](issues/10-endings-and-kind-words.md): a Subplot that ends by itself fires `FINISHED [WITH e]` (first match, like `FAILED`), so `ENDED` is only the catch-all for Goals and Subplots; `WITHOUT OUTCOME` retired (`R1715`), `END SUBPLOT` → `DROP SUBPLOT` (`R1717`); `DROPPED` shared; kind words stay put. ADR 0047.
- [Condition words](issues/11-condition-words.md): all five stay (`PURSUING g`, `IN p` first; `P RUNNING`, `?x PLAYS R`, `?x SENT e` after the subject); a condition item is a keyword-first form or a term plus one condition word, so it parses without declarations; condition words bind tighter than `NOT`. Chapters 01, 06, 26.

## Not yet specified

- **Diagnostics.** How a renamed keyword shows up in the Transpiler checks: a retired spelling as an error with a hint (as `EVENT` → `CUE`, `R0513`), and which codes are retired or renumbered. A clause missing its comma is settled (`R0111`, *The comma*). So far each rename gives its retired spelling a new error code with a hint in the chapter that owns the construct (`R0407`, `R0808`, `R0906`, `R1412`, `R1514`, `R1515`, `R1516`, `R1517`, `R2016`, `R1608`, `R1715`, `R1717`, `R2124`, `R2125`, `R2606`). Still open: whether to keep doing that or gather them into one place.
- **The hand-off to the showcase.** Whether the showcase update needs a written list of old and new spellings (a *Since 1.5 revision* section, or a list on the map), and where it lives. Known items so far: the showcase relies on new lines rather than trailing dots (its "house style writes it" note goes), the *Flat blocks* row of `docs/showcase/README.md` goes, an Option that does nothing holds `PASS`, `?x = e.` becomes `LET ?x BE e.`, `NOT ?a = ?b` becomes `?a != ?b`, and `TARGET` settings drop their `=`. From *`TO` and `FROM` outside Triggers*: `CHANGE f TO f2` → `UPDATE f TO f2`, `TRANSITION TO p` → `ENTER p`, `MAPPING a TO b` → `MAPPING a AS b`, `UNASSIGN`/`UNASSIGNED` → `REMOVE`/`REMOVED`. From *`AND`, `OR` and `EITHER`*: `EITHER:` / `OR:` → `RANDOMLY:` with `OPTION:` Blocks (one more indent), and `AND` in `SUITS`/`SHIFTS`/`SHIFT`/`PLAYS` lists → `,`. From *`BY`, `WITH`, `WITHOUT`, `AT` and `UNTIL`*: `, AT RANDOM` → `, RANDOMLY`, `WHEN EXITED BY PARENT:` → `WHEN EXITED, BY PARENT:`. From *Quantities*: `n PERCENT OF Role` → `n% OF Role`. From *Setups and `ROLE`*: `ROLE X STARTS WITH:` → `ROLE X:`, `CAST STARTS WITH:` → `CAST:`. From *Endings and kind words*: `WHEN P ENDED WITH e` → `WHEN P FINISHED WITH e`, `WHEN P ENDED WITHOUT OUTCOME` → a plain `WHEN P FINISHED` after the `WITH` Plans, `END SUBPLOT P` → `DROP SUBPLOT P`.

## Out of scope

- **Updating the 1.5 showcase** (`docs/showcase/`) and its reference Build to the new syntax. It's a later effort, and the user will run it after this map.
- **The 2.0 guide** (`docs/guide/`). It's derived and never normative, and it follows the spec in its own effort.
- **Constructs that only 2.0 has**, except where a 1.5 rename forces their spelling (*Notes*, *Scope*).
