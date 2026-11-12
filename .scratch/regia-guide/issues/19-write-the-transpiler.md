# Write: The Transpiler

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 03

## Task

Write `docs/guide/16 - The Transpiler.md`.

Covers: Using the CLI: Entry files, Builds and what is written, Diagnostics and their codes, reading a Trace, Conformance cases. Architecture only as far as it explains what a user sees.

Sources: 23, 27, 34; ADR 0010, 0012.

Follow the chapter template fixed in *Fix the chapter template with a sample chapter* (03) and the map's Notes. Take snippets from `docs/guide/showcase/`; if a construct has no natural place there, either add it to the showcase or tag it `#revise`. Finish by re-reading every example against the cited spec chapters.

## Resolution

Written on 2026-11-12: [`docs/guide/16 - The Transpiler.md`](../../../docs/guide/16%20-%20The%20Transpiler.md), about 4,700 words counting snippets, tables and the diagram, over nine sections (checking a Program, Entry files, reading a Diagnostic, Diagnostic codes, what a check works on, building, reading a Trace, following a Failure, Conformance cases). Every command line, Diagnostic and Trace line is put together by hand from chapters 23, 27, 28, 34 and 35, and the chapter says so. The showcase Program is unchanged. The contents of the Build's files are left to *Translation to ASL*, and the Workspace and LSP shapes to *The Visual Editor*. Not yet read by the user.

Fifteen `#revise`, among them:
- Only a whole story can be checked: a Playbook file alone gets "no Root Plot", and `honor_duel.regia` alone is taken for the Root Plot and gets an error on its `PARENT` line.
- A warning can't be marked as seen, and the showcase carries `R0307` on purpose.
- Target checks come out of the emit, so a Program can pass `regia check` and fail `regia build`.
- The Build folder mixes generated files with the Traces that are to be kept.
- The command line has `check` and `build` only: nothing starts a Build, prints the conflict report, or runs a behaviour case of our own.
- The Trace has no entry for what didn't happen, and a Director's name changes with the number of Stagings.

Eight entries were added to the README's *Spec wording*, and one to *Gaps in the showcase*.
