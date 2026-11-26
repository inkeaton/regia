# Cut M1 into tickets

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 01, 06

## Question

Cut the lexer milestone into implementation and exercise tickets, from the resolutions of *Review: text to tokens* and *Review: how we test*.

Starting list, to be reordered: ownership drill; a cursor over `&str`; token kind and range; names and keywords; numbers and strings; comments; terminators and dotted names; indent stack; dedent errors; continuation lines; prints-back test over the showcase; move into `regia-core`.

From *Review: how we test*: token dumps are `insta` snapshots (the first ticket using them adds `insta` and installs `cargo-insta`); the prints-back test covers the showcase and every file in `docs/spec/cases/`.

## Resolution

Cut on 2026-11-26 into tickets 14–34, in the Rust Book's order (ch 4, 5, 6, 7, 8), so each ticket brings at most one new concept:

- **ch 4–6, scan in `regia-cli`:** *Drill: ownership, borrowing and slices*; whitespace and line breaks (structs); names and every reserved word (enums, `match`); *The token dump* (adds `insta`); *A stray character is R0112* (`enum Code`, Diagnostics beside the tokens); Placeholders, punctuation and operators; STOP and dotted names (`Option`); numbers and `R0401`.
- **ch 7:** *The lexer moves into regia-core*. Moved from the end of the starting list to the middle, to follow the book and move less code; everything after it is written in `regia-core`.
- **ch 8, the rest of scan:** *Drill: vectors, Strings and hash maps*; Strings and `R0113` (UTF-8, non-ASCII ERROR tokens); line and doc comments and `R0202`; multiline comments and `R0201`.
- **ch 8, layout:** NEWLINE; continuation lines; INDENT and DEDENT; `R0104`; `R0105`; `R0103`; indentation after a multiline comment.
- **Closing M1:** *Print-back over the showcase and every case*, with a token-dump file snapshot of `courtesy.regia`.

Conformance cases: `R0112` and `R0104` already have one. The tickets for `R0401`, `R0113`, `R0202`, `R0201`, `R0105` and `R0103` write theirs first; they run from M3, so the red test in M1 is a unit test. *Cut M2 into tickets* opened, blocked by the last M1 ticket and by *Readable generated ASL* (M2 emits a `.asl`).
