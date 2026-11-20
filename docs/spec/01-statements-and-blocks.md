# Statements and blocks

How Regia source is split into Statements and Blocks. Decided in the ticket *Statement and block syntax* (`.scratch/regia-2/issues/01-statement-and-block-syntax.md`). This chapter replaces the syntax part of primer ch.1. `PASS` was added in the ticket *Words that do several jobs, and syntax nobody used* (`.scratch/regia-revision/issues/20-words-and-syntax.md`), which also added Flat blocks; the ticket *`.`, `;` and the Block styles* (`.scratch/syntax-review/issues/03-dot-semicolon-blocks.md`) removed them and set the two styles below. Comments are covered in *Comments* (`02-comments.md`). The principles every construct follows (*The principles of the syntax*, below) were set in the ticket *The principles of the 1.5 syntax* (`.scratch/syntax-review/issues/01-principles.md`, ADR 0041).

## Two styles

There are two ways to structure code, and they can be mixed freely:

- **Indentation style** (the default): one line is one Statement. A line ending in `:` is a Block header, and its body is the lines indented under it.
- **Explicit style**: the same layout written on one line. A body starting on its header's line after `:` stands for an indent, `.` stands for a new line, and `;` stands for a dedent. This lets you put several Statements, or a whole Block, on one line.

The three marks are the one-line spellings of indent, new line and dedent, and nothing more: the explicit style never spans lines. A Block whose body is on later lines is always indented under its header.

**Indentation is the default**, for code written by hand and for code a tool generates: one Statement per line, Blocks by indentation, no trailing `.`. The Visual Editor and any formatter write this style. The explicit marks are never required. They are there for code that has to fit on one line (a short Inline block, `IF x: DO a; ELSE: DO b`, or a generator that emits single lines), and for writers who prefer not to indent, as a matter of style: such a writer puts each Block on one line.

```regia
PLAYBOOK NobleSocializing:

    WHEN insult_heard:
        IF NOT is_drunk AND hates(host):
            DO complain
            SIGNAL insult_thrown
        ELSE:
            DO toast(host)

    WHEN digestion_check:
        IF is_hungry: DO eat_food. FORGET is_hungry. PRINT("A guest finishes their meal.")

    WHEN food_served:
        PRINT("A guest notices food arriving.")
        IF is_hungry: DO eat_food; ELSE: DO complain
```

## Block headers

Every Block header ends with `:`, without exceptions. `PLOT` is included, and everything inside a Plot is indented under its header:

```regia
PLOT RoyalBanquet:
    PHASE reception INITIAL
    ROLE Host
```

A line that doesn't end in `:` (or open an Inline block, see below) never opens a Block.

## Where a Block's body starts decides its style

- **Body on the next line, indented further**: an indentation Block. It ends at the first line indented less than its body or as much as its header.
- **Body on the same line as the `:`**: an **Inline block**. Its Statements are separated by `.`, and it ends at a `;` or at the end of the line, whichever comes first. An Inline block never spans several lines.
- **Header ending its line, with no line indented further after it**: an empty Block (below, *Empty Blocks*). The next line, at the header's indentation or less, is not inside it.

Consequences:

| Source | Meaning |
|---|---|
| `IF is_hungry: DO eat_food` | Inline block, closed by the end of the line. No `;` needed. |
| `IF x: DO a; ELSE: DO b` | On one line, the `;` before `ELSE` is required. |
| `IF x: DO a` then `ELSE: DO b` on the next line | No `;` needed. IF/ELSE has no special case. |
| `IF x: DO a; DO b` | After `;`, the line goes back to the enclosing Block. `DO b` runs whether or not `x` holds. |
| `DO a. DO b` inside an indentation Block | Two Statements on one line. |
| `IF a: IF b: DO c;; DO d` | Nested Inline blocks. Each `;` closes one Block. |

A whole program on one line (as in primer ch.1) is valid. Any trailing `;` at the end of the line can be left out.

Styles mix freely. Here a Trigger's body is indented, its first `GIVEN` is an Inline block, and its second holds two Statements on one line:

```regia
WHEN hit, FROM opponent, SHIFTS aggressiveness BY 0.1:
    GIVEN stamina(?now) AND ?now > 1: UPDATE stamina(?now) TO stamina(?now - 1)
    GIVEN stamina(?now):
        FORGET stamina(?now). DO drop_sword
        TELL opponent yielded
```

