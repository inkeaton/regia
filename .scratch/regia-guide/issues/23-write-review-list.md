# Write: Review List

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 22

## Task

Write `docs/guide/20 - Review List.md`: every `#revise` in the guide and the showcase README, collected and grouped by system, each with its chapter, the one-line reason, and the spec chapters a change would touch. Add a short section on what the whole guide shows that no single chapter does (constructs that read alike, systems that overlap, ceremony that repeats). No design changes: this list is the input to a later effort.

## Resolution

Written on 2026-11-13: [`docs/guide/20 - Review List.md`](../../../docs/guide/20%20-%20Review%20List.md), about 7,200 words. Not yet read by the user, and not passed through `humanizer`.

At the user's request the list is not grouped by system. The roughly 225 `#revise` notes are reduced to 70 causes (one miss that explains several notes is one entry), and the causes are sorted by the answer they call for:

- Bugs (B1 to B16): two rules that disagree or a result nobody chose, such as dotted External names that Jason refuses, Role setups that run before the first Quota counts, `PERCENT` rounding two ways.
- Deliberate limits (L1 to L9): decisions with an ADR or a spec section behind them, with what they cost in the showcase.
- Features for 2.0 (N1 to N15): a Trigger for a Goal reached, a start and an end for a Giving, a declared interface between Playbook and Plot, "from the game" and "me", a readable Failure, a Director that can ask about its own state, starting Facts per kind, a fuller command line, a Trace of what didn't happen, `DURING PLOT` on the default drawing.
- Features for a later version (F1 to F10): what the spec already lists as not in 2.0. F1 (Role tests and richer Mappings) and F2 (identity of Givings and Stagings) explain more notes than any 2.0 cause.
- To discuss (D1 to D20): no decision exists, starting with a table of eleven words that do several jobs.

Each cause lists its notes by chapter and the spec chapters a change would touch. A closing section has eight patterns no single chapter shows (the Playbook/Plot seam, silence at run time, four mechanisms for "which Plan runs", ceremony that repeats, Comments doing the language's work, workarounds whose words say the opposite).

The sorting into the five parts is a proposal. Which version a feature belongs to, and whether a limit stays, is for the revision effort to decide. The spec contradictions, the showcase gaps and the glossary fixes are not `#revise` notes and stay where they are (README and the map).
