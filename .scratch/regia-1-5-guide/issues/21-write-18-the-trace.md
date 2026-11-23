# Write guide chapter 18, The Trace

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 05

## Question

Write `docs/guide/18-the-trace.md`, *The Trace*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 34.
- **Covers:** what it records, entry fields, the failure chain, Trace codes, the console line, behaviour cases and their scripts (`link` steps, `> lose link`).
- **Quotes most:** throwaway traces of a banquet run.
- **"In 2.0" notes:** `count` entries, `T1801`, `T1802`, departures, `JOINED` in `cast` entries.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.

## Resolution

Done on 2026-11-20 (task). [`docs/guide/18-the-trace.md`](../../../docs/guide/18-the-trace.md), about 530 lines, written from the template:

- An opening table of the three forms of an entry (file, console line, expected line).
- Sections: Reading a run (the banquet's first moments as a table of `seq`, `agent` and console line); Kinds of entry (the 1.5 kinds with their console texts); Fields (common and per kind, with *Names*: Agents of a kind, `director:<Plot>#<n>`); Why a Plan ran (`Keeping_watch OVER NobleSocializing ON scandal` as an entry); What didn't run (`T0702` at a Servant, `T3801` for `insult_thrown` in `reception`, `T3802` by a throwaway without `WHEN HonorDuel(?) ENDED`); The failure chain (the Guest with no seat, *When a Director's Plan fails* with `open_doors`, *A drop is not a Failure* with `DROP strike`); Trace codes (every 1.5 code in *Checks*); The console; Behaviour cases (a throwaway `cases/no_seat/` case, *The script* with case errors in *Checks*, *Time, chance and order in a case*, *Expected lines and matching*).
- Three "In 2.0" notes: `count` entries, departures and `JOINED`; `T1801`/`T1802` and `T1902` retired; `> join` and `#! regia:`.
- `T1102` left out, as in *Goals and Failure*. The example case leaves out the Guest's `took_seat` Signal, since nothing orders a Goal's `FAILED` and `ENDED` Plans.
- Showcase snippets checked against their files by script (5 linked snippets); traces and the case are throwaways. Grep for retired spellings: none. The humanizer pass removed one dash and one aphorism.
- No `Guide:` line added: the showcase README's *Coverage* has no heading for chapter 34 (it covers 01–21, 26 and 38).

Four non-blocking findings: `T0902`/`T0903`/`T2601` have no kind (and `T0403` is missing from chapter 34's table); console texts fixed only by example; nothing scriptable before `> start` but link Facts; when the virtual clock jumps around steps.
