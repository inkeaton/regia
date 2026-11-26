# Bidirectional editing

How an edit made on the Visual Editor's graph becomes an edit to the Regia source, and what the syntax tree must hold to make that possible. Decided in the ticket *Bidirectional editing model* (`.scratch/regia-2/issues/27-bidirectional-editing-model.md`). ADR 0011.

## The text is the source of truth

The source text is the only model. The syntax tree is rebuilt from it and is a read-only index over it.

1. The user does something on the graph, for example adds a Phase.
2. The Visual Editor calls an **edit operation** in the Transpiler core (running as WASM), passing the current tree.
3. The core returns a list of **text edits per file**: replace this range with this text. One graph action may touch several files.
4. The Visual Editor applies them to Monaco with `pushEditOperations`, followed by `pushUndoStop`, so one graph action is one undo step, in every file it touches (chapter 24).
5. The changed files are parsed again in full, and the graph is redrawn from the new tree.

Text edits typed in Monaco take the same path from step 5.

## Edit operations

The edit API is made of domain operations, such as adding a Phase to a Plot, adding a transition, renaming, or deleting a construct. Each operation returns text edits. Moving a construct under another parent is not a 2.0 operation; the Extent and indentation rules below are written so that it can be added later without changing them.

The Visual Editor reads node spans to highlight a construct, reveal it in the text, or keep a selection. It never builds edits out of spans itself. All editing logic lives in the core, in Rust, and is tested as *source before, operation, expected source after*.

Which operations exist, and where a new declaration lands (for example a new Cue a transition needs), are in chapter 25 (`25-graph-view.md`).

## Extent: what moves with a construct

A construct's **extent** is the construct plus the comments that belong to it. Deleting a construct deletes its extent, and a later move operation moves it. The rules:

1. Comment lines directly above the construct, at its indentation and with no blank line in between, belong to it. This is the same rule that attaches doc comments (chapter 2).
2. A comment on the same line, after a construct's last token, belongs to the outermost construct that started on that line and ends there: to the Option in `OPTION, WEIGHT 5: PASS  # nothing`, to `DO b` in `DO a. DO b  # why`. After a header's `:`, it belongs to the construct the header opens. The line break goes with it.
3. Comment lines at the end of a Block's body, and in that Block by the rule below, belong to that Block, even when the line right below is a construct outside it. Under a header with no body, comment lines indented further than the header belong to the header.
4. A comment separated from every construct by a blank line belongs to none of them. It stays where it is, and is kept when a neighbouring construct is deleted.

The first blank line above a construct is the boundary of its extent.

```regia
PLAYBOOK Guest:

    # Reacts to rude guests        <- belongs to WHEN insult_heard (rule 1)
    WHEN insult_heard:
        DO complain                 # loudly   <- belongs to DO complain (rule 2)
        # TODO: add a retort        <- belongs to WHEN insult_heard's body (rule 3)

    # --- eating ---                <- belongs to nothing (rule 4)

    WHEN food_served:
        DO eat_food
```

### Which Block a comment is in

A comment line never opens a Block. Between two code lines, it is in the deepest open Block whose body is indented no further than the comment, but never in one shallower than the next code line's. The first code line of a body counts as next, so a comment between a header and its body is in the body. In practice:

| Comment line | Is in |
| --- | --- |
| At the body's level, with a shallower code line directly below | the body |
| Shallower than the body, with more of the body after it | the body |
| Between a header and its body | the body |
| Deeper than a header with no body | no Block; it belongs to the header (rule 3) |

## Style is kept

- Deleting the last Statement of a shared line keeps that line's break.
- Text an edit doesn't touch stays byte-for-byte the same. That includes redundant `.` and `;`, Inline blocks, continuation lines and the user's spacing.
- New constructs are written in indentation style, one Statement per line, without redundant terminators.
- An edit that adds to an Inline block first expands the smallest Inline block around the insertion point into indentation style, then inserts. For example, adding a Statement to the `IF` branch of `IF is_hungry: DO eat_food; ELSE: DO complain` gives:

  ```regia
  IF is_hungry:
      DO eat_food
      DO new_statement
  ELSE: DO complain
  ```

