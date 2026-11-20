# Syntax

A Guest is told to take its seat. It walks to the place laid for it, sits down and greets the Host, and if no place was laid it does none of this. To write that down we have to show where one step ends and which steps belong together under "if a seat was laid". Regia does both with the layout of the text: a line is a step, and indentation groups the steps. This chapter is about that layout, the two marks that put it on one line, comments, and the words the language keeps for itself.

| We write | It means |
|---|---|
| a new line | a new Statement |
| `:` at the end of a line, then lines indented under it | a Block header and its body |
| `:` with the body on the same line | an Inline block |
| `.` followed by a space | a new Statement, on the same line |
| `;` | the end of an Inline block, on the same line |
| `#`, `#[ … ]#` | a comment, for people only |
| `#@key: …`, `#@key[ … ]#` | a Doc comment, for the declaration below it |

What the names on a line stand for is in *Vocabulary and files*.

## Statements and Blocks

[`playbooks/courtesy.regia`](../showcase/playbooks/courtesy.regia)
```regia
PLAYBOOK Courtesy:
    ROLE host

    CUE greeting                             # only holders of Courtesy say it, and hear it

    TO take_seat, FROM DIRECTOR:
        GIVEN seat(?place):
            DO walk_to(?place)               # waits until we have arrived
            DO sit_down
            TELL host greeting
        # no ELSE: with no seat laid for us, take_seat fails at once
```

One line is one Statement or one declaration. A line that ends in `:` is a Block header, and the lines indented under it are its body. Three Blocks sit inside each other here: the Playbook, the Plan, and the `GIVEN`. The `GIVEN`'s body ends at `# no ELSE…`, which is indented less than `DO sit_down`, and the Plan's ends with the file.

- Every Block header ends in `:`, with no exceptions: `PLAYBOOK`, `PLOT`, a Trigger, `GIVEN`, `IF`, `ELSE`, `ROLE` with a setup, `RANDOMLY`, `OPTION`. A line that doesn't end in `:` never opens a Block. `ROLE host` declares a Role and nothing more.
- A body ends at the first line indented as much as its header, or less.
- We indent with tabs or with spaces, at any width, but never with both in one file.
- Coming back to a depth that no open Block has is an error.
- Blank lines, comment-only lines and the lines a multiline comment spans don't count for indentation.
- No line ends in `.` or `;`. A Statement ends with its line.

This is the default style, for code written by hand and for code a tool generates. The Visual Editor and any formatter write it, and nothing ever requires the marks of the next sections.

**Checks**

- Tabs and spaces mixed for indentation in one file → `R0103`
- A line dedented to a depth that was never opened → `R0104`

Spec: chapter 01.

## Inline blocks

[`playbooks/courtesy.regia`](../showcase/playbooks/courtesy.regia)
```regia
WHEN take_seat ENDED: SIGNAL took_seat   # seated or standing, the Director counts us
```

[`playbooks/noble_socializing.regia`](../showcase/playbooks/noble_socializing.regia)
```regia
RANDOMLY:
    OPTION, WEIGHT 3: DO chat
    OPTION, WEIGHT 2:
        DO sip_wine
        IF RANDOM(1, 100) <= 30:     # one cup too many
            DO laugh
    OPTION, WEIGHT ?grudges: PURSUE vent
    OPTION, WEIGHT 5: PASS           # nothing, this time
```

When the body follows the `:` on the header's line, the Block is an Inline block. It ends at the end of the line, so `SIGNAL took_seat` is the whole of its Plan. Three of the four Options are Inline blocks, which lets the choice read as a list; the one with more to do is indented. The two styles mix freely, Block by Block.

Where the body starts decides the style:

| The header is followed by | The Block is |
|---|---|
| a line indented further | an indentation Block, ending at the first line indented as much as the header or less |
| more text on the same line | an Inline block, ending at a `;` or at the end of the line, whichever comes first |
| neither | an empty Block (*Empty Blocks*, below) |

An Inline block never spans lines. So a header that ends its line can't sit inside one, because its indented body would have no parent:

```regia
PLAYBOOK Hosting: TO open_feast, FROM DIRECTOR:
    DO stand_up              # error: the PLAYBOOK's Inline block ended with the line above
```

The fix is to put `TO open_feast, FROM DIRECTOR:` on its own line, indented under `PLAYBOOK Hosting:`.