The same Plan written by someone who doesn't indent goes on one line:

```regia
WHEN hit, FROM opponent: GIVEN stamina(?now): FORGET stamina(?now). DO drop_sword. TELL opponent yielded
```

### No Block without indentation across lines

A `;` closes only an Inline block. Taking the indentation out of a multi-line Block doesn't make it an explicit Block:

```regia
WHEN hit, FROM opponent:          # an empty Block: the next line isn't indented further
GIVEN stamina(?now):              # a sibling of the WHEN, not its body
...
;                                 # error R0108: no Inline block is open
```

Earlier drafts had **Flat blocks**, closed by `;` across lines. They were removed: a Block header whose body was forgotten swallowed the rest of the file, and a generator gets the same result from indentation or from Inline blocks. A `;` that would have closed one is `R0108`, and its hint says so.

### Headers inside an Inline block

**Error:** a Block header that ends a line must not sit inside an Inline block:

```regia
PLAYBOOK P: WHEN e:      # the PLAYBOOK's Inline block ends here, at the end of the line
    DO a                 # error: no valid parent for this indented body
```

Hint: put `WHEN e:` on its own line, indented under `PLAYBOOK P:`.

## When `.` ends a Statement

A `.` ends a Statement only when it is followed by a space, the end of the line, `;`, or `#` (a comment). Anywhere else it belongs to a dotted name (`engine.security.summon_guards`) or a number (`0.5`).

So `DO complain.SIGNAL insult_thrown` reads as one dotted name and is an error; write `DO complain. SIGNAL insult_thrown`. When a dotted name contains a keyword, the Transpiler hints at the likely mistake ("did you mean `. SIGNAL`?").

## Redundant terminators

A `.` at the end of a line, or a `;` closing an Inline block right at the end of a line, does nothing and is allowed without a warning. The Visual Editor and formatters never write either. A `;` at the end of a line that isn't inside an Inline block is not redundant: it closes nothing, and is an error (`R0108`). This keeps most pasted 1.0 code parsing. The Visual Editor keeps it when it writes edits back: it never normalises text an edit doesn't touch (chapter 22, `22-bidirectional-editing.md`).

## Indentation rules

- Tabs or spaces, at any width, but consistent within a file. Mixing tabs and spaces for indentation in one file is an error.
- Dedenting to a level that was never opened is an error ("this line is indented less than the Block it's in, but more than the one outside").
- Blank lines and comment-only lines don't count for indentation.

## Continuation lines

A physical line continues onto the next one, forming one logical line, when:

- it ends with `,`: a `,` always says that something more follows (*Clauses and the comma*, below), so it never ends a logical line; or
- it has a `(` that isn't closed yet.

Continuation lines must be indented further than the logical line's first line. Physical lines are joined into logical lines before any of the rules above apply, so an Inline block can continue this way too.

```regia
WHEN hates(?h) LEARNED, FROM ?teller,
        SUITS sympathy AT -0.5, bravery AT 0.8,
        SHIFTS aggressiveness BY 0.2:
    ...
```

A `,` never joins two Statements: Statements are separated by a new line or by `.`.

## Parsing never depends on declarations

Every construct can be parsed from its tokens alone, without knowing what any name is declared as or in which file. Keywords carry the shape (`DO`, `LEARN`, `PURSUE`, …), and names are only names. This is what lets each file be parsed on its own and its imports be found before any name is resolved (chapter 23). A syntax that would need to know a name's kind to be parsed is rejected.

## The principles of the syntax

Every construct in the spec follows these rules, and a new construct is judged by them. They were set by the syntax review (ADR 0041).

### One meaning per word

A keyword or symbol may appear in several constructs only if a reader who knows one use can predict the others:

