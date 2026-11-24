# Final check: every finding closed

Type: task
Status: open
Assignee:
Blocked by: 01, 03, 05, 07, 09, 11, 13, 15, 17, 19, 21

## Question

Check the destination:

- every finding F6–F88 in `../regia-1-5-guide/findings.md` has a ticket whose resolution fixed it or ruled it intended, and every in-scope line of this map's `findings.md` is handled;
- the guide README's paragraph on open details lists only what is still open, or is removed if nothing is;
- a grep of `docs/spec/`, `docs/guide/` and `GLOSSARY.md` finds no retired spelling and no code the decisions retired;
- the guide's *Checks* lists agree with the spec's *Transpiler checks* for every code a ticket touched.

Fix small gaps in place. Anything bigger becomes a new ticket.

Done when the checks pass.
