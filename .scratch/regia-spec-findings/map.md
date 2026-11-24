# Map: Closing the 1.5 guide's findings in the spec

Label: wayfinder:map

## Destination

Every finding in [`../regia-1-5-guide/findings.md`](../regia-1-5-guide/findings.md) is closed in `docs/spec/`, `GLOSSARY.md` or `docs/adr/`: fixed, or ruled intended with the spec saying so plainly. The guide in `docs/guide/` follows every decision, and its README paragraph on details the spec leaves open lists only what is still open.

Charted with the user on 2026-11-23.

## Notes

- **This map carries execution.** Each theme has a *Decide* ticket (grilling, HITL) and an *Apply* ticket (task, AFK) that edits the spec, glossary and ADRs to match. The obvious slips have one task ticket of their own and come first.
- **Findings are cited as F\<line\>**: the line number of the finding in `../regia-1-5-guide/findings.md`. That file is frozen; don't edit it. New findings go one per line into this map's [`findings.md`](findings.md), with the ticket that found them, and are handled here when they're in scope.
- **The guide's reading is the default.** Every finding says what the guide did ("The guide reads it as…"). A *Decide* ticket starts each question from that reading as its recommended answer, unless it is clearly worse.
- **The guide is fixed in the same session.** Each *Apply* ticket (and the slips ticket) fixes the guide passages its findings name, and removes from the README paragraph (*How a chapter reads*, "In some places the spec leaves a detail open…") any point it settles. The final ticket only checks.
- **ADRs only for behaviour.** A decision gets an ADR when it changes what the language or a Target does (a new Trace kind, a retired code, a way to empty setup lines). A code assignment or a wording fix lives in the spec alone. Codes are never reused; a dropped one is marked retired (spec chapter 27).
- **The showcase changes only when the text can't.** Prefer fixing the spec or the README; change a showcase file only when the README promises coverage the spec needs shown, and re-point every spec and guide citation into it in the same ticket.
- **Order is priority, not blocking.** Slips, Diagnostic codes, Trace, runtime, Instancing, Interfaces and Precedence, Jason, Visual Editor, command line, showcase README, 2.0 only. *Decide* tickets don't depend on each other and can run in parallel. *Apply* tickets wait for their *Decide* and for the slips sweep, since both edit the same chapters.
- **Strictly 1.5 first.** 2.0-only findings (F6, F83) come last and are fixed only in the chapters that already describe them.
- Every *Apply* ticket ends by grepping its edited chapters for retired spellings (spec chapter 01's table) and re-reading the guide passages it touched against the new spec text.
- Tickets: `.scratch/regia-spec-findings/issues/NN-<slug>.md`, with `Type:`, `Status:`, `Assignee:` and `Blocked by:` lines. The frontier is the open, unblocked, unclaimed tickets, lowest number first.
- Skills: `grilling` and `domain-modeling` for every *Decide* ticket; `humanizer:humanizer` on any guide prose rewritten. Memories: *Guide is a 1.5 reference*, *Language vs game design*, *Java is plumbing only*, *Regia is generated too*.

## Decisions so far

<!-- one line per resolved ticket: [title](issues/NN-slug.md): gist -->

- [Fix the obvious slips](issues/01-fix-obvious-slips.md): all 19 slips fixed in the spec, with the guide's reading (chapter 36 rebuilt on the banquet). Two more slips were found and fixed on the way. The guide needed no changes.
- [Decide: Diagnostic codes and the Vocabulary](issues/02-decide-diagnostic-codes.md): guide readings kept (`R2005` goes further, to cover Subplot endings); `R1016`, `R0305`, `R0404`, `R2005`, `R3802` widened; `R1501` retired into `R0303` (needs an ADR); new `R2607` for `GIVEN n OF`; `ROLE` order is a convention; Names aren't Vocabulary.
- [Apply: Diagnostic codes and the Vocabulary](issues/03-apply-diagnostic-codes.md): all applied in spec chapters 02–04, 09, 10, 12, 15, 17, 20, 26, 38, the glossary and ADR 0048 (`R1501` retired); guide Checks follow; the guide README no longer lists uncoded misuses as open.

## Not yet specified

- Findings that editing the spec will surface. They land in `findings.md` and become tickets once their theme is clear.
- Whether some decisions overlap enough to share an ADR (for example, a Trace kind for non-warning codes and retiring `T1102`); seen only once the Trace tickets are decided.

## Out of scope

- Writing the showcase runs (`runs/evening`, `runs/two_duels`, `runs/short_evening`) and the Jason reference Build: the showcase hand-off effort. F47 is only noted for it.
- Constructs only Regia 2.0 has, beyond fixing the two findings about chapters that already exist.
- Restructuring the guide or the spec beyond what a finding needs.
- Editing `docs/primer/`.