- **One sense.** A single one-line gloss covers every use ("`FROM` introduces where something comes from or leaves": the Sender in `, FROM Guest ?who`, the holders in `REMOVE P FROM Guest ?who`). Two glosses mean two meanings, even if English allows both: `TO` before a Goal (`TO g:`, `ASK x TO g`) and `TO` before a destination are two words.
- **The exceptions** are closed, and no other construct may cite them as a precedent:
  - `TO` as a destination in `ASSIGN P TO Role` and `UPDATE f TO f2`. Everywhere else `TO` introduces a Goal. The two Statements keep the English idiom ("assign X to Y", "update X to Y") because no other word reads as well (ADR 0043).
  - `BY` as an amount in `SHIFT m BY n` and the Label `SHIFTS m BY n` (chapter 14). Everywhere else `BY` names who did it: `WHEN EXITED, BY PARENT:` (chapter 20), and in 2.0 whose Pursuit ended (`, BY waiter ?s`, chapter 05). "Shift by 0.1" is the idiom, and nothing else read as well (ADR 0044).
  - `RANDOMLY` in two jobs: the head of a Random choice (`RANDOMLY:`, chapter 09) and the Pick clause `, RANDOMLY` (chapter 26). The sense is the same, "chosen by chance", among Options or among Matches (ADR 0044).
- **One job.** The word does the same structural job in every use: always the head keyword of a construct, always a connector that introduces a complement, or always an operator. What it introduces may be of different kinds: a Role, a Phase and a Fact can all be "where something ends up".
- **A noun naming a kind of thing** passes on its sense alone, when every use refers to that kind of thing, whether it heads a declaration or names one (`PLOT Dinner:`, `DURING PLOT:`, `END PLOT`; `PARENT`).
- **Fixed phrases** (`ELSE IF`, `WITHOUT WAITING`) get no exemption: each word in them still fits its own gloss. That is why the idiom `AT RANDOM` was retired: `AT` introduces a level (`SUITS p AT n`).
- **A symbol that keeps its usual programming meaning** passes even with several jobs: `( )` for calls, grouping and arguments, `"…"` for any string literal (a String or an `IMPORT` path), `-` for minus and a number's sign. The test applies to the symbols Regia gives meanings of its own: `,`, `.`, `:`, `;`, `=`, `%`. `%` is the everyday percent sign, written only before `OF` (`50% OF Guest`, chapter 15), and never the programmer's remainder (ADR 0045). Text inside a comment (the `:` of a doc comment) isn't code and isn't tested.

### Clauses and the comma

A Block header or a Statement has a **core** and, after it, optional **clauses**:

- The **core** is the head keyword, the item it requires, and that item's **complements**. A complement finishes a single word and is never preceded by `,`: `FAILED WITH r`, `SHIFT m BY n`, `UPDATE f TO f2`. The kind word after a Trigger's item is part of the core.
- A **clause** is an optional part that applies to the whole header or Statement. It is always written **`, KEYWORD …`**: `WHEN e, FROM DIRECTOR:`, `, SUITS …`, `, RANDOMLY`, `PURSUE g, WITHOUT WAITING`, `WAIT d, UNTIL c`, `, MAPPING …`.
- A **list** separates its items with `,` too: arguments, a Multi-definition, `EXCEPT ?a, ?b`, `LIKE a, b`. A list ends at the first token that can't be one of its items: a clause keyword after a `,`, or the next word of the core (`MAPPING Guest EXCEPT ?a, ?b AS Spectator`).
- So **`,` means "something more follows"**: either a clause or the next item of a list. The token after the `,` tells which: a clause keyword starts a clause, anything else is the next item. No list item may start with a clause keyword.
- **Clauses come in any order.** Each appears at most once unless its chapter allows several (Labels). The Visual Editor and any formatter write them in the order their chapter lists them.
- **A clause keyword without its `,`** after the core is an error, `R0111`, whose hint adds the `,`: `WHEN e FROM DIRECTOR:` is `WHEN e, FROM DIRECTOR:`. The same word may introduce the required item itself, as part of the core: `WAIT UNTIL c` (the condition is what `WAIT` waits for) next to `WAIT d, UNTIL c` (a limit added to a Duration).
- **A `,` never joins conditions.** Two conditions that must both hold are joined with `AND`: `GIVEN gold(?g) AND price(?item, ?p):`. Alternatives, either of which may hold, are joined with `OR`, also in `FROM a OR b` (chapter 05).
- **`AND` and `OR` are only the condition operators.** They never join the items of a list: the Propensities of a Label (`SUITS sympathy AT -0.5, bravery AT 0.8`), the Moods of a `SHIFT`, the Roles after `PLAYS` (`PLAYS Guest, Drunkard`). `OR` is never a Block header: a Random choice is `RANDOMLY:` with `OPTION:` Blocks (chapter 09).