**Checks**

- A Block header ending a line inside an Inline block → `R0101` (hint: put the header on its own line)

Spec: chapter 01.

## Several Statements on one line: `.`

Inside an Inline block, `.` followed by a space starts the next Statement. The `yielded` Plan of [`playbooks/duelling.regia`](../showcase/playbooks/duelling.regia), written on one line:

```regia
WHEN yielded, FROM opponent: DROP strike. DO salute. SIGNAL duel_won
```

All three Statements are in the Plan's body. A `.` works the same in an indentation Block: `DO stand_up. DO raise_cup` on one line of a body is two Statements of that body.

A `.` ends a Statement only when it is followed by a space, the end of the line, a `;` or a `#`. Anywhere else it belongs to a number or a dotted name:

[`vocabulary.regia`](../showcase/vocabulary.regia)
```regia
#@desc: The Target's own code, not the game's: done when that code returns.
ACTION hall.music.fanfare AS play_fanfare
```

[`banquet.regin`](../showcase/banquet.regin)
```regia
KIND knight, PLAYS Guest, Guard:
    COUNT 1
    bravery AT 0.8
```

`hall.music.fanfare` is one name, the game's, and `0.8` is one number. The space after a `.` is therefore part of the syntax: `DO stand_up.SIGNAL insult_thrown(?who)` reads as one Action named `stand_up.SIGNAL`, which is an error. The Transpiler sees the keyword inside the name and suggests the space.

A `.` at the end of a line does nothing and gets no warning, so `DO sit_down.` means `DO sit_down`. It is kept because older text and some generators write it. The Visual Editor never adds one, and never removes one from a line an edit doesn't touch.

**Checks**

- A dotted name that contains a keyword, such as `stand_up.SIGNAL` → `R0102` (hint: `. SIGNAL`)

Spec: chapter 01.

## Closing an Inline block: `;`

A `;` closes the innermost open Inline block, and the line goes on in the Block around it. With `.` and `;` a whole Plan fits on one line. The `hit` Plan of [`playbooks/duelling.regia`](../showcase/playbooks/duelling.regia):

```regia
WHEN hit, FROM opponent, SHIFTS aggressiveness BY 0.1: GIVEN stamina(?now) AND ?now > 1: UPDATE stamina(?now) TO stamina(?now - 1); GIVEN stamina(?now): FORGET stamina(?now). DO drop_sword. TELL opponent yielded
```

The `;` closes the first `GIVEN`, so the second `GIVEN` is back in the Plan's body, next to the first. Without it, the second `GIVEN` would be a Statement of the first. The `;` that would close the second `GIVEN` and the Plan is left out: the end of the line closes every open Inline block.

| We write | It means |
|---|---|
| `IF stamina(?): DO lunge` | An Inline block, closed by the end of the line. |
| `IF grudge(?who, ?size): UPDATE …; ELSE: LEARN grudge(?who, 1)` | On one line, the `;` before `ELSE` is needed. |
| `IF grudge(?who, ?size): UPDATE …` then `ELSE: LEARN …` on the next line | No `;` needed. `IF` and `ELSE` have no special case. |
| `IF stamina(?): DO lunge; TELL opponent hit` | After the `;` we are back outside. `TELL` runs whether or not the `IF` held. |
| `IF stamina(?now): IF ?now > 1: DO lunge;; TELL opponent hit` | Each `;` closes one Block. `TELL` is outside both `IF`s. |

A `;` closes only an Inline block. Taking the indentation out of a Block written over several lines doesn't make it a Block closed by `;`:

```regia
WHEN take_seat ENDED:          # an empty Block: the next line isn't indented further
SIGNAL took_seat               # a sibling of the WHEN, not its body
;                              # error: no Inline block is open
```

A `;` at the end of a line that closes an Inline block does nothing and is allowed, like a `.` there. One that closes nothing is an error, and its hint says that a body on later lines is indented under its header. Earlier drafts had Blocks closed by `;` across lines, and this is the error that catches them.

Indentation remains the way to write a Plan. One-line layout is for code that has to fit on a line, such as a short `IF … ; ELSE: …` or the output of a generator that emits single lines, and for writers who prefer not to indent: such a writer puts each Block on one line.

**Checks**

- A `;` that closes no Inline block → `R0108` (hint: a body on later lines is indented under its header)

