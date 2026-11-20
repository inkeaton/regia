# Which Plan runs

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

Text order, falling through and Precedence each decide part of which Plan runs for a Trigger. Is each rule right, and do they fit together?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- L2 `GIVEN` is the Context and `IF` is control flow (ADR 0004)
- D2 A missing `ELSE` means two things
- D3 Name order is the default Precedence
- D4 A Subplot orders itself against a parent it can't see
- B8 A default order can close a cycle
- L6 Precedence is written where Playbooks are put together (ADR 0008)
- F6 One Plan per Trigger, and Plans that know nothing of each other

Decide:

- Whether Statements may stand before or after `GIVEN` branches. Confirm or reopen ADR 0004.
- What a missing `ELSE` means, and whether falling through is written out.
- The default order: name order, an error, or something a rename can't change.
- `PARENT`, `SELF`, and whether a default gives way in a cycle.
- From chapter 13's *Not in 2.0*: a Phase Plan that adds to `DURING PLOT`'s, and Actions that can't run together. 2.0 or later.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

## Resolution

Resolved on 2026-11-17, with the user.

- **L2** kept. ADR 0004 stands: no Statements before, between or after `GIVEN` Blocks. A prefix would look as if it ran before the Context check, and a shared tail would make a `GIVEN` Block less than one Plan. A `GIVEN` chain with an `ELSE` does what an `IF` chain filling the Body does, so `Wagering` and `HonorDuel` write their shared last lines once after an `IF`. A chain is worth writing when a case should fall through, or needs its own `SHIFTS` or its own Trace entry. No warning either way.
- **D2** fixed in wording, kept in meaning. A missing `ELSE` means one thing for every Trigger: the Trigger falls through to the next candidate. A recipe falls through to another Playbook's recipe like an Event does; only the end of the order differs (an Event is dropped, a Goal fails). Falling through stays implicit. An `ELSE` or a Block with no Context is a full stop, and the conflict report marks it and the candidates it makes unreachable. No warning: stopping a Trigger is power the writer uses.
- **D3** kept. Name order stays the last resort with its warning. Every order a rename can't change is as invisible as the alphabet, an error demands relations for pairs that never meet, and a random pick is irreproducible. The Visual Editor's rename should say when it flips such a pair (handed to ticket 18).
- **B8** fixed. Written relations, `PARENT` ones included, are placed first; a default is added only if it doesn't contradict what they imply. A default is never part of a cycle. `SELF OVER Poisoning ON scandal` in `RoyalBanquet` becomes unnecessary. New note `R1312`.
- **D4** kept, with `SELF` given one meaning: a Plot's own Playbooks and Director Plans. A Subplot moves with its whole subtree because of the hierarchy, not because `SELF` means more. `PARENT` is a statement about the Subplot's own Plans and stays; a Subplot still can't place itself against siblings. The showcase comment on `HonorDuel`'s line should speak only of `Wagering`.
- **L6** kept. ADR 0008 stands. Reading the order whole is the conflict report's job, and its command goes to ticket 16.
- **F6** deferred past 2.0, whole. Chapter 13's *Not in 2.0* adds a Phase Plan that adds to `DURING PLOT`'s, and says Actions that can't run together need a body model. The `IF hungry`/`DROP` race is a game-design hazard the Trace shows.

Changed:

- Spec:
  - Chapter 05: a second request falls through before it fails.
  - Chapter 06: falling through is one rule, an `ELSE` stops the Trigger, a chain with an `ELSE` is an `IF`.
  - Chapter 11: a recipe whose `GIVEN`s fail doesn't fail the Goal by itself.
  - Chapter 13: falling through for every kind and full stops; `SELF` and `PARENT`; a default gives way; why name order is kept; `R1301` written relations only; new note `R1312`; conflict report shows full stops and defaults left out; *Not in 2.0* additions.
  - Chapter 32: `PARENT` relations are folded in before the defaults, which are added only where they don't contradict.
- ADR: new ADR 0032 *A default gives way to what is written*. ADR 0004 and ADR 0008 stand.
- Glossary: *Falling through* added.

Handed on:

- To [*The command line, Programs and Diagnostics*](16-command-line-and-diagnostics.md): the conflict report's command, with full stops and defaults left out.
- To [*The Visual Editor*](18-visual-editor.md): what a rename says when it flips a pair ordered by name.
- To the guide (fog on the map): the four "no ELSE" comments in the showcase can go; `RoyalBanquet`'s `SELF OVER Poisoning ON scandal` can go; the comment on `HonorDuel`'s `PARENT` line; `Wagering` and `HonorDuel` rewritten with `IF`.

1.5, from [*Which systems Regia 1.5 keeps*](21-which-systems-1-5-keeps.md):

- L2, D2, D3, B8, D4, L6: in. Precedence is in 1.5, and nothing here needs a later part.
- F6: later (deferred past 2.0).