### Where condition words go

A condition word **follows its subject** when the subject is written: `?x PLAYS Role`, `P(args) RUNNING`, a Trigger's item before its kind word. When the subject is implicit, the Agent itself or the running Plot, the word **comes first**: `PURSUING g` ("I am pursuing g"), `IN phase` ("this Plot is in phase"). `NOT` is an operator, not a condition word.

The word after a written subject is what tells a condition item apart from a Fact, so a condition parses without knowing what its names are (*Parsing never depends on declarations*, above): `Poisoning RUNNING` is a Subplot condition and `is_hungry` a Fact. A condition word binds to its subject more tightly than `NOT`: `NOT ?x PLAYS Guard` is `NOT (?x PLAYS Guard)` (chapter 06, *Conditions*).

### Keywords

- **Keywords are UPPERCASE, and case matters for them.** An all-caps word that is a keyword is always the keyword. `count` or `Wait` is an ordinary name.
- **Every keyword is reserved.** A name spelled exactly like a keyword is an error (`R0110`). Names still compare ignoring case among themselves (chapter 10). The keywords are listed in one place, *Reserved words* (below).
- **A keyword is reused only if the new use passes *One meaning per word*.** Otherwise the new use gets a new word, even though the vocabulary grows. A plain English word is preferred to an invented compound.

### What syntax can be dropped

A spelling is removed only when **all** of these hold: nobody writes it by hand, a generator gains nothing from it, and the Visual Editor doesn't need it. Two spellings of one thing become one. The exception is an explicit spelling of layout (`.` for a new line, `;` for a dedent), which stays because generated code uses it. A retired spelling becomes an error with a hint that names the new one, not a silent synonym (as `EVENT` became `CUE`, `R0513`):

- **The error lives in the chapter that owns the construct**, numbered like any other check of that chapter (chapter 27). *Retired spellings* (below) lists them all in one place.
- **It stays for ever.** Its code is never marked retired, and its hint keeps naming the new spelling. Regia is generated as well as written, and a generator that learned from older text can produce an old spelling long after writers have stopped.
- **A retired keyword stays reserved** for the same reason: the parser needs to recognise the old form so it can name the new one. Only the exact all-caps spelling is blocked as a name (`Change` and `change` are free), and the word is listed under *Reserved words*.
- **Only a spelling that was once in this spec gets an error.** Words of Regia 1.0, of earlier drafts and of the primer get none and aren't reserved: 1.0 is a different language, and this spec is the only text a writer or a generator was told to follow.

## Empty Blocks

A Block header with no body is allowed, and the Transpiler warns about it: the Block may not be written yet. An empty Block is a header followed by a dedent or the end of the file, or an Inline block with nothing in it (`: ;`).

**`PASS`** is a Statement that does nothing. It goes anywhere a Statement goes, on its own line or inline, and says that the emptiness is meant, so a Block holding only `PASS` gets no warning: a Plan that deliberately ignores its Trigger, or an Option of a Random choice that means "otherwise nothing" (chapter 09). The Visual Editor writes `PASS` in the Blocks it creates empty. There is no keyword for "not written yet": that is a bare empty Block, which warns, or a comment.

Every empty Block follows this one rule, an Option of a Random choice included.

## Reserved words

Every keyword of the language, in one list. All of them are reserved (*Keywords*, above), and a chapter that uses one points here. A word is listed once, under its first family; the chapter in brackets is the one that specifies it.