Spec: chapter 01.

## Continuation lines

[`plots/royal_banquet.regia`](../showcase/plots/royal_banquet.regia)
```regia
WHEN insult_thrown(?offender), FROM Guest ?offended:
    GIVEN NOT HonorDuel(?offender) RUNNING:  # one duel per offender at a time
        START SUBPLOT HonorDuel(?offender),
            MAPPING ?offended AS Challenger,
            MAPPING ?offender AS Defender,
            MAPPING Guest EXCEPT ?offended, ?offender AS Spectator
```

The last four lines are one Statement. A line goes on to the next one, forming one logical line, when it ends with `,` or has a `(` that isn't closed yet. A `,` always says that something more follows, so it never ends a logical line.

- The lines that carry on are indented further than the logical line's first line. How much further is up to us; they never count as a Block's body.
- Lines are joined into logical lines before anything else is read, so a header can wrap before its `:`, and an Inline block can wrap too.
- A `,` never joins two Statements. Statements are separated by a new line or by `.`.

**Checks**

- A continuation line not indented further than its logical line's first line → `R0105`

Spec: chapter 01.

## Clauses and the comma

[`playbooks/noble_socializing.regia`](../showcase/playbooks/noble_socializing.regia)
```regia
WHEN insulted, FROM peer ?who, SUITS aggressiveness AT 0.8, bravery AT 0.8:
    DO stand_up
    SIGNAL insult_thrown(?who)
```

A header or a Statement has a core and, after it, optional clauses:

- The core is the head keyword, the item it needs, and that item's complements. A complement finishes a single word and has no `,` before it: `SHIFT m BY n`, `UPDATE f TO f2`, `FINISHED WITH r`. Here the core is `WHEN insulted`.
- A clause applies to the whole header or Statement, and is always written `, KEYWORD …`. Here there are two, `, FROM peer ?who` and `, SUITS …`. Other clauses are `, WEIGHT`, `, RANDOMLY`, `, WITHOUT WAITING`, `, UNTIL`, `, MAPPING`.
- A list separates its items with `,` too: the Propensities of `SUITS`, arguments, `EXCEPT ?offended, ?offender`, `PLAYS Guest, Guard`.
- The word after a `,` tells which it is: a clause keyword starts a clause, and anything else is the next item of the list. No list item may start with a clause keyword. A list ends at the first token that can't be one of its items: here `bravery AT 0.8` is the second Propensity, and the `:` ends the list. `MAPPING Guest EXCEPT ?offended, ?offender AS Spectator` ends its list at `AS`, the next word of the core.
- Clauses come in any order, each at most once unless its chapter allows more. The Visual Editor and formatters write them in the order their chapter lists them.
- A clause keyword with no `,` before it is an error whose hint adds the comma: `WHEN insulted FROM peer:` is `WHEN insulted, FROM peer:`. The same word may introduce the required item as part of the core, with no comma: `WAIT UNTIL on_plate(?)` waits for the condition, and `WAIT 1 MINUTE, UNTIL on_plate(?)` adds a limit to a Duration.
- A `,` never joins conditions. Conditions that must both hold are joined with `AND`, alternatives with `OR`. `AND` and `OR` never join list items: `SUITS sympathy AT -0.5, bravery AT 0.8`, not `… AND …`.

A condition word follows its subject when the subject is written: `?foe PLAYS peer`, `HonorDuel(?offender) RUNNING`, a Trigger's item before its kind word (`take_seat ENDED`). With the subject left implicit, the Agent itself or the running Plot, the word comes first: `PURSUING have_dinner`, `IN arrival`. A condition word binds tighter than `NOT`, so `NOT HonorDuel(?offender) RUNNING` is `NOT (HonorDuel(?offender) RUNNING)`.

Every line can be parsed from its words alone, without knowing what any name is declared as or in which file. Keywords carry the shape, and names are only names: the word after `HonorDuel(?offender)` is what makes it a Subplot condition, where `is_hungry` alone would be a Fact. That is what lets each file be parsed on its own and its Imports found before any name is resolved.

**Checks**

- A clause keyword after the core with no `,` before it → `R0111` (the message names the clause; hint: add the `,`)
- `AND` between the items of a `SUITS` Label or a `SHIFT` → `R1412` (hint: `,`)
- `AND` between the Roles after `PLAYS` → `R2125` (hint: `,`)

