# Failure a Plan can read, and answers to an `ASK`

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

How does an Agent learn why something failed, and how does whoever asked learn how it went?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- N6 A Failure has no reason a Plan can read
- F3 A request has no reply
- L3 `PURSUE` waits and `ASK` does not (ADR 0005)

Decide:

- Whether `FAILED` carries a reason, and what the reasons are.
- Whether a `WHEN` Plan's Failure or a non-waited Action's result can be reacted to.
- Whether any part of replies (chapter 07's reserved clauses) comes into 2.0, since the showcase reports a Failure by sending the Signal for success.
- Confirm or reopen ADR 0005.
- Whether an asking Agent hears how its `ASK` ended, as a Director now does through `REACHED`, `DROPPED`, `FAILED` and `ENDED` (spec 20, from [*A Goal's life: reached, dropped, repeated*](02-goal-lifecycle.md)).

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

## Resolution

Resolved on 2026-11-16, with the user.

- **N6, fixed in part.** `FAIL WITH <event>.` gives a Failure a **Reason**, read by `WHEN g FAILED WITH r`. The Reason is one declared Event with filled arguments, as an Outcome is. It travels unchanged up the chain of waiting Plans and to whoever asked; a Goal in the chain can't replace it. Only `FAIL WITH` gives one: the mechanical causes stay in the Trace and get no names in the language. `FAILED` Plans with and without `WITH` share a Trigger and are tried in written order; plain `FAILED` matches every Failure and there is no `WITH ?why`. **Kept**: a failed `WHEN` Plan can't be reacted to (it has no name; wrap the step in a Goal). **Deferred**: reacting to how a `DO a, WITHOUT WAITING.` ended; chapter 08 gives the recipe that puts the Action in a Goal.
- **F3, fixed in part.** An asking Agent hears `REACHED`, `DROPPED`, `FAILED` and `ENDED` for a Goal it asked, with a new clause, `BY`, that names who pursued it: `WHEN bring(?dish) FAILED WITH sold_out(?dish) BY waiter ?s`. `FROM` after a Goal's ending always means who asked; a Plot moves from `FROM` to `BY` (`WHEN take_seat ENDED BY ALL Guest`). `BY` takes the Quota forms, in a Playbook too; a Quota with `WITH` is an error. An Agent that leaves the Program reports nothing for its Pursuits. **Deferred**, still reserved: `, AND WAIT` on an `ASK`, `REFUSE`, `AGREED`, `REFUSED`. A refusal is written `FAIL WITH …` in a `TO g FROM …` Plan. An Agent can't call off a Goal it asked.
- **L3, kept.** ADR 0005 is confirmed: `PURSUE` waits and `ASK` does not. The asker reacts to the ending with a Trigger.

Changed:

- Spec: chapters 05, 07, 08, 10, 11, 18, 20, 34 and 38. New codes: `R0506`, `R0507`, `R0508`, `R1104`, `R1105`, `R1106`, `R1805`, `R2013`, `R3804`. `R0706` and `R1801` reworded.
- ADR: 0019 *A Goal's ending is heard by whoever asked, and a Failure carries a Reason*.
- Glossary: *Reason* added; *Failure*, *Sender*, *Signal* and *Interface* reworded.

Handed on:

- Whether an Agent can hear that another Agent left, for an asker waiting on `BY ?s`: [*Facts that are told, and news in general*](11-told-facts.md), which already asks whether Agents hear of cast changes.
- The words `BY` and `WITH` on a Goal's ending are open to [*Words and syntax*](20-words-and-syntax.md), with `ENDED`.
- The Jason chapters don't yet carry a Reason along the failure chain, or the report of an ending from Agent to Agent; chapters 07, 11 and 20 only note them.
- The guide's *Goals and Failure*, *Messages* and the showcase still carry the hand-written replies (`sold_out`, the minute's wait in `Dining`).

1.5, from [*Which systems Regia 1.5 keeps*](21-which-systems-1-5-keeps.md):

- N6 in for a Reason read along the Agent's own waiting chain; later for a Reason reaching the asker. F3 later: no `BY`, and the asker hears no ending. L3 in.
