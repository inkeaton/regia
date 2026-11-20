# The Regia syntax on 2026-11-19

What the spec (chapters 01–21 and 26) says about symbols and keywords when the map *Regia 1.5 syntax review* was charted. It's a snapshot: tickets change the spec, not this file.

## 1. Symbols

| Symbol | Meanings | Count |
|---|---|---|
| `:` | (a) ends a Block header; text after it opens an Inline block. (b) separates the key from the value in a doc comment, `#@key: value` | 2 |
| `.` | (a) ends a Statement, optional at the end of a line. (b) decimal point, `0.5`. (c) joins the parts of an External name, `engine.security.summon_guards`. The next character decides which | 3 |
| `;` | closes the innermost Inline or Flat block | 1 |
| `,` | (a) at the end of a line, the line continues. (b) separates arguments: `f(a, b)`, `PRINT(…)`, `RANDOM(a, b)`. (c) separates items in a Multi-definition, `FACT a, b`. (d) starts a trailing clause: the Labels `, SUITS` and `, SHIFTS`, `, WEIGHT`, `, WITHOUT WAITING`, `, MAPPING`, `, UNTIL EXITED`, `, UNTIL` (in `WAIT`), and the Picks `, AT RANDOM`, `, HIGHEST`, `, LOWEST`. (e) separates list items after `EXCEPT ?a, ?b`, `LIKE a, b` and `#@allow: R1, R2`. (f) opens an inline Context, `WHEN x, GIVEN …:` (used, not specified) | 6+ |
| `?` | `?name` is a Placeholder, a bare `?` is a "don't care", `?_name` is a "don't care" with a name for the reader | 1 family |
| `=` | (a) equality in a condition. (b) naming a value in a Body, `?x = expr`. (c) a Target setting in `.regin`, `key = value` | 3 |
| `< > <= >=` | comparison | 1 |
| `+ - * /` | arithmetic. `-` directly before a digit is also the sign of a literal | 1 |
| `( )` | (a) parameters and arguments. (b) grouping. (c) the argument list of `RANDOM`, `COUNT` and `PRINT`. An unclosed `(` also continues the line | 3 |
| `#` | `#` comment, `#[ … ]#` nested comment, `#@key` / `#@key[ … ]#` doc comment | 1 family |
| `"…"` | a String value, and the path of an `IMPORT` | 2 |
| `%` | unused since `#%` was retired | 0 |

Layout: indentation opens Blocks. The three Block styles (indented, Inline, Flat closed by `;`) are told apart by where the body starts. `PASS` fills a Block that is meant to be empty.

## 2. Keywords by family

- **Vocabulary:** `FACT`, `CUE`, `GOAL`, `ACTION`, `NAME`, `TRAIT`, `MOOD`, with the modifiers `GAME` and `<ext> AS <name>`.
- **Structure:** `IMPORT`, `PLAYBOOK`, `PLOT`, `ROLE`, `PHASE … INITIAL`, `DURING <phase>:`, `DURING PLOT:`, `PRECEDENCE:` (`OVER`, `TIES`, `ON`, `SELF`, `PARENT`), and `ROLE X STARTS WITH:` / `CAST STARTS WITH:`.
- **Plan headers:**
  - `WHEN <item> [kind word] [WITH r] [FROM … | BY …] [, Labels]:`
  - `TO g:`, `AFTER <Duration>:`
  - `GIVEN cond[, Picks][, SHIFTS]:`, `ELSE:`
- **Kind words:**
  - Facts: `LEARNED`, `FORGOTTEN`.
  - Goals: `REACHED`, `DROPPED`, `FAILED`, `ENDED`.
  - Subplots: `ENDED [WITH e | WITHOUT OUTCOME]`, `DROPPED`.
  - No item: `ENTERED`, `EXITED [BY PARENT]`, `ASSIGNED`, `UNASSIGNED`.
  - With a Role: `LEFT`, `EMPTIED`; `JOINED` (2.0).
  - Reserved and unused: `TOLD`, `AGREED`, `REFUSED`, `REFUSE`.
- **Senders:** `FROM Role | ?who | Role ?who | DIRECTOR`. 2.0 adds `GAME`, `ME`, `a OR b`, `BY …` and the Quotas `ALL`, `n OF`, `n PERCENT OF`.
- **Conditions:** `NOT`, `AND`, `OR`, comparisons, `PURSUING g`, `?x PLAYS Role`, `P(args) RUNNING`, `IN <phase>`, `COUNT(…)`. `?x SENT e` is 2.0.
- **Agent Statements:**
  - `DO` (Custom Actions only).
  - `LEARN`, `FORGET`, `CHANGE … TO`.
  - `PURSUE [, WITHOUT WAITING]`, `DROP`.
  - `TELL`, `ASK … TO`, `SIGNAL`.
  - `PRINT(…)`, `WAIT d [, UNTIL c]` / `WAIT UNTIL c`.
  - `FAIL [WITH r]`, `SHIFT m BY n`, `PASS`.
