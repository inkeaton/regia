# Scoping, imports and aliases

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo

## Question

How are names organised across files and constructs (primer ch.2, ch.3)? Imports (header-only, diamond dependencies allowed, cycles rejected), Vocabulary declared locally inside a Playbook or Plot, aliases (`ACTION engine.security.summon_guards AS call_guards`), dotted names and namespaces, and the visibility of names across imports. Must the Vocabulary still be declared at the top of the file?

## Answer

Spec chapter: `docs/spec/10-scoping-and-imports.md`. ADR 0006 (one parameter count per name). Glossary: *Import*, *Entry file*, *Program*, *External name*, *Local Vocabulary* added.

- **Imports:** `IMPORT "path".` comes first in the file, after the file doc comment. The path is relative to the importing file, with `.regia` optional, and there are no roots or search paths in 2.0. Imports are **transitive**, as in 1.0. A file is loaded once, so diamonds are fine, and a cycle is an error naming the loop. There is no export control and no re-exporting. A name that breaks because an import further down changed gets a hint saying where it used to come from.
- **The Program** is every file reachable from the Transpiler's Entry files. Visibility is per file, uniqueness is checked across the whole Program.
- **One flat namespace** for Vocabulary, Playbooks and Plots, never qualified by file. Roles and Phases stay local to their Plot. A name has one kind and **one parameter count** (ADR 0006). A re-declaration with the same kind, count and External name is the same item. Any mismatch is an error, and re-declaring a Playbook or Plot is always one.
- **Declaration order:** after the imports, anything goes in any order, and names can be used before they are declared. "Vocabulary at the top" is dropped.
- **External names:** `FACT`/`EVENT`/`ACTION <external> AS <name>`. A dotted name is only ever an External name and needs `AS`. Goals can't have one. Parameters are written after the Regia name. One External name gets one Regia name, and merges require the External names to match.
- **Local Vocabulary:** only `FACT` and `GOAL`, inside a `PLAYBOOK` or `PLOT`, anywhere in the Block, with no `AS`. They are private to that Playbook or Director, even on a shared Agent. They never come from the game, can't be sent, and can't shadow a visible name. When a Playbook is taken away, its local Facts stay but go unseen, and its local Goals are dropped.
- Reserved: `IMPORT`, `AS`.