- **Structure:** `IMPORT`, `AS` (10, and `MAPPING … AS`, 15), `PLAYBOOK`, `PLOT`, `ROLE`, `CAST` (15), `PHASE`, `INITIAL`, `DURING` (16, 20), `PRECEDENCE`, `OVER`, `TIES`, `ON`, `SELF`, `PARENT` (13; `PARENT` also in `EXITED, BY PARENT`, 20).
- **Vocabulary:** `FACT`, `CUE`, `GOAL`, `ACTION` (05), `NAME` (03), `GAME` (10, and `FROM GAME`, 05), `TRAIT`, `MOOD` (14).
- **Plan headers:** `WHEN`, `TO` (05; also the two closed exceptions `ASSIGN … TO` and `UPDATE … TO`), `AFTER` (12), `GIVEN`, `ELSE` (06).
- **Trigger kind words:** `LEARNED`, `FORGOTTEN`, `REACHED`, `DROPPED`, `FAILED`, `ENDED` (05, 11), `FINISHED` (17), `ENTERED`, `EXITED` (20), `ASSIGNED`, `REMOVED` (15), `JOINED`, `LEFT`, `EMPTIED` (19). Reserved for later and not yet usable (`R0706`): `TOLD`, `AGREED`, `REFUSED` (07).
- **Clauses and complements:** `FROM`, `BY` (05; `BY` also the amount of `SHIFT`, 14), `WITH` (11, 17), `WITHOUT`, `WAITING` (08), `UNTIL` (12, and `UNTIL EXITED`, 15), `SUITS`, `SHIFTS`, `AT` (14), `WEIGHT` (09, 26), `HIGHEST`, `LOWEST` (26), `MAPPING`, `EXCEPT`, `OF` (15), `ALL` (18).
- **Values and units:** `ME` (03), `DIRECTOR` (05), `EVERYONE` (07), `SECOND`, `SECONDS`, `MINUTE`, `MINUTES` (12), `RANDOM` (04, only the function `RANDOM(a, b)`), `COUNT` (26, and the Instancing line `COUNT n`, 21).
- **Conditions:** `NOT`, `AND`, `OR` (06; `OR` also in `FROM a OR b`, 05), `PURSUING` (06), `IN` (20), `RUNNING` (17), `PLAYS` (15, and Instancing, 21), `SENT` (18).
- **Agent Statements:** `DO`, `LEARN`, `FORGET`, `UPDATE`, `PURSUE`, `DROP`, `PRINT`, `WAIT` (08), `TELL`, `ASK`, `SIGNAL` (07), `FAIL` (11), `SHIFT` (14), `LET`, `BE` (04), `PASS` (this chapter). Reserved for later (`R0706`): `REFUSE` (07).
- **Control flow:** `IF` (06), `RANDOMLY`, `OPTION` (09; `RANDOMLY` also the Pick `, RANDOMLY`, 26), `FOR`, `EACH` (26).
- **Director Statements:** `ASSIGN`, `REMOVE` (15), `START`, `SUBPLOT`, `END` (17), `ENTER` (20).
- **Instancing (`.regin`, chapter 21):** `ROOT`, `KIND`, `AGENT`, `LIKE`, `NO`, `SEED`, `TARGET`.
- **Retired keywords**, reserved for ever so their error can name the new spelling (*What syntax can be dropped*, above): `EVENT` (`R0513`, 05), `CHANGE` (`R0808`, 08), `EITHER` (`R0906`, 09), `UNASSIGN`, `UNASSIGNED` (`R1515`, 15), `PERCENT` (`R1516`, 15), `STARTS` (`R1608`, 16), `OUTCOME` (`R1715`, 17), `TRANSITION` (`R2016`, 20).

`BELIEVE`, `ACHIEVE`, `PRIORITY`, `TEMPER`, `EFFECTS`, `ENDS`, `WORLD` and `GROUP` from Regia 1.0, earlier drafts and the primer are not words of the language and are not reserved.

## Retired spellings

Every spelling this spec once had and has since replaced, with the error that names the new one. Each error is specified in the chapter in brackets, and none of them is ever retired (*What syntax can be dropped*, above).

| Retired spelling | Write instead | Code |
|---|---|---|
| `EVENT e` | `CUE e` | `R0513` (05) |
| `?x = e` as a Statement | `LET ?x BE e` | `R0407` (04) |
| `CHANGE f TO f2` | `UPDATE f TO f2` | `R0808` (08) |
| `EITHER:` … `OR:` | `RANDOMLY:` with `OPTION:` Blocks | `R0906` (09) |
| `SUITS a AT x AND b AT y`, `SHIFT m AND n …` | `,` between the items | `R1412` (14) |
| `MAPPING a TO b` | `MAPPING a AS b` | `R1514` (15) |
| `UNASSIGN`, `UNASSIGNED` | `REMOVE`, `REMOVED` | `R1515` (15) |
| `n PERCENT OF Role` | `n% OF Role` | `R1516` (15) |
| `ROLE r STARTS WITH:`, `CAST STARTS WITH:` | `ROLE r:`, `CAST:` | `R1608` (16) |
| `ENDED WITH e`, `ENDED WITHOUT OUTCOME` | `FINISHED WITH e`, `FINISHED` | `R1715` (17) |
| `END SUBPLOT P` | `DROP SUBPLOT P` | `R1717` (17) |
| `TRANSITION TO p` | `ENTER p` | `R2016` (20) |
| `key = value` in `.regin` | `key value` | `R2124` (21) |
| `PLAYS a AND b` | `PLAYS a, b` | `R2125` (21) |
| `, AT RANDOM` | `, RANDOMLY` | `R2606` (26) |

