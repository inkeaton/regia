# How a spec chapter proves itself

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo

## Question

How does each spec chapter in `docs/spec/` show that it is complete and correct, in a form the development effort can test the Transpiler against? Worked examples, conformance cases (Regia in, expected ASL or expected error/warning out), or both; where they live; how they are named; and what a chapter must cover (each rule, each error and warning). This is about the spec, not the development process.

## Answer

Spec chapter: `docs/spec/27-conformance.md`. Glossary: *Diagnostic*, *Diagnostic code* and *Conformance case* added. Spec 23 points to the new chapter for codes.

- **What a case checks**: check cases (exact Diagnostics: severity, code, line; or none) and behaviour cases (a scripted run and its expected Trace). Emitted ASL is not part of the spec: golden `.asl` files would freeze one lowering, and the spec promises meaning. ASL snapshots are a development-side choice. Behaviour cases wait for *Trace and logging*.
- **Scope**: language chapters 01–21 and 26 only. The architecture chapters 22–25 get no cases.
- **Diagnostic codes** `R<chapter><nn>`, never reused, listed in a uniform `## Transpiler checks` section (Errors / Warnings / Notes) in every language chapter.
- **Files**: `docs/spec/cases/NN-<chapter>/<slug>.regia`, or a folder for multi-file and Instancing cases (Entry: the root `.regin` if any, else every `.regia`). Behaviour expectations in a sibling `.trace`. The spec owns the cases; the development effort vendors them.
- **Annotations** are `#!` comments: header `case:`, `rule:` and `ok`; `#! error R1301` after code expects a Diagnostic starting on that line, `#!^` on its own line points at the line above. Exact match on severity, code and line; message wording, labels, hints and fixes are not checked.
- **Coverage**: every check has a case that reports it, every rule an accepting case, every case names its rule, and later every runtime rule a behaviour case.
- **Who writes them**: the spec carries one exemplar case per language chapter. Full coverage is the development effort's job, written test-first. Assigning codes, the uniform sections and the exemplars graduate to *Number the checks and add exemplar cases*.

## Comments

- Graduated from the map's fog in the scoping pass of 2026-11-09.
- Leaning: conformance cases beside each chapter.
