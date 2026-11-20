# The Sender, the game and "me"

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

Can a Trigger say "from the game" or "from myself", and can an Agent name itself as a Value?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- N4 The Sender can't be "the game" or "myself"
- N5 No word for "me"

Decide:

- A spelling for "from nobody" on a Trigger and on a recipe, and whether no `FROM` keeps meaning "anyone".
- What `FROM` on a recipe does to the Agent's own `PURSUE`.
- Which Sender a Goal has when a second request is ignored.
- A Value for the Agent itself, and where it may be written.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

## Resolution

Resolved on 2026-11-16, with the user.

- **N4, fixed.** The game and the Agent itself are not Senders, and two words name them: `FROM GAME` (what the game sent or reported) and `FROM ME` (the Agent's own `PURSUE`, `LEARN` or `CHANGE`). Each is legal only where it can match: `FROM GAME` on an Event and on `LEARNED`, in a Playbook or a Plot; `FROM ME` on `TO g`, a Goal's endings and `LEARNED`, in a Playbook only. `FROM` takes alternatives joined by `OR` (`TO take_seat FROM DIRECTOR OR ME:`), among `DIRECTOR`, `GAME`, `ME` and a bare Role, with no Placeholder and no quantity. **Kept**: no `FROM` matches anything; an own `PURSUE` is from `ME` and never takes the Sender of the Plan it is in, so it still fails under a recipe whose `FROM` doesn't list `ME`. Two new warnings report a `PURSUE` no recipe admits (which covers a repeating `FROM DIRECTOR` recipe) and an `ASK` when every recipe is `FROM ME`. The Sender of an ignored second request is no longer a question: every request is its own Pursuit (ADR 0017, from [*A Goal's life: reached, dropped, repeated*](02-goal-lifecycle.md)). **Not in 2.0**: `FROM` on `FORGOTTEN`, and a Director's own `LEARN` told from the game's.
- **N5, fixed.** `ME` is a reserved Value, the Agent running the Plan, legal wherever a Value is in a Playbook: `GIVEN NOT ?victim = ME`, `WHEN scandal(ME):`, an argument. It is filled in by the Agent that writes it and travels in a Message as that Agent. It is an error as a recipient and anywhere in a Plot, a Role setup included.

Changed:

- Spec: chapters 03, 05, 07, 08, 11, 16, 20 and 38. New codes: `R0309`, `R0509`, `R0510`, `R0511`, `R0512`, `R3805`, `R3806`. `R0704` reworded.
- ADR: 0020 *The game and the Agent itself are not Senders*.
- Glossary: *Sender* and *Value* reworded.

Handed on:

- The words `GAME`, `ME` and `OR` after `FROM` are open to [*Words and syntax*](20-words-and-syntax.md), with `BY` and `WITH`.
- The guide's *Messages*, *Goals and Failure* and the showcase still have the Guard's bare `saw_pouring` Plan, the two Messages for one insult, and the recipes with `FROM DIRECTOR` alone.
- The Jason chapters don't yet say how `FROM GAME`, `FROM ME` and the Value `ME` are generated; chapter 07 only notes `source(percept)`, `source(self)` and `.my_name`.

1.5, from [*Which systems Regia 1.5 keeps*](21-which-systems-1-5-keeps.md):

- N4 later: `FROM GAME`, `FROM ME`, `OR` and `R3805`/`R3806` are 2.0 only. Kept in 1.5: a Trigger with no `FROM` matches anything, and an own `PURSUE` has no Sender. N5 in.