Spec: chapter 01. For Labels, chapter 14; for `PLAYS` in Instancing, chapter 21.

## Empty Blocks

[`playbooks/noble_socializing.regia`](../showcase/playbooks/noble_socializing.regia)
```regia
OPTION, WEIGHT 5: PASS           # nothing, this time
```

A Block header with no body is allowed, with a warning: it may be a Block we haven't written yet. A header followed by a dedent or by the end of the file is empty, and so is an Inline block with nothing in it (`: ;`).

`PASS` is a Statement that does nothing. It goes wherever a Statement goes, on its own line or inline, and says that the emptiness is meant, so a Block holding only `PASS` gets no warning. Here it is an Option of a Random choice that means "otherwise nothing". A Plan that deliberately ignores its Trigger is written the same way.

- Every empty Block follows this one rule, Options included.
- There is no keyword for "not written yet". That is a bare empty Block, which warns, or a comment.
- The Visual Editor writes `PASS` in every Block it creates empty.

**Checks**

- A Block header with no body → `R0106` (warning)

Spec: chapter 01. For Options, chapter 09.

## Comments

[`plots/royal_banquet.regia`](../showcase/plots/royal_banquet.regia)
```regia
PRECEDENCE:
    Keeping_watch OVER NobleSocializing ON scandal   # a knight on duty is a Guard first
    Dining TIES NobleSocializing ON insulted         # over dinner, temper decides
    HonorDuel OVER Poisoning

#[
    Counting by hand. The Director learns `seated` and `finished` from the
    Guests' Signals and compares them with the number of Guests still here.
    A Guest who leaves sends no Signal, so the `LEFT` Plan forgets it and
    counts again. In Regia 2.0 a Quota Trigger does all of this.
]#
```

`#` starts a comment that runs to the end of the line. It can have a line to itself or follow code. A `#` inside a string is not a comment.

`#[` opens a comment over several lines, which ends at the matching `]#`. It can start and end in the middle of a line, and code after the `]#` carries on: `DO toast #[ for now ]# (?who)` is `DO toast(?who)`. These comments nest: every `#[` or `#@key[` inside one needs its own `]#`, so commenting out code that already holds one still works.

```regia
#[ Left out until the kitchen can run out of wine.
WHEN sold_out(?dish), FROM waiter:
    FORGET craves(?dish)        #[ and sulk? ]#
]#
```

Comments mean nothing to the Transpiler, but they are kept in the syntax tree next to the whitespace, so text goes through the Visual Editor exactly as written. When the editor moves or deletes a construct, the comments that belong to it go too:

- comment lines directly above it, with no blank line in between;
- a comment after it on its last line;
- for a Block, comment lines at the end of its body, indented at the body's level, like `# no ELSE: …` in `TO take_seat`.

A comment set apart by a blank line belongs to nothing and stays where it is, like the `#[ … ]#` above. A line starting with `##` or `#%` is an ordinary comment.

**Checks**

- A multiline comment never closed → `R0201` (pointing at its opener)

Spec: chapter 02. For what moves with a construct, chapter 22.

## Doc comments

[`plots/royal_banquet.regia`](../showcase/plots/royal_banquet.regia)
```regia
#@version: 1.5
#@desc[
    The Root Plot of the showcase: one evening at court, from the Guests
    arriving to the last one taking leave.
]#

IMPORT "../vocabulary"
```

```regia
#@desc: One evening at court. HonorDuel and Poisoning are started during the feast, as its Subplots.
PLOT RoyalBanquet:
```

```regia
#@desc: Everyone invited to the table. A knight is a Guest and a Guard at once.
ROLE Guest:
```

A Doc comment documents the declaration directly below it. Unlike a plain comment it is part of the grammar, and tools read it: the Visual Editor shows it in the Inspector and builds each file's Docs page from it. The first two lines above, followed by a blank line at the top of the file, document the file itself; the next documents the Plot, and the last a Role.

- `#@key: value` holds one value, running to the end of the line. `#@key[ … ]#` holds one value over several lines: everything up to the first `]#`, taken literally (it doesn't nest and can't hold `]#`), with the indentation its lines share removed and blank lines trimmed at both ends.
- With no key, `#@ text` and `#@[ … ]#` mean `desc`.
- Any word is accepted as a key. Tools understand four: `desc`, `author`, `version` and `allow` (next section). A key may repeat: two `#@author:` lines give two authors. Values are plain text, which documentation tools may render as Markdown.
- A Doc comment starts its own line.

