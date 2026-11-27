# Comments

How comments are written in Regia, and which of them mean something to the Transpiler. Decided in the ticket *Comment syntax* (`.scratch/regia-2/issues/02-comment-syntax.md`). This chapter replaces the comment parts of primer ch.1 and ch.6.

## Two kinds

| Kind | Single line | Multiline | Meaning |
|---|---|---|---|
| Plain comment | `# text` | `#[ … ]#` | None: for human readers only |
| Doc comment | `#@key: value` | `#@key[ … ]#` | Documents the declaration below it |

The rule is the same for both: the kind's marker (`#`, `#@key`) followed by `[` opens the multiline form, and `]#` closes it. The primer's `#-` continuation and `## … ##` are dropped, so a line starting with `##` is just a plain comment.

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

Multiline plain comments **nest**. Inside one, every opener (`#[`, `#@key[`) counts as a level and needs its own `]#`. This means commenting out code that already holds a multiline comment still works.

Plain comments mean nothing to the Transpiler. They are kept in the syntax tree as trivia, next to whitespace, so that text survives round-trips through the Visual Editor exactly as written. A plain comment directly above a construct, or after it on the same line, moves with that construct when the Visual Editor moves or deletes it; one set apart by a blank line stays where it is (chapter 22, `22-bidirectional-editing.md`).

Comment-only lines don't count for indentation (see *Statements and blocks*). Neither do the lines a multiline comment spans. A comment line's own indentation only says which Block it is in (chapter 22).

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

The set of keys is **open**: any `#@word:` is accepted. Tools understand four keys:

| Key | Meaning |
|---|---|
| `desc` | What the declaration is for |
| `author` | Who wrote it |
| `version` | Its version |
| `allow` | Warnings the writer has seen and accepts here (below) |

A key may repeat. Two `#@author:` lines give two authors. Values are plain text. Documentation tools may render them as Markdown.

### Attachment

- A run of doc comments attaches to the **declaration directly below it**, with no blank line in between. Plain comments between the doc comments and the declaration don't break the run.
- Any declaration can take doc comments: Plot, Playbook, Role, Phase, Plan, and Vocabulary items. Statements can't.
- A Vocabulary line that declares several items (`FACT purse(gold), craves(dish), on_duty`) passes its doc comments to **every item** on it. To document one item alone, declare it on its own line.
- A doc comment at the **top of the file**, followed by a blank line, documents the file itself.
- Any other doc comment, for example one followed by a blank line in the middle of a file or one above a Statement, or one indented further than the declaration below it, gets a **warning** ("detached doc comment") and is ignored.

### Allowing a warning: `#@allow`

```regia
#@allow: R13_05-competition-ordered-by-name
PLAYBOOK Gossip:
    ...
```

A warning the writer has seen and accepts is answered in the source, where a reviewer sees it:

- `#@allow: <code>, …` lists Diagnostic codes, each written whole (chapter 27). It silences those warnings when their primary span lies inside the declaration it attaches to, nested declarations included: on a Plot it covers the Plot's Plans, and as a file's doc comment it covers the whole file.
- Only warnings can be allowed. Naming an error's code is an error (`R02_04-allow-names-error`).
- A code is matched on its number. A code written without its Code name, or with a name that isn't its number's, is an error (`R02_06-allow-misnames-code`), with a quick fix that writes the right name. An unknown number gets `R02_05-stale-allow`, below.
- An `allow` that silences nothing, because the warning went away or the code is unknown, gets a warning of its own (`R02_05-stale-allow`), so allows don't go stale. `R02_05-stale-allow` can't itself be allowed, and it is reported only when the Program has no errors: an error can silence the warning the allow was written for.
- An allowed warning isn't gone: `regia check --all-warnings` shows it marked *allowed*, and the Visual Editor shows it faded (chapters 23, 24).

It is for a warning the writer can't, or chooses not to, avoid, such as an order by name between two Playbooks that are never held together (chapter 13). A warning the language could avoid by itself is fixed in the language instead, as `?_name` does for an ignored Placeholder (chapter 03).

## Instancing

Instancing has no comment form. It is written only in `.regin` Instancing files (chapter 21). The `#%` and `#%[ … ]#` markers of earlier drafts are gone: a line starting with `#%` is a plain comment.

## Transpiler checks

**Errors**

- `R02_01-unclosed-comment` An unclosed multiline comment, plain (`#[`) or doc (`#@key[`), pointing at its opener.
- `R02_02-doc-comment-mid-line` A doc comment that doesn't start its own line.
- `R02_04-allow-names-error` An `#@allow` naming the code of an error.
- `R02_06-allow-misnames-code` An `#@allow` code without its Code name, or with a name that isn't its number's (quick fix: the right name).

**Warnings**

- `R02_03-detached-doc-comment` A detached doc comment: not directly above a declaration, and not a file's doc comment. It is ignored.
- `R02_05-stale-allow` An `#@allow` code that silences no warning in its declaration. Absence check (chapter 23).

## Regia 1.5

All of this chapter is in 1.5 (ADR 0025).

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).