- Normalising a whole file is a formatter's job, not part of 2.0's design.

## Indentation

- Indentation stays as written (absolute columns).
- Each file has an **indent unit**: the indentation of its first indented line, or 4 spaces if no line is indented yet. Tabs or spaces follow the file, which can't mix them (chapter 1).
- A new construct is indented at its parent's body column, and its own body one indent unit deeper.
- A moved extent (once a move operation exists) is shifted line by line by the difference in columns. Continuation lines and the inside of `#[ … ]#` comments shift with it. `#@key[ … ]#` values don't need to, since their text is dedented anyway.

## Edits on broken source

The parser always produces a tree, even for invalid text. The graph is drawn from the latest tree. A construct whose extent contains a syntax error is shown, but can't be edited from the graph until the text is fixed. A syntax error is one the lexer or the parser reports, with its primary span inside the extent, whether or not there is an Error node (a missing `)` leaves none). Warnings and later passes' errors don't count. Each edit is computed against the tree of the current text. If Monaco has changed since the last parse, the core parses again before computing the edit.

## Identity across reparses

Nothing is stored to identify a construct between parses. The graph layout is automatic, so there are no positions to keep. When identity matters (keeping a selection, animating a change), it is a key built from the structure, such as `RoyalBanquet/feast/WHEN insult_heard#0`, recomputed on every parse. After a rename the key changes; the Visual Editor keeps the selection because it knows which rename it just applied.

## No incremental parsing

Every change reparses the whole file, debounced. The development effort checks a performance budget, for example a 5,000-line file parsed in under 16 ms in the WASM build. Incremental parsing comes back only if that fails.

## What the syntax tree holds

These requirements on the tree follow from the rules above. Chapter 1 and ADR 0010 fix the parser itself.

- **Lossless:** printing every token in order gives back the source exactly, invalid code included.
- **Ownership is structural.** The tree builder (chapter 23) applies the extent rules: comment lines that belong to a construct are placed inside its node, a trailing comment inside the construct rule 2 gives, and doc comments become the first children of their declaration. A construct's extent is its node's text range. Comments that belong to nothing stay at their parent's level.
- **Layout tokens:** INDENT and DEDENT are zero-width tokens of the lexer's, used by the parser and the tree builder and not kept in the tree, where a Block's node says the same. rowan doesn't promise to support zero-width tokens. Leading whitespace is a whitespace token. A NEWLINE token holds the line break that ends a logical line (chapter 23). The lexer places INDENT and DEDENT around comments by *Which Block a comment is in*; the tree builder only attaches comments within a level, and compares columns for rule 1 and for a comment under a header with no body.
- **Terminators:** `.` and `;` are real tokens inside the node they end. A redundant terminator stays inside its Statement.
- **Library:** rowan 0.17 (stable), where whitespace and comments are sibling tokens. It is wrapped in the core's own `syntax` module, and no other module names rowan types, so moving to rowan 0.18 (comments and whitespace attached to tokens, still alpha) or to a tree of our own stays local. Revisit when rowan 0.18 is stable.

## Later: editing the tree itself

The tree could later become the edit model: change the tree, print it, and turn the printed difference into text edits, in the style of Roslyn's and rust-analyzer's `SyntaxEditor`. That would replace only the code inside the core that computes text edits. The edit operations, the extent, style and indentation rules, the per-file text edits handed to Monaco, and the before/operation/after tests all stay the same. See ADR 0011.

## Regia 1.5

All of this chapter is in 1.5 (ADR 0025). Revised in the ticket *The Visual Editor* (`.scratch/regia-revision/issues/18-visual-editor.md`). *Which Block a comment is in*, *Extent* rules 1 to 3 as they stand, what a syntax error is, and leaving zero-width tokens out of the tree were decided in the tickets *Review: text to tokens* (`.scratch/transpiler/issues/01-text-to-tokens.md`) and *Review: tokens to tree to accessors* (`.scratch/transpiler/issues/02-tokens-to-tree.md`).
