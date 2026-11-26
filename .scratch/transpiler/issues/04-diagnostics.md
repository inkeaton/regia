# Review: Diagnostics and where checks live

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

Which pass reports which check?

Chapter 23 gives parse the syntax Diagnostics and Validate the checks that "need the whole Program". An unused Placeholder (chapter 03) is neither.

Decide: a rule that assigns any check to one pass, tried on one check from each of six chapters; how passes hand Diagnostics over; how cascades from one broken construct are removed; where `#@allow` is applied; how a code ties to its severity and message in Rust.

Chapters 02, 23, 27.

From *Review: tokens to tree to accessors*: include misplaced constructs (the parser accepts them anywhere) and `R0109`, which the parser and Validate share.

From *Review: files to Model*: Model build reports Diagnostics too, and a Goal's-ending `R0109` is now its own (not Validate's). Which checks are absence checks (chapter 23)? The silence rules need Conformance cases.

## Resolution

Agreed with Edoardo on 2026-11-26. The answer is in chapter 23, *Where a check lives*, *Absence checks* and *Diagnostics*.

- **The rule.** A check belongs to the first pass that has everything it reads. Lex: one line's characters. Parse: one construct's tokens, not where it sits. Model build: what can't enter the Model as written (misplaced constructs, names, duplicates, imports, a precedence cycle, the late `R0109`, `R2104`). Validate: everything about the built Model. Tried on `R0102`, `R0307`, `R1301`, `R1508`, `R1702`, `R3807`. "Needs the whole Program" is gone.
- **Handover.** Return values from each pass; one `check` gathers, applies allows, removes exact duplicates, sorts.
- **Cascades** are prevented at the source, never filtered. The lexer-token rule was already in *What the lexer hands to the parser*.
- **`#@allow`.** Each `Parse` carries allow scopes; `R0204` at parse; `check` marks (not removes) allowed warnings; `R0205` only when the Program has no errors (chapter 02 too).
- **Codes.** `enum Code` with variants named by code, severity in a `match`, messages at the report site; a spec-vs-enum test once the case runner exists (M3).
- **Absence checks.** Defined (nothing in a scope does X), with a closed list of 30 in chapter 23, each marked in its own chapter; `R0304` and `R1303` only in their *never* parts. Glossary: *Absence check*.
- **Several Programs** on one file: union, exact duplicates removed (chapter 23 *The Workspace*; chapter 27 for folder cases).
- **Cases** (pending until M3): `01/bad-character-reported-once`, `02/allow-made-stale-by-an-error`, `03/placeholder-used-in-broken-statement`, `10/missing-import-silences-names/`, `15/misplaced-plan-is-left-out`, `38/cue-sent-in-broken-statement`.
- **Found:** about 25 existing cases wait on a plain `CUE` nothing sends, so they lack `R3807`: *Sweep cases for unsent Cues*.
- **Teach-back.** Five-line example worked. Passes placed right; `R3807` was missed at first (a Cue nobody sends is a warning even when declared), and `R0304` on `?x` needed a hint for its code.
- No ADR: each choice is local to the core and cheap to change.
