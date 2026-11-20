# Facts that are told, and news in general

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

When is something a told Fact, an Event or a Signal, and can what was told be taken back or kept true?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- D10 What an Agent or a Director has been told stays as it was
- L5 A kind word follows the item, except for Goals and Messages (ADR 0003)

Decide:

- Taking a told Fact back, and who counts as its teller.
- A Director's copies of what Agents sent, when the Agent leaves.
- Whether Agents hear of cast changes.
- Whether `TELL` should show that it tells a Fact or an Event. Confirm or reopen ADR 0003.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

## Resolution

Resolved on 2026-11-17, with the user.

- **D10** kept, all four rows.
  - Taking a told Fact back: Messages still only add, and an undoing Message stays deferred past 2.0. The receiver forgets in its own Plans, usually the Playbook's `WHEN UNASSIGNED:` (`Keeping_watch` forgets `on_duty`). A Director that wants it gone at a moment of its own asks for a Goal whose recipe forgets it.
  - Who counts as the teller: only the first teller of a Fact is heard, because a Fact is a belief and repeating it changes nothing. Telling a Fact or an Event is chosen by what the receiver should do with it: what lasts, or each telling. Counting tellers is an Event plus a Quota, which can read who it counted with `SENT` (ticket 10). `TOLD` stays reserved.
  - A Director's copies after an Agent leaves: Facts naming a leaver stay, since some are meant to outlive it. The Director tidies its record on `WHEN Role ?who LEFT:` with `FOR EACH … FORGET`, and a Message to the leaver shows in the Trace as `T1901`. This is a game-design hazard the writer can avoid.
  - Agents hearing of cast changes: they don't. The Director passes it on or ends the Staging, which takes the Playbook away. A Playbook Trigger for its own Roles is deferred past 2.0: Playbook Roles are bound per giving.
- **L5** kept. ADR 0003 is confirmed: `TELL` doesn't show the kind, because the name's one kind does, and the Vocabulary and the editor show it.

Changed:

- Spec:
  - Chapter 07: `TELL` and the kind, *A Fact or an Event*, *Taking a told Fact back*.
  - Chapter 19: Facts naming a leaver stay, with the `LEFT` tidy-up; *What the Agents hear*; *Not decided here* updated.
- ADR: none. ADR 0003 stands.
- Glossary: none.

Handed on:

- To the guide (fog on the map): the `#revise` notes for D10 and L5 now have spec patterns to point to.

1.5, from [*Which systems Regia 1.5 keeps*](21-which-systems-1-5-keeps.md):

- D10: in. Nothing is added, and the patterns use `WHEN UNASSIGNED:`, `LEFT` and `FOR EACH`, which are all in 1.5. Counting tellers with a Quota is later, along with Quota Triggers.
- L5: in.
