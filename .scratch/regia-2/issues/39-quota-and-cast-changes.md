# Quota counts and cast changes in ASL

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo
Blocked by: 34, 35

## Question

How do Quota Triggers and cast changes run in Jason? Decide:
- Quota Trigger counts kept as generated Facts: in the Director, from its Role records, and per-Giving in Agents (spec 18).
- The game reporting Agents joining and leaving, and dropping sends to Agents that have left as trace entries (spec 19).

## Answer

Spec chapter: `docs/spec/33-jason-cast-changes-and-quotas.md`, ADR 0013, checked against Jason 3.2.1 (`.send` throws `ReceiverNotFoundException`) and VEsNA-Pro (an agent kills itself when its body closes; nothing creates agents at runtime). Chapters 18, 19 and 28–31 point to it.

- **Starting cast**: compiled into the Root Director's file as `regia_start_cast([cast(Role, Agent), …])`, run by an initial goal before `regia_begin`. Starting Agents are never reported.
- **Reports**: two new body message types on the Root Director only, `regia_join {kind, name, …body fields}` and `regia_leave {name}`. A body closing is not a leave. A `regia_` name, a duplicate name, an unknown kind or an unknown leaver is ignored and traced.
- **Joining**: the Root Director creates the agent with `regia.spawn_agent(Kind, Name, Body)`, adds it to `regia_cast`, sends `regia_cast_joined(Role, A)` to the rest of the cast, then runs `!regia_join` (chapter 30). No Quota check.
- **Leaving**: a leave walk (remove from cast, `regia_cast_left(A)` to the rest of the cast, `regia_left(A)` to the children, Quota recheck, then `LEFT`/`EMPTIED` per Role), passed down the tree and pruned by cast. The Root then `.kill_agent`s the leaver without waiting for its descendants. A leave between `START SUBPLOT` and `regia_start` needs no special case.
- **Agents**: `regia_cast_left` from D removes the copy, strips A from the `fixed` bindings of D's Givings and its Quota counts, then rechecks. Incremental per Director; a Root broadcast and full re-sends were rejected.
- **Sends**: every generated send is `regia.send`, a Java internal action that catches a missing receiver, traces it and never fails.
- **Quota counts in ASL** (ADR 0013): `regia_quota(Owner, Event, Quantity, Role, Args, Sender)`. Each watched Event name gets an atomic dispatcher that posts `!!regia_when__<e>(…, Sender)` (the plain Blocks, which start first) then `!regia_count`. Silence comes from `-!…[error(no_applicable)]`/`[error(no_relevant)]`. Met quotas reset and post `regia_quota_met`. In a Playbook the Agent itself is left out of the denominator. Directors clear on `TRANSITION` (re-entering too); Agents clear when a Playbook's last Giving goes. `regia-jason` gains no quota code.

## Comments

- Graduated from the map's fog in the scoping pass of 2026-11-09.
- From *Giving and taking Playbooks at runtime* (35): Agents keep a copy of each giving Staging's cast as `regia_cast(Staging, Role, Agent)`; keep it in sync on join/leave, and drop leavers from `fixed([…])` bindings in `regia_given`. Quota counts start on a Playbook's first Giving and are cleared when its last goes (chapter 29).
- From *Director runtime in ASL* (36): after the cast is updated, the Director runs `!regia_join(Agent, Roles)` (cast copy, setups, standing replay, then `JOINED`). The cast copy is `achieve regia_cast_copy(S, [cast(Role, Agent), …])`, which replaces the Agent's copy for `S`. `regia_transition` calls a Quota-clearing hook for the old Phase; define it here (chapter 30).
- From *Stagings and Subplots runtime in ASL* (37): the cast copy is `regia_cast(Director, Role, Agent)`, sent as `regia_cast_copy([…])` (no Staging argument). Decide the Root Director's starting cast (it then runs `regia_begin`), an Agent leaving between `START SUBPLOT` and the child's `regia_start`, and catching sends (Signals, Messages) to a Director that has ended with `.kill_agent`. Reject game-reported Agent names starting with `regia_`. A Staging's ending sends `regia_end_staging` to its cast (chapter 31).
- From *Precedence encoding in ASL* (38): the start message is now `regia_start(Cast, Prefix)`, and the Root Director's file holds `regia_rank_prefix([])` as an initial belief; the Root's starting cast must not need a prefix (chapter 32).
