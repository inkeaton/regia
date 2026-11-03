# Comment syntax

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo

## Question

What is the comment syntax in 2.0 (primer ch.1, ch.6)? Single-line `#`, multiline `## … ##` replacing `#-`, doc comments `#@key:` (and multiline `##@ … ##`), and instancing comments (`#%`, or another symbol?). Are doc and instancing comments part of the grammar, attached to the construct that follows them? Which doc keys exist (`desc`, `author`, `version`, …), and is that set fixed or open?

## Answer

Spec chapter: `docs/spec/02-comments.md`. Glossary entries added: Comment, Doc comment, Doc key. Instancing comment now names `#%`.

- **Three kinds, one multiline rule:** a plain comment is `#` or `#[ … ]#`, a doc comment is `#@key: value` or `#@key[ … ]#`, an instancing comment is `#%` or `#%[ … ]#`. The primer's `#-` and `## … ##` are dropped, because `## Section` lines and `####` banners would silently swallow code.
- **Plain comments** can go anywhere outside a string, including after code. A Statement-ending `.` may be followed directly by `#`. `#[ … ]#` can open and close mid-line and **nests**: every opener inside counts as a level. Plain comments are trivia in the syntax tree, kept for lossless round-trips.
- **Doc comments are grammar nodes.** They attach to the declaration directly below them, with no blank line in between: Plot, Playbook, Role, Phase, Plan, Vocabulary items, but not Statements. A doc block at the top of the file, followed by a blank line, documents the file. Any other doc comment gets a "detached doc comment" warning.
- **Doc keys are an open set.** Tools know `desc`, `author` and `version`. Keys may repeat, and a bare `#@` / `#@[` means `desc`. A multiline doc comment holds one key. Its text is literal (it doesn't nest) and is dedented and trimmed.
- **`#%` and `#%[ … ]#` are reserved** for Instancing comments. What they carry is decided in [Instancing comments](22-instancing-comments.md).
- Doc and instancing comments must start their own line. An unclosed multiline comment is an error at its opener.
