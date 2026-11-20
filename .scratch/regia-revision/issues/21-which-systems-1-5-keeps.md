# Which systems Regia 1.5 keeps

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

2.0 adds many systems to 1.0 at once. Regia 1.5 is a full version of the language, built first by the same Transpiler and Visual Editor, with a subset of 2.0's systems. Which systems are in it?

The revision goes on deciding all of 2.0, so the systems keep fitting together. This ticket decides which ones go into 1.5; the cause-by-cause cut is [*The Regia 1.5 cut*](22-the-1-5-cut.md).

## Resolution

Resolved on 2026-11-17, with the user. The systems are those of 2.0, compared with the primer's 1.0.

**In 1.5:**

- Layout syntax, Scoping (local Events included), Instancing.
- Placeholders (the Value `ME` included), Expressions, Match selection.
- Goals and Pursuits, Trigger kinds (`REACHED` and `ENDED` for an Agent's own Pursuits), Failure (`FAIL WITH` and `FAILED WITH`, read along the Agent's own waiting chain).
- `GIVEN` and `IF`, Random choice, Time.
- Messages, without hearing how an asked Goal ended (below).
- Part of Event origins: `FROM Role`, `FROM ?who`, `FROM Role ?who`, `FROM DIRECTOR`. A Trigger with no `FROM` still matches anything.
- Inferred Interfaces, without the checks on what is later (`R3805`, `R3806`).
- Precedence, Labels and Propensities.
- Playbook Roles, Mappings and Givings, Role setup.
- Counts and the Cast: counted recipients and picks, `EXCEPT`, `CAST` and its setup, `PLAYS`. The user first left this out and then kept it.
- The Director model, Subplots and Stagings.
- Cast changes, leaving only: `LEFT` and `EMPTIED`, and a leaver's Givings taken away.
- The Trace and behaviour cases, for what is in.

**Later, in 2.0 and not in 1.5:**

- `FROM GAME`, `FROM ME`, and `FROM` with `OR` alternatives.
- `BY`, and with it the asker hearing a Goal's endings: neither a Director nor an Agent hears `REACHED`, `DROPPED`, `FAILED` or `ENDED` for a Goal it asked, and a Reason doesn't reach the asker.
- Quota Triggers.
- Joining: `JOINED`, Givings that stay standing for joiners, and setups run for a joiner. The cast of a Staging is fixed when it starts and can only shrink.

What this costs, accepted:

- A Director or an Agent that needs to know an asked Goal ended is told so by a Signal or a `TELL` written in the recipe, the pattern 2.0 removed.
- "Every Guest has done it" is written by hand: the Director records each Signal in a Fact of its own and compares `COUNT` over it with `COUNT(? PLAYS Guest)`.

Changed:

- ADR: 0025 *Regia 1.5 is a subset of 2.0, built first*.
- Map: Destination and Notes; the closed tickets got a *1.5* line.
- No spec chapter yet: how 1.5 is marked in the spec is [*The Regia 1.5 cut*](22-the-1-5-cut.md).

Handed on:

- Whether a setup is still sugar for `ASSIGN` plus a `JOINED` Plan when there is no `JOINED` in 1.5, and what "standing" means for a Giving with no joiners: [*The Regia 1.5 cut*](22-the-1-5-cut.md).
- [*Quotas*](10-quotas.md) is decided for 2.0 only, and the parts of [*Facts that are told, and news in general*](11-told-facts.md) about cast changes affect 1.5 only for leaving.