- **Control flow:** `IF` / `ELSE IF` / `ELSE`, `EITHER` / `OR [, WEIGHT e]`, `FOR EACH`, `?x = expr`.
- **Director Statements:**
  - `ASSIGN P TO …`, `UNASSIGN P FROM …`.
  - `START SUBPLOT P(args)`, `END SUBPLOT`, `END PLOT [WITH e]`.
  - `TRANSITION TO p`.
  - The clauses `, MAPPING a TO b` and `, UNTIL EXITED`, plus `EXCEPT` and `CAST`.
- **Recipients:** `?who`, `Role`, `n OF Role`, `n PERCENT OF Role`, `EVERYONE`, `CAST`, `Role EXCEPT …`.
- **Values and Expressions:** `ME`, `RANDOM(a, b)`, `COUNT(…)`, and the units `SECOND(S)`, `MINUTE(S)`, `PERCENT`.
- **Picks:** `, AT RANDOM`, `, HIGHEST ?p`, `, LOWEST ?p`, `, WEIGHT e`.
- **Instancing (`.regin`):** `ROOT`, `KIND`, `AGENT`, `LIKE`, `PLAYS … AND …`, `COUNT n`, `<prop> AT v`, `NO KIND` / `NO AGENT`, `SEED`, `TARGET x:` with `key = value`.

## 3. Words with more than one meaning

| Word | Meanings |
|---|---|
| `TO` | `TO g:` (recipe), `ASK x TO g`, `ASSIGN P TO Role`, `MAPPING a TO b`, `TRANSITION TO p`, `CHANGE f TO f2` |
| `OR` | boolean or, the Random-choice header `OR:`, the sender alternatives `FROM a OR b` (2.0) |
| `AND` | boolean and, the list joiner in a Label (`SUITS a AT x AND b AT y`), the list joiner in `SHIFT`, the Roles list in `KIND … PLAYS A AND B` |
| `BY` | who pursued a Goal (2.0), the amount in `SHIFT` / `SHIFTS`, `EXITED BY PARENT` |
| `WITH` / `WITHOUT` | a Reason (`FAIL WITH`, `FAILED WITH`), an Outcome (`END PLOT WITH`, `ENDED WITH`), a setup (`STARTS WITH:`), `WITHOUT OUTCOME`, `WITHOUT WAITING` |
| `AT` | the target in `SUITS p AT n`, the Pick `AT RANDOM`, the value in Instancing `bravery AT 0.3` |
| `RANDOM` | the function `RANDOM(a, b)`, the Pick `AT RANDOM` |
| `COUNT` | the Expression `COUNT(cond)`, the Instancing line `COUNT 2.` |
| `FROM` | the Sender on a Trigger, the target of `UNASSIGN P FROM Role` (including `FROM Role ?who`, which only looks like the Sender form) |
| `UNTIL` | `WAIT … UNTIL cond`, the clause `UNTIL EXITED` |
| `DROPPED` / `ENDED` | Goal endings and Subplot endings. `WITH` goes on `FAILED` for Goals and on `ENDED` for Subplots |
| `ELSE` | the fallback Plan after `GIVEN`, the branch after `IF` |
| `LEARN` / `PURSUE` | the Agent's own Action in a Body, and the Director's tell or ask in `STARTS WITH:` and Instancing |
| `ROLE` | a played Role in a Plot, an address in a Playbook, and a reference that declares nothing inside `DURING` |
| `PARENT` | a precedence operand, and `EXITED BY PARENT` |
| `PLOT` | the declaration, `DURING PLOT`, `END PLOT` |

Condition words sit in different positions:
- prefix: `PURSUING g`, `IN phase`, `NOT`;
- postfix: `P RUNNING`, and the kind words after their item;
- infix: `?x PLAYS R`, `?x SENT e`.

## 4. Spec examples that contradict the spec

1. **Chapter 01's examples are out of date.** `FORGET(is_hungry)`, `DO PRINT(…)` (`R0803`), and the continuation example `DO eat_food, FORGET(…), PRINT(…)`, whose commas would read as trailing clauses.
2. **The inline Context `WHEN x, GIVEN cond:` is never specified.** It is used at `03-parameters-and-placeholders.md:60` and `15-roles-and-mappings.md:301,320,328,330`.
3. **A comma is used as AND in a Context:** `GIVEN gold(?g), price(?item, ?p):` at `11-failure.md:61`.
4. **A setup that breaks chapter 16's rules:** `Challenger STARTS WITH: TELL grievance(?quarrel)` at `17-subplots.md:31`. It has no `ROLE`, uses `TELL`, and uses a Placeholder.
5. **A Statement after a `GIVEN` Block** (`R0603`) at `18-quota-triggers.md:105`.
