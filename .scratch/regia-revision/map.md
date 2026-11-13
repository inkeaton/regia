# Map: Regia 2.0 revision

Label: wayfinder:map

## Destination

A decision for each of the 70 causes in `docs/guide/20 - Review List.md`: fixed in 2.0, kept as it is, or deferred. The decisions are carried into `docs/spec/`, `docs/adr/` and `GLOSSARY.md`, so that the spec handed to development is the revised one.

Confirmed by the user on 2026-11-13: a ticket closes when its spec chapters, ADRs and glossary entries are edited, not when the answer is agreed.

## Notes

- **One ticket per group of causes**, not per cause and not per `#revise`. Causes that the Review List cross-references are discussed together. Every cause (B1 to B16, L1 to L9, N1 to N15, F1 to F10, D1 to D20) is in exactly one ticket, except D1, D15, D16, F10 and L8, which are split by subject.
- **The Review List's five parts are a proposal.** A ticket may move a cause from one part to another.
- **Deliberate limits are confirmed or reopened inside the ticket of their subject.** There is no separate ticket for them.
- **Resolution**: one line per cause (fixed, kept, deferred), then the spec chapters, ADRs and glossary entries changed. A reopened ADR is superseded by a new one, not edited.
- **The guide is not kept in step here.** `docs/guide/` and its showcase describe the design before this revision. Updating them is under *Not yet specified*.
- Source material: the Review List for the causes, the guide chapters it names for the examples, `docs/guide/showcase/README.md` for *Spec wording* and *Gaps in the showcase*.
- Tickets: `.scratch/regia-revision/issues/NN-<slug>.md`, with `Type:`, `Status:`, `Assignee:` and `Blocked by:` lines. The frontier is the open, unblocked, unclaimed tickets, lowest number first.
- Skills: `grilling` and `domain-modeling` for every ticket.

## Decisions so far

<!-- one line per resolved ticket: [title](issues/NN-slug.md): gist -->

## Not yet specified

- The spec contradictions under *Spec wording* in the showcase README, and the glossary fixes listed in the guide's map. Some will be settled by the tickets above; what is left afterwards may need a ticket of its own.
- Bringing the guide and the showcase up to the revised design: which chapters change depends on what is decided.
- New Conformance cases and Diagnostic codes for whatever is added.

## Out of scope

- Building the Transpiler or the Visual Editor.
- Features that no `#revise` asked for.
