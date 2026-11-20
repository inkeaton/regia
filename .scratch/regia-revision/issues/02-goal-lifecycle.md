# A Goal's life: reached, dropped, repeated

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

Which Triggers does a Goal have, what tells two pursuits of one Goal apart, and how does a recipe repeat?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- N1 No Trigger for a Goal that is reached, or that is over
- D5 A Goal's arguments are its identity
- D6 A `DROP` goes down as a drop and up as a Failure
- B7 "Pursuing its Goal again" doesn't repeat

Decide:

- A Trigger for "reached", one for "over, however it went", both or neither; and whether a Director can hear them without a Signal.
- Whether a second request for a running Goal is still ignored, and what keeps two orders of roast apart without an argument added for that.
- What a waiting Body sees when the Goal it waits on is dropped.
- Fix the contradiction between chapters 06 and 08, and decide whether a `FAILED` Plan that pursues the failed Goal is checked.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

## Resolution

Resolved on 2026-11-16, with the user.

- **N1, fixed.** Two new Trigger kinds on a Goal: `REACHED`, and `ENDED`, which fires after whichever of `REACHED`, `DROPPED` or `FAILED` fired. All are notifications. A Director hears the four endings of a Goal it asked itself, with no Signal: `WHEN take_seat FAILED FROM Guest ?g`, `WHEN take_seat ENDED FROM ALL Guest`. In a Plot `FROM` names the Agent whose Goal it was; an ending with no Plan is silent; a Trigger on a Goal the Plot never asks is an error (`R2012`). The word `ENDED` is provisional, for [*Words and syntax*](20-words-and-syntax.md).
- **D5, fixed.** Every request starts a **Pursuit** of its own, with its own Sender. Nothing is ignored or joined, so `bring` and `fetch` lose the seat. A Goal that must not run twice writes `GIVEN NOT PURSUING g`; inside a recipe for `g`, `PURSUING g` leaves out the recipe's own Pursuit. `DROP g` stops every Pursuit of `g`.
- **D6, fixed.** A drop spreads upward as a drop: the waiting Body stops, its Pursuit fires `DROPPED` and `ENDED`, and no Failure is written. `T1102` covers only a waited-on Goal that fails.
- **B7, fixed.** A recipe repeats by ending with `PURSUE g, WITHOUT WAITING.`; each round is a Pursuit, and from the second round it has no Sender. The waiting form, unguarded, is a warning (`R0806`). A `WHEN g FAILED` Plan that pursues `g` unguarded is a warning (`R1103`). Loops proper stay deferred with F5.

Changed:

- Spec: chapters 05, 06, 07, 08, 11, 17, 18, 20, 34 and 38.
- ADRs: 0017 *Every request is its own Pursuit*; 0018 *A drop spreads as a drop*.
- Glossary: *Pursuit* added; *Director*, *Signal*, *Trigger*, *Trigger kind*, *Sender* and *Failure* reworded.

Handed on:

- Whether an asking Agent hears an ending as a Director does: [*How an Agent learns why something failed*](03-failure-and-replies.md).
- `UNASSIGN` drops a Goal whose `DROPPED` and `ENDED` Plans sit in the Playbook that has just gone, and a Director can't call off a Goal it asked: [*Givings and joiners*](05-givings-and-joiners.md).
- The Jason chapters don't yet describe Pursuits without joining, the generated `REACHED` and `ENDED` events, or the report of an ending to the asking Director; chapters 08, 11 and 20 only note them.
- The guide's *Goals and Failure* and the showcase still carry the done-Signals and the seat.

1.5, from [*Which systems Regia 1.5 keeps*](21-which-systems-1-5-keeps.md):

- N1 in for an Agent's own Pursuits; later for a Director hearing the endings of a Goal it asked. D5, D6 and B7 in.
