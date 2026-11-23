# Write guide chapter 19, The Transpiler

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 05

## Question

Write `docs/guide/19-the-transpiler.md`, *The Transpiler*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 23, 27.
- **Covers:** passes, the Model, Diagnostics and their codes, entry files, the command line, the Build folder, Targets, crates, the WASM Workspace, conformance cases and coverage, `regia test`.
- **Quotes most:** throwaway; the showcase `README.md`'s *Diagnostics*.
- **"In 2.0" notes:** `R0109` and `T1902` retired.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.

## Resolution

Done on 2026-11-20 (task). [`docs/guide/19-the-transpiler.md`](../../../docs/guide/19-the-transpiler.md), about 480 lines, written from the template:

- An opening table of the five commands.
- Sections: Checking a Program (Entry files, Programs, a `.regia` Entry); Reading a Diagnostic (a throwaway `R1004` from `serving.regia` without its `IMPORT`, the parts of a Diagnostic, *Warnings we accept*); Diagnostic codes; What a check works on (the passes as a mermaid and a table, the Model); Targets (a throwaway `ports.regin` with `base_port 0` → `R3602`, `--target none`); Building; Running (`lib/`, `--seed`, `--console`); Reports (`regia explain`); The command line (commands, options, exit status); Regia 1.5 and the Transpiler (a throwaway `FROM GAME` in `Keeping_watch` → `R0109`); Conformance cases (a throwaway check case for `R0503`, annotations, matching, case files); Coverage; `regia test`; Crates; The Workspace (calls, *The shapes at the boundary*).
- One "In 2.0" note: `R0109` and `T1902` retired.
- The showcase `README.md`'s *Diagnostics* says only that the Program builds clean; it's stated in *Checking a Program*. Every Diagnostic shown comes from breaking a showcase line; their line and column numbers were checked against the files. Grep for retired spellings: none. The humanizer pass merged one closing paragraph; the only dashes left are number ranges.
- No `Guide:` line added: the showcase README's *Coverage* has no heading for chapters 23 or 27.

Four non-blocking findings: chapter 38 missing from 27's language chapters; the form of command-line errors; what `--deny-warnings` adds to `regia test`; whether `--target none` skips `R2113`/`R2116`.