A clause keyword written without its `,` (`WHEN e FROM DIRECTOR:`) is reported as `R0111` (this chapter). It isn't listed above, because it is a missing comma rather than an old word. Flat blocks were removed outright: `R0107` is retired, and a stray `;` is `R0108`.

## A word of Regia 2.0 in a 1.5 build

A Transpiler built for Regia 1.5 (ADR 0025) still parses every construct of 2.0. If a Program uses one from a system that 1.5 leaves out, the build reports **`R0109`**. The error names the construct and says it is Regia 2.0, so a writer doesn't get a parse error for it. The constructs are:

- `FROM GAME`, `FROM ME`, and `FROM` with `OR` alternatives (chapter 05);
- `BY` on a Goal's ending (chapter 05), and a Goal's ending in a Plot, with or without `BY` (chapter 20): in 1.5 nobody hears how a Goal it asked ended;
- a quantity after `FROM` or `BY` (`FROM ALL Guest`, `BY 2 OF waiter`), which makes a Quota Trigger, and `SENT` (chapter 18);
- `JOINED` (chapter 19).

`WHEN EXITED, BY PARENT:` (chapter 20) and the `BY` of `SHIFT` and `SHIFTS` (chapter 14) are not a Goal's ending, and are in 1.5.

A construct reported with `R0109` gets no other Diagnostic: the checks of its own chapter aren't run on it. A 2.0 build never reports `R0109`. The code is retired there, and keeps its number. A Program that builds in 1.5 builds in 2.0 and does the same thing there.

## Transpiler checks

**Errors**

- `R0101` A Block header ending a line inside an Inline block, whose indented body has no valid parent (hint: put the header on its own line).
- `R0102` A dotted name that contains a keyword, such as `complain.SIGNAL` (hint: `. SIGNAL`).
- `R0103` Tabs and spaces mixed for indentation in one file.
- `R0104` A line dedented to a level that was never opened.
- `R0105` A continuation line not indented further than the first line of its logical line.
- `R0107` Retired with Flat blocks; the number is not reused.
- `R0108` A `;` that closes no Inline block (hint: a Block's body on later lines is indented under its header; Flat blocks closed by `;` no longer exist).
- `R0109` A construct of a system Regia 1.5 leaves out, in a 1.5 build (the message names it and says it is Regia 2.0). Reported by a 1.5 build only; retired in 2.0.
- `R0110` A name spelled exactly like a keyword (the message says the word is a keyword; hint: change its case or its spelling).
- `R0111` A clause keyword after the core of a header or Statement with no `,` before it, such as `WHEN e FROM DIRECTOR:` (the message names the clause; hint: `WHEN e, FROM DIRECTOR:`).

**Warnings**

- `R0106` A Block header with no body. A Block holding only `PASS` has a body.

## Regia 1.5

All of this chapter is in 1.5 (ADR 0025). `R0109` is reported by a 1.5 build only, and is retired in 2.0 (*A word of Regia 2.0 in a 1.5 build*, above).

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`). `R0111` was added in the ticket *The comma* (`.scratch/syntax-review/issues/02-the-comma.md`) and is in 1.5. Flat blocks and `R0107` were removed in the ticket *`.`, `;` and the Block styles* (`.scratch/syntax-review/issues/03-dot-semicolon-blocks.md`). *Retired spellings*, and the rules that retired spellings keep their error for ever, that retired keywords stay reserved, and that only this spec's own spellings get an error, were decided in the ticket *Retired spellings and their codes* (`.scratch/syntax-review/issues/13-retired-spellings.md`).
