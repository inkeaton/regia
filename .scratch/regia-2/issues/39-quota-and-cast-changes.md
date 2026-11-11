# Quota counts and cast changes in ASL

Type: grilling
Status: open
Blocked by: 34, 35

## Question

How do Quota Triggers and cast changes run in Jason? Decide:
- Quota Trigger counts kept as generated Facts: in the Director, from its Role records, and per-Giving in Agents (spec 18).
- The game reporting Agents joining and leaving, and dropping sends to Agents that have left as trace entries (spec 19).

## Comments

- Graduated from the map's fog in the scoping pass of 2026-11-09.
- From *Giving and taking Playbooks at runtime* (35): Agents keep a copy of each giving Staging's cast as `regia_cast(Staging, Role, Agent)`; keep it in sync on join/leave, and drop leavers from `fixed([…])` bindings in `regia_given`. Quota counts start on a Playbook's first Giving and are cleared when its last goes (chapter 29).
- From *Director runtime in ASL* (36): after the cast is updated, the Director runs `!regia_join(Agent, Roles)` (cast copy, setups, standing replay, then `JOINED`). The cast copy is `achieve regia_cast_copy(S, [cast(Role, Agent), …])`, which replaces the Agent's copy for `S`. `regia_transition` calls a Quota-clearing hook for the old Phase; define it here (chapter 30).
