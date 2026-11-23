# Write guide chapter 14, When an Agent leaves

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 05

## Question

Write `docs/guide/14-when-an-agent-leaves.md`, *When an Agent leaves*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 19.
- **Covers:** leaving, `LEFT`, `EMPTIED`, a leaver's Givings taken away, its Picks and bindings dropped, what the Director tidies, `T1901`; a spawn refused with `T1902`.
- **Quotes most:** `royal_banquet.regia`, `honor_duel.regia`.
- **"In 2.0" notes:** joining and `JOINED`; Quota Triggers (spec 18) as a whole, since no other chapter hosts them.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.

## Resolution

Done on 2026-11-20 (task). [`docs/guide/14-when-an-agent-leaves.md`](../../../docs/guide/14-when-an-agent-leaves.md), about 310 lines, written from the template:

- An opening table of the chapter's words (`DO leave_hall`, `LEFT`, `EMPTIED`, `CAST` with both).
- Sections, simple to full: Leaving the Program (`take_leave`, the cowardly Defender, `leave_hall`'s doc comment, only the game removes, the `cast` Trace entry and `> leave`); What goes with it (a table of what happens to Roles, Givings, Plans, waiting `DO`s, bindings, counted picks, Messages, Values and Facts; `T1901`); Hearing it: `LEFT` (the banquet's hand count) with *Tidying what the Director knows* (`HonorDuel`'s wagers and the Pick that would choose a leaver); `EMPTIED` with *An empty Role* (a throwaway `Poisoner EMPTIED`); The whole Cast (a throwaway); Order when leaving (Sir Percival's Roles, a mermaid flowchart of the Defender walking out); What the Agents hear (`Duelling`'s `REMOVED`); Nobody joins (`T1902`, `R0109`).
- "In 2.0" notes, as listed: Quota Triggers as a whole (under `LEFT`, as the hand count's replacement), and joining with `JOINED` (under *Nobody joins*).
- Throwaway snippets: `Poisoner EMPTIED`, `CAST ?who LEFT` / `CAST EMPTIED`.
- Every showcase snippet checked against its file by script (10 snippets). Codes appear in *Checks* only; they borrow `R0109` and `R1703`.
- `Guide: When an Agent leaves` added under *19 Cast changes* in the showcase README.
- Grep for retired spellings: none. The humanizer pass rewrote two phrases ("Nothing. Only Directors hear…", a not-X-but-Y on `REMOVED`).

Two non-blocking findings: what a Director's `ASSIGN`/`MAPPING` does with `?who` from `LEFT` (and its code); the order in which several Directors hear one leave.
