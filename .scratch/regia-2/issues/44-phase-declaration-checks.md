# Phase declaration checks

Type: grilling
Status: open

## Question

Which checks apply to a Plot's Phases, and in which chapter (20 is the natural home)? Decide:
- Whether a Plot must declare exactly one `INITIAL` Phase, whether a Plot may have no Phases at all (only `DURING PLOT` and Role setups), and what is reported for zero or several `INITIAL` Phases.
- A `DURING p:` or `TRANSITION TO p` naming a Phase the Plot doesn't declare (`R1303` already covers a relation naming one).
- A declared Phase with no `DURING` Block, and one that nothing transitions to: warnings, or nothing.
- Their codes, `R20nn`, continuing after `R2006`, and an exemplar case if a new chapter section is the result.

## Comments

- Surfaced by *Number the checks and add exemplar cases* (42), 2026-11-11: no chapter states these checks, and the 22 exemplar cases assume one `INITIAL` Phase per Plot.