What it attaches to:

- A run of Doc comments attaches to the declaration directly below it, with no blank line in between. Plain comments between them don't break the run.
- Any declaration can take one: a Plot, a Playbook, a Role, a Phase, a Plan, a Vocabulary item. A Statement can't.
- The first Doc comments of a file, followed by a blank line, document the file.
- Any other Doc comment, above a Statement or followed by a blank line in the middle of a file, gets a warning and is ignored.

A Vocabulary line that declares several items gives its Doc comments to every one of them. To document one item alone, we declare it on a line of its own:

[`vocabulary.regia`](../showcase/vocabulary.regia)
```regia
#@desc: Seeded by Instancing. Guests add their own and make them bigger as the evening goes on.
FACT grudge(person, size)
FACT purse(gold), craves(dish), on_duty
```

**Checks**

- A Doc comment after code on its line → `R0202`
- A Doc comment directly above no declaration, and not the file's → `R0203` (warning; it is ignored)

Spec: chapter 02.

## Allowing a warning: `#@allow`

Suppose `Hosting` had a Plan for `idle`, as `NobleSocializing` does. `RoyalBanquet` gives both and orders neither against the other, so the build warns that the two are ordered only by name. The writer knows the king plays no Guest and never holds both, and answers in the source:

```regia
#@allow: R1305
PLAYBOOK Hosting:
    ...
```

`#@allow: <code>, …` silences those warnings wherever their main span lies inside the declaration the Doc comment attaches to, nested declarations included. On a Plot it covers the Plot's Plans; as a file's Doc comment it covers the file.

- Only warnings can be allowed. Naming an error's code is itself an error.
- An `allow` that silences nothing, because the warning went away or the code doesn't exist, gets a warning of its own, so allows don't go stale. That warning can't be allowed.
- An allowed warning isn't gone: `regia check --all-warnings` lists it marked *allowed*, and the Visual Editor shows it faded.

It is meant for a warning the writer can't avoid or has chosen not to. A warning the language could avoid by itself is fixed in the language instead, as `?_who` does for a Placeholder that is named but not used.

**Checks**

- `#@allow` naming an error's code → `R0204`
- `#@allow` naming a code that silences no warning in its declaration → `R0205` (warning)

Spec: chapter 02. For the order by name, chapter 13; for `--all-warnings`, chapter 23.

## Keywords

```regia
ACTION wait                    # fine: an ordinary name
GOAL Pass                      # fine
FACT PASS                      # error: PASS is a keyword
```

Keywords are written in capitals, and for them case matters. An all-caps word that is a keyword is always that keyword; `wait` and `Pass` are ordinary names. Names compare among themselves ignoring case (*Vocabulary and files*).

- Every keyword is reserved: a name spelled exactly like one is an error. The full list, by family, is *Reserved words* in spec chapter 01.
- Reserved too, though they do nothing yet: `TOLD`, `AGREED`, `REFUSED` and `REFUSE`, kept for a version in which Agents answer each other (*Messages*).
- Every retired keyword stays reserved, so the parser can name its new spelling (next section). Only the exact all-caps spelling is blocked.
- Words of Regia 1.0, of earlier drafts and of the primer (`BELIEVE`, `ACHIEVE`, `PRIORITY`, `WORLD` and the like) are not words of the language and are not reserved.

A keyword has one meaning wherever it is written. A reader who knows one use of `FROM` can predict the others. The few closed exceptions are `TO` as a destination in `ASSIGN … TO` and `UPDATE … TO` (elsewhere it introduces a Goal), `BY` as the amount of `SHIFT` and `SHIFTS` (elsewhere it names who did something), and `RANDOMLY` as both the head of a Random choice and a Pick clause.

**Checks**

- A name spelled exactly like a keyword → `R0110` (hint: change its case or its spelling)
- `TOLD`, `AGREED`, `REFUSED` or `REFUSE` used → `R0706`

Spec: chapter 01. For the reserved Message words, chapter 07.

## Retired spellings

```regia
WHEN idle:
    EITHER, WEIGHT 3: DO chat          # error: renamed; the hint says RANDOMLY: with OPTION: Blocks
```

