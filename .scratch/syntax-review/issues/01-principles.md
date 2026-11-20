# The principles of the 1.5 syntax

Type: grilling
Status: closed
Assignee: claude (with Edoardo)
Blocked by:

## Question

Which rules does every later ticket apply? Settle them once, so that no other ticket argues them again:

1. **The test for one meaning** (the map's *Notes*). Sharpen it into something a ticket can check: what counts as "the same grammatical role", and whether a shared English sense alone is enough (`TO` as "toward" in `ASK x TO g`, `ASSIGN P TO R`, `MAPPING a TO b`, `TRANSITION TO p`).
2. **What `,` means.** The user's leaning is "let me add something more": an optional addition to a Statement or header, or the next item of a list. Decide whether that is the rule, and what it implies in general:
   - every optional part after the core of a header or Statement is written `, KEYWORD …`, `FROM` included (`WHEN e, FROM DIRECTOR:`);
   - the end-of-line `,` continues the line because more is coming;
   - argument separators and Multi-definition lists are lists.

   *The comma* applies it construct by construct.
3. **The shape of a header.** What is the core of a Trigger, a Statement or a Director Statement, which parts are clauses, and whether clauses may come in any order.
4. **Where condition words go.** Prefix (`PURSUING g`, `IN p`), postfix (`P RUNNING`, kind words) or infix (`?x PLAYS R`). Choose one rule, or a reason for each.
5. **Keywords.** Do they stay UPPERCASE and reserved, and is a new word preferred over reusing an old one?
6. **What can be dropped.** When is syntax that nobody writes (inventory §2, *Layout*) removed, and how much weight does *Regia is generated too* carry?

Done when each point has a rule, worded so a ticket can apply it, and the rules are written where the spec states its general syntax (chapter 01 and `GLOSSARY.md`), with an ADR if the comma rule or the header shape meets the ADR bar.

## Resolution

Grilled with the user on 2026-11-19. Every rule is written in chapter 01, *The principles of the syntax*; the comma and keyword rules are also in ADR 0041 (`docs/adr/0041-clauses-follow-a-comma-and-keywords-are-uppercase.md`), and `GLOSSARY.md` has **Clause**.

1. **One meaning.** One gloss covers every use, and the word does one structural job (head keyword, connector introducing a complement, or operator); the kind of thing it introduces may vary. Fixed phrases get no exemption. A noun naming a kind of thing passes on sense alone when every use refers to that kind of thing. A symbol keeping its mainstream programming meaning passes; the test applies to `,` `.` `:` `;` `=` `%`. Applied to `TO`: two senses (purpose: `TO g:`, `ASK x TO g`; destination: the rest), so *`TO` and `FROM` outside Triggers* picks which keeps it.
2. **The comma, and the shape of a header** (points 2 and 3). Core = head keyword + required item + its complements (no comma: `FAILED WITH r`, `SHIFT m BY n`, `CHANGE f TO f2`; the kind word is core). Clause = optional part applying to the whole, always `, KEYWORD …` (`WHEN e, FROM DIRECTOR:`). Lists use `,` too; the token after `,` tells which, so no list item starts with a Clause keyword. Clauses in any order, at most once unless the chapter allows more; tools write the chapter's order. A `,` never ends a logical line and never joins Statements.
3. **Condition words.** Follow the subject when it's written (`?x PLAYS R`, `P RUNNING`, kind words); come first when the subject is implicit (`PURSUING g`, `IN phase`). `NOT` is an operator.
4. **Keywords.** UPPERCASE, case-sensitive, all reserved; a name spelled exactly like a keyword is `R0110`. Reuse a keyword only if the new use passes rule 1, else a new plain English word.
5. **Dropping syntax.** Only when nobody writes it by hand, a generator gains nothing, and the Visual Editor doesn't need it. Two spellings become one, except explicit layout (`.`, `;`). Retired spellings are errors with a hint.

**The lighter overloads (map fog), resolved without tickets:** `ELSE` after `GIVEN` and `IF` ("otherwise", same header job) passes; `PLOT` and `PARENT` pass as nouns; `:` in doc comments is comment text; `"…"`, `( )` and `-` keep their programming meanings.

Also fixed in chapter 01: the stale examples of inventory §4.1 (`FORGET(…)`, `DO PRINT`, the comma-joined continuation example, replaced with a wrapped Trigger in the new `, FROM` spelling). Left for later: consolidating the per-chapter *Reserved words* lists into chapter 01 (added to *Spec examples after the review*).
