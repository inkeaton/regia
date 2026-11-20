# Exclusions, one Agent and a Phase in the Giving record

Type: grilling
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05

## Question

Group F of the [inventory](../jason-open-questions.md#f-the-giving-record-exclusions-one-agent-and-a-phases-givings-in-the-giving-record): what `regia_given` and `regia_standing` need for `EXCEPT`, `UNASSIGN … FROM Role ?who`, a Giving to one Agent next to a Role's, and a Giving made for a Phase.

Decide:

- the exclusion list of a standing Giving, and the Agent's target for `ASSIGN … TO Role EXCEPT ?who`;
  `EXCEPT` now takes a list of Roles and Placeholders ([*Leaving two Agents out of one Role*](07-two-exceptions.md)); the showcase only has it on a Subplot's Mapping (`royal_banquet.regia:95`);
- `EXCEPT` on a Director's recipient and on a Subplot's Mapping;
- the message and record change for `UNASSIGN P FROM Guest ?culprit`;
- the mark on a Giving made for a Phase;
- a Giving to `?winner` next to the same Playbook held from a Role setup.

Closes when chapters 29 and 30 are edited.

## Comments

- From [*Roles an Agent reads*](14-roles-an-agent-reads.md): every reader of a Playbook Role now goes through one rule, `regia_plays(P, R, A)` in `regia/agent.asl` (chapter 29, *Who plays a Playbook Role*). An `EXCEPT` on a binding should extend that rule's `bind` cases, not the readers. The Director side is `regia_plays(R, A)` (chapter 30).

## Resolution

Grilled with the user on 2026-11-18. Recorded in chapter 29 (*The Giving record*, *Givings set aside*, *`EXCEPT` in a binding*, *Messages between Director and Agent*, *What each Director Statement sends*), chapter 30 (*`TRANSITION`* step 3, *Role setups*, *An Agent joining*, *The standing-Giving record*, *A Role with `EXCEPT`*, *Messages from a Director*), chapter 31's step 1 and `regia_end_staging`, and the record's new arity in chapters 33, 39 and 40.

1. **Targets and take-aways.** `Target` is `role(guest)`, `role(cast)` or `agent(Name)`. "Includes Guest" is `role(guest)`, or `role(cast)` while the Agent plays `Guest` in that cast copy. `FROM Guest` sends `regia_take(p, role(guest))` to the whole cast, which narrows `CAST` Givings. `FROM ?who` sends `regia_take(p, agent)` and takes only Givings made to that Agent, which fixes chapter 29's old `all`. `FROM CAST ?who` and `FROM CAST` send `regia_take(p, all)`.
2. **`EXCEPT` in a binding** is `live(Role, Except)`, always with a list: `role(r)` items read live, and `agent(a)` items fixed when the Statement runs. An empty Placeholder is dropped with `T1504`. `regia_plays/3` gains a `regia_excepted` test. On the Director, `regia_reach(Role, Except, A)` serves recipients, `ASSIGN` targets, counted pools, the replay for joiners, and a Subplot's Mapping (a snapshot at `START SUBPLOT`, so `royal_banquet.regia:95` needs no record).
3. **`UNASSIGN P FROM Guest ?who` sets Givings aside.** `regia_set_aside(p, guest)` moves the matching Givings to `regia_aside(…)`. Readers see only `regia_given`, so a Playbook that is only set aside isn't held. `regia_restore` moves the Givings back. A full take also clears `regia_aside`. The Director adds `agent(who)` to the matching standing records' `Except`. The Agent writes `T1505`/`T1506` when its record has nothing to act on, and the Director writes them when `?who` doesn't play the Role.
4. **A Phase's Givings** carry a sixth argument, `Until`: `staging` or `phase(Ph)`. It is not an annotation, because Jason merges the annotations of identical literals. After `EXITED`, `TRANSITION` step 3 sends `regia_take_phase(Ph)` to the cast and removes the `phase(Ph)` standing records.
5. **`ASSIGN Keeping_watch TO ?winner`** is a second belief with target `agent(w)` next to `role(guard)`. `FROM Guard` leaves it, `FROM ?winner` takes only it, and no `ASSIGNED` fires.
6. **The standing record** is `regia_standing(Seq, Playbook, Role, Except, Until, Rank, Bindings)`. `FROM Guest` removes the `guest` records and adds `role(guest)` to the `cast` ones. `FROM Guest ?who` adds `agent(who)`.
7. **Giving back.** `ASSIGN P TO Guest ?who` lifts what was set aside, plus a written `EXCEPT ?who` on a standing Giving. It removes `agent(who)` from the `Except` lists, and the Director resends `regia_give` from the record. It lifts nothing a whole-Role `FROM Guest` ended, and nothing from a counted pick.
8. **`T1506`.** The Director sends any resent Givings, then `regia_restore(p, guest, Resent)`. The Agent warns only when nothing moved and `Resent` is false.
