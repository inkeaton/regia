# Write guide chapter 19, The Transpiler

Type: task
Status: open
Assignee:
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
