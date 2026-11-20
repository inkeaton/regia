# What can be said about a Role

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

Which parts of *Richer Mappings and Role tests* (chapters 15 and 26, not in 2.0) does the showcase need now?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- F1 Roles can be mapped and addressed, and little else
- D17 A Plot's Role and a Playbook's Role are told apart by a capital

Decide:

- Go through the ten notes of F1 one at a time: counted recipients, a pick per receiver, "everyone else", excluding a Role, Role tests in a Playbook, naming the Agent of a Role, a recipient for the whole Plot.
- For each: 2.0, later, or a check that at least warns.
- Whether Roles bind by name without a `MAPPING`, and what the capital letter means.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

## Resolution

Resolved on 2026-11-16, with the user.

- **F1, fixed, except the pick per receiver.** By note:
  - *Three roasts on one plate*: `TELL` and `ASK` take a counted recipient, `ASK 1 OF waiter TO bring(?dish).`, drawn each time the Statement runs. A count that finds nobody sends nothing, with a Trace warning, as for an empty Role.
  - *A Servant of their own*: **deferred**. A pick per receiving Agent (`EACH`) needs a binding per Agent inside one Giving, and goes with a Giving's identity. A counted `ASK` picks afresh per request in the meantime.
  - *Everyone else*, and *a knight who is Poisoner and Watchman*: a Plot's Role takes `EXCEPT <Role>` or `EXCEPT ?who` as a recipient, an `ASSIGN` target and the giver's side of a `MAPPING`. Not on `UNASSIGN`, `FROM`, `BY`, Quotas or `PLAYS`, and not in a Playbook.
  - *A Playbook can't ask which Roles an Agent plays*, *`DO lunge.` has no target*, *the Director can't name the one `Challenger`*, *`duel_abandoned` can't say who was duelling*: the condition `<who> PLAYS <Role>`, in Plots and Playbooks, matched like a Fact. It doesn't leave the Agent itself out, and it is a condition only. `COUNT(? PLAYS Guest)` counts a Role.
  - *No recipient between a Role and `EVERYONE`*: `CAST` is the Role every Agent of the Staging plays, each once. A Plot writes it wherever one of its Roles can be.
  - *`ASSIGN Courtesy` four times*: `CAST STARTS WITH:`, for the Plot and for a Phase, run before the Role setups.
- **D17, fixed.** Same-name binding ignores case, so a Plot's `Host` fills a Playbook's `host` with no `MAPPING`. The capital is a convention the language doesn't read. That a given Playbook has a Role is shown by the inferred Interface and the editor.

Settled while writing, not asked:

- `PLAYS` is the word Instancing already uses (`AGENT noble PLAYS Guest`), with the same meaning.
- There is no `!=`: the test for "someone else" is `AND NOT ?o = ME`.
- `WHEN CAST ?who JOINED` fires before the per-Role `JOINED` Plans, and `WHEN CAST … LEFT` after the per-Role `LEFT` Plans.
- `R1505` (`MAPPING ?who TO …`) was still listed although chapter 20 allows the form. It is no longer given.
- Recasting was sketched in chapter 19 as `CAST ?who AS Host`. With `CAST` reserved as a Role it will need another word. It stays out of 2.0.

Reopened by the user after the first write, and settled the same day:

- `UNASSIGN P FROM Guest` takes `P` from the Guests through every Giving this Staging made whose target includes `Guest`, Givings to `CAST` and the `CAST` setups included. A Giving to another Role or to one Agent is untouched. `UNASSIGN P FROM CAST` takes everything this Staging gave of `P`. The first write had kept a Cast Giving separate; the user ruled that adding and removing Playbooks per Role is the core of the language and must always work.
- A standing Cast Giving narrowed this way reads `CAST EXCEPT Guest`: a Guest who joins later doesn't get `P`, anyone else does. Narrowing twice gives a Giving several exclusions, which source can't write in 2.0.

Changed:

- Spec: chapter 15 (new sections *The whole Cast*, *A counted recipient*, *Leaving Agents out*, *Who plays a Role*), and chapters 07, 10, 16, 17, 18, 19, 20, 26, 34 and 38. New codes: `R1510`, `R1511`, `R1512`, `T1504`. `R1501` and `R1506` narrowed, `R1606`, `R1802` and `R1902` widened.
- ADRs: 0023 *A Role can be tested, and is still not a Value*; 0024 *The Cast is a Role every Plot has*.
- Glossary: *Role*, *Role setup*, *Cast*, *Mapping* and *Recipient* reworded.

Handed on:

- The pick per receiver, and `UNASSIGN` of one of two Givings to a Role: [*Telling Stagings and Givings apart*](08-stagings-and-casts.md).
- A Quota over part of a Role, and a Quota that knows who was asked: [*Quotas*](10-quotas.md).
- Whether an Agent hears of cast changes (a Trigger on `PLAYS`): [*Facts that are told, and news in general*](11-told-facts.md).
- `COUNT(? PLAYS Guest)` and `?x PLAYS CAST` are part of what N7 asks for: [*What a Director knows about itself*](09-director-state-and-endings.md).
- The words `CAST`, `EXCEPT` and `PLAYS` are open to [*Words and syntax*](20-words-and-syntax.md).
- The Jason chapters 29, 30 and 33 don't yet describe a counted recipient drawn by an Agent, `PLAYS` against the cast copy, a binding with `EXCEPT`, the `CAST` Role, or the `CAST` setup.
- The guide's *Messages*, *Playbooks and Roles*, *Plots and Directors*, *Subplots and Stagings*, *Randomness* and the showcase still have the three roasts, the `duel_won` Signal, the duellists wagering on their own duel and the four `MAPPING Host TO host` lines.

1.5, from [*Which systems Regia 1.5 keeps*](21-which-systems-1-5-keeps.md):

- F1 in, except `JOINED` on `CAST` and Cast Givings reaching joiners. D17 in.