When the language replaces a spelling, the old one becomes an error whose hint names the new spelling, and never keeps working as a synonym. The Guests' small talk was written this way before the syntax review.

- Each such error belongs to the chapter of its construct and is numbered with that chapter's checks. The table of them all, with the spelling to write instead, is *Retired spellings* in spec chapter 01.
- The error stays for ever, and its hint keeps naming the new spelling. Regia is generated as well as written, and a generator that learned from older text may produce an old spelling long after writers have stopped.
- Only a spelling that was once in the spec gets an error. Regia 1.0 is a different language: its words get the ordinary parse error.
- A clause written without its `,` has an error of its own, for a missing comma, and isn't in the table (*Clauses and the comma*).

**Checks**

- Any spelling in spec chapter 01's *Retired spellings* table → that table's code (hint: the spelling to write instead)

Spec: chapter 01, *Retired spellings*, and the chapter of each construct.

## Words of Regia 2.0

A Transpiler for Regia 1.5 still parses every construct of 2.0. If a Program uses one from a system 1.5 leaves out, the build reports one error for it, which names the construct and says it is Regia 2.0, so the writer never sees a parse error there. Nothing else is checked on that construct. The constructs are:

- `FROM GAME`, `FROM ME`, and `FROM` with alternatives joined by `OR`;
- `BY` on a Goal's ending, and a Goal's ending heard in a Plot;
- a quantity after `FROM` or `BY`, which makes a Quota Trigger, and `SENT`;
- `JOINED`.

`WHEN EXITED, BY PARENT:` and the `BY` of `SHIFT` and `SHIFTS` are not a Goal's ending, and are in 1.5.

> **In 2.0** these constructs build, and the error is retired with its number kept. A Program that builds in 1.5 builds in 2.0 and does the same thing there. Spec chapter 01, *A word of Regia 2.0 in a 1.5 build*, and the chapters of each construct (05, 18, 19, 20).

**Checks**

- A construct of a system Regia 1.5 leaves out, in a 1.5 build → `R0109` (the message names it)

Spec: chapter 01. Each construct in chapters 05, 18, 19 and 20.

## How this combines with…

### Vocabulary and files

[`plots/honor_duel.regia`](../showcase/plots/honor_duel.regia)
```regia
IMPORT "../vocabulary"
IMPORT "../playbooks/duelling"
IMPORT "../playbooks/wagering"

#@desc: One duel over one insult. The offender is the Defender; it also tells this duel from the others.
PLOT HonorDuel(offender):
```

Imports are Statements like any other, one per line, and come first in a file, after the file's Doc comment. Dotted names such as `hall.music.fanfare` are the game's names, given a Regia name with `AS`. Both are in *Vocabulary and files*.

### Instancing

[`banquet.regin`](../showcase/banquet.regin)
```regia
KIND hothead, LIKE noble:
    COUNT 2
    bravery AT 0.9
    sympathy AT -0.4
    aggressiveness AT RANDOM(0.6, 1)
    LEARN grudge(percival, 2)                # every hothead has a score to settle with Sir Percival
```

```regia
AGENT percival, LIKE knight                  # the second knight, named so that a grudge can name him
```

A `.regin` file follows the same rules for lines, Blocks, clauses and comments. An Agent with nothing to set is one line with no `:`. Instancing has no comment form: it lives only in `.regin` files. (*Instancing*)

### Randomness

Options are where Inline blocks and `PASS` show most. `RANDOMLY:` is a Block header like any other, and each `OPTION` is a Block of its own, inline or indented. (*Randomness*)

### Precedence and Labels

A header with several Labels is the longest line a Playbook has, and the commas between its clauses are where it wraps onto continuation lines. The warning that `#@allow` most often answers, an order by name between Playbooks never held together, is in *Precedence and Labels*.

### The Transpiler

Each file is parsed on its own, from its words alone, and a mistake of layout is reported in its file even when an Import beside it is broken. Every error and warning of the build has a code, `R` and the spec chapter's two digits, and a docs page of its own. (*The Transpiler*)

### The Visual Editor

The editor writes indentation, one Statement per line, with `PASS` in new Blocks. It changes only the text an edit touches, and keeps our `.`, `;` and comments as we typed them; the comments that belong to a construct move with it. (*The Visual Editor*)
