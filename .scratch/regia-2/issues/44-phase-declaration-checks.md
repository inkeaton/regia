# Phase declaration checks

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo

## Question

Which checks apply to a Plot's Phases, and in which chapter (20 is the natural home)? Decide:
- Whether a Plot must declare exactly one `INITIAL` Phase, whether a Plot may have no Phases at all (only `DURING PLOT` and Role setups), and what is reported for zero or several `INITIAL` Phases.
- A `DURING p:` or `TRANSITION TO p` naming a Phase the Plot doesn't declare (`R1303` already covers a relation naming one).
- A declared Phase with no `DURING` Block, and one that nothing transitions to: warnings, or nothing.
- Their codes, `R20nn`, continuing after `R2006`, and an exemplar case if a new chapter section is the result.

## Answer

Written into chapter 20's new *Declaring Phases* section and its checks (`R2007`–`R2011`). Chapters 25 and 30 and the glossary's *Phase* entry were updated too. No ADR.

- A Plot that declares Phases marks exactly one `INITIAL`, even with a single Phase. Zero or several is `R2007`, with a quick fix.
- A Plot may declare no Phases: only Role setups and `DURING PLOT`. Jason gives it a hidden initial Phase, `regia_phase__plot`, which is never left, writes no Trace entry, and is drawn as a single node. Any `TRANSITION TO` in such a Plot is `R2008`.
- `DURING p` or `TRANSITION TO p` naming an undeclared Phase is `R2008`, with a "did you mean" hint. Two Blocks for one Phase, or two `DURING PLOT`, is `R2009`. `PHASE`/`DURING` in a Playbook is `R2010`.
- The only warning is a Phase that can never be entered: not `INITIAL`, and no `TRANSITION TO` names it (`R2011`). A Phase with no `DURING` Block, or one that nothing leaves, is fine.

## Comments

- Surfaced by *Number the checks and add exemplar cases* (42), 2026-11-11: no chapter states these checks, and the 22 exemplar cases assume one `INITIAL` Phase per Plot.
