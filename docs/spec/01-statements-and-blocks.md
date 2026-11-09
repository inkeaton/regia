# Statements and blocks

How Regia source is split into Statements and Blocks. Decided in the ticket *Statement and block syntax* (`.scratch/regia-2/issues/01-statement-and-block-syntax.md`). This chapter replaces the syntax part of primer ch.1. Comments are covered in *Comments* (`02-comments.md`).

## Two styles

There are two ways to structure code, and they can be mixed freely:

- **Indentation style** (the default): one line is one Statement. A line ending in `:` is a Block header, and its body is the lines indented under it.
- **Explicit style**: `.` ends a Statement and `;` closes a Block. This lets you put several Statements, or a whole Block, on one line.

```regia
PLAYBOOK NobleSocializing:

    WHEN insult_heard:
        IF NOT is_drunk AND hates(host):
            DO complain
            SIGNAL insult_thrown
        ELSE:
            DO toast(host)

    WHEN digestion_check:
        IF is_hungry: DO eat_food. FORGET(is_hungry). PRINT("A guest finishes their meal.")

    WHEN food_served:
        DO PRINT("A guest notices food arriving.")
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
- **Body on the same line as the `:`**: an **Inline block**. Its Statements are separated by `.`, and it ends at a `;` or at the end of the line, whichever comes first. An Inline block never spans several lines; to go multi-line, use indentation.

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

A `.` at the end of a line, or a `;` closing an Inline block right at the end of a line, does nothing and is allowed without a warning. This keeps most pasted 1.0 code parsing. The Visual Editor keeps it when it writes edits back: it never normalises text an edit doesn't touch (chapter 22, `22-bidirectional-editing.md`).

## Indentation rules

- Tabs or spaces, at any width, but consistent within a file. Mixing tabs and spaces for indentation in one file is an error.
- Dedenting to a level that was never opened is an error ("this line is indented less than the Block it's in, but more than the one outside").
- Blank lines and comment-only lines don't count for indentation.

## Continuation lines

A physical line continues onto the next one, forming one logical line, when:

- it ends with `,`, or
- it has a `(` that isn't closed yet.

Continuation lines must be indented further than the logical line's first line. Physical lines are joined into logical lines before any of the rules above apply, so an Inline block can continue this way too.

```regia
DO eat_food,
    FORGET(is_hungry),
    PRINT("A guest finishes their meal.")
```

A Trigger with many Labels wraps after any of the `,` that separate them (chapter 14, `14-labels.md`).

## Parsing never depends on declarations

Every construct can be parsed from its tokens alone, without knowing what any name is declared as or in which file. Keywords carry the shape (`DO`, `LEARN`, `PURSUE`, …), and names are only names. This is what lets each file be parsed on its own and its imports be found before any name is resolved (chapter 23). A syntax that would need to know a name's kind to be parsed is rejected.

## Empty Blocks

A Block header with no body is allowed, and the Transpiler warns about it. This supports sketching, for example in the Visual Editor. There is no placeholder keyword.
