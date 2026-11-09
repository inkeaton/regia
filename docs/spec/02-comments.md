# Comments

How comments are written in Regia, and which of them mean something to the Transpiler. Decided in the ticket *Comment syntax* (`.scratch/regia-2/issues/02-comment-syntax.md`). This chapter replaces the comment parts of primer ch.1 and ch.6.

## Three kinds

| Kind | Single line | Multiline | Meaning |
|---|---|---|---|
| Plain comment | `# text` | `#[ … ]#` | None: for human readers only |
| Doc comment | `#@key: value` | `#@key[ … ]#` | Documents the declaration below it |
| Instancing comment | `#% …` | `#%[ … ]#` | Instancing information, see chapter 21 |

The rule is the same for all three: the kind's marker (`#`, `#@key`, `#%`) followed by `[` opens the multiline form, and `]#` closes it. The primer's `#-` continuation and `## … ##` are dropped, so a line starting with `##` is just a plain comment.

## Plain comments

`#` starts a comment that runs to the end of the line. It can sit on its own line or after code. A `#` inside a string is not a comment.

```regia
# Guests react to the food
WHEN food_served:
    DO eat_food.  # only when hungry, see below
    DO eat_food.# also fine: `.` may be followed directly by `#`
```

`#[` opens a multiline plain comment, which ends at the matching `]#`. It may start or end in the middle of a line, and code after `]#` carries on:

```regia
#[
    Old behaviour, kept for reference:
    WHEN insult_heard: DO complain
]#
DO toast #[ for now ]# (host)
```

Multiline plain comments **nest**. Inside one, every opener (`#[`, `#@key[`, `#%[`) counts as a level and needs its own `]#`. This means commenting out code that already holds a multiline comment still works.

Plain comments mean nothing to the Transpiler. They are kept in the syntax tree as trivia, next to whitespace, so that text survives round-trips through the Visual Editor exactly as written. Which construct a plain comment moves with when the Visual Editor edits the tree is decided in *Bidirectional editing model*.

Comment-only lines don't count for indentation (see *Statements and blocks*). Neither do the lines a multiline comment spans.

## Doc comments

A doc comment documents a declaration. It is part of the grammar, unlike a plain comment.

```regia
#@author: Mari
#@version: 0.2
#@desc[
    Reactive behaviour for guests mingling
    and eating at the banquet.
]#
PLAYBOOK Guest:
```

### Form

- **Single line:** `#@key: value`. The value runs to the end of the line.
- **Multiline:** `#@key[ … ]#`, with one key per block. Everything up to the first `]#` is the value. The text is literal: it doesn't nest and can't contain `]#`. The value has its common leading indentation removed, as in Python's `textwrap.dedent`, and its leading and trailing blank lines trimmed.
- **No key:** `#@ text` and `#@[ … ]#` both mean `desc`.

A doc comment must start its own line, since it documents a whole declaration.

### Keys

The set of keys is **open**: any `#@word:` is accepted. Tools understand three keys:

| Key | Meaning |
|---|---|
| `desc` | What the declaration is for |
| `author` | Who wrote it |
| `version` | Its version |

A key may repeat. Two `#@author:` lines give two authors. Values are plain text. Documentation tools may render them as Markdown.

### Attachment

- A run of doc comments attaches to the **declaration directly below it**, with no blank line in between. Plain comments between the doc comments and the declaration don't break the run.
- Any declaration can take doc comments: Plot, Playbook, Role, Phase, Plan, and Vocabulary items. Statements can't.
- A doc comment at the **top of the file**, followed by a blank line, documents the file itself.
- Any other doc comment, for example one followed by a blank line in the middle of a file or one above a Statement, gets a **warning** ("detached doc comment") and is ignored.

## Instancing comments

`#%` (single line) and `#%[ … ]#` (multiline) mark Instancing comments. Like doc comments, they are part of the grammar, must start their own line, and their multiline form doesn't nest. They sit only at the top level of a file, after its Imports. What they carry, and the `.regin` Instancing file that holds the same content without the markers, are in chapter 21 (`21-instancing.md`).

## Errors

- An unclosed multiline comment is an error that points at its opener.
- A doc or instancing comment that doesn't start its own line is an error.
